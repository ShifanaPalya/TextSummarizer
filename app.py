from fastapi import FastAPI, HTTPException
from langchain.prompts import PromptTemplate
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize.chain import load_summarize_chain
from langchain.docstore.document import Document

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize Groq LLM
llm = ChatGroq(
    model_name="llama3-70b-8192",
    temperature=0.7
)

app = FastAPI(
    title = "Langchain Server",
    version = "1.0",
    description = "A simple Langchain Server"
)

# Input model for summarization requests. Input request can contain only text and summary length.
class SummarizationRequest(BaseModel):
    text: str
    summary_length: str  # "short", "medium", "long"
    language: str # "English", "French"


# Map summary length to word/character limits
length_mapping = {
    "short": 50,
    "medium": 100,
    "long": 300,
}



@app.post("/summarize")
async def summarize_text(request: SummarizationRequest):
    print("!!!!!Printing input text!!!!")
    print(request.text)
    # Validate input length
    if len(request.text) < 50:
        raise HTTPException(status_code=400, detail="Text is too short for summarization.")
    
    # Validate summary length
    length_config = length_mapping.get(request.summary_length.lower())
    print("!!!!!Printing length config!!!!")
    print(length_config)
    if not length_config:
        raise HTTPException(status_code=400, detail="Invalid summary length option.")
    
    language = request.language

    #Split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=100)
    chunks = [Document(page_content=x) for x in text_splitter.split_text(request.text)]
    print("!!!!!Printing chunks!!!!")
    print(len(chunks))
    
    #Define prompts

    question_prompt_template = """
                    Please provide a summary of the following text.
                    TEXT: {text}
                    SUMMARY:
                    """

    question_prompt = PromptTemplate(
        template=question_prompt_template, input_variables=["text"]
    )

    #The following prompt is not giving the summary in bullet points!!
    # refine_prompt_template = """
    #             Write a concise summary of the following text in in exactly {length_config} number of words. 
    #             Make sure to not exceed the word limit.
    #             Return your response in bullet points which covers the key points of the text.
    #             ```{text}```
    #             """

    refine_prompt_template = """
            Write a concise summary of the following text delimited by triple backquotes in {language} language in exactly {length_config} number of words using bullet points.
            Return your response in bullet points which covers the key points of the text.
            ```{text}```
            """

    refine_prompt = PromptTemplate(
        template=refine_prompt_template, input_variables=["language","length_config","text"]
    )

    #Load the summarization chain. Using refine chain type for better summarization.
    try:
        refine_chain = load_summarize_chain(
        llm,
        chain_type="refine",
        question_prompt=question_prompt,
        refine_prompt=refine_prompt,
        return_intermediate_steps=True,
        )
        

        summary = refine_chain({
        'input_documents': chunks,
        'length_config': length_config,
        'language': language
        })

        print("!!!!!Printing summary!!!!")
        print(summary)  
        return {"summary": summary['output_text']}
    except Exception as e:
        print(e)


if __name__=="__main__":
    uvicorn.run(app, host="localhost", port=8000)



