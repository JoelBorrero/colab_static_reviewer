import nbformat
import shutil
from fastapi import UploadFile
from nbformat.notebooknode import NotebookNode


def is_python_code(cell: NotebookNode) -> bool:
    if cell.cell_type == "code":
        lines = cell.source.split("\n")
        if "def " in cell.source:
            def_lines = [line for line in lines if "def " in line]
            for line in def_lines:
                if any([char not in line for char in ["(", ")", ":"]]):
                    return False
            return True
        elif "class " in cell.source:
            class_lines = [line for line in lines if "class " in line]
            for line in class_lines:
                if not line.strip().startswith("class ") or not line.endswith(":"):
                    return False
            return True
        elif "assert " in cell.source:
            return True
    return False


def is_swift_code(cell: NotebookNode) -> bool:
    if cell.cell_type == "code":
        lines = cell.source.split("\n")
        if "func " in cell.source:
            func_lines = [line for line in lines if "func " in line]
            for line in func_lines:
                if any([char not in line for char in ["(", ")", "{"]]):
                    return False
            return True
        elif "class " in cell.source:
            class_lines = [line for line in lines if "class " in line]
            for line in class_lines:
                if not line.startswith("public ") or not line.startswith("private ") or not line.endswith("{"):
                    return False
            return True
    return False


def load_colab_file(file_path: str = None, file: UploadFile = None) -> NotebookNode:
    """
    Load a Google Colab file

    :param file_path: The path of the file to be loaded
    :param file: The file to be loaded
    :return: The content of the file
    """
    if file:
        return nbformat.read(file.file, as_version=4)
    elif file_path:
        with open(file_path, "r") as file:
            return nbformat.read(file, as_version=4)
    else:
        raise ValueError("Either file_path or file must be provided")


def save_to_files(file: UploadFile, path: str = None) -> None:
    """
    Save the file to the specified path

    :param file: The file to be saved
    :param path: The path where the file will be saved
    :return: None
    """
    if not path:
        path = file.filename
    path = f"uploaded_files/{path}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
