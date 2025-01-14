import os
import base64

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from app.models import UploadScreenshot


class GoogleDriveService:
    def __init__(self):
        creds = service_account.Credentials.from_service_account_file(
            'serviceAccount.json',
            scopes=['https://www.googleapis.com/auth/drive']
        )
        self.drive = build('drive', 'v3', credentials=creds)
        self.parent_folder_id = os.getenv("GOOGLE_DRIVE_PARENT_FOLDER_ID")

    def _create_colab_template(self, task_id: str, model: str, folder: str) -> str:
        file = self._get_or_create_file(f"{task_id}_{model}.ipynb", "Template.ipynb", folder)
        print(f"File {model}: https://colab.research.google.com/drive/{file}")
        return file

    def _create_folder(self, folder_name: str, parent_folder_id: str = None):
        folder_metadata = {
            'name': folder_name,  
            "mimeType": "application/vnd.google-apps.folder",
            'parents': [parent_folder_id] if parent_folder_id else None
        }
        folder = self.drive.files().create(body=folder_metadata, fields='id').execute()
        return folder['id']

    def _create_file(self, file_name: str, file_path: str, parent_folder_id: str = None):
        file_metadata = {
            'name': file_name,
            'parents': [parent_folder_id] if parent_folder_id else None
        }
        mimetype = "application/vnd.google.colaboratory" if file_name.endswith(".ipynb") else "image/png"
        media = MediaFileUpload(file_path, mimetype=mimetype)
        file = self.drive.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file['id']

    def _get_or_create_file(self, file_name: str, file_path: str, parent_folder_id: str = None):
        file = self.drive.files().list(q=f"'{parent_folder_id}' in parents and name='{file_name}'").execute()
        if file['files']:
            return file['files'][0]['id']
        else:
            return self._create_file(file_name, file_path, parent_folder_id)

    def _get_or_create_folder(self, folder_name: str, parent_folder_id: str = None) -> tuple[str, bool]:
        folder = self.drive.files().list(q=f"'{parent_folder_id}' in parents and name='{folder_name}'").execute()
        if folder['files']:
            return folder['files'][0]['id'], False
        else:
            return self._create_folder(folder_name, parent_folder_id), True

    def _search_folder(self, folder_name: str, parent_folder_id: str = None):
        folder = self.drive.files().list(q=f"'{parent_folder_id}' in parents and name='{folder_name}'").execute()
        return folder['files'][0]['id'] if folder['files'] else None

    def create_task_files(self, task_id: str) -> None:
        folder, _ = self._get_or_create_folder(task_id, self.parent_folder_id)
        self._create_colab_template(task_id, "A", folder)
        self._create_colab_template(task_id, "B", folder)

    def create_task_folders(self, task_id: str, create_colab_template: bool = False) -> dict[str, str]:
        if not os.path.exists(f"screenshots/{task_id}"):
            os.makedirs(f"screenshots/{task_id}/model_a", exist_ok=True)
            os.makedirs(f"screenshots/{task_id}/model_b", exist_ok=True)

        folder, created = self._get_or_create_folder(task_id, self.parent_folder_id)
        screenshots_folder, _ = self._get_or_create_folder("screenshots", folder)

        if create_colab_template:
            self._create_colab_template(task_id, "A", folder)

        model_a_folder, _ = self._get_or_create_folder("model_a", screenshots_folder)

        if create_colab_template:
            self._create_colab_template(task_id, "B", folder)

        model_b_folder, _ = self._get_or_create_folder("model_b", screenshots_folder)

        return {
            "model_a": f"https://drive.google.com/drive/folders/{model_a_folder}",
            "model_b": f"https://drive.google.com/drive/folders/{model_b_folder}",
            "created": created
        }

    def create_task_screenshots(self, task_id: str, images: list[UploadScreenshot]):
        created_images = []
        for image in images:
            if image.model == "ideal":
                filename = f"screenshots/{task_id}/{image.turn}_ideal_response.png"
            else:
                suffix = f"_{image.suffix}" if image.suffix else ""
                filename = f"screenshots/{task_id}/model_{image.model}/{image.turn}{suffix}.png"
            with open(filename, "wb") as f:
                b64 = image.image.split(",")[1]
                f.write(base64.b64decode(b64))
            created_images.append(filename)
        return self.upload_task_screenshots(task_id, created_images)

    def upload_task_screenshots(self, task_id: str, created_images: list[str] = None):
        task_folder_id = self._search_folder(task_id, self.parent_folder_id)
        screenshots_folder_id = self._search_folder("screenshots", task_folder_id)
        count = {"model_a": 0, "model_b": 0, "ideal": 0}

        model_a_folder_id = self._search_folder("model_a", screenshots_folder_id)
        if created_images is not None:
            images = [image.split("/")[-1] for image in created_images if "model_a" in image]
        else:
            images = os.listdir(f"screenshots/{task_id}/model_a")
        for file in images:
            self._create_file(file, f"screenshots/{task_id}/model_a/{file}", model_a_folder_id)
            count["model_a"] += 1

        model_b_folder_id = self._search_folder("model_b", screenshots_folder_id)
        if created_images is not None:
            images = [image.split("/")[-1] for image in created_images if "model_b" in image]
        else:
            images = os.listdir(f"screenshots/{task_id}/model_b")
        for file in images:
            self._create_file(file, f"screenshots/{task_id}/model_b/{file}", model_b_folder_id)
            count["model_b"] += 1

        if created_images is not None:
            images = [image.split("/")[-1] for image in created_images if "ideal" in image]
        else:
            images = os.listdir(f"screenshots/{task_id}")
        for file in images:
            self._create_file(file, f"screenshots/{task_id}/{file}", screenshots_folder_id)
            count["ideal"] += 1
        return count
