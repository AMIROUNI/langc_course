# Failure Mode 2 - Embedding Mismatch

**Simple idea:** if documents and questions are not embedded with the **same
model and configuration**, their vectors live in different "number spaces" and
similar meaning no longer looks similar.

A classic mistake:

```text
documents -> embedding model A -> stored vectors
question  -> embedding model B -> query vector   # mismatch
```

The retriever then returns unrelated chunks, and the LLM answers from noise.

## The rule

> Same embedding model, same configuration, and compatible preprocessing for
> documents and queries. If you change the embedding model, re-embed all
> documents instead of mixing old and new vectors.

## What is in this folder?

| Function in `embeddings_deep.py` | What it shows |
| --- | --- |
| `basic_embedding()` | Embeds one sentence and prints the first 5 dimensions. |
| `batch_embedding()` | Embeds several texts and prints each vector dimension. |
| `similarity_search_demo()` | Embeds 5 documents and a question, then ranks them with cosine similarity. |

`similarity_search_demo()` is the one enabled in `if __name__ == "__main__":`.

## Run the example

From the repository root:

```powershell
uv run python src/langc_course/the_5_rag_failure_modes/embedding_mismatch/embeddings_deep.py
```

Before running it:

1. Put `OLLAMA_API_KEY=...` in `.env` at the repository root.
2. Start Ollama locally with the embedding model.

The output prints a similarity score for each document and the best match for
the question "What is machine learning?".

## Beginner notes

- Embeddings from Ollama are already normalized, so the vector norm is `1.0`.
- Cosine similarity compares the direction of two vectors. Higher is closer.
- Mixing vectors from two different models is the fastest way to silently break
  retrieval.

## Next failure mode

Go to [Failure Mode 3 - Retrieval noise and hybrid search](../hybrid_search/README.md)
to see how BM25 and vector search can be combined.

Back to [The 5 RAG failure modes](../README.md) or the
[course start](../../../../README.md).
