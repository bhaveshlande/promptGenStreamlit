import streamlit as st
import sys
import os
import spacy
import string
import time
import pandas as pd
import numpy as np
import re
from collections import Counter
from spacy.lang.en.stop_words import STOP_WORDS
from textblob import TextBlob
import vertexai
from vertexai.language_models import TextGenerationModel

# Set the Google Cloud credentials path
credential_path = "C:\\Users\\bbaliram\\AppData\\Roaming\\gcloud\\application_default_credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# Initialize Vertex AI
vertexai.init(project="genai-loreal-sandbox", location="us-central1")

temperature=0.2
# Parameters for text generation model
parameters = {
        "candidate_count": 1,
        "max_output_tokens": 1000,
        "temperature": temperature,
        "top_p": 0.8,
        "top_k": 40
    }

# Load the English dictionary
nlp = spacy.load("en_core_web_sm")

# All stopwords from spaCy
all_stopwords = nlp.Defaults.stop_words

def generate_better_prompt(input_prompt,temp, context,answer_prompt):
    
    # Remove punctuation
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for ele in input_prompt:
        if ele in punc:
            input_prompt = input_prompt.replace(ele, "")
    doc = nlp(input_prompt)
    
    # Sentiment analysis using TextBlob
    blob = TextBlob(input_prompt)
    
    # Tokenize the input and perform POS tagging
    token_list = [token for token in doc if not token.is_stop]
    arr = []
    for token in token_list:
        if str(token) != "\n":
            mat = np.append(arr, [str(token.text), str(token.tag_), str(token.dep_), str(token.head.text)], axis=0)
    
    # Get the length of input prompt tokens
    len_input = len(token_list)
    
    # Get named entities from tokens
    named_entities = [ent.text for ent in token_list]
    
    prompt = f"I want you to act as a creative AI prompt generator. Given an input prompt with the following entities: \
        {''.join(named_entities)} having, context is {context}, your task is to generate a better prompt on given answer by user{answer_prompt} \
        The prompt should be specific, clear, easy to understand, open-ended, interesting, and relevant to the context of the conversation.\
        The prompt should start with \"I want you to act as \", and expand the prompt accordingly. Describe the content to make it useful."

    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(prompt)
    return response

def ask_specific_question(input_prompt):
    prompt = f"ask a question to understand the context of {input_prompt}"
    model = TextGenerationModel.from_pretrained("text-bison@001")
    question = model.predict(prompt)
    return question

def calculate_focus(prompt):
    focus_words_regex = r"\b(main|primary|essential|important)\b"
    complete_doc = nlp(prompt)
    words = [
        token.text
        for token in complete_doc
        if not token.is_stop and not token.is_punct
    ]
    focus = Counter(words).most_common(5)
    focus_words = re.findall(focus_words_regex, prompt)
    
    if len(focus_words) == 0:
        return 0.0
    return 1.0

def evaluate_prompt(prompt):
    doc = nlp(prompt)
    specific_nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    specificity_score = len(specific_nouns) / len(doc)
    
    clarity_score = 1 - (len(doc) - len(doc.ents)) / len(doc)
    
    relevant_verbs = [token.text for token in doc if token.pos_ == "VERB"]
    relevant_adjectives = [token.text for token in doc if token.pos_ == "ADJ"]
    relevance_score = (len(relevant_verbs) + len(relevant_adjectives)) / len(doc)
    
    return specificity_score, clarity_score, relevance_score

def Launch():
    # st.title("AI Prompt Generator and Evaluator")
    

    # by using two button one for add and second for minus
    # temp = st.number_input("Enter temperature:", min_value=0.0, max_value=1.0, value=0.2, step=0.01)

    #by using selectbox
    # temp_options = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    # temp = st.selectbox("Select Temperature:", temp_options)

    # by using slider
    # temp = st.slider("Select Temperature:", min_value=0.0, max_value=1.0, value=0.2, step=0.01)
    
    #by using radio button
    # Display descriptive labels for temperature options
    # st.write("Select the Temperature Option:")
    # option = st.radio("Option:", ("Creative", "Balanced", "Precise"))


    # # Define text options
    # text_options = ["Creative", "Balanced", "Precise"]

    # # Create a slider for selecting text options
    # selected_option = st.select_slider("Select an Option:", options=text_options)

    # # Display the selected text option
    # st.write(f"Selected Option: {selected_option}")
   
   if st.button("Next"):
    input_prompt = st.text_area("Enter a prompt:")
    if input_prompt:
        st.write(f"Value 1: {input1}")
        st.write("Now enter value 2 and click 'Submit'")
    else:
        st.warning("Please enter value 1 before proceeding.")
    
    Original_input_prompt= input_prompt

    # Define text options and their corresponding temperature values
    text_options = {
        "Creative": 1.0,
        "Balanced": 0.5,
        "Precise": 0.2
    }

    # Create a slider for selecting text options
    selected_option = st.select_slider("Select an Option for better output:", options=list(text_options.keys()))

    # Get the temperature value based on the selected option
    temp = text_options[selected_option]

    # Display the selected text option and the corresponding temperature value
    # st.write(f"Selected Option: {selected_option}")
    # st.write(f"Selected Temperature Value: {temp}")

 
    
    if st.button("Generate Better Prompt"):
        if not input_prompt:
            st.warning("Please enter a prompt before clicking 'Generate Better Prompt'.")
        else:
            quest = ask_specific_question(input_prompt)
            question = quest
            st.write(f"Generated Question for Context Understanding: {question}")
            if question is not None:
                answer_prompt = st.text_area("Enter answer prompt:")
            
                if answer_prompt is not None:
                    button_clicked2 = st.button("Submit answer prompt")

                    if button_clicked2 and answer_prompt is not None:
                        st.warning("Please enter an Answer for question before Generating prompt'.")
                    else:
                        for i in range(20):
                            time.sleep(1)
                        res = generate_better_prompt(Original_input_prompt, temp, question,answer_prompt)
                        st.write("\nOriginal Prompt:")
                        st.write("\t",input_prompt)
                        st.write("\nBetter Prompt:")
                        st.write("\n")
                        st.write("\t",f"{res}")
                            
                        specificity, clarity, relevance = evaluate_prompt(f"{res}")
                        st.write("Specificity Score:", specificity)
                        st.write("Clarity Score:", clarity)
                        st.write("Relevance Score:", relevance)

                else:
                    st.warning("Please enter answer prompt'.")
            else:
                st.warning("question is not generate wait...'.")
    else:
        st.warning("Please click the button next Generate Better Prompt'.")

if __name__ == "__main__":
    Launch()
