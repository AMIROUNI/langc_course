"""
PARENT DOCUMENT RETRIEVER — LEARNING EXAMPLE
============================================

Goal
----
Understand how LangChain's ParentDocumentRetriever works and why it is useful.

The problem it solves
---------------------
A normal vector retriever usually:
1. Splits documents into chunks.
2. Embeds each chunk.
3. Searches for the chunks most similar to the user's question.
4. Returns those small chunks.

Small chunks can improve search precision, but they may not contain enough
context to answer a question.

ParentDocumentRetriever uses two levels:

    Original document
          |
          v
    Split into PARENT chunks
          |
          v
    Split every parent into smaller CHILD chunks
          |
          +--> Embed and index CHILD chunks in the vector store
          |
          +--> Keep PARENT documents in a document store

At search time:
1. The question is compared with CHILD chunks.
2. The retriever finds the most relevant child chunks.
3. It looks up the IDs of their PARENT documents.
4. It returns the PARENT documents, which contain more context.

Important:
- Child chunks are used for searching.
- Parent chunks are returned to the LLM.
- The original document is not necessarily returned as one giant block.
- ParentDocumentRetriever does not generate embeddings itself; it uses the
  embedding model configured in the vector store.

Install
-------
Example dependencies:

    uv add langchain-classic langchain-chroma langchain-text-splitters chromadb

Depending on your installed LangChain version, the import paths can differ.
This example uses the commonly used LangChain Classic import.

Example document
----------------
This example uses a small document so you can run it without loading a file.
Replace the sample Document with your own loaded documents when ready.

Run
---
    uv run python parent_document_retriever.py

The example uses Ollama's local embedding endpoint through
OllamaEmbeddings. Make sure Ollama is running and the embedding model exists:

    ollama pull embeddinggemma-2:latest

If you already have your own OllamaEmbeddingAdapter, you can use it instead.
See the alternative section near the bottom.
"""

from langchain_core.documents import Document
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.storage import InMemoryStore


# ---------------------------------------------------------------------------
# 1. Prepare the source documents
# ---------------------------------------------------------------------------

documents = [
    Document(
        page_content=(
            "TechNova Solutions uses an enterprise network with routers, "
            "managed switches, and high-speed Ethernet connections. "
            "The IT team separates network traffic using VLAN segmentation. "
            "VLANs help organize devices into logical network groups and "
            "limit unnecessary communication between groups.\n\n"
            "The company uses DNS to translate domain names into IP addresses. "
            "When an employee cannot open a website, the IT team checks the "
            "DNS server configuration, tests name resolution with nslookup, "
            "checks network connectivity, and verifies that the DNS service "
            "is available.\n\n"
            "The error E_CONN_REFUSED means that the destination server "
            "refused the connection. Possible causes include a server that "
            "is not running, an incorrect port, or a firewall rule. The IT "
            "team should verify the server status, configured port, and "
            "firewall rules.\n\n"
            "Network security includes firewalls, VPN access, network "
            "segmentation, and multi-factor authentication (MFA). The company "
            "also performs regular backups and tests restoration procedures "
            "to prepare for data loss or hardware failure."
        ),
        metadata={
            "company": "TechNova Solutions",
            "department": "IT Infrastructure",
            "source": "sample_it_guide",
        },
    )
]


# ---------------------------------------------------------------------------
# 2. Configure the embedding model
# ---------------------------------------------------------------------------

# This example uses a local Ollama embedding model.
# The same embedding model must be used when indexing documents and searching.
embeddings = OllamaEmbeddings(
    model="embeddinggemma-2:latest",
    base_url="http://localhost:11434",
)


# ---------------------------------------------------------------------------
# 3. Create the CHILD and PARENT splitters
# ---------------------------------------------------------------------------

# CHILD chunks:
# - Small pieces of text.
# - Embedded in Chroma.
# - Used to find the most relevant part of a document.
child_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30,
)

# PARENT chunks:
# - Larger pieces of text.
# - Stored in the document store.
# - Returned after a matching child chunk is found.
parent_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100,
)

