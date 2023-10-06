import sys
import re
sys.path.append("AWS-Squad/Unit-Test-Generation/utils")
import utils.bedrock as bedrock
import src.prompt_template as pt
import streamlit as st

def singleton(class_):
    instances = {}
    def wrapper(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return wrapper

# This class is used to generate unit test cases for the model.
# It takes in the prompt and the temperature, top_k, top_p, max_tokens_to_sample, and stop_sequences as inputs.
# It then uses the Bedrock class to generate the test case.
# TestCoverageGenerator is singleton to avoid re-initializing the Bedrock client.
@singleton
class TestCoverageGenerator(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    # Constructor
    def __init__(self, temperature=0.5, top_k=10, top_p=0.5, 
                  max_tokens_to_sample=300, stop_sequences=["\n\nHuman"]):
         self.max_tokens_to_sample = max_tokens_to_sample
         self.temperature = temperature
         self.top_k = top_k
         self.top_p = top_p
         self.stop_sequences = stop_sequences
         self.prompt = None
         self.bedrock_client = None
         self.custom_bedrock_client = None
         self.bedrock_client = bedrock.get_bedrock_client( inference_modifier = {'max_tokens_to_sample':self.max_tokens_to_sample,
                      "temperature": self.temperature,
                      "top_k": self.top_k,
                      "top_p": self.top_p,
                      "stop_sequences":  self.stop_sequences
                     })
    
    # Generates the test coverage using the LLM model call.
    def generate_test_coverage(self, code, test_cases):
     # Generate test coverage
        self.prompt = pt.GetTestCoveragePrompt(code, test_cases)
        test_coverage = self.bedrock_client(str(self.prompt))
        if __debug__:
            with open("coverage", "w") as f:
                f.write(test_coverage)
        pattern = r'code_coverage=([\d\.]+)'
        match = re.search(pattern, test_coverage)
        if match:
            code_coverage = float(match.group(1))
            text = "Code Coverage (%) = {}".format(int(code_coverage))
            highlighted_text = f"<div style='background-color: white; border-radius: 5px; padding: 2px'><h3><strong>{text}</strong></h3></div>"
            st.markdown(highlighted_text, unsafe_allow_html=True)
