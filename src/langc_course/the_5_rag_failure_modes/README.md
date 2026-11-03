# The 5 RAG Failure Modes

**Simple idea:** RAG can fail in a small number of common ways. This folder is a
reference gallery for recognising them.

| # | Failure mode | What it means in simple words |
| --- | --- | --- |
| 1 | Bad chunking | A chunk is cut in the middle of a sentence, so its meaning is lost. |
| 2 | Embedding mismatch | The question and the documents are embedded in a way that does not match, so they look unrelated. |
| 3 | Retrieval noise | The search returns irrelevant chunks along with the useful ones. |
| 4 | Context overflow | Too much text is sent to the model and it exceeds the context window. |
| 5 | Hallucination | The model invents facts that are not in the retrieved context. |

See the two images in this folder:

- `the_5_rag_fail.png` - all five failure modes on one page.
- `1Bad_chunking.png` - a clear before/after example of bad chunking.

## The runnable example

`bad_chunking/text_splitters.py` contains a long text about machine learning and
shows how `RecursiveCharacterTextSplitter` cuts it into chunks.

Run it from the repository root:

```powershell
uv run python src/langc_course/the_5_rag_failure_modes/bad_chunking/text_splitters.py
```

The output shows:

- the original text length,
- how many chunks were created,
- the size of each chunk,
- the beginning of the first chunk.

## How to use this folder

When your RAG system gives a bad answer, check the list in order:

1. Is the chunking destroying meaning?
2. Was the question embedded the same way as the documents?
3. Did the retrieval bring back noise?
4. Is the context too large?
5. Did the model hallucinate despite the context?

Back to [Step 6 - Build a basic RAG system](../build_a_basic_rag_system/README.md)
or the [course start](../../../README.md).
