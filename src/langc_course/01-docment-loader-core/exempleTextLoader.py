import os
import tempfile
from pathlib import Path

from langchain_community.document_loaders import (TextLoader)
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


def load_text_file():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
        temp_file.write("Hello, this is a sample text file for testing the TextLoader.".encode('utf-8'))
        temp_file_path = temp_file.name
    try:
        loader = TextLoader(temp_file_path)
        documents = loader.load()
        for doc in documents:
            print(f"Document content:   \n")
            print(f"doc: {doc}\n")
            print(f"Page content: {doc.page_content}")
    finally:
        # clean up the temporary file
        os.remove(temp_file_path)

load_text_file()