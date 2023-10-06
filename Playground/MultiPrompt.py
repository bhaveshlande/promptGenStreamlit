
"""Multi prompt example"""
# Python Built-Ins:
import json
from utils import bedrock


unit_test_package = 'pytest'

example_function = """def pig_latin(text):
    def translate(word):
        vowels = 'aeiou'
        if word[0] in vowels:
            return word + 'way'
        else:
            consonants = ''
            for letter in word:
                if letter not in vowels:
                    consonants += letter
                else:
                    break
            return word[len(consonants):] + consonants + 'ay'

    words = text.lower().split()
    translated_words = [translate(word) for word in words]
    return ' '.join(translated_words)
"""

package_comment = "# below, each test case is represented by a tuple passed to the @pytest.mark.parametrize decorator"

plan_user_message = f"""
Assistant:You are a world-class Python developer with an eagle eye for unintended bugs and edge cases. You write careful, accurate unit tests. When asked to reply only with code, you write all of your code in a single block

Human:
A good unit test suite should aim to:
- Test the function's behavior for a wide range of possible inputs
- Test edge cases that the author may not have foreseen
- Be easy to read and understand, with clean code and descriptive names
- Be deterministic, so that the tests always pass or fail in the same way
- Follow a clear naming convention for your test functions, making it easy to understand their purpose.
- Provide clear and concise comments within your test cases to explain the test's intention and any test-specific details.
- Give test coverage report in percentage
- Begin by importing the {unit_test_package} library and the code to be tested.

```python
import {unit_test_package}
from your_module import your_function_or_class
```

- Create and reuse mock data or variable references that will be used in your test cases. This helps ensure consistency and repeatability in your tests.

```python
@pytest.fixture
def mock_data():
# Define your mock data here
data = ...
return data
```

- Organize your tests using the `describe` function to group related test cases. Each `describe` block represents a unit of code (function or class) you want to test.

```python
# Describe the unit tests for the provided function or class
def describe_unit_tests():
# Test case 1: Describe the first test case
def it_should_do_something(mock_data):
# Arrange: Set up any necessary preconditions or data
...
# Act: Call the function or method being tested
result = your_function_or_class(...)
# Assert: Check the expected outcome against the actual result
assert result == expected_result
# Test case 2: Describe the second test case
def it_should_do_something_else(mock_data):
...
# Add more test cases as needed
# You can use the @pytest.mark.parametrize decorator for parameterized testing
@pytest.mark.parametrize("input, expected_output", [
(..., ...),
(..., ...),
# Add more parameterized test cases here
])
def it_should_handle_multiple_input_cases(input, expected_output):
# Arrange
...
# Act
result = your_function_or_class(input)
# Assert
assert result == expected_output
```

To help unit test the function {example_function}, list diverse scenarios that the function should be able to handle (and under each scenario, include a few examples as sub-bullets)
Using Python and the `{unit_test_package}` package, write a suite of unit tests for the function, following the cases above. Include helpful comments to explain each line. Reply only with code, formatted as follows:

```python
# imports
import {unit_test_package}  # used for our unit tests
{{insert other imports as needed}}


# unit tests
{package_comment}
{{insert unit test code here}}
```
"""

# # Claude - Body Syntex
body = json.dumps({
                    "prompt": plan_user_message,
                    "max_tokens_to_sample":4096,
                    "temperature":0.5,
                    "top_k":250,
                    "top_p":0.5,
                    "stop_sequences": ["\n\nHuman:"]
                  })

modelId = 'anthropic.claude-v2' # change this to use a different version from the model provider
accept = 'application/json'
contentType = 'application/json'

response = bedrock.get_bedrock_client().invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
response_body = json.loads(response.get('body').read())

print(response_body.get('completion'))