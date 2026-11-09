from dotenv import load_dotenv
load_dotenv()
from langc_course.clients.ollama_client import OllamaCloudClient
from langc_course.vector_db_using_chroma.ollama_embedding_adapter import OllamaEmbeddingAdapter
import numpy as np
client = OllamaCloudClient(
    model="gemma4:31b",
    embedding_model="embeddinggemma-2:latest",
    temperature=0
)


embeddings=OllamaEmbeddingAdapter(client)



def basic_embedding():
    # single text
    text = "What is Machine Learning?"
    embedding = embeddings.embed_query(text)
    print(f"Embedding for '{text}': {embedding[:5]}...")  # Print first 5 dimensions


def batch_embedding():
    texts = [
        "What is Machine Learning?",
        "Explain the concept of Artificial Intelligence.",
        "What are the applications of Deep Learning?"
    ]
    embeddings_list = embeddings.embed_documents(texts)
    for i, emb in enumerate(embeddings_list):
        print(f"Text {i + 1} - Vector Dimension: {len(emb)}")
        print(f"Embedding for '{texts[i]}': {emb[:5]}...")  # Print first 5 dimensions
        #print(f"Vector norm: {np.linalg.norm(emb)}") the output of ollama embedding is aready  normalized, so the norm is 1.0. If you want to check the norm, you can uncomment this line.
def similarity_search_demo():
    docs = [
        "Python is a high-level programming language.",
        "Java is a versatile programming language used for building applications.",
        "JavaScript is primarily used for web development.",
        "Deep learning is a subset of machine learning that uses neural networks.",
        "Machine learning is a field of artificial intelligence that focuses on building systems that can learn from "
        "data and improve their performance over time."
    ]

    query = "What is machine learning?"

    # Generate embeddings
    doc_vectors = embeddings.embed_documents(docs)
    query_vector = embeddings.embed_query(query)

    # Calculate cosine similarity
    def cosine_similarity(vec1, vec2):
        return np.dot(vec1, vec2) / (
            np.linalg.norm(vec1) * np.linalg.norm(vec2)
        )

    # Compare query with every document
    similarities = [
        cosine_similarity(query_vector, doc_vec)
        for doc_vec in doc_vectors
    ]

    # Display results
    for i, score in enumerate(similarities):
        print(f"Document {i + 1}: {docs[i]}")
        print(f"Similarity: {score:.4f}\n")

    # Find the most relevant document
    best_index = np.argmax(similarities) # argmax reutrn the max value in a array np 

    print("Most relevant document:")
    print(f" the Query  :{query}")
    print(docs[best_index])
    print(f"Similarity: {similarities[best_index]:.4f}")




if __name__ == "__main__":
   # basic_embedding()
   # batch_embedding()
    similarity_search_demo()




"""Remember this rule: Same embedding model, 
   same model configuration, and compatible preprocessing for documents and queries.
   If you change the embedding model, 
   re-embed your documents rather than mixing old and new vectors."""