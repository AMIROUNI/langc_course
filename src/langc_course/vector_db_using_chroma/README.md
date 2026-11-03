# Step 4 - Vector Database with Chroma

**Simple idea:** a vector database stores embeddings and finds the vectors that
are closest to a question.

A normal database searches by exact words or IDs. A vector database searches by
**meaning**. You give it a question, it embeds the question, and it returns the
stored chunks whose vectors are closest.

## Important words

| Word | Meaning |
| --- | --- |
| Chroma | An open-source vector database. |
| Collection | A named group of documents inside Chroma, like a table. |
| Similarity search | Find the stored vectors closest to the query vector. |
| Distance / score | How far the results are. Lower distance usually means "more similar". |

## What is in this folder?

| File | What it does |
| --- | --- |
| `app.py` | The simplest Chroma example: create a collection, add 3 short texts, query it. |
| `sample_doc.py` | Four sample `Document` objects used by the LangChain example. |
| `ollama_embedding_adapter.py` | A small bridge so LangChain can use the Ollama client for embeddings. |
| `vector_stores.py` | Creates a persistent Chroma store and runs a similarity search with distance scores. |
| `00chroma-database.png` | Diagram of a vector database. |

## Why the adapter file exists

LangChain expects an embedding object with two methods:

- `embed_documents(texts)` - used when adding documents.
- `embed_query(text)` - used when searching.

The Ollama client has a different method (`embed`), so
`OllamaEmbeddingAdapter` translates between the two.

## Run the examples

From the repository root:

```powershell
uv run python src/langc_course/vector_db_using_chroma/app.py
uv run python src/langc_course/vector_db_using_chroma/vector_stores.py
```

- `app.py` uses Chroma's default embedding function. The first run may download
  a small model.
- `vector_stores.py` saves the database in a `chroma_db/` folder. That folder is
  generated data and is not committed to Git.

## Next step

Go to [Step 5 - Metadata filtering](../metadata_filtering/README.md) to learn
how to narrow a search before comparing vectors.

Back to the [course start](../../../README.md).
