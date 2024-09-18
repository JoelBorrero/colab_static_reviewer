from fastapi import APIRouter, File, HTTPException, UploadFile

from app.utils.services import save_to_files, load_colab_file
from app.services import check_for_snake_case_functions


router = APIRouter(prefix="/conversations")


@router.post("/review")
async def review_conversation(file: UploadFile = File(...), save_file: bool = False):
    """
    Review a conversation and check if it is valid

    :param file: The Google Colab file to be reviewed
    :param save_file: If the file should be saved
    :return: A dictionary with the review result
    """
    file_name = file.filename
    if not file_name.endswith(".ipynb"):
        raise HTTPException(status_code=400, detail="Invalid file format")

    if save_file:
        save_to_files(file, path=file.filename)

    colab_file = load_colab_file(file=file)

    snake_case_errors = check_for_snake_case_functions(colab_file)
    return {
        "snake_case_errors": snake_case_errors
    }