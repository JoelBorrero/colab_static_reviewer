from nbformat.notebooknode import NotebookNode
from pydantic import BaseModel

from app.utils.services import is_python_code, is_swift_code


# Code blocks
class BlockType:
    PROMPT = "Prompt"
    SOLUTION = "Solution"
    PYTHON_HEADER = "Python header"
    PYTHON_CODE = "Python code"
    PYTHON_TEST = "Python test"
    SWIFT_HEADER = "Swift header"
    SWIFT_CODE = "Swift code"
    SWIFT_TEST = "Swift test"
    UNKNOWN = "Unknown"


class Block(BaseModel):
    content: str

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, cell: NotebookNode):
        """
        Represents a block of code or text

        :param cell: The cell to be represented as a block
        """
        super().__init__(content=cell.source)
        self._cell = cell

    @property
    def type(self) -> str:
        """
        Get the type of the block

        :return: The type of the block
        """
        if self.content.startswith("# Prompt"):
            return BlockType.PROMPT
        elif self.content.startswith("# Solution"):
            return BlockType.SOLUTION
        elif self.content.startswith("# Python Answer"):
            return BlockType.PYTHON_HEADER
        elif is_python_code(self._cell):
            if "import unittest" in self.content or "assert " in self.content:
                return BlockType.PYTHON_TEST
            return BlockType.PYTHON_CODE
        elif self.content.startswith("# Swift Answer"):
            return BlockType.SWIFT_HEADER
        elif is_swift_code(self._cell):
            if "import XCTest" in self.content or "assert(" in self.content:
                return BlockType.SWIFT_TEST
            return BlockType.SWIFT_CODE
        return BlockType.UNKNOWN


class StructureError(BaseModel):
    line_number: int
    line_text: str
    error_message: str

    class Config:
        from_attributes = True

    def __init__(self, block: Block, line_number: int, line_text: str, error_message: str):
        """
        Denotes an error in the structure of the code

        :param block: The block where the error occurred
        :param line_number: The line number where the error occurred
        :param line_text: The text of the line where the error occurred
        :param error_message: The message of the error
        """
        super().__init__(
            block=block,
            line_number=line_number,
            line_text=line_text,
            error_message=f"{error_message}.\nBlock: {block.type}\nLine {line_number}: {line_text}"
        )
        self.block = block


# Request bodies
class SolveTaskRequest(BaseModel):
    prompt: str

class TranslateCodeRequest(BaseModel):
    code: str
