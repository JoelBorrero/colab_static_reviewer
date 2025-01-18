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

    def generate_test_code_examples(self, language: Languages):
        """
        Generates the examples for the test code prompt.

        Returns:
            The examples for the test code prompt.
        """
        examples = self.data["generate_test_code"].get(language, self.data["generate_test_code"][_Prompts.Languages.JAVASCRIPT])
        response = "<examples>"
        for example in examples:
            response += "<example>"
            for key, value in example.items():
                response += f"<{key.upper()}>{value.replace('\\n', '\n').replace("\\'", "\'")}</{key.upper()}>"
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

    def get_system_compare(self) -> str:
        return self.data["system"]["compare"]

    def get_system_generate_test_code(self) -> str:
        return self.data["system"]["generate_test_code"]

    def get_system_generate_turns(self) -> str:
        return self.data["system"]["generate_turns"]

class AnthropicService:
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.prompts = _Prompts()  # TODO: Build json from the Anthropic generated code (XML)

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
            system=self.prompts.get_system_generate_turns(),
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
            system=self.prompts.get_system_compare(),
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
        try:
            return json.loads(message.content[0].text)
        except json.decoder.JSONDecodeError:
            return message.content[0].text

    def generate_test_code(
        self,
        question: str,
        response: str,
        model: ClaudeModel = ClaudeModel.SONET_3_5,
        language: _Prompts.Languages = _Prompts.Languages.PYTHON
    ) -> dict:
        # return "Here's a minimal test code to verify the functionality of the TokenManager implementation:\n\n```javascript\nimport jwt from 'jsonwebtoken';\n\n// First, import all the classes from the response\n// (Assuming they're in the same file or properly exported)\n\n// Test function\nasync function runTests() {\n    console.log('Starting TokenManager Tests\\n');\n    \n    const secretKey = 'test-secret-key';\n    const tokenManager = new TokenManager(secretKey);\n    \n    // Test 1: Token Generation and Validation\n    console.log('Test 1: Token Generation and Validation');\n    try {\n        const payload = {\n            userId: 123,\n            ipAddress: '127.0.0.1'\n        };\n        \n        const token = tokenManager.generateToken(payload);\n        console.log('Generated Token:', token);\n        \n        const validatedPayload = tokenManager.validateToken(token, payload.ipAddress);\n        console.log('Validated Payload:', validatedPayload);\n        console.log('Test 1: ✅ Success\\n');\n    } catch (error) {\n        console.log('Test 1: ❌ Failed -', error.message, '\\n');\n    }\n    \n    // Test 2: Rate Limiting\n    console.log('Test 2: Rate Limiting');\n    try {\n        const payload = {\n            userId: 456,\n            ipAddress: '127.0.0.2'\n        };\n        \n        // Generate first token (should succeed)\n        const token1 = tokenManager.generateToken(payload);\n        console.log('First token generated successfully');\n        \n        // Try to generate second token (should fail due to rate limit)\n        try {\n            const token2 = tokenManager.generateToken(payload);\n            console.log('Test 2: ❌ Failed - Rate limit not working\\n');\n        } catch (error) {\n            console.log('Expected rate limit error:', error.message);\n            console.log('Test 2: ✅ Success\\n');\n        }\n    } catch (error) {\n        console.log('Test 2: ❌ Failed -', error.message, '\\n');\n    }\n    \n    // Test 3: Token Blacklisting\n    console.log('Test 3: Token Blacklisting');\n    try {\n        const payload = {\n            userId: 789,\n            ipAddress: '127.0.0.3'\n        };\n        \n        const token = tokenManager.generateToken(payload);\n        console.log('Generated token for blacklist test');\n        \n        // Blacklist the token\n        tokenManager.blacklistToken(token);\n        console.log('Token blacklisted');\n        \n        // Try to validate blacklisted token\n        try {\n            tokenManager.validateToken(token, payload.ipAddress);\n            console.log('Test 3: ❌ Failed - Blacklist not working\\n');\n        } catch (error) {\n            console.log('Expected blacklist error:', error.message);\n            console.log('Test 3: ✅ Success\\n');\n        }\n    } catch (error) {\n        console.log('Test 3: ❌ Failed -', error.message, '\\n');\n    }\n}\n\n// Run the tests\nrunTests().catch(console.error);\n```\n\nTo run this test, you'll need to:\n\n1. Install the required dependency:\n```bash\nnpm install jsonwebtoken\n```\n\n2. Save both the implementation and test code in files with `.js` extension\n\n3. Run the test using Node.js with ES modules enabled:\n```bash\nnode --experimental-modules test.js\n```\n\nThis test code verifies three main functionalities:\n1. Token generation and validation\n2. Rate limiting functionality\n3. Token blacklisting\n\nThe tests are designed to be minimal while still covering the core functionality of the TokenManager facade pattern implementation. Each test provides clear output indicating success or failure, making it easy to verify that the implementation is working as expected."
        message = self.client.messages.create(
            model=model,
            max_tokens=4096,
            temperature=0,
            system=self.prompts.get_system_generate_test_code(),
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": self.prompts.generate_test_code_examples(language),
                        },
                        {
                            "type": "text",
                            "text": f"<question>{question}</question><response>{response}</response>"
                        }
                    ]
                }
            ],
        )
        return message.content[0].text

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
