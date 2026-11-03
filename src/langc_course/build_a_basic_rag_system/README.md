# Step 6 - Build a Basic RAG System

**Simple idea:** RAG (Retrieval-Augmented Generation) means:

1. **Retrieve** relevant text from your own documents.
2. **Generate** an answer with a language model, using that text as context.

This folder puts all the previous steps together.

## The pipeline

```text
langchain_knowledge_base.md
        |
        v
   read the file
        |
        v
   split into chunks          (step 2)
        |
        v
   embed each chunk           (step 3)
        |
        v
   store in Chroma            (step 4)
        |
        v
   user question -> retrieve top 2 chunks
        |
        v
   prompt = context + question
        |
        v
   chat model writes the answer
```

## What is in this folder?

| File | What it does |
| --- | --- |
| `langchain_knowledge_base.md` | The small knowledge base about LangChain, vector stores, RAG, and ChromaDB. |
| `rag_pipeline.py` | The complete RAG example. |
| `chroma_db/` | Generated database folder. It is not committed to Git. |

## The important parts of `rag_pipeline.py`

| Line / part | Meaning |
| --- | --- |
| `RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)` | Cut the knowledge base into overlapping chunks. |
| `Chroma.from_documents(...)` | Embed the chunks and store them in Chroma. |
| `collection_name="knowledge_base"` | The name of the Chroma collection. |
| `search_kwargs={"k": 2}` | Retrieve the 2 most similar chunks. |
| `format_docs` | Join the retrieved chunks into one context string. |
| `rag_chain` | Retrieve, build the prompt, call the model, parse the answer. |
| "Answer only from the context" | The instruction that should stop the model from inventing facts. |

## Run the example

From the repository root:

```powershell
uv run python src/langc_course/build_a_basic_rag_system/rag_pipeline.py
```

Before running it:

1. Put `OLLAMA_API_KEY=...` in `.env` at the repository root.
2. Start Ollama locally with the embedding model.

The example question tries to make the model forget the context and answer a
general question. Because the prompt says "answer only from the context", a good
answer is "I don't know". This is a simple test of whether the model follows the
RAG instruction.

## Next step

Read [The 5 RAG Failure Modes](../the_5_rag_failure_modes/README.md) to learn
what can go wrong and how to recognise it.

Back to the [course start](../../../README.md).
