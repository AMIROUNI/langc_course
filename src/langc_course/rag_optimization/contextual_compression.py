
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor

from langc_course.clients.ollama_client import OllamaCloudClient
from langc_course.vector_db_using_chroma.ollama_embedding_adapter import OllamaEmbeddingAdapter

from dotenv import load_dotenv

load_dotenv()


# ============================================================
# 1. SAMPLE DOCUMENTS
# ============================================================

documents = [
    Document(
        page_content="""
        Company: TechNova Solutions
        Department: IT Infrastructure

        TechNova Solutions uses an enterprise network with routers,
        managed switches, and high-speed Ethernet connections.

        The IT team separates network traffic using VLAN segmentation.
        VLANs help organize devices into logical network groups and
        limit unnecessary communication between groups.

        The company uses DNS to translate domain names into IP addresses.
        When an employee cannot open a website, the IT team checks the
        DNS server configuration, tests name resolution with nslookup,
        checks network connectivity, and verifies that the DNS service
        is available.

        The error E_CONN_REFUSED means that the destination server
        refused the connection. Possible causes include a server that
        is not running, an incorrect port, or a firewall rule.

        The IT team should verify the server status, configured port,
        and firewall rules.

        Network security includes firewalls, VPN access, network
        segmentation, and multi-factor authentication (MFA).

        The company also performs regular backups and tests restoration
        procedures to prepare for data loss or hardware failure.
        """,
        metadata={
            "company": "TechNova Solutions",
            "department": "IT Infrastructure",
            "source": "sample_it_guide",
        },
    )
]


# ============================================================
# 2. SPLIT DOCUMENTS INTO CHUNKS
# ============================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print(f"Total chunks created: {len(chunks)}")


# ============================================================
# 3. INITIALIZE LLM AND EMBEDDING MODEL
# ============================================================

llm = OllamaCloudClient(
    model="gemma4:31b",
    embedding_model="embeddinggemma-2:latest",
    temperature=0
)

embedding = OllamaEmbeddingAdapter(llm)


# ============================================================
# 4. CREATE CHROMA VECTOR DATABASE
# ============================================================

collection_name = "contextual_compression_demo"

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    collection_name=collection_name
)


# ============================================================
# 5. CREATE BASE RETRIEVER
# ============================================================

base_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}
)


# ============================================================
# 6. CREATE DOCUMENT COMPRESSOR
# ============================================================

compressor = LLMChainExtractor.from_llm(llm)


# ============================================================
# 7. CREATE CONTEXTUAL COMPRESSION RETRIEVER
# ============================================================

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)


# ============================================================
# 8. TEST THE RETRIEVERS
# ============================================================

def demo_contextual_compression():

    query = "What does E_CONN_REFUSED mean and how can IT fix it?"

    print("\n" + "=" * 70)
    print("CONTEXTUAL COMPRESSION RETRIEVER")
    print("=" * 70)

    # STEP A: Retrieve original documents
    original_docs = base_retriever.invoke(query)

    print("\n1. ORIGINAL RETRIEVED DOCUMENTS")
    print("-" * 70)

    for i, doc in enumerate(original_docs):
        print(f"\nDocument {i + 1}:")
        print(doc.page_content)

    # STEP B: Apply contextual compression
    compressed_docs = compression_retriever.invoke(query)

    print("\n\n2. COMPRESSED DOCUMENTS")
    print("-" * 70)

    for i, doc in enumerate(compressed_docs):
        print(f"\nDocument {i + 1}:")
        print(doc.page_content)

    # STEP C: Compare results
    original_length = sum(
        len(doc.page_content) for doc in original_docs
    )

    compressed_length = sum(
        len(doc.page_content) for doc in compressed_docs
    )

    print("\n\n3. COMPARISON")
    print("-" * 70)

    print("Original characters:", original_length)
    print("Compressed characters:", compressed_length)

    if original_length > 0:
        reduction = (
            (original_length - compressed_length)
            / original_length
        ) * 100

        print(f"Content reduction: {reduction:.2f}%")


if __name__ == "__main__":
    demo_contextual_compression()
