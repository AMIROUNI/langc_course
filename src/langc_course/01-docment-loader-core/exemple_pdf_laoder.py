
import os
import tempfile
from langchain_community.document_loaders import  (PyPDFLoader)
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

def load_pdf_file(pdfPath : str):
    loader = PyPDFLoader(pdfPath)
    documents = loader.load()
    for doc in documents:
        print(f"Document content:   \n")
        print(f"doc: {doc}\n")
        print(f"Page content: {doc.page_content}")



load_pdf_file("./pdf/Lettre_motivation_.pdf")
