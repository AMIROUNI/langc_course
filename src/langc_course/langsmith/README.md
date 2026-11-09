# LangSmith - Tracing and Observability

**Simple idea:** LangSmith records what happens inside your chains - prompts,
model calls, outputs, timing, metadata - so you can see **why** an answer was
good or bad instead of guessing.

```text
your chain -> trace -> LangSmith dashboard
              (every step, input, output, tags, metadata)
```

## Why observability matters

- Debugging: see the exact prompt that was sent and the raw model output.
- Evaluation: compare runs and spot regressions.
- Production monitoring: filter by tags or metadata (user, request type).
- Cost and latency: find slow or expensive steps.

## What is in this folder?

| File | What it shows |
| --- | --- |
| `langsmith_setup.py` | Three tracing demos: basic tracing, named runs with tags, and traces with metadata. |
| `langsmith_setup.png` | Where to create a LangSmith API key. |
| `why_observability_matters.png` | Why tracing matters in production. |
| `lang_smith.png` | Overview of the LangSmith UI. |

## What the script does

| Function | Demonstrates |
| --- | --- |
| `demo_basic_tracing()` | `@traceable` on a simple prompt chain. |
| `demo_name_runs()` | `@traceable(name=..., tags=[...])` to label runs. |
| `demo_traca_with_metadata()` | Function arguments (`user_id`, `request_type`) captured as trace metadata. |

The script also sets `LANGSMITH_TRACING=true` before running anything.

## Environment variables

Add these to `.env` at the repository root:

```dotenv
LANGSMITH_API_KEY=your_key_here
LANGSMITH_PROJECT=langc-course
LANGSMITH_TRACING=true
```

Get the key from https://smith.langchain.com (see `langsmith_setup.png`). Never
commit a real key - `.env` is gitignored.

## Run the demo

From the repository root:

```powershell
uv run python src/langc_course/langsmith/langsmith_setup.py
```

Before running it:

1. Put `OLLAMA_API_KEY=...` and the LangSmith variables in `.env`.
2. Start Ollama locally with the embedding model.

After the run, open the LangSmith dashboard and inspect the three traces. If you
do not see them, check `LANGSMITH_TRACING` and the API key.

## Beginner notes

- `@traceable` works on any function, not only LangChain chains.
- Tags and metadata are the easiest way to find a trace later.
- Tracing is optional: the rest of the course works without LangSmith.

Back to the [course start](../../../README.md).
