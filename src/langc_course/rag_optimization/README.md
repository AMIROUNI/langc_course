# RAG Optimization

**Simple idea:** once a basic RAG pipeline works, these techniques improve the
quality of what is retrieved - better chunk boundaries, less noise in the
context, and more surrounding context for the model.

| Technique | Problem it solves |
| --- | --- |
| Semantic chunking | Fixed-size cuts break ideas apart; split where the meaning changes instead. |
| Contextual compression | Retrieved chunks contain text the question does not need; keep only the relevant parts. |
| Parent-document retrieval | Small chunks search well but lack context; return the larger parent chunk instead. |

## What is in this folder?

| File | What it shows |
| --- | --- |
| `doc.py` | A sample TechNova IT guide as a LangChain `Document`. Shared by the examples. |
| `semantic_chunking.py` | Compares `RecursiveCharacterTextSplitter` with `SemanticChunker`, stores both versions in Chroma, and runs the same queries against each. |
| `contextual_compression.py` | Uses `ContextualCompressionRetriever` with `LLMChainExtractor` to shrink retrieved documents, then prints the size reduction. |
| `parent_document_retriever.py` | Uses `ParentDocumentRetriever`: search small child chunks, return larger parent chunks. Includes detailed comments. |

## Run the examples

From the repository root:

```powershell
uv run python src/langc_course/rag_optimization/semantic_chunking.py
uv run python src/langc_course/rag_optimization/contextual_compression.py
uv run python src/langc_course/rag_optimization/parent_document_retriever.py
```

Before running them:

1. Put `OLLAMA_API_KEY=...` in `.env` at the repository root.
2. Start Ollama locally with the embedding model.
3. Make sure the extra packages are installed (they are in `pyproject.toml`):
   `langchain-experimental`, `langchain-classic`, `langchain-chroma`, `chromadb`.

For `parent_document_retriever.py`, the embedding model must exist locally:

```powershell
ollama pull embeddinggemma-2:latest
```

## How each technique works

### Semantic chunking

`SemanticChunker` embeds neighbouring sentences and cuts where the distance
between them is large (`breakpoint_threshold_amount=90` means the 90th
percentile). Chunks follow meaning instead of a character count. It costs more
embedding calls than recursive splitting.

### Contextual compression

A normal retriever returns the whole chunk. `LLMChainExtractor` asks the LLM to
keep only the sentences that answer the query. The demo prints original versus
compressed character counts and the reduction percentage. This saves context
tokens but adds LLM latency and cost.

### Parent-document retrieval

```text
source document
   -> parent chunks (stored in a docstore)
        -> child chunks (embedded in Chroma, used for search)
question -> match child chunk -> return its parent chunk
```

The trade-off: larger parents give more context but may include irrelevant text.
A common starting point is child chunks of 200-400 characters and parent chunks
of 600-1,000 characters. `parent_document_retriever.py` uses an `InMemoryStore`,
so the parents disappear when the process stops.

## Beginner notes

- Optimize chunking before adding compression; bad chunks cannot be fixed later.
- Compression and parent retrieval change what is sent to the LLM, not what is
  stored in the vector database.
- Always compare retrieval quality with your own test queries - there is no
  universal best setting.

## Related

- [Step 2 - Chunking](../02-chunking/README.md)
- [Step 4 - Vector database with Chroma](../vector_db_using_chroma/README.md)
- [The 5 RAG failure modes](../the_5_rag_failure_modes/README.md)

Back to the [course start](../../../README.md).
