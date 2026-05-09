import fitz
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def extract_text_from_pdf(uploaded_file):
    """
    Extract text from PDF file

    Args:
        uploaded_file: path to PDF file

    Returns:
         str: extracted text from PDF file
    """
    doc = fitz.open(stream=uploaded_file.read(),filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def ask_groq(prompt,model="llama-3.1-8b-instant",temperature=0):
    llm =ChatGroq(temperature=temperature,
                  max_tokens=500,
                  api_key=GROQ_API_KEY,
                  model=model)
    response = llm.invoke(prompt)

    return response.content


