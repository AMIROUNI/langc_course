# Failure Mode 1 - Bad Chunking

**Simple idea:** a chunk that is cut in the wrong place loses its meaning, so the
retriever can never find the answer - even when the text is in your database.

Example:

```text
Chunk 1: "The API key expires after 24 hours."
Chunk 2: "You must refresh it using the token endpoint."
```

Ask "How do I handle API key expiration?" and chunk 1 matches the question but
has no solution, while chunk 2 has the solution but no context. A little overlap
between chunks fixes this.

## What is in this folder?

| File | What it does |
| --- | --- |
| `text_splitters.py` | Splits a long machine-learning text with `RecursiveCharacterTextSplitter`, with and without overlap. |

## Run the example

From the repository root:

```powershell
uv run python src/langc_course/the_5_rag_failure_modes/bad_chunking/text_splitters.py
```

The output compares the two settings:

- `chunk_overlap=0` - chunk boundaries can cut sentences apart.
- `chunk_overlap=50` - neighbouring chunks share 50 characters, so context
  survives the cut.

To see the basic splitter demo, uncomment `recursive_splitter()` in
`if __name__ == "__main__":` and comment out `overlap_importance()`.

## Beginner notes

- `chunk_size` is the maximum characters per chunk.
- `chunk_overlap` is how many characters two neighbouring chunks share.
- A good default is `RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)`.
- See [Step 2 - Chunking](../../02-chunking/README.md) for the strategy diagrams.

## Next failure mode

Go to [Failure Mode 2 - Embedding mismatch](../embedding_mismatch/README.md) to
see how a mismatch between document and query vectors breaks retrieval.

Back to [The 5 RAG failure modes](../README.md) or the
[course start](../../../../README.md).
