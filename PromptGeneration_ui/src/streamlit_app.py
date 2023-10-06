import streamlit as st
import requests

# Define the API endpoint URL
API_URL = "http://localhost:5000/processData"  # Replace with your Flask API URL

st.title("Better Prompt Generator")

# Create input fields and widgets
text_area_input = st.text_area("Enter a prompt:")
max_tokens = st.number_input("Max Tokens:", min_value=1, value=50)
temperature = st.slider("Temperature:", min_value=0.1, max_value=1.0, value=0.7)

if st.button("Generate Better Prompt"):
    # Make a POST request to your Flask API
    data = {
        "textAreaInput": text_area_input,
        "maxTokens": max_tokens,
        "temperature": temperature,
    }
    response = requests.post(API_URL, json=data)

    if response.status_code == 200:
        result = response.json()

        # Display the generated better prompts and related information
        st.subheader("Generated Better Prompts:")
        for i, better_prompt in enumerate(result["betterPrompts"]):
            st.write(f"{i + 1}. {better_prompt}")
        # Display similarities and scores as well if needed

    else:
        st.error("Error generating better prompts. Please check your input.")
