# Step 2 - Chunking

**Simple idea:** chunking means cutting a long document into small pieces
("chunks") that are easy to search.

Why do we do it?

- An embedding model works best on a small, focused piece of text.
- A retriever should return the few sentences that answer the question, not a
  whole 50-page document.
- The language model has a limited context window, so we cannot send everything.

## The two important numbers

| Setting | Meaning | Simple advice |
| --- | --- | --- |
| `chunk_size` | Maximum number of characters in one chunk. | Start around `500`. |
| `chunk_overlap` | How many characters two neighbouring chunks share. | Start around `50` so a sentence cut in half can still be understood. |

Example: with `chunk_size=500` and `chunk_overlap=50`, chunk 2 starts 50
characters before chunk 1 ends.

## Chunking strategies (see the images)

| Image | Strategy | Short explanation |
| --- | --- | --- |
| `fixed-size-chunking.png` | Fixed-size | Cut every N characters. Simple but can break sentences. |
| `recursive-chunking.png` | Recursive | Try paragraph breaks first, then lines, then spaces. Usually the best default. |
| `sementic-chunking.png` | Semantic | Cut when the meaning changes. Better quality, more complex. |
| `1-traditioinal-chunking-vs-late-chunking.png` | Traditional vs late chunking | Compares cutting text before embedding with chunking after embedding. |
| `2-chunking-decision-framework.png` | Decision framework | A guide for choosing a strategy. |

## Important

This folder contains **diagrams only**. The runnable splitter example is in
[the_5_rag_failure_modes/bad_chunking/text_splitters.py](../the_5_rag_failure_modes/bad_chunking/text_splitters.py),
and the final RAG pipeline also uses `RecursiveCharacterTextSplitter`.

A good default for beginners:

```python
RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
```

## Next step

Go to [Step 3 - Embeddings](../03-embedding/README.md) to turn each chunk into
numbers that a computer can compare.

Back to the [course start](../../../README.md).
