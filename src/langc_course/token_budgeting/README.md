# Token Budgeting and Cost Optimization

**Simple idea:** every request to a language model costs tokens (input plus
output). A token budget stops a request before it becomes too large or too
expensive.

This folder is a reference lesson about **failure mode 4 - context overflow**:
sending more text than the model can handle, or more than you are willing to pay
for.

## What is in this folder?

| Class in `cost_optimization.py` | What it does |
| --- | --- |
| `TokenBudget` | Estimates tokens, checks the limit, and records usage statistics. |
| `BudgetedLLM` | Wraps a chat model: checks the budget, calls the model, records usage. |

## How tokens are estimated

`estimate_tokens()` uses a simple approximation:

```python
math.ceil(len(text.split()) * 1.3)
```

That is, roughly 1.3 tokens per word. It is not exact, but it is fast and good
enough to catch oversized requests before paying for them.

## Run the demo

From the repository root:

```powershell
uv run python src/langc_course/token_budgeting/cost_optimization.py
```

Before running it:

1. Put `OLLAMA_API_KEY=...` in `.env` at the repository root.
2. Start Ollama locally with the embedding model.

The demo sets `max_tokens=100` and sends two queries:

1. A short query that fits the budget and gets an answer.
2. A deliberately long query that raises `ValueError` before any API call.

At the end it prints total input tokens, total output tokens, total requests,
and the average per request.

## Beginner notes

- Check the budget **before** calling the model, not after.
- Output tokens count too - cap them when you only need a short answer.
- Real tokenizers are model-specific. The word-based estimate is a guardrail,
  not an invoice.
- The same idea protects you from context-window errors: if the prompt is too
  big, the model cannot answer at all.

## Related

- [Failure Mode 4 in the gallery](../the_5_rag_failure_modes/README.md)
- [The shared Ollama client](../clients/README.md)

Back to the [course start](../../../README.md).
