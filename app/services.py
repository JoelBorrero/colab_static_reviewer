from nbformat.notebooknode import NotebookNode

from app.models import Block, BlockType, StructureError
from app.utils.regex import is_snake_case


def check_for_snake_case_functions(colab_file: NotebookNode) -> list[StructureError]:
    """
    Check if the Google Colab file has functions in snake_case

    :param colab_file: The Google Colab file to be checked
    :return: A list of errors if the file has functions not in snake_case
    """
    errors = []
    blocks = [Block(cell) for cell in colab_file.cells]
    for block in blocks:
        lines = block.content.split("\n")
        for index, line in enumerate(lines):
            if "def " in line:
                function_name = line.split("def ")[1].split("(")[0]
                if not is_snake_case(function_name):
                    errors.append(
                        StructureError(
                            block=block,
                            line_number=index,
                            line_text=line,
                            error_message="Function names should be in snake_case",
                        )
                    )
    return errors
