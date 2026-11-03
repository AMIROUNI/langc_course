# Step 5 - Metadata Filtering

**Simple idea:** metadata is extra information about a document, such as its
category, language, date, or source. Metadata filtering tells the search
"only look at documents that match these labels."

## Why is it useful?

A similarity search returns the closest chunks, but "closest" is not always
"correct". For example, a question about databases might return a text about
search engines because the words are similar.

Metadata filtering removes the wrong documents **before** the similarity search:

```text
all documents -> filter by metadata -> similarity search -> best results
```

## What is in this folder?

| File | What it does |
| --- | --- |
| `sample_doc.py` | Seven sample documents. Two of them have `category` and `topic` metadata. |
| `app.py` | Stores the documents in Chroma, then runs two filtered searches. |

The useful metadata looks like this:

```python
{"source": "metadata_filtering.txt", "category": "A", "topic": "database"}
```

## Run the example

From the repository root:

```powershell
uv run python src/langc_course/metadata_filtering/app.py
```

The script runs two searches:

1. `filter={"category": "A"}` - keep only category A documents.
2. `filter={"topic": "database"}` - keep only documents about databases.

## Beginner notes

- Metadata is written **when you create the documents**. You cannot filter on a
  field that was never stored.
- The filter syntax in Chroma looks like a small dictionary, for example
  `{"category": "A"}`.
- Filtering is not a replacement for good embeddings. It is an extra tool that
  makes retrieval more precise.

## Next step

Go to [Step 6 - Build a basic RAG system](../build_a_basic_rag_system/README.md)
to connect loading, chunking, embedding, storing, and answering in one pipeline.

Back to the [course start](../../../README.md).
