import json

import anthropic

from app.constants import ClaudeModel


class _Prompts:
    class Languages:
        JAVASCRIPT = "javascript"
        PYTHON = "python"

    def __init__(self):
        self.data = json.load(open("app/llm/prompts.json"))

    def build_prompt(
        self, prompt: str, model_a: str, model_b: str, code_output: str = None
    ) -> str:
        """
        Concatenates the prompt, model_a response, model_b response and code output into a single string.

        Args:
            prompt: The user prompt.
            model_a: The response of the first model.
            model_b: The response of the second model.
            code_output: The output of the code.

        Returns:
            The concatenated prompt.
        """
        combined_prompt = (
            f"{prompt}\n\nModel A response:\n{model_a}\n\nModel B response:\n{model_b}"
        )
        if code_output:
            combined_prompt = f"{combined_prompt}\n\nCode output:\n{code_output}"
        return combined_prompt

    def generate_comparison_examples(self, language: Languages):
        """
        Generates the examples for the comparison prompt.

        Returns:
            The examples for the comparison prompt.
        """
        examples = self.data["generate_comparison"].get(language, self.data["generate_comparison"][_Prompts.Languages.PYTHON])
        response = "<examples>"
        for example in examples:
            response += "<example>"
            for key, value in example.items():
                response += f"<{key.upper()}>{str(value).replace('\\n', '\n').replace("\\'", "\'")}</{key.upper()}>"
            response += "</example>"
        response += "</examples>"
        return response

    def generate_turns_examples(self, language: Languages):
        """
        Generates the examples for the generate turns prompt.

        Returns:
            The examples for the generate turns prompt.
        """
        turns = self.data["generate_turns"][language]
        response = "<examples>"
        for example in turns:
            response += "<example>"
            for key, value in example.items():
                response += f"<{key.upper()}>{value.replace('\\n', '\n').replace("\\'", "\'")}</{key.upper()}>"
            response += "</example>"
        response += "</examples>"
        return response

    SYSTEM_GENERATE_TURNS = """Given the use case and user profile, you will generate a conversation of 3 user questions with a code assistant. The assistant responses will be single line placeholders with the idea of the solution in order to develop the next turn, do not provide the complete assistant response.\nFocus on providing realistic, specific scenarios when asking for help or implementations. Instead of generic prompts like "How can I...?" or "Example...", describe a particular situation and request precise solutions or guidance. Some examples to start the conversation:\n\"\"\"\n- Design a Python function that extracts the X'th shortest URL from a list of URLs, considering only URLs that have a path component and a domain component. If no such URL is found, it should return an empty string.\n- Implement a function generate_balanced_expression_recursively that generates all possible balanced expressions using the following characters: ("(", ")", "+", "-") . The function should return a list of strings. Each string should represent a valid balanced expression. Hint: The base case is when there are no characters.\n\"\"\"\nThe main point is try to be creative about the prompt by providing a specific scenario and specific instructions rather than a generic stuff., trying to make questions easy to answer. Only if the use case requires using a text response, you can generate a question where the assistant do not provide code, could be a theorical concern, suggestions about improvements, or something related."""

    SYSTEM_COMPARE = """You are a code reviewer. The user will give you the prompt and the response of two models, you need to evaluate and grade each model's response based on the categories: Instruction Following, Truthfulness, Conciseness, Content Safety, and Overall Satisfaction. Important: Provide a paragraph with a brief explanation on why the chosen score was assigned, highlighting specific aspects of the response that influenced the rating for each category, both positive and negative. Use clear language to ensure the justification for instruction following is understandable and informative.\nEvaluate the two model responses, Model A and Model B, based on these criteria:\n- Instruction following: No issues, minor issues, major issues. Refers to following the prompt's requirements. This includes:\n1. Using the specified algorithm.\n2. Calculating the requested output.\n3. Adhering to the stated approach.\nNote: Errors or incorrect results in the code do not affect Instruction. If the response does not follow the explicit prompt requirements, it fails on Instruction, regardless of correctness.\n- Truthfulness: No issues, minor issues, major issues. It ensures that what the response describes aligns with what the code does. This means:\n1. The implementation and the description must match without contradictions.\n2. The output should be correct and consistent with the intended logic.\nNote: Even if the response doesn't meet the prompt's requirements, Truthfulness is intact as long as the code and the response match.\n- Conciseness: Just right, too verbose, too short.\n- Content Safety: No issues, minor issues, major issues.\n- Overall satisfaction: Amazing, Pretty good, Okay, Pretty bad, Bad.\n\nAfter evaluating both models, compare with the previous criteria and choose a final preference using this scale:\n- Model A is significantly better than Model B\n- Model A is better than Model B\n- Model A is slightly better than Model B\n- Model A is negligibly better than Model B\n- Model B is negligibly better than Model A\n- Model B is slightly better than Model A\n- Model B is better than Model A\n- Model B is significantly better than Model A\n\nPreference Explanation: Briefly justify your choice in a single paragraph, considering the following:\n- How well each model followed the user's request.\n- Which model's explanation or code was more accurate, clear, and adaptable.\n- Any differences in style, tone, or usability.\n\nConsiderations:\n- If both models meet expectations, consider small differences in clarity or user-friendliness.\n- For code, consider robustness, best practices, and flexibility.\n- Focus on which response provides a better user experience overall.\n- When writing a rationale for a Minor issue, mention why it is good enough not to be a Major Issue and what It accomplishes\n- Use creative, vivid and uncommon verbs and talk like a human, not a robot, using short paragraphs.\n- Do not refer to the user as "you", instead use "the user".\n- When reviewing each one, do not refer to each model as "Model A does...", instead just "The model..." or "The response...". Use "Model A" and "Model B" just for the final comparisson, for the other rationales just treat each one as an individual case.\n- When evaluating the next answer, do not mention the first one again, it is a new independent one.\n- Do not punish Instruction Following if it is an issue of missing import or a simple syntax error\n- Punish both Instruction Following and Truthfulness. If it is a logical issue, Truthfulness should be punished at least as much as Instruction Following or more if there are additional issues.\n\nOutput in JSON format with keys: “model_a", "model_b” and "comparison". Each model has a list of the evaluated keys with "score" and "comment". The comparison also is a dict with "score" and "comment"."""


