# Step 3 - Embeddings

**Simple idea:** an embedding turns text into a list of numbers (a vector).
Texts with a similar meaning get similar numbers.

Example:

```text
"Python is a programming language."  ->  [0.12, -0.44, 0.98, ...]
"Java is used for backend work."    ->  [0.10, -0.40, 0.91, ...]
```

Those two vectors are close because the sentences talk about similar things.
A vector might contain hundreds or thousands of numbers. The number of values
is called the **dimension** of the embedding.

## Chat model vs embedding model

| Model type | What it does | Example here |
| --- | --- | --- |
| Chat model | Reads a question and writes an answer. | `gemma4:31b` |
| Embedding model | Turns text into vectors. It does not write answers. | `embeddinggemma-2:latest` |

You need both for RAG: embeddings find the right text, and the chat model writes
the final answer.

## What is in this folder?

| File | What it shows |
| --- | --- |
| `raw_emb.py` | Sends a chat message, then embeds two sentences and prints the vector dimension. |
| `embedding-models-vs-chat-models.png` | The difference between the two model types. |
| `1-embedding-dimensions.png` | How embedding dimensions work. |
| `2-three ruls for production rag .png` | Practical rules for production RAG. |

## Run the example

From the repository root:

```powershell
uv run python src/langc_course/03-embedding/raw_emb.py
```

Before running it:

1. Put `OLLAMA_API_KEY=...` in a `.env` file at the repository root.
2. Start Ollama locally so the embedding model can run.

## Next step

Go to [Step 4 - Vector database with Chroma](../vector_db_using_chroma/README.md)
to store these vectors and search them.

Back to the [course start](../../../README.md).
