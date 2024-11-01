import json

from openai import OpenAI

from app.constants import GPTModel

client = OpenAI()


def solve_task(prompt: str, model: GPTModel = GPTModel.GPT_4o) -> dict[str, str]:
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "text": "Given the use case and the examples, you will need to generate:\n1. # Examples: Three examples using the following structure:\n```\n**Example:**-\nExample 1:\n- Input:\n  - a: 1\n  - b: 1\n- Output: 2\n- Explanation: The sum of 1 + 1 is 2\nExample 2:\n- Input:\n  - a: 2\n  - b: 2\n- Output: 4\n- Explanation: The sum of 2 + 2 is 4\nExample 3:\n- Input:\n  - a: 17\n  - b: 3\n- Output: 20\n- Explanation: The result of sum 17 and 3 is 20\n```\n2. # Solution: A single paragraph (300 to 400 characters) with an explanation of how to solve the problem.\n3. # Python Answer: A Python function to meet all the requirements and constraints. At the end of the code you will need to add from 5 to 10 unit tests commenting each one with the format: # Test Case <Number>: <Test name>.\n```python\n# Test Case 1: Trivial test\nassert sum_two_numbers(1 + 1) == 2\n\n# Test Case 2: Trivial test with two even numbers\nassert sum_two_numbers(2 + 2) == 8\n\n# Test Case 3: Test a prime number + odd number\nassert sum_two_numbers(17 + 3) == 20\n\n# Test Case 4: Test a power of 2\nassert sum_two_numbers(64 + 4) == 68\n\n# Test Case 5: Test a large number\nassert sum_two_numbers(10101 + 5) == 10106\n```",
                    "type": "text",
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Given a string `s` and a list of words `wordDict`, insert spaces in `s` to form sentences where each word is a valid word from the dictionary. Return all possible sentences in any order.\nNote that a word from the dictionary can be used multiple times in the segmentation.\n\nKeywords:- ['Dynamic Programming', 'Backtracking', 'String']\n\nStarter Code: -\n```python\ndef wordBreak(s: str, wordDict: List[str]) -> List[str]:\npass\n```",
                }
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": '{\n  "examples": [\n    {\n      "input": [\n        {\n          "var_name": "s",\n          "value": "catsanddog"\n        },\n        {\n          "var_name": "word_dict",\n          "value": "[\'cat\',\'cats\',\'and\',\'sand\',\'dog\']"\n        }\n      ],\n      "output": "[\\"cats and dog\\",\\"cat sand dog\\"]",\n      "explanation": "The output is a list of all possible sentences that can be formed using the words in the words dict. The words are \\"cat\\", \\"cats\\", \\"and\\", \\"sand\\", and \\"dog\\". The sentences are \\"cats and dog\\" and \\"cat sand dog\\"."\n    },\n    {\n      "input": [\n        {\n          "var_name": "s",\n          "value": "pineapplepenapple"\n        },\n        {\n          "var_name": "word_dict",\n          "value": "[\'apple\',\'pen\',\'applepen\',\'pine\',\'pineapple\']"\n        }\n      ],\n      "output": "[\\"pine apple pen apple\\",\\"pineapple pen apple\\",\\"pine applepen apple\\"]",\n      "explanation": "The output is a list of all possible sentences that can be formed using the words in the words dict. The words are \\"apple\\", \\"pen\\", \\"applepen\\", \\"pine\\", and \\"pineapple\\". The sentences are \\"pine apple pen apple\\", \\"pineapple pen apple\\", and \\"pine applepen apple\\"."\n    },\n    {\n      "input": [\n        {\n          "var_name": "s",\n          "value": "catsandog"\n        },\n        {\n          "var_name": "word_dict",\n          "value": "[\'cats\',\'dog\',\'sand\',\'and\',\'cat\']"\n        }\n      ],\n      "output": "[]",\n      "explanation": "The output is an empty list because there are no valid sentences that can be formed using the words in the words dict."\n    }\n  ],\n  "solution": "The task is to split the string `s` into valid words from the given words dict to form all possible sentences. This problem can be solved using recursive backtracking with memoization to avoid redundant work. By storing the results of subproblems, we can ensure the solution is efficient.",\n  "python_code": "def word_break(s: str, word_fict: list[str]) -> list[str]:\\n    \\"\\"\\"\\n    Given a string s and a list of words word_fict, insert spaces in s to form sentences where each word is a valid word from the dictionary.\\n    Args:\\n        s: The input string.\\n        word_fict: A list of valid words.\\n    Returns:\\n        A list of all possible sentences that can be formed using the words in word_fict.\\n    \\"\\"\\"\\n    word_set = set(word_fict)\\n    memo = {}\\n    def backtrack(index: int) -> list[str]:\\n        if index in memo:\\n            return memo[index]\\n        if index == len(s):\\n            return [\\"\\"]\\n         sentences = []\\n        for end in range(index + 1, len(s) + 1):\\n            word = s[index:end]\\n            if word in word_set:\\n                rest_of_sentences = backtrack(end)\\n                for sentence in rest_of_sentences:\\n                    if sentence:\\n                        sentences.append(word + \\" \\" + sentence)\\n                   else:\\n                        sentences.append(word)\\n                   memo[index] = sentences\\n            return sentences\\n    return backtrack(0)\\n\\n## Python Test\\n# Test Case 1: Basic test with two possible outputs\\nassert set(word_break(\\"catsanddog\\", [\\"cat\\", \\"cats\\", \\"and\\", \\"sand\\", \\"dog\\"])) == set([\\"cats and dog\\", \\"cat sand dog\\"])\\n\\n# Test Case 2: Basic test with three possible outputs\\nassert set(word_break(\\"pineapplepenapple\\", [\\"apple\\", \\"pen\\", \\"applepen\\", \\"pine\\", \\"pineapple\\"])) == set([\\"pine apple pen apple\\", \\"pineapple pen apple\\", \\"pine applepen apple\\"])\\n\\n# Test Case 3: Test case with no valid sentences\\nassert word_break(\\"catsandog\\", [\\"cats\\", \\"dog\\", \\"sand\\", \\"and\\", \\"cat\\"]) == []\\n\\n# Test Case 4: Test case with two possible outputs\\nassert set(word_break(\\"nowhere\\", [\\"no\\", \\"where\\", \\"now\\", \\"here\\"])) == set([\\"no where\\", \\"now here\\"])\\n\\n# Test Case 5: Test case with three possible outputs\\nassert set(word_break(\\"spamsandwich\\", [\\"spam\\", \\"sandwich\\", \\"and\\", \\"sand\\", \\"wich\\", \\"spams\\"])) == set([\\"spam sand wich\\", \\"spam sandwich\\", \\"spams and wich\\"])"\n}',
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Given a list of words, find the word that has the maximum number of unique characters. If there are multiple words with the same number of unique characters, return the one that appears first in the list. Implement a function to solve this problem.\n\nKeywords: - ['bit manipulation', 'trie', 'string']\n\nStarter Code: -\n```python\ndef max_unique_chars_word(words: List[str]) -> str:\n# Your code here\npass\n```",
                }
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": '{\n  "examples": [\n    {\n      "input": [\n        {\n          "var_name": "words",\n          "value": "[\'ant\', \'bear\', \'cobra\']"\n        }\n      ],\n      "output": "cobra",\n      "explanation": "The word \\"cobra\\" has 5 unique characters, while \\"ant\\" and \\"bear\\" have 3 and 4 unique characters respectively, the output should be \\"cobra\\" as it was the longest in the list."\n    },\n    {\n      "input": [\n        {\n          "var_name": "words",\n          "value": "[\'xylophone\', \'zebra\', \'rhythm\']"\n        }\n      ],\n      "output": "xylophone",\n      "explanation": "The word \\"xylophone\\" has 8 unique characters, \\"zebra\\" has 5 unique characters, while \\"rhythm\\" has 5 unique characters, therefore the output is \\"xylophone\\"."\n    },\n    {\n      "input": [\n        {\n          "var_name": "words",\n          "value": "[\'aaa\', \'bbb\', \'ccc\', \'ddd\']"\n        }\n      ],\n      "output": "aaa",\n      "explanation": "All words have only 1 unique character, thus the first word \\"aaa\\" is returned."\n    }\n  ],\n  "solution": "To solve this problem, we need to iterate through the list of words, compute the number of unique characters for each word, and track the word with the maximum count of unique characters. If multiple words have the same maximum count, we\'ll keep the first one encountered.",\n  "python_code": "def max_unique_chars_word(words: list[str]) -> str:\\n    max_unique_count = 0\\n    result_word = \\"\\"\\n    \\n    for word in words:\\n        unique_chars = set(word)\\n        unique_count = len(unique_chars)\\n        \\n        if unique_count > max_unique_count:\\n            max_unique_count = unique_count\\n            result_word = word\\n        elif unique_count == max_unique_count and result_word == \\"\\":\\n            result_word = word\\n            \\n    return result_word\\n\\n## Python Test\\n# Test Case 1: Basic test with unique characters\\nassert max_unique_chars_word([\\"apple\\", \\"banana\\", \\"cherry\\"]) == \\"banana\\"\\n\\n# Test Case 2: Test with same number of unique characters, returning the first one\\nassert max_unique_chars_word([\\"xylophone\\", \\"zebra\\", \\"rhythm\\"]) == \\"xylophone\\"\\n\\n# Test Case 3: Test with all words having the same number of unique characters\\nassert max_unique_chars_word([\\"a\\", \\"bb\\", \\"ccc\\"]) == \\"a\\"\\n\\n# Test Case 4: Test with single word in the list\\nassert max_unique_chars_word([\\"elephant\\"]) == \\"elephant\\"\\n\\n# Test Case 5: Test with empty list\\nassert max_unique_chars_word([]) == \\"\\"\\n\\n# Test Case 6: Test with words having no unique characters (empty string special case)\\nassert max_unique_chars_word([\\"aaa\\", \\"bbbb\\", \\"ccccc\\", \\"dddddd\\"]) == \\"aaa\\"\\n\\n# Test Case 7: Test with varied unique character counts\\nassert max_unique_chars_word([\\"unique\\", \\"characters\\", \\"identical\\", \\"aabbcc\\"]) == \\"characters\\""\n}',
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "You are given a list of power stations, each with a certain power output. Your task is to find the maximum power output that can be achieved by combining the power outputs of exactly two power stations. If there are fewer than two power stations, return -1. Write a function `max_combined_power` that takes a list of integers representing the power outputs of the power stations and returns the maximum combined power output of any two power stations.\n\nKeywords:- ['Array', 'Binary Search', 'Power Station']\n\nStarter Code: -\n\n```python\ndef max_combined_power(power_stations):\n# Write your code here\npass\n```",
                }
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": '{\n  "examples": [\n    {\n      "input": [\n        {\n          "var_name": "power_stations",\n          "value": "[10, 20]"\n        }\n      ],\n      "output": "30",\n      "explanation": "The maximum combined power output of the two power stations (10 and 20) is 30."\n    },\n    {\n      "input": [\n        {\n          "var_name": "power_stations",\n          "value": "[]"\n        }\n      ],\n      "output": "-1",\n      "explanation": "There are no power stations, so it\'s not possible to combine powers from two stations. The function returns -1."\n    }\n  ],\n  "solution": "To solve this problem, we need to find the two largest elements in the list and sum their values. If there are fewer than two elements in the list, we should return -1. The detailed process is to check if the length of the list is less than 2. If it is, return -1, Then initialize two variables to keep track of the largest and the second-largest values encountered so far. After that, iIterate through the list and update the two variables whenever a larger value is encountered, and finally return the sum of the two largest values after finishing the iteration.",\n  "python_code": "def max_combined_power(power_stations):\\n    \\"\\"\\"\\n    Given a list of power outputs of power stations,\\n    find the maximum combined power output of any two power stations.\\n    Args:\\n        power_stations: List of integers representing power outputs.\\n    Returns:\\n        The maximum combined power output of any two power stations,\\n        or -1 if fewer than two power stations exist.\\n    \\"\\"\\"\\n    # If there are fewer than 2 power stations, we cannot combine them\\n    if len(power_stations) < 2:\\n        return -1\\n    \\n    # Initialize two variables to keep track of the two largest values\\n    max1 = float(\'-inf\')\\n    max2 = float(\'-inf\')\\n    \\n    # Iterate through the list to find the two largest values\\n    for power in power_stations:\\n        if power > max1:\\n            max2 = max1\\n            max1 = power\\n        elif power > max2:\\n            max2 = power\\n    \\n    # Return the combined power of the two largest power stations\\n    return max1 + max2\\n\\n## Python Test\\n# Test Case 1: Basic test with two elements\\nassert max_combined_power([10, 20]) == 30\\n\\n# Test Case 2: Test with multiple elements\\nassert max_combined_power([3, 5, 7, 2, 8]) == 15\\n\\n# Test Case 3: Test with large elements\\nassert max_combined_power([1001, 1002, 1003]) == 2005\\n\\n# Test Case 4: Test with negative elements\\nassert max_combined_power([-1, -2, -3, -4]) == -3\\n\\n# Test Case 5: Test with positive and negative elements\\nassert max_combined_power([5, -10, 3, -6]) == 8\\n\\n# Test Case 6: Test with single element\\nassert max_combined_power([10]) == -1\\n\\n# Test Case 7: Edge case with empty list\\nassert max_combined_power([]) == -1\\n\\n# Test Case 8: Test with duplicate values\\nassert max_combined_power([5, 5, 5, 5]) == 10"\n}',
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Given a 2D grid network of integers, find the sum of all integers in the grid. The grid will always be a square matrix (n x n) where 1 <= n <= 100. The integers in the grid will range from -1000 to 1000.\n\nKeywords: - ['grid network', 'mathematics'] \n\nStarter Code: -\n```python\ndef sum_of_grid(grid: list[list[int]]) -> int:\n    # Implementation of the function goes here\n    pass\n```",
                }
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": '{\n  "examples": [\n    {\n      "input": [\n        {\n          "var_name": "grid",\n          "value": "[[1, 2], [3, 4]]"\n        }\n      ],\n      "output": "10",\n      "explanation": "The sum of all numbers in the grid is 1 + 2 + 3 + 4 = 10."\n    },\n    {\n      "input": [\n        {\n          "var_name": "grid",\n          "value": "[[-1, -2], [-3, -4]]"\n        }\n      ],\n      "output": "-10",\n      "explanation": "The sum of all numbers in the grid is -1 + (-2) + (-3) + (-4) = -10."\n    },\n    {\n      "input": [\n        {\n          "var_name": "grid",\n          "value": "[[5, 8, -3], [2, 0, 4], [-7, 1, -9]]"\n        }\n      ],\n      "output": "1",\n      "explanation": "Adding all elements: 5 + 8 - 3 + 2 + 0 + 4 - 7 + 1 - 9 = 1."\n    }\n  ],\n  "solution": "The task is straightforward; we need to iterate over each element of the 2D grid and compute their sum. To achieve this, we can leverage Python\'s comprehensions and the built-in `sum()` function. We will use a nested list comprehension to iterate over each row in the grid and then over each element in the row. The result of the inner iteration will be passed to the `sum()` function to get the total of all integers in the grid.",\n  "python_code": "def sum_of_grid(grid: list[list[int]]) -> int:\\n    \\"\\"\\"\\n    Calculate the sum of all integers in a given grid.\\n    Args:\\n        grid: A list of lists representing a square matrix of integers.\\n    Returns:\\n        The sum of all integers in the grid.\\n    \\"\\"\\"\\n    return sum(sum(row) for row in grid)\\n\\n## Python Test\\n# Test Case 1: Basic test with positive numbers\\nassert sum_of_grid([[1, 2], [3, 4]]) == 10\\n\\n# Test Case 2: Test with negative numbers\\nassert sum_of_grid([[-1, -2], [-3, -4]]) == -10\\n\\n# Test Case 3: Test with mixed numbers\\nassert sum_of_grid([[5, 8, -3], [2, 0, 4], [-7, 1, -9]]) == 1\\n\\n# Test Case 4: Edge case with single element\\nassert sum_of_grid([[1000]]) == 1000\\n\\n# Test Case 5: Test with large grid, all elements are zero\\nassert sum_of_grid([[0] * 100 for _ in range(100)]) == 0\\n\\n# Test Case 6: Test with elements at maximum positive range\\nassert sum_of_grid([[1000] * 100 for _ in range(100)]) == 10000000\\n\\n# Test Case 7: Test with elements at maximum negative range\\nassert sum_of_grid([[-1000] * 100 for _ in range(100)]) == -10000000"\n}',
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "You are given an array of integers representing the heights of buildings in a city skyline. Determine if the sequence of building heights is bitonic. A sequence is bitonic if it monotonically increases and then monotonically decreases. The sequence must have at least three elements to be considered bitonic. Return True if the sequence is bitonic, otherwise return False.\n\nKeywords: - ['bitonic sort', 'arrays', 'monotone sequences']\n\nStarter Code: -\n```python\ndef is_bitonic(buildings: list[int]) -> bool:\n    # Implementation of the function goes here\n    pass\n```",
                }
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": '{\n  "examples": [\n    {\n      "input": [\n        {\n          "var_name": "buildings",\n          "value": "[1,3,5,4,2]"\n        }\n      ],\n      "output": "True",\n      "explanation": "The buildings heights first increase (1, 3, 5) and then decrease (5, 4, 2). Thus, they form a bitonic sequence."\n    },\n    {\n      "input": [\n        {\n          "var_name": "buildings",\n          "value": "[5,3,1,2]"\n        }\n      ],\n      "output": "False",\n      "explanation": "The buildings heights decrease (5, 3, 1) and then increase (1, 2). This is not a bitonic sequence as it does not increase first."\n    },\n    {\n      "input": [\n        {\n          "var_name": "buildings",\n          "value": "[1,3,5,7]"\n        }\n      ],\n      "output": "False",\n      "explanation": "The sequence (1, 3, 5, 7) only increases and does not decrease, so it is not bitonic."\n    }\n  ],\n  "solution": "To determine if the sequence of building heights is bitonic, we should first check if the sequence has at least three elements. Then, iterate over the sequence to find the point where it stops increasing and starts decreasing. If such a point exists, ensure the sequence decreases afterward. During the iteration, check for strictly increasing until the peak and strictly decreasing after it. Return True only if both segments are found and valid.",\n  "python_code": "def is_bitonic(buildings: list[int]) -> bool:\\n    \\"\\"\\"\\n    Checks if the sequence of building heights is bitonic.\\n\\n    Args:\\n        buildings: The buildings list to work with.\\n\\n    Returns:\\n        True if the sequence is bitonic, False otherwise\\n    \\"\\"\\"\\n    n = len(buildings)\\n    if n < 3:\\n        return False\\n    \\n    # Find the peak of the sequence\\n    i = 1\\n    # Check for initial strictly increasing order\\n    while i < n and buildings[i] > buildings[i - 1]:\\n        i += 1\\n    \\n    # if no increasing part or the sequence ends before decreasing part\\n    if i == 1 or i == n:\\n        return False\\n    \\n    # Check for strictly decreasing after the peak\\n    while i < n and buildings[i] < buildings[i - 1]:\\n        i += 1\\n    \\n    # If we exhausted the list, it means it is bitonic\\n    return i == n\\n\\n## Python Test\\n# Test Case 1: Typical bitonic sequence\\nassert is_bitonic([1, 3, 5, 4, 2]) == True\\n\\n# Test Case 2: Not bitonic, because it strictly increases\\nassert is_bitonic([5, 6, 7, 8]) == False\\n\\n# Test Case 3: Not bitonic, because it does not decrease after increasing\\nassert is_bitonic([1, 3, 2, 2]) == False\\n\\n# Test Case 4: Not bitonic, because it does not increase first\\nassert is_bitonic([4, 3, 2, 1]) == False\\n\\n# Test Case 5: Small array with less than 3 elements\\nassert is_bitonic([10, 20]) == False\\n\\n# Test Case 6: Single peak with exact bitonic pattern\\nassert is_bitonic([1, 2, 3, 2, 1]) == True\\n\\n# Test Case 7: Array with equal peak values making it not strictly increasing/decreasing\\nassert is_bitonic([1, 3, 3, 2, 1]) == False"\n}',
                }
            ],
        },
        {"role": "user", "content": [{"type": "text", "text": prompt}]},
    ]
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "examples_schema",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "examples": {
                        "type": "array",
                        "description": "A list of examples with input, output and explanation.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "input": {
                                    "type": "array",
                                    "description": "The list of inputs for the example.",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "var_name": {
                                                "type": "string",
                                                "description": "The variable name for the input.",
                                            },
                                            "value": {
                                                "type": "string",
                                                "description": "The input value for the example.",
                                            },
                                        },
                                        "required": ["var_name", "value"],
                                        "additionalProperties": False,
                                    },
                                },
                                "output": {
                                    "type": "string",
                                    "description": "The expected output for the example.",
                                },
                                "explanation": {
                                    "type": "string",
                                    "description": "Description of how the input leads to the output.",
                                },
                            },
                            "required": ["input", "output", "explanation"],
                            "additionalProperties": False,
                        },
                    },
                    "solution": {
                        "type": "string",
                        "description": "A solution paragraph containing 300 to 400 characters.",
                    },
                    "python_code": {
                        "type": "string",
                        "description": "A block of Python code relevant to the examples or solution.",
                    },
                },
                "required": ["examples", "solution", "python_code"],
                "additionalProperties": False,
            },
        },
    }

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=1,
            max_tokens=1322,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format=response_format,
        )
        content = response.choices[0].message.content
        if type(content) is str:
            content = json.loads(content)
        return content
    except Exception as e:
        return f"Error: {e}"


def translate_to_python(swift_code: str, model: GPTModel = GPTModel.GPT_4o) -> dict[str, str]:
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "text": "You are a code translator from Swift to Python. The user will come up with a solution in Swift and your response will be the same function in every condition and variable but available to run in Python. The only differences will be the syntax and variables in snake_case instead of lowCamelCase. You will use docstrings and typing for the functions. Sometimes, the user will bring just the tests to be translated to unittest if they are using xcassert, otherwise to single asserts. Do not generate nothing, wait for the user input.",
                    "type": "text",
                }
            ],
        },
        {"role": "user", "content": [{"type": "text", "text": swift_code}]},
    ]
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "python_code",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "A string representing Python code.",
                    }
                },
                "required": ["code"],
                "additionalProperties": False,
            },
        },
    }

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=1,
            max_tokens=1599,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format=response_format,
        )
        content = response.choices[0].message.content
        if type(content) is str:
            content = json.loads(content)
        return content
    except Exception as e:
        return f"Error: {e}"
