from flask import Flask, request, jsonify
import os
import openai
from dotenv import load_dotenv
import numpy as np
import spacy
import re
from collections import Counter
from spacy.lang.en.stop_words import STOP_WORDS
from textblob import TextBlob

# Configure Flask
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Configure OpenAI API
openai.api_key = os.getenv("OPEN_AI_KEY")

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define utility functions for text analysis


def generate_better_prompt(input_prompt, temperature, max_tokens):
    # Removal of stop words
    punc = """!()-[]{};:'"\,<>./?@#$%^&*_~"""
    for ele in input_prompt:
        if ele in punc:
            input_prompt = input_prompt.replace(ele, "")
    doc = nlp(input_prompt)

    # For sentiment analysis. It will return the polarity of the sentence.
    blob = TextBlob(input_prompt)

    # Tokenize the input and perform POS tagging.
    token_list = [token for token in doc if not token.is_stop]
    arr = []
    for token in token_list:
        if str(token) != "\n":
            mat = np.append(
                arr,
                [
                    str(token.text),
                    str(token.tag_),
                    str(token.dep_),
                    str(token.head.text),
                ],
                axis=0,
            )

    # Get the input prompt token length and pass this to create function where max_token is the ceiling value of input token length and 100
    # len_input = len(max_tokens)

    # Get the entities from the token
    named_entities = [ent.text for ent in token_list]

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Given the input prompt '{input_prompt}', please generate a better prompt with the following entities: {''.join(named_entities) } where part-of-speech tagging is {mat} and sentiment should be {blob.polarity} ",
        max_tokens=max_tokens,
        # max_tokens=max(len_input, 200),
        temperature=temperature,
        n=3,  # how many times output
    )
    return response


def similarity_calculate(input_prompt, better_prompt):
    doc = nlp(input_prompt)
    doc2 = nlp(better_prompt)

    similar = doc.similarity(doc2)
    return similar


def count_specific_words(prompt):
    # Create a regular expression to match specific words
    specific_words_regex = r"\b[A-Za-z]+\b"

    # Find all specific words in the prompt
    specific_words = re.findall(specific_words_regex, prompt)

    # Return the number of specific words
    return len(specific_words)


def calculate_focus(prompt):
    # Create a regular expression to match focus words
    focus_words_regex = r"\b(main|primary|essential|important)\b"

    complete_doc = nlp(prompt)
    words = [
        token.text for token in complete_doc if not token.is_stop and not token.is_punct
    ]
    focus = Counter(words).most_common(5)

    # Find all focus words in the prompt
    focus_words = re.findall(focus_words_regex, prompt)

    # If there are no focus words in the prompt, then the focus is unclear
    if len(focus_words) == 0:
        return 0.0

    # Otherwise, the focus is clear
    return 1.0


def calculate_clear_direction(prompt):
    imperative_verbs = []

    # Process the input text with spaCy
    doc = nlp(prompt)

    # Iterate through the tokens in the processed text
    for token in doc:
        # Check if the token is a verb and has the imperative mood
        if token.pos_ == "VERB":
            imperative_verbs.append(token.text)
    return len(imperative_verbs)


def score_output_prompt(prompt):
    specific_words = count_specific_words(prompt)
    focus = calculate_focus(prompt)
    clear_direction = calculate_clear_direction(prompt)

    score = (specific_words * focus * clear_direction) / 30.0

    return score


# Define Flask route to process data
@app.route("/processData", methods=["POST"])
def process_data():
    try:
        # Access the data sent from the client
        data = request.get_json()

        # Extract the data you need from the JSON request
        text_area_input = data.get("textAreaInput", "")
        max_tokens_str = data.get("maxTokens", "")
        temperature_str = data.get("temperature", "")

        # Check if max_tokens_str and temperature_str are not empty
        if max_tokens_str and temperature_str:
            # Convert maxTokens and temperature to numbers
            max_tokens = int(max_tokens_str)
            temperature = float(temperature_str)

            # Perform server-side operations with the data
            response = generate_better_prompt(text_area_input, temperature, max_tokens)

            # Process the response to extract better prompts and related information
            better_prompts = []
            similarities = []
            scores = []

            for choice in response.choices:
                better_prompt = choice.text.strip()
                similarity = similarity_calculate(text_area_input, better_prompt)
                score = score_output_prompt(better_prompt)

                better_prompts.append(better_prompt)
                similarities.append(similarity)
                scores.append(score)

            # Send a response back to the client with the processed data
            response_data = {
                "betterPrompts": better_prompts,
                "similarities": similarities,
                "scores": scores,
            }

        else:
            response_data = {"error": "Missing input values"}
    except (ValueError, TypeError) as e:
        # Handle the conversion errors or invalid input values here
        response_data = {"error": "Invalid input values"}

    return jsonify(response_data)


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
