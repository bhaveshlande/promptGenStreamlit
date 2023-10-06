import sys
sys.path.append("AWS-Squad/Unit-Test-Generation/utils")
import utils.bedrock as bedrock

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
# Make this class singleton to initialize bedrock_client once
@singleton
class UnitTestCaseGenerator(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    # Constructor
    def __init__(self, temperature=0.5, top_k=10, top_p=0.5, 
                  max_tokens_to_sample=4096, stop_sequences=["\n\nHuman"]):
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
    
    # Generates the test case using the Bedrock class.
    def Generate_test_case(self, custom_client=False):
        response = self.bedrock_client(str(self.prompt))
        return response