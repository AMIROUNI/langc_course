# Clients

**Simple idea:** this folder holds shared code that the examples use. It is not a
lesson step, but it is useful to understand what happens behind the scenes.

## What is in this folder?

| File | What it does |
| --- | --- |
| `ollama_client.py` | A custom LangChain chat model that talks to Ollama Cloud and also creates local embeddings. |

## `OllamaCloudClient`

It has two jobs:

1. **Chat:** send messages to the Ollama Cloud API and return the answer.
2. **Embeddings:** call a local Ollama server to turn text into vectors.

It reads the `OLLAMA_API_KEY` environment variable from the `.env` file at the
repository root. Without that key it raises an error.

Simple usage:

```python
from langc_course.clients.ollama_client import OllamaCloudClient

client = OllamaCloudClient(
    model="gemma4:31b",
    embedding_model="embeddinggemma-2:latest",
    temperature=0,
)

answer = client.invoke("Explain LangChain in simple terms.")
vectors = client.embed(["Python is a programming language."])
```

## Why write a custom client?

LangChain can use many model providers. This course uses Ollama Cloud for chat and
a local Ollama server for embeddings. The custom class gives both jobs one simple
interface that works with the rest of the course.

## Where is it used?

- [03-embedding](../03-embedding/README.md)
- [vector_db_using_chroma](../vector_db_using_chroma/README.md)
- [metadata_filtering](../metadata_filtering/README.md)
- [build_a_basic_rag_system](../build_a_basic_rag_system/README.md)

You do not need to run this file directly.

Back to the [course start](../../../README.md).
