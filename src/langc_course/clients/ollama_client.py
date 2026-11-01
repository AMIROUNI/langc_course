
import os
from urllib import response
import requests
import ollama

from typing import Optional


class OllamaCloudClient:

    BASE_URL = "https://ollama.com/v1"

    def __init__(
        self,
        model: str,
        embedding_model: str,
        api_key: Optional[str] = None,
        temperature: float = 0
    ):
        self.api_key = api_key or os.getenv("OLLAMA_API_KEY")

        if not self.api_key:
            raise ValueError("OLLAMA_API_KEY is missing")

        self.model = model
        self.temperature = temperature
        self.embedding_model = embedding_model

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # OpenAI-style interface
        self.chat = self.Chat(self)

    class Chat:

        def __init__(self, client):
            self.completions = client.Completions(client)

    class Completions:

        def __init__(self, client):
            self.client = client

        def create(
            self,
            model: Optional[str] = None,
            messages: Optional[list] = None,
            temperature: Optional[float] = None,
            stream: bool = False
        ):

            if not messages:
                raise ValueError("messages cannot be empty")

            url = f"{self.client.BASE_URL}/chat/completions"

            payload = {
                "model": model or self.client.model,
                "messages": messages,
                "temperature": (
                    temperature
                    if temperature is not None
                    else self.client.temperature
                ),
                "stream": stream
            }

            response = requests.post(
                url,
                headers=self.client.headers,
                json=payload,
                timeout=120
            )

            response.raise_for_status()

            return response.json()

    # Simple convenience method
    def invoke(self, prompt: str) -> str:

        response = self.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response["choices"][0]["message"]["content"]


    # Embedding methods this in 03-embedding/raw_emb.py 


    def embed(self, texts: list[str]) -> list[list[float]]:

        response = ollama.embed(
                model=self.embedding_model,
                input=texts
            )

        return response.embeddings

