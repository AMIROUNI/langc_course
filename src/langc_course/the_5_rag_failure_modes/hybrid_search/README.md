# Failure Mode 3 - Retrieval Noise and Hybrid Search

**Simple idea:** vector search understands meaning but is weak on exact words
(SKUs, error codes, names). BM25 keyword search is the opposite. Hybrid search
runs both and combines the results, so you get fewer irrelevant chunks.

```text
question -> vector search  --\
                              >-- weighted RRF -> best chunks
question -> BM25 search    --/
```

## Vector search vs BM25

| Search | Good at | Weak at |
| --- | --- | --- |
| Vector | Paraphrases and meaning ("slow internet" ~ "network congestion"). | Exact codes, IDs, rare names. |
| BM25 | Exact words: `SKU-7742X`, `E_CONN_REFUSED`, `WCAG`. | Synonyms and wording changes. |
| Hybrid | Both at once. | Needs tuning of the weights. |

The images in the parent folder explain this visually:

- `2when_vector_seearch_fails.png`
- `3vector_vs_BM25.png`
- `4_hybrid_search_pipeline$.png`
- `5_when_to_use_hybrid_search.png`
- `6_tunig_the_weights.png`

## What is in this folder?

| File | What it does |
| --- | --- |
| `hybrid_retriever.py` | A reusable `HybridRetriever` class: BM25 + Chroma vector search + weighted Reciprocal Rank Fusion (RRF). |
| `prod_hybrid_serach.py` | Compares vector-only, BM25-only, and hybrid results with `EnsembleRetriever`, then shows RRF by hand. |

## Run the examples

From the repository root:

```powershell
uv run python src/langc_course/the_5_rag_failure_modes/hybrid_search/hybrid_retriever.py
uv run python src/langc_course/the_5_rag_failure_modes/hybrid_search/prod_hybrid_serach.py
```

Before running them:

1. Put `OLLAMA_API_KEY=...` in `.env` at the repository root.
2. Start Ollama locally with the embedding model.
3. Keep `rank-bm25` and `langchain-classic` installed (both are in `pyproject.toml`).

## How the weighting works

- `bm25_weight=0.7` means 70% of the score comes from BM25 and 30% from vectors.
- `rrf_k` (default `60`) smooths the rank-based scores.
- Raise the BM25 weight when queries contain exact IDs or codes; raise the vector
  weight when users ask in natural language.

`prod_hybrid_serach.py` saves its vectors in `./chroma_db` under the collection
name `hybrid`. Run it from the repository root so the path matches
[clean_chroma](../../clean_chroma/README.md).

## Beginner notes

- RRF combines **ranks**, not raw scores, so the two retrievers do not need
  comparable score scales.
- Hybrid search does not fix bad chunking or a bad embedding model - fix those
  first.

## Next steps

- [Failure Mode 4 - Context overflow](../../token_budgeting/README.md)
- [Failure Mode 5 - Hallucination](../../build_a_basic_rag_system/README.md)

Back to [The 5 RAG failure modes](../README.md) or the
[course start](../../../../README.md).