# The parent size should normally be larger than the child size.
# For example: child = 200 characters, parent = 700 characters.


# ---------------------------------------------------------------------------
# 4. Create the vector store and parent document store
# ---------------------------------------------------------------------------

# Chroma stores the child chunks and their embeddings.
vectorstore = Chroma(
    collection_name="parent_document_retriever_demo",
    embedding_function=embeddings,
)

# InMemoryStore keeps the parent Documents in memory.
# This is convenient for learning, but its contents disappear when the
# Python process stops. For a persistent application, use a persistent
# document store supported by your LangChain version.
docstore = InMemoryStore()


# ---------------------------------------------------------------------------
# 5. Build the ParentDocumentRetriever
# ---------------------------------------------------------------------------

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=docstore,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
    search_kwargs={"k": 3},
)


# ---------------------------------------------------------------------------
# 6. Index the documents
# ---------------------------------------------------------------------------

# add_documents() performs the important work:
# 1. Splits each source document into parent chunks.
# 2. Splits each parent into child chunks.
# 3. Adds child chunks to Chroma after embedding them.
# 4. Stores parent chunks in the document store.
retriever.add_documents(documents)


# ---------------------------------------------------------------------------
# 7. Search
# ---------------------------------------------------------------------------

question = "How can the IT team troubleshoot a DNS problem?"

# The retriever searches using child chunks, then returns their parent chunks.
retrieved_parents = retriever.invoke(question)


# ---------------------------------------------------------------------------
# 8. Inspect the results
# ---------------------------------------------------------------------------

print("\nQUESTION:")
print(question)

print("\nRETRIEVED PARENT DOCUMENTS:")
for index, parent_doc in enumerate(retrieved_parents, start=1):
    print(f"\n--- Parent result {index} ---")
    print("Metadata:", parent_doc.metadata)
    print("Content:")
    print(parent_doc.page_content)


# ---------------------------------------------------------------------------
# 9. Compare the two chunk levels
# ---------------------------------------------------------------------------

# This section is for understanding the design.
# It displays child chunks currently stored in Chroma.
# Chroma's collection access below is useful for this demo, but direct
# collection access is a lower-level API and can vary by Chroma version.

print("\nCHILD CHUNKS STORED IN CHROMA:")
try:
    child_records = vectorstore.get(include=["documents", "metadatas"])
    for index, child_text in enumerate(child_records.get("documents", []), start=1):
        print(f"\n--- Child chunk {index} ---")
        print(child_text)
except Exception as error:
    print("Could not inspect child chunks through vectorstore.get():", error)


# ---------------------------------------------------------------------------
# 10. How to use your own embedding adapter
# ---------------------------------------------------------------------------

# If you already created OllamaEmbeddingAdapter in your project, import it
# and replace the OllamaEmbeddings configuration above:
#
#     from your_module import OllamaEmbeddingAdapter
#     embeddings = OllamaEmbeddingAdapter(your_ollama_client)
#
# Keep the same embedding model for both indexing and querying.


# ---------------------------------------------------------------------------
# 11. Key ideas to remember
# ---------------------------------------------------------------------------

# Standard vector retriever:
#     Search child-sized chunks -> return those same small chunks.
#
# ParentDocumentRetriever:
#     Search child-sized chunks -> find their parent IDs -> return larger
#     parent chunks.
#
# Why use it?
#     It balances precise retrieval (small child chunks) with useful context
#     (larger parent chunks).
#
# When is it useful?
#     - Long technical documentation
#     - Manuals and guides
#     - Policies and procedures
#     - Documents where a small matching passage needs surrounding context
#
# Trade-off:
#     Larger parent chunks provide more context, but may include more
#     irrelevant text and use more LLM context tokens.
#
# Practical tuning:
#     Start with child chunks around 200–400 characters and parent chunks
#     around 600–1,000 characters, then evaluate using your own test queries.
#     These are starting points, not universal best settings.
