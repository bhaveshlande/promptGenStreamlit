import os
import streamlit as st
from PIL import Image
from src import *
import src.myappv4 as app
import Unit_TestCases.src.appv1 as apptc

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
    st.write("This is Page 2b ")

    
def page_2c():
    app.Launch()


def page_3a():
    st.write("This is Page 3a")


def page_3b():
    st.write("This is Page 3b")


def page_4a():
    apptc.Launch()


def page_4b():
    st.header("Test case generation App")


if __name__ == "__main__" :
    logo_path = os.path.join(os.path.dirname(__file__), 'data','img.png')
    # # Load the CG logo
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
