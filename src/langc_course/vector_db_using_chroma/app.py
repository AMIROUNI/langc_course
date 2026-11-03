import chromadb
chroma_client = chromadb.Client()

collection_name = "my_collection"
collection = chroma_client.create_collection(name=collection_name)


# Define the documents
documents = [
    {"id": "doc1", "text": "Hello, world!"},
    {"id": "doc2", "text": "how are you?"},
    {"id": "doc3", "text": "Goodbye, see you later!"},]


# Add the documents to the collection


for doc in documents:
    collection.upsert(
        ids=[doc["id"]],
        documents=[doc["text"]],
    )


# define a query  text
query_text = "Hello, world!"


# Query the collection for similar documents
results= collection.query(
    query_texts=[query_text],
    n_results=3)    



print("Query results:"+str(results))