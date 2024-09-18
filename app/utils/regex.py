import re


def is_snake_case(string: str) -> bool:
    """
    Check if a string is in snake_case

    :param string: The string to be checked
    :return: True if the string is in snake_case, False otherwise
    """
    return bool(re.match(r"^[a-z]+(_([a-z]+|[0-9]+))*$", string))
