from langchain import PromptTemplate

def GetPrompt(user_input, language):
    if language == 'Python':
        return GetPythonPrompt(user_input), "response_test.py"
    elif language == 'Java':
       return GetJavaPrompt(user_input), "response_test.java"
    elif language == 'C++':
         return GetCppPrompt(user_input), "response_test.cpp"
    elif language == 'Golang':
         return GetGolangPrompt(user_input), "response_test.go"
    elif language == 'JavaScript':
         return GetJavaScriptPrompt(user_input), "response_test.js"
    elif language == 'SQL':
         return GetDefaultPrompt(user_input, "sql"), "response_test.sql"
    elif language == 'AutomationTestCase':
         return GetAutomationtestcasePrompt(user_input), "response_automation_test_cases.txt"
    elif language == 'ManualTestCase':
         return GetManualtestcasePrompt(user_input), "response_manual_test_cases.txt"
    else:
        return GetDefaultPrompt(user_input, language), "response_test.{}".format(language)


def GetCppPrompt(user_input, unit_test_package='gtest'):
    multi_var_prompt = PromptTemplate(
    input_variables=["code", "unit_test_package"],
    template="""Human: Unit testing is an essential part of the software development process, ensuring the correctness and robustness of individual units of code. Here, I will present some industry best practices for writing comprehensive unit test cases in C++, including detailed documentation, mock data, classes, code coverage, and suggestions. 
    - Choose a reliable and widely-used C++ testing framework like Google Test or Catch2 to write your test cases.
    - Familiarize yourself with the framework's syntax and capabilities, as they often provide built-in mocking and assertion functionalities.
    - Follow the AAA Pattern:
    - Name your test cases descriptively to convey their purpose, inputs, and expected outputs.
    - Use sentence-style naming conventions, such as "should_return_correct_sum" or "should_throw_exception_on_invalid_input."
    - Document Test Cases
    - Mock data and classes allow you to simulate real-world scenarios and control test environments.
    - Use mock data to test specific edge cases, error conditions, or invalid inputs.
    - Create mock classes/interfaces for external dependencies to isolate your code and perform focused unit testing.
    - Aim for comprehensive code coverage by exercising all branches and statements in your code.
    - Use code coverage tools like GCC’s coverage analysis (-fprofile-arcs -ftest-coverage) or Clang's `-fprofile-instr-generate` to identify areas lacking proper testing.
    - Maintain a reasonable coverage percentage, typically above 80%, depending on the project's complexity.
    - Consider Test-Driven Development (TDD):
    - Distinguish Between Unit and Integration Tests:
    - Prioritize Test Maintainability:
    - Remember that these best practices are not exhaustive, and can adapt to the specific needs and constraints of your project. Regularly review and improve your unit testing processes as new industry practices emerge.

    Write a suite of unit tests for the function, following the cases above. Include helpful comments to explain each line. Reply only with code, formatted as follows:
    ```cpp
    # imports
    include {unit_test_package}  # used for our unit tests
    {{insert other imports as needed1}}

    # function to test
    {code}

    # unit tests
    {{insert unit test code here}}
    ```
    Assistant:
    """
    )
    # Pass in values to the input variables
    prompt = multi_var_prompt.format(code=user_input, unit_test_package=unit_test_package)
    return prompt


