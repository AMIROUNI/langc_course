from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langc_course.clients.ollama_client import OllamaCloudClient
from langc_course.vector_db_using_chroma.ollama_embedding_adapter import OllamaEmbeddingAdapter 
"""================================================================================"""
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
# you added those by this command: 
# uv add langchain-classic rank-bm25  

from langchain_chroma import Chroma
load_dotenv()



"==============added a document ======================================================"
from langchain_core.documents import Document

documents = [
    Document(
        page_content=(
            "Product SKU-7742X is our flagship router. "
            "It supports 10 gigabit speeds and advanced QoS features."
        ),
        metadata={"type": "product", "sku": "SKU-7742X"}
    ),

    Document(
        page_content=(
            "For network connectivity issues, first check "
            "the ethernet cable and router status lights."
        ),
        metadata={"type": "troubleshooting"}
    ),

    Document(
        page_content=(
            "Error E_CONN_REFUSED occurs when a connection "
            "attempt is rejected by the destination server. "
            "Check the server status and network configuration."
        ),
        metadata={"type": "error", "error_code": "E_CONN_REFUSED"}
    ),

    Document(
        page_content=(
            "WCAG stands for Web Content Accessibility Guidelines. "
            "These guidelines help make websites accessible to people "
            "with disabilities."
        ),
        metadata={"type": "standards", "acronym": "WCAG"}
    ),

    Document(
        page_content=(
            "John Smith is responsible for the company's accounting "
            "department and financial reporting."
        ),
        metadata={"type": "employee", "person": "John Smith"}
    ),

    Document(
        page_content=(
            "The company's accounting department manages financial "
            "records, budgets, invoices, and financial statements."
        ),
        metadata={"type": "department", "category": "accounting"}
    )
]

"--------------------------------------------------------------------------------------"

client = OllamaCloudClient(
      model="gemma4:31b",
    embedding_model="embeddinggemma-2:latest",
    temperature=0
)



embedding= OllamaEmbeddingAdapter(client)


vector_store=Chroma.from_documents(
        documents=documents,
        embedding=embedding ,
        persist_directory="./chroma_db",
        collection_name='hybrid'
)



# create vctor retriever
voctor_retriever= vector_store.as_retriever(
    search_kwargs={'k':3}  # Return top 3 

)


print('Vector reetriever ready')



# BM25 works on the raw text 

bm25_retriever=BM25Retriever.from_documents(
    documents=documents,
    k=3 
)


print("BM25 retriever")




# Combine with EnsembleRetriever

ensemble_retriever=EnsembleRetriever(
    retrievers=[bm25_retriever,voctor_retriever],
    weights=[0.5,0.5]
)


print('Hybrid retriever ready ')


def test_query(query,name,retriver):
    """Test a query  and show results"""
    result=retriver.invoke(query)
    print(f'\n{name}-Query: {query}')
    for i ,doc in enumerate(result[:3]):
        previw=doc.page_content[:80]+"..."
        print(f'  {i+1} . {previw}')
    return result
test_queries = [
    "SKU-7742X",
    "E_CONN_REFUSED",
    "What does WCAG mean?",
    "Information about John Smith",
    "How can I fix network connectivity problems?"
]


for query in test_queries:
    print('='*60)

    # Vector only 
    vector_results=test_query(query,'VECTOR',voctor_retriever)


    # BM25 only
    bm25_results=test_query(query,'BM25',bm25_retriever)



    # hybrid
    hybrid_results = test_query(query,'HYBRID',ensemble_retriever)





# hybrid retriever  using Reciprocal Rank fusion (RRF)
# This is what EnsmbleRetriever did internally

print(f"===========================================================================================")
print(f"===========================================================================================")
print(f"===========================================================================================")

def hybrid_retrieve(query, retrievers, weights, k=3, rrf_k=60):
    """Combine multiple retrievers using weighted Reciprocal Rank Fusion."""

    doc_scores = {}

    for retriever, weight in zip(retrievers, weights):
        results = retriever.invoke(query)

        for rank, doc in enumerate(results, start=1):
            key = doc.page_content

            rrf_score = weight * (1.0 / (rrf_k + rank))

            if key in doc_scores:
                doc_scores[key] = (
                    doc_scores[key][0] + rrf_score,
                    doc
                )
            else:
                doc_scores[key] = (rrf_score, doc)

    sorted_docs = sorted(
        doc_scores.values(),
        key=lambda x: x[0],
        reverse=True
    )

    return [doc for score, doc in sorted_docs[:k]]



retrievers = [bm25_retriever, voctor_retriever]
weights = [0.5, 0.5]

query = "SKU-7742X"

hybrid_results = hybrid_retrieve(
    query=query,
    retrievers=retrievers,
    weights=weights,
    k=3
)

for i, doc in enumerate(hybrid_results, start=1):
    print(i, doc.page_content)






