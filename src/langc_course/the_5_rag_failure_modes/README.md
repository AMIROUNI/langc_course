# The 5 RAG Failure Modes

**Simple idea:** RAG can fail in a small number of common ways. This folder is a
reference gallery for recognising them, with runnable examples where they exist.

| # | Failure mode | What it means in simple words | Example |
| --- | --- | --- | --- |
| 1 | Bad chunking | A chunk is cut in the middle of a sentence, so its meaning is lost. | [bad_chunking](bad_chunking/README.md) |
| 2 | Embedding mismatch | The question and the documents are embedded in a way that does not match, so they look unrelated. | [embedding_mismatch](embedding_mismatch/README.md) |
| 3 | Retrieval noise | The search returns irrelevant chunks along with the useful ones. | [hybrid_search](hybrid_search/README.md) |
| 4 | Context overflow | Too much text is sent to the model and it exceeds the context window. | [token_budgeting](../token_budgeting/README.md) |
| 5 | Hallucination | The model invents facts that are not in the retrieved context. | [build_a_basic_rag_system](../build_a_basic_rag_system/README.md) |

## Images in this folder

| Image | Shows |
| --- | --- |
| `the_5_rag_fail.png` | All five failure modes on one page. |
| `1Bad_chunking.png` | A clear before/after example of bad chunking. |
| `2when_vector_seearch_fails.png` | When vector search misses exact words. |
| `3vector_vs_BM25.png` | Vector search compared with BM25 keyword search. |
| `4_hybrid_search_pipeline$.png` | The hybrid search pipeline. |
| `5_when_to_use_hybrid_search.png` | When hybrid search is worth it. |
| `6_tunig_the_weights.png` | How to tune the BM25 and vector weights. |

## Runnable examples

From the repository root:

```powershell
uv run python src/langc_course/the_5_rag_failure_modes/bad_chunking/text_splitters.py
uv run python src/langc_course/the_5_rag_failure_modes/embedding_mismatch/embeddings_deep.py
uv run python src/langc_course/the_5_rag_failure_modes/hybrid_search/hybrid_retriever.py
```

Each subfolder has its own `README.md` with the details and expected output.

## How to use this folder

When your RAG system gives a bad answer, check the list in order:

1. Is the chunking destroying meaning?
2. Was the question embedded the same way as the documents?
3. Did the retrieval bring back noise?
4. Is the context too large?
5. Did the model hallucinate despite the context?

Back to [Step 6 - Build a basic RAG system](../build_a_basic_rag_system/README.md)
or the [course start](../../../README.md).
