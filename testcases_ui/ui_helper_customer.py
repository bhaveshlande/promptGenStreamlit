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
option = None

# Set up the layout with two columns
st.set_page_config(
        page_title="Ex-stream-ly Cool App",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )

# Launch function will launch the UI for the test case generator and take the user input
# It will then use the user input to generate test cases using the UnitTestCaseGenerator class
def Launch():
    # Define CSS styles for the header and logo
    # Define CSS styles for the header and logo
    # Define the CSS style for the header
    # Define the CSS style for the header
    header_style = "background-color:light-grey; color: black; padding: 10px; text-align: center;"

    # Apply CSS styles to the header
    st.markdown(
        f"<div style='{header_style}'>"
        "<h1 style='margin-left: 10px;'>GENERATIVE AI POWERED SOFTWARE PRODUCT ENGINEERING</h1>"
        "</div>",
        unsafe_allow_html=True
    )

    # Create a container for the logo and text
    header_container = st.container()

    # Load and display the logo with CSS for positioning
    header_container.markdown(
        f"<div style='display: flex; justify-content: flex-end;'>"
        "<div style='margin-right: 10px;'>"
        "</div>"
        "<div>"
        "Powdered by Capgemini"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )
    global topP, topK, temperature, language, inputTaken, customPrompt

    # Create a Session State object to track the button state
    session_state = st.session_state
    if 'generate_button_clicked' not in session_state:
        session_state.generate_button_clicked = False

    # Set up the layout with two columns
    left_column, right_column = st.columns([5, 2])

    with left_column:
        with st.container():
            prompt = st.text_area("", height=200,
                                  placeholder="Enter your code here if you have text as input prompt:")

            generate_button_label = "Generate"

            generate_button_disabled = len(prompt.strip()) == 0 or session_state.generate_button_clicked
            generate_button_clicked = st.button(generate_button_label, disabled=generate_button_disabled)

            if generate_button_clicked:
                # Create a CSS class to center the spinner
                st.markdown(
                    """
                    <style>
                    .spinner-container {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 200px; /* Adjust the height as needed */
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )
                with st.spinner("Cooking up your test-cases!"):
                    # Generate test cases
                    prompt, outfile = pt.GetPrompt(prompt, language)
                    utGen = ut.UnitTestCaseGenerator(temperature, topK, topP)
                    utGen.prompt = prompt
                    test_cases = utGen.Generate_test_case()
                    ce.extract_code(prompt, test_cases, outfile, language)

                    # Display test_cases and enable the button after it's done
                    st.write(test_cases)
                    session_state.generate_button_clicked = False
                    st.success('Done!')

    # Right Column - Dropdown, Radio Buttons, and Download Button
    with right_column:
        # Dropdown to select language
        lang_options = ['Python', 'Golang', 'C++', 'JavaScript', 'Java', 'SQL', 'ManualTestCase', 'AutomationTestCase',
                        'Other']
        language = st.selectbox('Select a Language', lang_options)

        # Radio button to choose between file upload or text input
        radio_button = "Radio Options"
        option = st.radio("Upload a file or enter text as a prompt to Amazon Bedrock:", ["Text", "File"],
                          key=radio_button)

        # File Uploader
        if option == "File":
            file = st.file_uploader("Upload a file")
            st.write("Upload a file to generate test cases")


if __name__ == "__main__":
    st.markdown("<h1 style='text-align: center; color: White;'></h1>", unsafe_allow_html=True)
    Launch()