def GetGolangPrompt(user_input, unit_test_package = 'go_test'):
    multi_var_prompt = PromptTemplate(
    input_variables=["code", "unit_test_package"],
    template="""Human: You are an expert golang architect. Please share industries' best practices to write unit test-cases with minute details, mock data and classes (if needed). Add documentation for each test-case. Include code coverage and suggestions. Curate it for prompt engineering
    When writing unit test cases in Go, there are several best practices to follow:
     - Write independent test cases 
     - Use the testing package `{unit_test_package}`
     - Begin by importing the {unit_test_package} library and the code to be tested.
     ```go
        import (
        "testing"
        "your_package"
        )
    ```
    - Write test functions with names beginning with `Test`. These functions should accept a `*testing.T` parameter to report test failures.
    ```go
        func TestYourFunctionName(t *testing.T) {{Test logic goes here
        }}
    ```
     - Include test coverage: Use the `-cover` flag while running your tests to check the code coverage.
     - Use table-driven tests
     ```go
        func TestYourFunction(t *testing.T) {{
        t.Run("TestCase1", func(t *testing.T) {{
        // Test logic for case 1
        }})
        t.Run("TestCase2", func(t *testing.T) {{
        // Test logic for case 2
        }})
        }}
        ```
     - Follow the Arrange, Act, and Assert (AAA) pattern
     - Test edge cases and non-happy paths: Don't just focus on the typical scenarios
     - Include mocking function by using the `gomock` package
        ```go
            package test
            import "testing"
            func mockData() any {{
            // Define your mock data here
            var data any = ...
            return data 
            }}
            func TestSomething(t *testing.T) {{
            data := mockData()

            // Use mock data in tests
            ...
            }}
        ```
     

    To help unit test the function {code}, list diverse scenarios that the function should be able to handle (and under each scenario, include a few examples as sub-bullets)
    Using Golang and the `{unit_test_package}` package, write a suite of unit tests for the function, following the cases above.Use the package name same as given in the code snippet.
    Include helpful comments to explain each line. Reply only with code do not create function for test coverage instead write coverage in comment at the last,
    formatted as follows:

    ```go
    # imports
    package main
    import {unit_test_package}  # used for our unit tests
    {{insert other imports as needed}}

    # function to test
    {code}

    # unit tests
    {{insert unit test code here}}
    //end here
    // test coverage {{ write code coverage here}}
    ```
    Assistant:
    """
    )
    # Pass in values to the input variables
    prompt = multi_var_prompt.format(code=user_input, unit_test_package=unit_test_package)
    return prompt

def GetPythonPrompt(user_input, unit_test_package = "pytest"):
    unit_test_package = "pytest"
    example_function = user_input
    package_comment = "# below, each test case is represented by a tuple passed to the @pytest.mark.parametrize decorator"
    plan_user_message = f"""Human: A good unit test suite should aim to:
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
Using Python and the `{unit_test_package}` package, write a suite of unit tests for the function that covers atleast 90% of code, following the cases above. You need to cover atleas 90% of code coverage while writing unit test functions.
Include helpful comments to explain each line. Reply only with code, formatted as follows:

```python
# imports
import {unit_test_package}  # used for our unit tests
{{insert other imports as needed}}


# unit tests
{package_comment}
{{insert unit test code here}}
```
Assistant:
"""
    return plan_user_message


def GetJavaPrompt(user_input, unit_test_package = 'Mockito'):
       
    multi_var_prompt = PromptTemplate(
    input_variables=["code", "unit_test_package"],
    template="""Human: Unit testing is an essential part of software development to ensure the quality and reliability of the code. Here are some best practices for writing effective unit test cases in Java, along with detailed documentation, mock data, and class suggestions:
    - Use a widely adopted Java testing framework:
    - JUnit is a popular choice for unit testing Java applications. It provides a rich set of assertions, annotations, and test runners.
    - JUnit documentation: https://junit.org/junit5/docs/current/user-guide/
    - Follow the Arrange-Act-Assert (AAA) pattern:
    - Provide a clear and concise description of the test case, including its purpose and expected behavior.
    - Add comments within the test code to explain any implementation-specific details.
    - Test case names should clearly convey their purpose and the scenario being tested.
    - Utilize mocking frameworks, such as Mockito for Java, to generate test doubles (mocks, stubs, or spies) for external dependencies.
    - Method names should follow a standard naming convention (e.g., `testMethodName_GivenCondition_ExpectedResult`)

    To help unit test the function {code}, list diverse scenarios that the function should be able to handle (and under each scenario, include a few examples as sub-bullets)
    Using Java and the `{unit_test_package}` package, write a suite of unit tests for the function, following the cases above. Cover atleast 90 percent of code while writing unit test functions. Include helpful comments to explain each line. Reply only with code, formatted as follows:

    ```java
    # imports
    import {unit_test_package}  # used for our unit tests
    {{insert other imports as needed}}

    # function to test
    {code}

    # unit tests
    {{insert unit test code here}}
    ```
    Assistant:
    """
    )
    # Pass in values to the input variables
    prompt = multi_var_prompt.format(code=user_input, unit_test_package=unit_test_package)
    return prompt

