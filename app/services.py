from nbformat.notebooknode import NotebookNode

from app.models import Block, BlockType, StructureError
from app.utils.regex import is_snake_case


class Rule:
    def __init__(self, text: str | None = "", allow_startswith: bool = False):
        """
        Create a new rule for the prompt block

        :param text: The text pattern to be checked. If None, the text can be anything
        :param allow_startswith: If the text does not need to match exactly, but can start with the text
        """
        self.text = text
        self.allow_startswith = allow_startswith


class Section:
    PROMPT = "# Prompt:"
    EXAMPLES = "**Example:**-"
    STARTER_CODE = " **Starter Code:** -"
    PYTHON_CODE = "```python"
    SWIFT_CODE = "```swift"

    @staticmethod
    def all():
        return [Section.PROMPT, Section.EXAMPLES, Section.STARTER_CODE, Section.PYTHON_CODE, Section.SWIFT_CODE]


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


def check_prompt_block(colab_file: NotebookNode) -> list[StructureError]:
    """
    Check if the Google Colab file has a prompt block

    :param colab_file: The Google Colab file to be checked
    :return: A list of errors if the file does not have a prompt block
    """

    errors = []
    block = Block(colab_file.cells[0])
    rules = [
        Rule(Section.PROMPT),
        Rule(),
        Rule(None),
        Rule(),
        Rule("**Keywords:**-", True),
        Rule(),
        Rule("**Difficulty Level:** -", True),  # TODO: Check the space in the format: **Word:**- or **Word:** -
        Rule(),
        Rule(Section.EXAMPLES),
        Rule(),
        Rule(Section.STARTER_CODE, True),  # TODO: Check the space in the format
        Rule(),
        Rule(Section.PYTHON_CODE),
        Rule(None),
        Rule("```"),
        Rule(Section.SWIFT_CODE),
        Rule(None),
        Rule("```"),
    ]
    example_rules = [
        Rule("Example ", True),
        Rule(),
        Rule("Input: ", True),
        Rule(),
        Rule("Output: ", True),
        Rule(),
        Rule("Explanation: ", True),
        Rule(),
    ]
    if block.type == BlockType.PROMPT:
        lines = block.content.split("\n")
        section = Section.PROMPT
        example_count = 0
        rule_index = 0
        example_index = 0
        for index, line in enumerate(lines):
            if rule_index <= 9:
                # Main prompt section
                rule = rules[rule_index]
                if rule.text is not None and line != rule.text:
                    if not rule.allow_startswith or not line.startswith(rule.text):
                        errors.append(
                            StructureError(
                                block=block,
                                line_number=index,
                                line_text=line,
                                error_message=f"Expected '{rule.text}' on line {index}, but got '{line}'",
                            )
                        )
                if rule_index == 8:
                    section = Section.EXAMPLES
                rule_index += 1
            elif section == Section.EXAMPLES:
                # Examples section
                example_rule = example_rules[example_index]
                if example_index == 0:
                    # This is the example header
                    if line.startswith(example_rule.text):
                        example_count += 1
                        # Check the format
                        expected = f"{example_rule.text}{example_count}:"
                        if not line == expected:
                            errors.append(
                                StructureError(
                                    block=block,
                                    line_number=index,
                                    line_text=line,
                                    error_message=f"Expected '{expected}' on example {example_count}, but got '{line}'",
                                )
                            )
                    elif line == rules[rule_index]:
                        # Starter code section starts here
                        section = Section.STARTER_CODE
                        rule = rules[rule_index]
                        if line != rule.text:
                            if not rule.allow_startswith or not line.startswith(rule.text):
                                errors.append(
                                    StructureError(
                                        block=block,
                                        line_number=index,
                                        line_text=line,
                                        error_message=f"Expected '{rule.text}' on line {index}, but got '{line}'",
                                    )
                                )
                        rule_index += 1
                    else:
                        if example_count == 0:
                            errors.append(
                                StructureError(
                                    block=block,
                                    line_number=index,
                                    line_text=line,
                                    error_message=f"The examples should start with '{example_rule.text}1:'"
                                )
                            )
                        else:
                            if line == "":
                                errors.append(
                                    StructureError(
                                        block=block,
                                        line_number=index,
                                        line_text=line,
                                        error_message=f"There is an extra empty line in the examples section "
                                                      f"after example {example_count}"
                                    )
                                )
                                continue

                    example_index += 1
                else:
                    if example_rule.text is not None and line != example_rule.text:
                        if not example_rule.allow_startswith or not line.startswith(example_rule.text):
                            if line in [s for s in Section.all()]:
                                section = line
                                rule_index = rules.index([r for r in rules if r.text == line][0])
                                continue
                            else:
                                errors.append(
                                    StructureError(
                                        block=block,
                                        line_number=index,
                                        line_text=line,
                                        error_message=f"Expected '{example_rule.text}' on line/section {index},"
                                                      f" but got '{line}'",
                                    )
                                )
                    example_index += 1
                    if example_index == 8:
                        example_index = 0
            else:
                # Starter code section
                if example_count is not None and example_count < 2:
                    errors.append(
                        StructureError(
                            block=block,
                            line_number=index,
                            line_text=line,
                            error_message="There should be at least two examples"
                        )
                    )
                    example_count = None
                rule = rules[rule_index]
                if rule in [Section.PYTHON_CODE, Section.SWIFT_CODE]:
                    section = rule.text
                elif rule.text == "```":
                    if section == Section.PYTHON_CODE:
                        section = Section.SWIFT_CODE
                    else:
                        break
                rule_index += 1
    else:
        errors.append(
            StructureError(
                block=block,
                line_number=0,
                line_text=block.content,
                error_message="The first block should be the prompt",
            )
        )
    return errors
