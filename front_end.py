import streamlit as st
import requests
import json

# FastAPI endpoint
API_URL = "http://localhost:8000/summarize"

# UI for the summarization tool
st.title("AI-Powered Text Summarizer")
st.write("Enter a long piece of text and get a summary in seconds!")

# User input
text_input = st.text_area("Enter your text here:")
summary_length = st.radio("Select Summary Length:", ["Short", "Medium", "Long"])
language = st.radio("Select Language:", ["English", "French"])

# Submit button
if st.button("Summarize"):
    if not text_input.strip():
        st.error("Please enter some text to summarize.")
    else:
        # API request
        response = requests.post(API_URL, json={"text": text_input, "summary_length": summary_length.lower(), "language": language})
        if response.status_code == 200:
            summary = response.json()["summary"]
            st.subheader("Summary:")
            st.write(summary)
        else:
            st.error("Error: " + response.json().get("detail", "Unknown error"))
