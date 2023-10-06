import os
import streamlit as st
from PIL import Image
import testcases_ui.ui_helper_utc as ui_helper_utc
import testcases_ui.ui_helper_tc as ui_helper_tc


#from incontext_learn_refactored_ver2 import generate_response
#import config

selected_section = None
selected_page = None

# Define functions for each page
def page_1a():
    st.write("This is Page 1a")


def page_1b():
    st.write("This is Page 1b")


def page_1c():
    st.write("This is Page 1c")


def page_2a():
    st.write("This is Page 2a")


def page_2b():
    '''
    st.header("Text Generation App")

    # Temperature slider
    #temperature = st.slider("Temperature", 0.01, 1.0, 0.01, format="%f")

    choice = st.selectbox(
        "Select the type of file you want to upload?", ("txt", "py")
    )

    st.write("You have selected:", choice)

    # File upload
    if choice == "txt":
        uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
    else:
        uploaded_file = st.file_uploader("Upload a python file", type=["py"])
    

    #txt_input = ""

    if uploaded_file is not None:
        txt_input = uploaded_file.read()

   # result = ["111222", "2345"]

    ip = st.radio(
        "Do you want to do incontext learning? 👉",
        key="incontext_learning",
        options=["yes", "no"],
    )

    # Download button for the generated text
    result = []
    with st.form('summarize_form', clear_on_submit=True):
        submitted = st.form_submit_button('Submit')
        with st.spinner('Calculating...'):
            if submitted:
                if ip =='yes':
                    response = generate_response(txt_input,choice, incontext_learning= True )
                    result.append(response)
                else:
                    response = generate_response(txt_input,choice, incontext_learning= False)
                    result.append(response)
    
    if len(result):
        st.info(response)

    if len(result) > 0:
        # Provide a unique filename for the downloaded file
        download_filename = "generated_output.txt"

        # Create a download button
        st.download_button(
            label="Download Output",
            data=response.encode('utf-8'),
            key="download_output",
            file_name=download_filename,
            mime="text/plain",
        )
    '''
def page_2c():
    st.write("This is Page 2c prompt generation")


def page_3a():
    st.write("This is Page 3a")


def page_3b():
    st.write("This is Page 3b")


def page_4a():
    st.header("Unit test case generation App")
    ui_helper_utc.Launch()


def page_4b():
    st.header("Test case generation App")
    ui_helper_tc.Launch()


if __name__ == "__main__" :
    logo_path = os.path.join(os.path.dirname(__file__), 'data','img.png')
    # Load the CG logo
    logo = Image.open(logo_path)

    st.image(logo, width=50)
    st.title("Generative AI Powered Software Product Engineering")

    page_hierarchy = {
        "Knowledge Management": {
            "Sub-Pages": ["Document Chatbot", "Database Chatbot", "Code Chatbot"],
        },
        "Solutioning": {
            "Sub-Pages": ["Document to User-Story", "Code to User Story","Prompt Generation"],
        },
        "Coding": {
            "Sub-Pages": ["Code Generation", "Code Transformation"],
        },
        "Testing": {
            "Sub-Pages": ["Unit Test Creation", "Test Cases Generation"],
        },
    }

    # Create a Streamlit sidebar with top-level headings as text
    st.sidebar.title("Categories")

    # Initialize selected_section and selected_page with defaults
    if 'selected_section' not in st.session_state: 
        st.session_state['selected_section'] = list(page_hierarchy.keys())[3]

    if 'selected_page' not in st.session_state:
        st.session_state['selected_page'] = page_hierarchy[st.session_state['selected_section']]["Sub-Pages"][0]

    # Create a Streamlit sidebar with buttons for the sub-pages under the selected section
    for section, sub_pages in page_hierarchy.items():
        st.sidebar.subheader(section)
        for sub_page in sub_pages["Sub-Pages"]:
            if st.sidebar.button(sub_page):
                st.session_state['selected_section'] = section 
                st.session_state['selected_page'] = sub_page

    # Display the selected section name
    st.sidebar.markdown(f"**Selected Section:** {st.session_state['selected_section']}")

    # Display the selected sub-page name
    st.sidebar.markdown(f"**Selected Sub-Page:** {st.session_state['selected_page']}")
    # Update the page hierarchy with the corresponding functions
    page_hierarchy["Knowledge Management"]["Document Chatbot"] = page_1a
    page_hierarchy["Knowledge Management"]["Database Chatbot"] = page_1b
    page_hierarchy["Knowledge Management"]["Code Chatbot"] = page_1c

    page_hierarchy["Solutioning"]["Document to User-Story"] = page_2a
    page_hierarchy["Solutioning"]["Code to User Story"] = page_2b
    page_hierarchy["Solutioning"]["Prompt Generation"] = page_2c


    page_hierarchy["Coding"]["Code Generation"] = page_3a
    page_hierarchy["Coding"]["Code Transformation"] = page_3b

    page_hierarchy["Testing"]["Unit Test Creation"] = page_4a
    page_hierarchy["Testing"]["Test Cases Generation"] = page_4b

    # Call page function
    page_function = page_hierarchy[st.session_state['selected_section']][st.session_state['selected_page']]
    page_function()
