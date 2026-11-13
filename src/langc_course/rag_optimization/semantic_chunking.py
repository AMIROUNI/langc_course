from langchain_chroma import Chroma

from langc_course.clients.ollama_client import OllamaCloudClient
from  langc_course.rag_optimization.doc import  document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from dotenv import load_dotenv

from langc_course.vector_db_using_chroma.ollama_embedding_adapter import OllamaEmbeddingAdapter



load_dotenv()



client=OllamaCloudClient(
    model="gemma4:31b",
    embedding_model="embeddinggemma-2:latest",
    temperature=0
)

embedding=OllamaEmbeddingAdapter(client)



text_splitter= RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=100,
     separators=["\n\n", "\n", " ", ""]
)

chunks = text_splitter.split_documents([document])


for i,chunk in enumerate(chunks):
    content=chunk.page_content
    print(f"n-----  chunk {i+1}({len(content)}  chars)")
    print(content[:100]+"............"if len(content)>100 else content)





print("---------------------SemanticChuker:---------------------------------------")





semantic_chunker=SemanticChunker(
    embeddings=embedding,
    breakpoint_threshold_amount=90, # Split at 90th percientile dissimilarity
    breakpoint_threshold_type="percentile"
)


semantic_chunks=semantic_chunker.split_documents(documents=[document])


print(f"=====================================================")

for i,chunk in enumerate(semantic_chunks):
    content= chunk.page_content

    print(f"\n Chunk {i+1} ({len(content)} chars) -----------------")
    print(content[:100]+'...........'if len(content)>100 else content)







print(f"{'='*60}")
print("The difirence ")
print(f"{'='*60}")

recursive_vectorstore=Chroma.from_documents(
    chunks,
    embedding,
    collection_name='recursive_chunks'
)

sematic_vectorstore=Chroma.from_documents(
    semantic_chunks,
    embedding,
    collection_name='sematic_chunks'

)







test_queries = [
    # General information
    "What is TechNova Solutions?",

    # DNS configuration
    "What does DNS stand for?",

    # Network errors
    "What does the error E_CONN_REFUSED mean?",

    # Network security
    "What security mechanisms protect the company's network?",


    # Backup and disaster recovery
    "How does the company recover data after hardware failure?",


    # Combined questions
    "What should the IT team check when a connection is refused?"
]



def test_retrieval(query,vectorstore,name):
    results= vectorstore.similarity_search(query,k=1)
    print(f"\\n {name} - Query \"{query}\" ")
    print(f"Retrived: {results[0].page_content[:150]}.......")
    return results[0].page_content 


print(f"\n{'='*60}")
print("RETRIEVAL TESTS")
print(f"{'='*60}")


for query in test_queries:
    recursive_result= test_retrieval(query=query,vectorstore=recursive_vectorstore,name='RECURSIVE')
    semantic_result= test_retrieval(query=query,vectorstore=sematic_vectorstore,name='SEMANTIC')