import streamlit as st
import sys
sys.path.append("AWS-Squad/Unit-Test-Generation/src/")
#import unit_test as ut
from src import *
import src.prompt_template as pt
import src.test_case_generator as ut
import src.code_extract as ce
import re
import time

# Global variables to store slider values
topP = float(0.7)
topK = int(30)
temperature = float(0.5)
language = ""
customPrompt = ""

def get_user_input():
    # Title
    global topP, topK, temperature, language, inputTaken, customPrompt
    # Radio button to choose between file upload or text input
    radio_button = "Radio Options"
    option = st.radio("Upload a file or enter text as a prompt to Amazon Bedrock:", ["Text", "File"], key=radio_button)
    # Dropdown to select language
    lang_options = ['Python', 'Golang', 'C++','JavaScript' ,'Java', 'SQL','Other']
    language = st.selectbox('Select a Language', lang_options)
    # If language is not listed in the dropdown, then ask the user to enter the language
    if language == 'Other':
        other_lang = st.text_input('Enter the language you want to use')
        language = other_lang

    if option == "File":
        file = st.file_uploader("Upload a file")
        if file is not None:
            return file.read()
        st.write("Upload a file to generate test cases")
    elif option == "Text":
        text = st.text_input("Enter your code here if you have text as input prompt:")
        return text

# Launch function will launch the UI for the test case generator and take the user input
# It will then use the user input to generate test cases using the UnitTestCaseGenerator class
def Launch():
    global user_input
    # Create a Streamlit button
    user_input = get_user_input()
    generate_button_placeholder = st.empty()  # Create an empty placeholder for the button
    # Enable the "Generate" button only if there is user input
    if user_input:
        if generate_button_placeholder.button("Generate"):
            # After clicking the "Generate" button, replace it with an empty text to hide it
            generate_button_placeholder.empty()
            with st.spinner('Wait for it...'):
                # Generate test cases
                prompt, outfile = pt.GetPrompt(user_input, language)
                utGen = ut.UnitTestCaseGenerator(temperature, topK, topP)
                utGen.prompt = prompt
                test_cases = utGen.Generate_test_case()
                ce.extract_code(user_input, test_cases, outfile, language)
                st.write(test_cases)
                st.success('Done!')

            

if __name__ == "__main__":
    st.markdown("<h1 style='text-align: center; color: Blue;'>Capgemini</h1>", unsafe_allow_html=True)
    Launch()
