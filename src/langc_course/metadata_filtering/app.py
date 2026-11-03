

import tempfile
from dotenv import load_dotenv
load_dotenv()
from langc_course.metadata_filtering.sample_doc    import SAMPLE_DOCS
from langc_course.clients.ollama_client import OllamaCloudClient
from langc_course.vector_db_using_chroma.ollama_embedding_adapter import OllamaEmbeddingAdapter
from langchain_chroma import Chroma



client = OllamaCloudClient(
    model="gemma4:31b",
    embedding_model="embeddinggemma-2:latest",
    temperature=0
)


embeddings=OllamaEmbeddingAdapter(client)

def metadata_filtering():
    # Create a temporary directory for the Chroma database

        # Create a Chroma vector store with metadata filtering
        vectorstore = Chroma.from_documents(
        documents=SAMPLE_DOCS,
        embedding=embeddings,
        persist_directory="./chroma_db",
        collection_name="my_documents"
    )

        # Perform a similarity search with metadata filtering
        query = "what data is stored are available?"
        results = vectorstore.similarity_search(
            query=query,
            k=3,
            filter={"category": "A"}  # Filter by metadata category A
        )

        print("Filtered Results:")
        for i, doc in enumerate(results):
            print(f"Result {i + 1}:")
            print("Content:", doc.page_content)
            print("Metadata:", doc.metadata)
        # with metadata filtering
        filter_criteria={"topic": "database"}
        filtered_results=vectorstore.similarity_search(
            query=query,
            k=3,
            filter=filter_criteria    # Filter by metadata topic "database" the idea is to set the filter criteria to match the metadata of the documents you want to retrieve. In this case, we are filtering for documents with the topic "database".
        )
        print("Filtered Results (Database Topic):")
        print(f"\n Results with metadata filtering for query '{query}' and filter {filter_criteria}:")
        for i, doc in enumerate(filtered_results):
            print(f"Result {i + 1}:")
            print("Content:", doc.page_content)
            print("Metadata:", doc.metadata)



if __name__ == "__main__":
    metadata_filtering()