import re
import streamlit as st
import src.test_coverage as test_coverage

def extract_code(user_input, testcode, outfile, language, pattern=""):
  unknown_language = False
  if pattern == "":
    if language == 'Python':
        pattern = r"```python(.*?)```"
    elif language == 'Java':
       pattern = r"```java(.*?)```"
    elif language == 'C++':
         pattern = r"```cpp(.*?)```"
    elif language == 'Golang':
         pattern = r"```go(.*?)```"
    elif language == 'JavaScript':
         pattern = r"```js(.*?)```"
    elif language == 'SQL':
         pattern = r"```sql(.*?)```"
    elif language == 'ManualTestCase':
         pattern = r"```(.*?)```"
    elif language == 'AutomationTestCase':
         pattern = r"```(.*?)```"
    else:
       pattern = fr"(\s*```{language}\n)(.*)(\n\s*```)"
       unknown_language = True

  matches = re.findall(pattern, testcode, re.DOTALL)

  if matches:
    code = matches[0]
    if unknown_language:
       code = code[1]
    with open(outfile, "w") as f:
      f.write(code)
      if language != 'ManualTestCase' and language != 'AutomationTestCase':
          coverage_gen = test_coverage.TestCoverageGenerator()
          coverage_gen.generate_test_coverage(user_input, code)
      st.download_button('Download testcases file', code, file_name=outfile)

    
