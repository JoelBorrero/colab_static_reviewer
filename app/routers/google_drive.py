from app.models import UploadScreenshotsRequest
from fastapi import APIRouter

from app.google_drive.services import GoogleDriveService

router = APIRouter(prefix="/gdrive")
gdrive = GoogleDriveService()


@router.post("/create-folders")
async def create_folders(task_id: str):
    """
    Create folders for a task

    :param task_id: The ID of the task
    :return: A dictionary with the model A and B folder IDs
    """
    response = gdrive.create_task_folders(task_id)
    return response


@router.post("/upload-screenshots")
async def upload_screenshots(body: UploadScreenshotsRequest):
    response = gdrive.create_task_screenshots(body.task_id, body.images)
    return response
