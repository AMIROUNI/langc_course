
from langchain_core.embeddings import Embeddings


class OllamaEmbeddingAdapter(Embeddings):

    def __init__(self, ollama_client):
        self.client = ollama_client

    # Used when inserting documents into ChromaDB  LangChain calls named "embed_documents" with this name exactly
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.client.embed(texts)

    # Used when searching for similar documents
    def embed_query(self, text: str) -> list[float]:
        return self.client.embed([text])[0]
