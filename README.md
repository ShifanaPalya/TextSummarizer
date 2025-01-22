# TextSummarizer
An AI powered text summarizer application to summarize long piece of text to user desired length summaries.
3 modes are provided to the user to choose the length in which the summary is needed, which are:

1. Short - Summarizes the input text in 50 words
2. Medium - Summarizes the input text in 100 words
3. Long - Summarizes the input text in 300 words

This project is built using python 3.10.13 and Llama3-70B model is used for summarization to which the prompt along with the input text and summarization mode is passed that generates summaries in bullet points as specified in the prompt. Calls to the LLM model is made through Groq API for faster inferencing. Backend of this project is implemented using FastAPI exposing the summarization tool as an API. Streamlit framework is used for an interactive UI which is quick to setup and higly user-friendly.

Steps to run the project in local:

1. Create a virtual env with Python version 3.10.13
2. Install requirements.txt
3. Start the server by running the command "uvicorn app:app"
4. Open another terminal and run the streamlit app with the command "streamlit run front_end.py"

### Snapshot of summary generated with "Short" mode being selected:

![Alt text](https://github.com/ShifanaPalya/TextSummarizer/blob/main/summary_short_50.png?raw=true "Optional Title")


### Snapshot of summary generated with "Medium" mode being selected:

![Alt text](https://github.com/ShifanaPalya/TextSummarizer/blob/main/summary_medium_100.png?raw=true "Optional Title")


### Snapshot of summary generated with "Long" mode being selected:

![Alt text](https://github.com/ShifanaPalya/TextSummarizer/blob/main/summary_long_300.png?raw=true "Optional Title")

#### Future improvements in consideration:

Implement a functionality to upload any kind of document(pdf, text, url) and generate summaries.
