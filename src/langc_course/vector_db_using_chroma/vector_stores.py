
from langchain_chroma import Chroma

from langc_course.clients.ollama_client import OllamaCloudClient
from langc_course.vector_db_using_chroma.ollama_embedding_adapter import OllamaEmbeddingAdapter
from langc_course.vector_db_using_chroma.sample_doc import SAMPLE_DOCS

from dotenv import load_dotenv

load_dotenv()

client = OllamaCloudClient(
    model="gemma4:31b",
    embedding_model="embeddinggemma-2:latest",
    temperature=0
)


#LangChain expects an embedding object with two methods:
#- embed_documents() – converts documents into vectors.
#- embed_query() – converts a search query into a vector. 
# that"s why we created the OllamaEmbeddingAdapter class to adapt the Ollama client to the LangChain interface.

embeddings = OllamaEmbeddingAdapter(client)





def chroma_basics():
    vectorstore = Chroma.from_documents(
        documents=SAMPLE_DOCS,
        embedding=embeddings,
        persist_directory="./chroma_db",
        collection_name="my_documents"
    )

    print("Documents stored successfully!")


def similarity_search_with_scores():
    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory="./chroma_db",
        collection_name="my_documents"
    )

    query = "Explain vector stores."

    results = vectorstore.similarity_search_with_score(
        query=query,
        k=3
    )

    for i, (doc, score) in enumerate(results):
        print(f"\nResult {i + 1}:")
        print("Content:", doc.page_content)
        print("Metadata:", doc.metadata)
        print("Distance:", score)


if __name__ == "__main__":   # Execute these functions only when this file is executed directly, not when it is imported. 
    chroma_basics()
    similarity_search_with_scores()
