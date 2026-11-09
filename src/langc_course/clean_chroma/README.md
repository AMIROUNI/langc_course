# Clean Chroma - Remove Duplicate Documents

**Simple idea:** if the same text is added to a Chroma collection more than once,
searches return repeated chunks and waste context. This small utility finds and
deletes those duplicates.

## What is in this folder?

| File | What it does |
| --- | --- |
| `clean_chroma.py` | Connects to a Chroma collection, finds duplicate documents, and deletes them. |

## How duplicates are detected

A document is considered a duplicate when **both** its text and its metadata
match an earlier document:

```python
key = (content, json.dumps(metadata or {}, sort_keys=True))
```

The first copy is kept, later copies are deleted.

## Run the utility

From the repository root:

```powershell
uv run python src/langc_course/clean_chroma/clean_chroma.py
```

The script uses these defaults:

| Setting | Value |
| --- | --- |
| `chroma_path` | `./chroma_db` |
| `collection_name` | `hybrid` |

Run it from the repository root because the path is relative. The `hybrid`
collection is the one created by
[prod_hybrid_serach.py](../the_5_rag_failure_modes/hybrid_search/prod_hybrid_serach.py).

The output shows:

1. documents before cleaning,
2. total / unique / duplicate counts,
3. how many documents were deleted and how many remain.

## Beginner notes

- This deletes data. Back up `chroma_db/` first if the collection matters.
- Deduplication is not the same as updating: if a document changed, you may want
  to delete the old version by ID instead.
- `collection.get(include=["documents", "metadatas"])` loads everything into
  memory, which is fine for small course collections but slow for large ones.

Back to the [course start](../../../README.md).
