from langchain_core.documents import Document


SAMPLE_DOCS = [
    Document(
        page_content="LangChain is a framework for building applications with language models.",
        metadata={"source": "langchain.txt"}
    ),

    Document(
        page_content="Vector stores save embeddings and allow similarity search.",
        metadata={"source": "vectorstores.txt"}
    ),

    Document(
        page_content="RAG retrieves relevant documents before generating an answer.",
        metadata={"source": "rag.txt"}
    ),

    Document(
        page_content="ChromaDB is a vector database used to store and search embeddings.",
        metadata={"source": "chromadb.txt"}
    ),
]