def GetJavaScriptPrompt(user_input, unit_test_package = 'Jest'):
       
    multi_var_prompt = PromptTemplate(
    input_variables=["code", "unit_test_package"],
    template="""Human:You are a world-class Javascript developer with an eagle eye for unintended bugs and edge cases. You write careful, accurate unit tests. When asked to reply only with code, you write all of your code in a single block
    Unit testing is a crucial aspect of software development, enabling developers to verify the correctness of individual units (functions, methods, classes) of their JavaScript code. Here are some best practices to follow when writing unit test cases:
   - Use descriptive names for test cases that specify the behavior being tested.
   - Begin by importing the code to be tested and any necessary testing libraries:
    ```javascript
        import yourFunction from './yourModule';
    ```
   -  Organize your tests using Jest's `describe` and `it` functions. `describe` is used to group related test cases, and `it` defines individual test cases:
    ```javascript
            describe('Your Module or Function', () => {{
            it('should do something', () => {{
            // Test logic goes here
            }});
            it('should do something else', () => {{
            // Test logic goes here
            }});
            // Add more test cases as needed
            }});
    ```
   - Follow a consistent naming convention for the tests, such as "should_<expected behavior>_<conditions>".
   - Each test case should be independent and isolated to avoid dependence on the order of execution or shared state.
   - Group related test cases using test suites.
   - Use a testing framework/library such as Mocha, Jest, or Jasmine to organize and run your tests.
   -  For asynchronous code or promises, use `async` and `await` with `resolves` or `rejects` matchers:
    ```javascript
            it('should resolve with the correct value', async () => {{
            await expect(asyncFunction()).resolves.toEqual(expectedValue);
            }});
    ```
   - Arrange-Act-Assert Pattern:
   - Use mock data or create test-specific data to ensure predictable and controlled inputs.
   - Mock external dependencies or use stubs to isolate the unit under test. Use Jest's mocking capabilities to simulate external dependencies or functions.
    ```javascript
        jest.mock('./dependency', () => ({{
        someFunction: jest.fn(() => 'mocked result'),
        }}));
    ```
To help unit test the function {code}, list diverse scenarios that the function should be able to handle (and under each scenario, include a few examples as sub-bullets)
Using JavaScript and the `{unit_test_package}` package, write a suite of unit tests for the function. You need to cover atleast 90 percent of code while writing unit test functions. Include helpful comments to explain each line. Reply only with code and no other textual output, formatted as follows:

    ```javaScript
        # imports
        import {unit_test_package}  # used for our unit tests
        {{insert other imports as needed}}

        # function to test
        {code}

        # unit tests
        {{insert unit test code here}}
    ```
    Assistant:
    """
    )
    # Pass in values to the input variables
    prompt = multi_var_prompt.format(code=user_input, unit_test_package=unit_test_package)
    return prompt

def GetDefaultPrompt(user_input, srcProgrammingLanguage):
       
    multi_var_prompt = PromptTemplate(
    input_variables=["code", "srcProgrammingLanguage"],
    template="""Human: You are a world-class '{srcProgrammingLanguage}' developer with an eagle eye for unintended bugs and edge cases. You write careful, accurate unit tests. When asked to reply only with code, you write all of your code in a single block
    A good unit test suite should aim to:
    - Test the function's behavior for a wide range of possible inputs
    - Test edge cases that the author may not have foreseen
    - Take advantage of the features of unit-test-package to make the tests easy to write and maintain
    - Be easy to read and understand, with clean code and descriptive names
    - Be deterministic, so that the tests always pass or fail in the same way

    To help unit test the function {code}, list diverse scenarios that the function should be able to handle (and under each scenario, include a few examples as sub-bullets)
    Using {srcProgrammingLanguage} language and the unittest package, write a suite of unit tests for the function, following the cases above. Include helpful comments to explain each line. Reply only with code, formatted as follows:

    ```{srcProgrammingLanguage}
    # imports
    import unit-test-package    # used for our unit tests
    insert other imports here

    # function to test
    {code}

    # unit tests
    insert unit test code here
    ```
    Assistant:
    """
    )
     # Pass in values to the input variables
    prompt = multi_var_prompt.format(code=user_input, srcProgrammingLanguage=srcProgrammingLanguage)
    return prompt
    
