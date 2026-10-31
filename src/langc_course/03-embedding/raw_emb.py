import os
from dotenv import load_dotenv

from langc_course.clients.ollama_client import OllamaCloudClient
load_dotenv()  # Load environment variables from .env file




client   = OllamaCloudClient(
    model="gemma4:31b",
    embedding_model="embeddinggemma",
    temperature=0
)

conversation = client.chat.completions.create(
    model="gemma4:31b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain LangChain in simple terms."}
    ],


)


print(conversation["choices"][0]["message"]["content"])


texts = [
    "Python is a programming language.",
    "Java is used for backend development."
]

vectors = client.embed(texts)
print(vectors)