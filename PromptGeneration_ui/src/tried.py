import streamlit as st
import spacy
import string
import pandas as pd
import numpy as np
import re
from collections import Counter
from spacy.lang.en.stop_words import STOP_WORDS
from textblob import TextBlob
from vertexai.language_models import TextGenerationModel

# Set the Google Cloud credentials path
import os

try:
    credential_path = "C:\\Users\\bbaliram\\AppData\\Roaming\\gcloud\\application_default_credentials.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
except Exception as e:
    st.error(f"Error setting Google Cloud credentials: {str(e)}")

# Initialize Vertex AI
import vertexai

try:
    vertexai.init(project="genai-loreal-sandbox", location="us-central1")
except Exception as e:
    st.error(f"Error initializing Vertex AI: {str(e)}")

# Load the English dictionary
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    st.error(f"Error loading English dictionary: {str(e)}")

# All stopwords from spaCy
all_stopwords = nlp.Defaults.stop_words

def generate_better_prompt(input_prompt, temp, context, answer_prompt):
    try:
        # Remove punctuation
        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        input_prompt = ''.join([char for char in input_prompt if char not in punc])
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
        named_entities = [ent.text for ent in doc]
        named_entities_str = ' '.join(named_entities)

        prompt = f"I want you to act as a creative AI prompt generator. Given an input prompt with the following entities: {named_entities_str} having, context is {context}, your task is to generate a better prompt on given answer by user {answer_prompt} The prompt should be specific, clear, easy to understand, open-ended, interesting, and relevant to the context of the conversation. The prompt should start with \"I want you to act as \", and expand the prompt accordingly. Describe the content to make it useful."

        model = TextGenerationModel.from_pretrained("text-bison@001")
        response = model.predict(prompt)
        st.write(response)
        return response
        
    except Exception as e:
        st.error(f"Error generating better prompt: {str(e)}")


def ask_specific_question(input_prompt):
    try:
        prompt = f"ask a question to understand the context of {input_prompt}"
        model = TextGenerationModel.from_pretrained("text-bison@001")
        question = model.predict(prompt)
        return question
    except Exception as e:
        st.error(f"Error asking specific question: {str(e)}")


def calculate_focus(prompt):
    try:
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
    except Exception as e:
        st.error(f"Error calculating focus: {str(e)}")


def evaluate_prompt(prompt):
    try:
        doc = nlp(prompt)
        specific_nouns = [token.text for token in doc if token.pos_ == "NOUN"]
        specificity_score = len(specific_nouns) / len(doc)

        clarity_score = 1 - (len(doc) - len(doc.ents)) / len(doc)

        relevant_verbs = [token.text for token in doc if token.pos_ == "VERB"]
        relevant_adjectives = [token.text for token in doc if token.pos_ == "ADJ"]
        relevance_score = (len(relevant_verbs) + len(relevant_adjectives)) / len(doc)

        return specificity_score, clarity_score, relevance_score
    except Exception as e:
        st.error(f"Error evaluating prompt: {str(e)}")

def display_output(input_prompt, better_prompt):
    st.write("\nOriginal Prompt:")
    st.write(input_prompt)
    st.write("\nBetter Prompt:")
    st.write("\n")
    st.write(better_prompt)

    specificity, clarity, relevance = evaluate_prompt(f"{better_prompt}")
    st.write("Specificity Score:", specificity)
    st.write("Clarity Score:", clarity)
    st.write("Relevance Score:", relevance)

def Launch():
    try:

        # st.title("AI Prompt Generator and Evaluator")

        with st.form('addPrompt'):
            # gettting input 
            input_prompt = st.text_area("Enter a prompt:")     

            #getting temp value
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
            submit = st.form_submit_button('Generate Better Prompt')
        
        if submit:
            if not input_prompt:
                st.warning("Please enter a prompt before clicking 'Generate Better Prompt'.")
            else:
                # col1i, col2i= st.columns(2)

                question = ask_specific_question(input_prompt)
                with st.form('answerPrompt'):
                    col1,col2 = st.columns([1,2])
                    with col1:
                        st.write(f"Generated Question for Context Understanding: {question}")
                    with col2:
                        answer_prompt = st.text_input("Enter answer prompt:")     
                        # button_clicked2 = st.button("Submit answer prompt")
                        button_clicked2 = st.form_submit_button('Submit answer prompt')
                    
                if button_clicked2:
                    if not answer_prompt:        
                        st.warning("Please enter an Answer for question before Generating prompt'.")   
                    else:
                        better_prompt = generate_better_prompt(input_prompt, temp, question,answer_prompt)
                        display_output(input_prompt, better_prompt)
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
if __name__ == "__main__":
    Launch()