class AnthropicService:
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.prompts = _Prompts()

    def generate_turns(
        self, prompt: str, model: ClaudeModel = ClaudeModel.SONET_3_5, language: _Prompts.Languages = _Prompts.Languages.PYTHON
    ) -> list[dict[str, str]]:
        """
        Generates the initial conversation turns between the user and the assistant.

        Args:
            prompt: The user prompt.
            model: The model to use.

        Returns:
            The conversation turns.
        """
        # return [{"user": "I'm working on a shared repository where multiple teams access sensitive data through API endpoints. I need to create a function that validates user permissions and logs access attempts. Could you help me implement this with clear comments explaining the security implications?","assistant": "Implementation of a permission validation decorator with detailed security comments, logging mechanisms, and access control checks using environment variables.",},{"user": "For our CI/CD pipeline, I want to add a function that automatically checks for potential security vulnerabilities in merge requests, specifically focusing on hardcoded credentials and insecure data access patterns. How can I implement this with clear documentation?","assistant": "Implementation of a security check function using ast module to parse Python code and detect security issues, with comprehensive comments about each vulnerability pattern.",},{"user": "What are the best practices for documenting security-related code changes in a way that helps prevent merge conflicts while maintaining sensitive information confidentiality? Our team is growing and we need to establish clear guidelines.","assistant": "Detailed explanation of documentation best practices, including templates for security-related changes and strategies for handling sensitive information in comments.",},]
        prompt = f"{prompt}\nLanguage: {language}"
        message = self.client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=0.3,
            system=self.prompts.SYSTEM_GENERATE_TURNS,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": self.prompts.generate_turns_examples(language),
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )
        text = message.content[0].text
        print(text)
        lines = text.split("\n")
        turns = []
        for line in lines:
            if line.startswith("U:"):
                turns.append({"user": line[2:].strip().replace('"', "")})
            elif line.startswith("A:"):
                turns[-1]["assistant"] = line[2:].strip().replace('"', "")
            elif turns:
                if "assistant" in turns[-1]:
                    turns[-1]["assistant"] += f"\n{line}"
                else:
                    turns[-1]["user"] += f"\n{line}"
        for turn in turns:
            turn["user"] = turn["user"].strip()
        return turns if turns else text

    def compare_responses(
        self,
        prompt: str,
        model_a: str,
        model_b: str,
        output: str = None,
        model: ClaudeModel = ClaudeModel.SONET_3_5,
        language: _Prompts.Languages = _Prompts.Languages.PYTHON
    ) -> dict:
        """
        Compares the responses of two models and returns the comparison result.

        Args:
            prompt: The user prompt.
            model_a: The response of the first model.
            model_b: The response of the second model.
            output: The output of the code.
            model: The model to use.

        Returns:
            The comparison result.
        """
        # return {'model_a': {'instruction_following': {'score': 'No issues', 'comment': 'The response directly addresses the request to create a function simulating salt precipitation in a sabkha environment, incorporating relevant environmental parameters like temperature, salinity, and evaporation rates.'}, 'truthfulness': {'score': 'No issues', 'comment': 'The implementation matches the explanation provided, with the code accurately modeling salt precipitation based on the described parameters and processes. The output shows gradual salt accumulation over time as expected in a sabkha environment.'}, 'conciseness': {'score': 'Just right', 'comment': 'The response provides necessary detail about the implementation while maintaining clarity, including relevant parameters, considerations, and example usage without unnecessary verbosity.'}, 'content_safety': {'score': 'No issues', 'comment': 'The content focuses purely on geological modeling and scientific calculations, with no concerning elements.'}, 'overall_satisfaction': {'score': 'Pretty good', 'comment': 'The solution offers a practical implementation for modeling salt precipitation, with clear documentation and consideration of key environmental factors.'}}, 'model_b': {'instruction_following': {'score': 'No issues', 'comment': 'The model implements a function that simulates salt precipitation in a sabkha environment, incorporating the requested environmental parameters and producing relevant outputs.'}, 'truthfulness': {'score': 'No issues', 'comment': 'The code implementation aligns with the explanation, showing accurate modeling of salt precipitation based on physical parameters. The output demonstrates expected behavior in salinity changes and precipitation patterns.'}, 'conciseness': {'score': 'Just right', 'comment': 'The response provides a well-structured explanation with appropriate detail level, including key parameters and considerations without excessive information.'}, 'content_safety': {'score': 'No issues', 'comment': 'The content remains focused on scientific modeling and geological processes without any concerning elements.'}, 'overall_satisfaction': {'score': 'Pretty good', 'comment': 'The solution provides a comprehensive approach to modeling salt precipitation, with clear implementation and consideration of relevant physical parameters.'}}, 'comparison': {'score': 'Model A is slightly better than Model B', 'comment': "While both models provide solid implementations, Model A edges ahead with its more detailed precipitation process and clearer accumulation pattern in the output. Model A's implementation shows a more realistic gradual increase in salt precipitation over time, whereas Model B's output shows less variation in precipitation values. Both models handle the core requirements well, but Model A's more nuanced approach to the precipitation process makes it marginally more suitable for paleoenvironment reconstruction."}}
        message = self.client.messages.create(
            model=model,
            max_tokens=1520,
            temperature=0.3,
            system=self.prompts.SYSTEM_COMPARE,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": self.prompts.generate_comparison_examples(language),
                        },
                        {
                            "type": "text",
                            "text": self.prompts.build_prompt(
                                prompt, model_a, model_b, output
                            ),
                        },
                    ],
                }
            ],
        )
        return json.loads(message.content[0].text)

    def reevaluate_responses(
        self,
        prompt: str,
        model_a: str,
        model_b: str,
        code_output: str,
        comparison_response: str,
        requested_changes: str,
        language: _Prompts.Languages = _Prompts.Languages.PYTHON
    ) -> dict:
        """
        Reevaluates the comparison response and returns the final response.

        Args:
            prompt: The user prompt.
            model_a: The response of the first model.
            model_b: The response of the second model.
            code_output: The output of the code.
            comparison_response: The first comparison evaluation.
            requested_changes: The changes requested by the reviewer.

        Returns:
            The re-evaluated comparison for the models.
        """
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": self.prompts.generate_comparison_examples(language),
                    },
                    {
                        "type": "text",
                        "text": self.prompts.build_prompt(
                            prompt, model_a, model_b, code_output
                        ),
                    },
                ],
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": comparison_response}],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": requested_changes,
                    }
                ],
            },
        ]
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1520,
            temperature=0.3,
            messages=messages,
        )
        text = message.content[0].text
        try:
            return json.loads(text[text.index("{") : text.rindex("}") + 1])
        except json.decoder.JSONDecodeError:
            return text
