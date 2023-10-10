import streamlit as st
import sys
import os
import spacy
import string
import pandas as pd
import numpy as np
import re
import vertexai

from collections import Counter
from spacy.lang.en.stop_words import STOP_WORDS
from textblob import TextBlob
from vertexai.language_models import TextGenerationModel


credential_path = "C:\\Users\\bbaliram\\AppData\\Roaming\\gcloud\\application_default_credentials.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path

vertexai.init(project="genai-loreal-sandbox", location="us-central1")

# # Set up credentials (if not already done in your environment)
# credential_path = "C:\\Users\\bbaliram\\AppData\\Roaming\\gcloud\\application_default_credentials.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# # Initialize Vertex AI
# vertexai.init(project="genai-loreal-sandbox", location="us-central1")
parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1000,
    "temperature": 0.2,
    "top_p": 0.8,
    "top_k": 40
}
# Load the English dictionary
nlp = spacy.load("en_core_web_sm")


all_stopwords = nlp.Defaults.stop_words

# Function to generate a better prompt
def generate_better_prompt(input_prompt,temp,context):
    #removal of stop words
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for ele in input_prompt:
        if ele in punc:
            input_prompt = input_prompt.replace(ele, "")
    doc = nlp(input_prompt)
    
    #for sentiment analysis. It will return the polarity of the sentence.
    blob = TextBlob(input_prompt)
    
    #tokenize the input and done POS tagging. Fill the matrix and pass it to the model
    token_list = [token for token in doc if not token.is_stop]
    arr = []
    for token in token_list:
        if str(token) != "\n":
            mat = np.append(arr, [ str(token.text), str(token.tag_), str(token.dep_), str(token.head.text) ], axis = 0)
    
    #get the input prompt token length and pass this to create function where max_token is the ceiling value of input token length and 100
    len_input = len(token_list)
    
    #Get the entities from the token
    named_entities =  [ent.text for ent in token_list]
   

    prompt=f"I want you to act as a creative AI prompt generator. Given an input prompt with the following entities: \
            {''.join(named_entities) } having ,context is {context}, your task is to generate a better prompt. \
            The prompt should be specific, clear, easy to understand, open-ended, interesting and relevant to the context of the conversation.\
            The prompt should start with \"I want you to act as \", and expand the prompt accordingly. Describe the content to make it useful."

    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(prompt)
    return response


# Function to ask a specific question
def ask_specific_question(input_prompt):
    
        prompt=f"ask question to understand the context of {input_prompt} "
        model = TextGenerationModel.from_pretrained("text-bison@001")
        question = model.predict(prompt)
        
        return question

# Function to evaluate the prompt
def evaluate_prompt(prompt):
    # Tokenize the prompt using spaCy
    doc = nlp(prompt)
    
    # Specificity Evaluation: Check for specific nouns in the prompt
    specific_nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    specificity_score = len(specific_nouns) / len(doc)
    
    # Clarity Evaluation: Check for clear and concise language
    clarity_score = 1 - (len(doc) - len(doc.ents)) / len(doc)
    
    # Relevance Evaluation: Check for relevant verbs and adjectives
    relevant_verbs = [token.text for token in doc if token.pos_ == "VERB"]
    relevant_adjectives = [token.text for token in doc if token.pos_ == "ADJ"]
    relevance_score = (len(relevant_verbs) + len(relevant_adjectives)) / len(doc)
    
    return specificity_score, clarity_score, relevance_score

# Streamlit UI design

# def main():
#     st.title("Prompt Generation App")

#     # Input prompt
#     input_prompt = st.text_area("Enter a prompt:")
#     temp_option = st.radio("Select Temperature Option:", ("Creative", "Balanced", "Precise"), format_func=lambda option: f" {option}")

#     # Map temperature options to values
#     temp_mapping = {"Creative": 100, "Balanced": 50, "Precise": 10}
#     temp = temp_mapping[temp_option]

#     if st.button("Generate Better Prompt"):
#         question = ask_specific_question(input_prompt)
#         better_prompt = generate_better_prompt(input_prompt, temp, question)
#         st.subheader("Better Prompt:")
#         st.text(better_prompt)

#         # Evaluate and display prompt scores
#         specificity, clarity, relevance = evaluate_prompt(better_prompt)
#         st.subheader("Prompt Scores:")
#         st.write(f"Specificity Score: {specificity}")
#         st.write(f"Clarity Score: {clarity}")
#         st.write(f"Relevance Score: {relevance}")

# if __name__ == "__main__":
#     main()


def main():
    st.title("Prompt Generation App")

    # CSS style for buttons
    st.markdown(
        """
        <style>
        .styled-button {
            background-color: #007BFF;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Input prompt
    input_prompt = st.text_area("Enter a prompt:")

    # Temperature options with associated values
    temp_options = {"Creative": 100, "Balanced": 50, "Precise": 10}
    selected_temp = st.radio(
        "Select Temperature Option:",
        list(temp_options.keys()),
        format_func=lambda option: f"{option}",
    )

    # Get the selected temperature value
    temp = temp_options[selected_temp]

    if st.button("Generate Better Prompt", key="generate_button"):
        question = ask_specific_question(input_prompt)
        better_prompt = generate_better_prompt(input_prompt, temp, question)
        
        # Display output with different colored boxes
        st.markdown(
            f"""
            <div style="background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;">
                <strong>Better Prompt:</strong>
                <br>
                {better_prompt}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Evaluate and display prompt scores
        specificity, clarity, relevance = evaluate_prompt(better_prompt)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("Prompt Scores:")
        st.write(f"Specificity Score: {specificity}")
        st.write(f"Clarity Score: {clarity}")
        st.write(f"Relevance Score: {relevance}")

if __name__ == "__main__":
    main()

