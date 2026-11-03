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
    Document(
        page_content="Metadata filtering allows you to filter search results based on metadata attributes.",
        metadata={"source": "metadata_filtering.txt", "category": "A", "topic": "database"}
    ),
    Document(

        page_content="Metadata filtering is useful for narrowing down search results to specific categories or topics.",
        metadata={"source": "metadata_filtering.txt", "category": "B", "topic": "search"}
    ),
    Document(
        page_content="Metadata filtering can be applied to various types of data, including documents, images, and videos.",
        metadata={"source": "metadata_filtering.txt", "category": "A", "topic": "data"}
    ),
]
