import sys
import spacy
import string
import pandas as pd
import numpy as np
import re
from collections import Counter
from spacy.lang.en.stop_words import STOP_WORDS
from textblob import TextBlob
import vertexai
from vertexai.language_models import TextGenerationModel
import sys
import os    

credential_path = "C:\\Users\\bbaliram\\AppData\\Roaming\\gcloud\\application_default_credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


vertexai.init(project="genai-loreal-sandbox", location="us-central1")
parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1000,
    "temperature": 0.2,
    "top_p": 0.8,
    "top_k": 40
}


#load the english dictory
nlp = spacy.load("en_core_web_sm")

#openai.api_key = "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"

all_stopwords = nlp.Defaults.stop_words

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


def ask_specific_question(input_prompt):
    
        prompt=f"ask question to understand the context of {input_prompt} "
        model = TextGenerationModel.from_pretrained("text-bison@001")
        question = model.predict(prompt)
        
        return question

# def count_specific_words(prompt):
#     # Create a regular expression to match specific words
#   specific_words_regex = r"\b[A-Za-z]+\b"

#   # Find all specific words in the prompt
#   specific_words = re.findall(specific_words_regex, prompt)

#   # Return the number of specific words
#   return len(specific_words)

def calculate_focus(prompt):
    #Create a regular expression to match focus words
    
    focus_words_regex = r"\b(main|primary|essential|important)\b"

    complete_doc = nlp(prompt)
    words = [
        token.text
        for token in complete_doc
        if not token.is_stop and not token.is_punct
    ]
    focus = Counter(words).most_common(5)
    
     # Find all focus words in the prompt
    focus_words = re.findall(focus_words_regex, prompt)
    

  # If there are no focus words in the prompt, then the focus is unclear
    if len(focus_words) == 0:
        return 0.0

  # Otherwise, the focus is clear
    return 1.0
  

def main():
    input_prompt = input("Enter a prompt: ")
    temp = float(input("\n Enter temperature: \n "))
    
    quest = ask_specific_question(input_prompt)
    question = quest
    print(question)
    answer_prompt = input("Enter answer prompt: ")
    
    res = generate_better_prompt(input_prompt,temp,question)
    
    better_prompt = res  
    print("\nOriginal Prompt:")
    print(input_prompt)
    
    import spacy    
    # Load the English NLP model from spaCy
    nlp = spacy.load("en_core_web_sm")
    print("\nBetter Prompt:")
    print("\n")
    print(better_prompt)
    specificity, clarity, relevance = evaluate_prompt(f"{better_prompt}")
        # Output scores
    print("Specificity Score:", specificity)
    print("Clarity Score:", clarity)
    print("Relevance Score:", relevance)

    
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

if __name__ == "__main__":
    main()
