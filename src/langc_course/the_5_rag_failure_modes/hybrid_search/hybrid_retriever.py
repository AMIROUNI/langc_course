
import __main__
from typing import List
from uuid import uuid4

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document

from langc_course.clients.ollama_client import OllamaCloudClient
from langc_course.vector_db_using_chroma.ollama_embedding_adapter import (
    OllamaEmbeddingAdapter
)

load_dotenv()


# Initialize the Ollama client
client = OllamaCloudClient(
    model="gemma4:31b",
    embedding_model="embeddinggemma-2:latest",
    temperature=0
)


class HybridRetriever:
    """Hybrid retriever using BM25 + Vector Search + Weighted RRF."""

    def __init__(
        self,
        documents: List[Document],
        bm25_weight: float = 0.5,
        k: int = 4,
        rrf_k: int = 60
    ):
        if not 0 <= bm25_weight <= 1:
            raise ValueError("bm25_weight must be between 0 and 1")

        self.k = k
        self.rrf_k = rrf_k

        self.bm25_weight = bm25_weight
        self.vector_weight = 1 - bm25_weight

        self.documents = list(documents)

        self.embeddings = OllamaEmbeddingAdapter(client)

        # Create vector store
        self.vectorstore = Chroma(
            collection_name="hybrid_search",
            embedding_function=self.embeddings
        )

        # Add initial documents to Chroma
        if self.documents:
            self.vectorstore.add_documents(
                documents=self.documents,
                ids=[str(uuid4()) for _ in self.documents]
            )

        # Create vector retriever
        self.vector_retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": k}
        )

        # Create BM25 retriever
        self._update_bm25()

    def _update_bm25(self):
        """Rebuild BM25 index using all current documents."""

        if self.documents:
            self.bm25_retriever = BM25Retriever.from_documents(
                documents=self.documents,
                k=self.k
            )
        else:
            self.bm25_retriever = None

    def search(self, query: str) -> List[Document]:
        """Run hybrid search using weighted Reciprocal Rank Fusion."""

        if not self.documents:
            return []

        # Get results from both retrievers
        bm25_results = self.bm25_retriever.invoke(query)
        vector_results = self.vector_retriever.invoke(query)

        retrievers_results = [
            (bm25_results, self.bm25_weight),
            (vector_results, self.vector_weight)
        ]

        # Store combined scores
        doc_scores = {}

        for results, weight in retrievers_results:

            for rank, doc in enumerate(results, start=1):

                # Identify the document
                key = (
                    doc.page_content,
                    tuple(sorted((doc.metadata or {}).items()))
                )

                # Calculate RRF score
                score = weight / (self.rrf_k + rank)

                if key in doc_scores:
                    old_score, old_doc = doc_scores[key]
                    doc_scores[key] = (old_score + score, old_doc)

                else:
                    doc_scores[key] = (score, doc)

        # Sort documents by their combined scores
        sorted_docs = sorted(
            doc_scores.values(),
            key=lambda item: item[0],
            reverse=True
        )

        # Return the top k documents
        return [
            doc for score, doc in sorted_docs[:self.k]
        ]

    def add_documents(self, documents: List[Document]):
        """Add documents to Chroma and update the BM25 index."""

        if not documents:
            return

        # Add documents to the vector database
        self.vectorstore.add_documents(
            documents=documents,
            ids=[str(uuid4()) for _ in documents]
        )

        # Update our document list
        self.documents.extend(documents)

        # Rebuild BM25 with the new documents
        self._update_bm25()

        print(f"Added {len(documents)} documents successfully.")




from langchain_core.documents import Document

documents = [
    # 1. Product information
    Document(
        page_content=(
            "The NetCore X7 router, product SKU-7742X, "
            "supports 10 Gbps ethernet speeds, advanced QoS, "
            "and secure wireless connectivity. It is designed "
            "for medium and large businesses."
        ),
        metadata={
            "type": "product",
            "sku": "SKU-7742X"
        }
    ),

    # 2. Network troubleshooting
    Document(
        page_content=(
            "When users experience slow internet connections, "
            "they should check the ethernet cable, restart the router, "
            "inspect network congestion, and verify DNS settings."
        ),
        metadata={
            "type": "troubleshooting",
            "topic": "network"
        }
    ),

    # 3. Error code
    Document(
        page_content=(
            "Error E_CONN_REFUSED occurs when a client attempts "
            "to connect to a server but the server refuses the connection. "
            "Possible causes include a stopped server, incorrect port, "
            "or firewall restrictions."
        ),
        metadata={
            "type": "error",
            "error_code": "E_CONN_REFUSED"
        }
    ),

    # 4. Technical standard
    Document(
        page_content=(
            "WCAG stands for Web Content Accessibility Guidelines. "
            "It provides recommendations for making websites accessible "
            "to people with visual, auditory, cognitive, and physical disabilities."
        ),
        metadata={
            "type": "standard",
            "acronym": "WCAG"
        }
    ),

    # 5. Employee information
    Document(
        page_content=(
            "John Smith is the IT manager at NetCore Solutions. "
            "He supervises network infrastructure, cybersecurity, "
            "technical support, and IT operations."
        ),
        metadata={
            "type": "employee",
            "name": "John Smith"
        }
    ),

    # 6. Department information
    Document(
        page_content=(
            "The accounting department manages invoices, employee salaries, "
            "financial reports, budgets, and company expenses."
        ),
        metadata={
            "type": "department",
            "name": "Accounting"
        }
    ),

    # 7. Security information
    Document(
        page_content=(
            "Two-factor authentication (2FA) improves account security "
            "by requiring users to provide two different forms of verification, "
            "such as a password and a one-time verification code."
        ),
        metadata={
            "type": "security",
            "topic": "authentication"
        }
    ),

    # 8. Database information
    Document(
        page_content=(
            "PostgreSQL is a relational database management system "
            "used to store structured information. It supports SQL, "
            "transactions, indexing, and complex queries."
        ),
        metadata={
            "type": "database",
            "name": "PostgreSQL"
        }
    ),

    # 9. Related network information
    Document(
        page_content=(
            "DNS translates domain names into IP addresses. "
            "If DNS resolution fails, users may be unable to access "
            "websites even when their internet connection is working."
        ),
        metadata={
            "type": "network",
            "topic": "DNS"
        }
    ),

    # 10. Backup information
    Document(
        page_content=(
            "A database backup is a copy of stored information that "
            "can be restored after accidental deletion, hardware failure, "
            "or data corruption. Companies should test their backups regularly."
        ),
        metadata={
            "type": "database",
            "topic": "backup"
        }
    )
]







test_queries = [
    "SKU-7742X",
    "E_CONN_REFUSED",
    "What does WCAG mean?",
    "Who manages network infrastructure?",
    "My internet is slow. How can I fix it?",
    "How can I protect user accounts?",
    "What database supports SQL and transactions?",
    "Why can't I access websites even though my internet works?",
    "How can a company recover lost database information?"
]


if  __name__ =="__main__" :
    hybrid = HybridRetriever(
    documents=documents,
    bm25_weight=0.7,
    k=4
)

    for query in test_queries:
        print("\n" + "=" * 70)
        print("QUERY:", query)

        results = hybrid.search(query)

        for i, doc in enumerate(results, start=1):
            print(f"\n{i}. {doc.page_content}")
            print("Metadata:", doc.metadata)