def GetAutomationtestcasePrompt(AutomationTestRequirement):
    multi_var_prompt = PromptTemplate(input_variables=["AutomationTestRequirement"],
    template="""Human:Test-case suite generation using Appium should aim to:
    - Name your test cases descriptively to convey their purpose, inputs, and expected outputs.
    - Use fixtures for setup and teardown.
    - Utilize parameterization to run tests with different data.
    - Implement markers for categorizing and filtering tests.
    - Use command-line options for running tests selectively (e.g., -k, -m).
    - Leverage pytest plugins for reporting and custom test behaviors.
    - Place your test cases in separate test modules.
    - Use conftest.py for fixture definitions and shared setup/teardown code.
    - Use external data files (e.g., JSON, CSV) for test data.
    - Import packages like unittest
    - Use world's best practices for code coverage
    - Reply only with code, you write all of your code in a single block
    
    To help automate test {AutomationTestRequirement}, list diverse test cases that the covers the functionality in userstory (and under each scenario, include a few examples as sub-bullets)
    Using python, write automation code for {AutomationTestRequirement}, following the cases above. Include helpful comments to explain each line. Reply only with automation code, formatted as follows:
    ```python
    # function to automate
    {AutomationTestRequirement}

    # tests
    insert automation code here
    ```
    Assistant:
    """
    )
    # Pass in values to the input variables
    prompt = multi_var_prompt.format(AutomationTestRequirement=AutomationTestRequirement)
    return prompt

def GetManualtestcasePrompt(ManualTestRequirement):
    multi_var_prompt = PromptTemplate(input_variables=["ManualTestRequirement"],
    template="""Human:You are a proficient quality analyst with an eagle eye for unintended bugs and edge cases. A good test case suite should aim to use below steps with their description respectively:
    Test Case Name: One sentence summary of test case
    
    Description: Detailed background of what is being tested and why. Explains the feature or functionality that is being tested.  

    Preconditions: 
    - Any setup needed before the test can be run
    - Initial program state

    Input Data: 
    - Sample input data covering common cases, edge cases, and invalid data
    - Should be easy to read and understand  
    - Cover typical usage, minimum values., maximum values, empty values, invalid values etc.
    
    Test Steps:
    - How to execute a test case with descriptive steps
    - How to utilize the input data to execute a test case

    Expected Output:
    - Detailed description of expected result for each input
    - Cover both positive and negative scenarios
    - Include expected return values, calculations, errors etc.

    Postconditions:
    - Expected system state after the test executes 
    
    To help test the functionality {ManualTestRequirement}, list diverse test cases that the covers the functionality in ManualTestCase (and under each scenario, include Test Case Name:, Preconditions:, Input Data:, Test Steps:, Expected Output:, Postconditions: as heading and description with sub-bullets)
    Using {ManualTestRequirement}, write a suite of tests cases for the functional and non-functional requirement using world's best practices for code coverage, following the cases above. Include helpful comments to explain each line. Reply only with Test Cases, formatted as follows:
    ```{ManualTestRequirement}
    # function to test
    {ManualTestRequirement}

    # tests
    insert ManualTestCase here
    ```
	Assistant:
    """
    )
    # Pass in values to the input variables
    prompt = multi_var_prompt.format(ManualTestRequirement=ManualTestRequirement)
    return prompt

def GetTestCoveragePrompt(code, testcases):
       
    multi_var_prompt = PromptTemplate(
    input_variables=["code", "testcases"],
    template="""Human: You are a world-class code analyzer with an eagle eye for unintended bugs and edge cases. Reply with code coverage for the code {code} covered by test {testcases}.
        Human: To calculate code coverage use coverage utility.
       You need to reply with the accurate number of code coverage, calculated by test coverage utility
        for the respective language.
     - Format the ouput like "code_coverage={{Write calculated code coverage here}}". Fill in the placeholder with actual output. Do not reply on actual code
    just give the output as a percentage. Your output should not include anything other than code coverage percentage.
    Assistant:
    """
    )
     # Pass in values to the input variables
    prompt = multi_var_prompt.format(code=code, testcases=testcases)
    return prompt
