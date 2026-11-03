# Step 1 - Document Loaders

**Simple idea:** a document loader opens a file and gives its text to your program.

You cannot search a PDF or a text file directly. First you load it into a
LangChain `Document` object. Think of a `Document` as one page with two parts:

- `page_content` - the text itself.
- `metadata` - extra information about the text (for example, the file name).

## What is in this folder?

| File | What it does |
| --- | --- |
| `exempleTextLoader.py` | Loads a small `.txt` file with `TextLoader`. |
| `exemple_pdf_laoder.py` | Loads a PDF with `PyPDFLoader`. |
| `pdf/Lettre_motivation_.pdf` | Sample PDF used by the example. |
| `exemple.md` | Short notes and a cheat sheet for more loaders. |

## Run the examples

Run from the repository root:

```powershell
uv run python src/langc_course/01-docment-loader-core/exempleTextLoader.py
```

The PDF example uses a relative path, so run it from its own folder:

```powershell
cd src/langc_course/01-docment-loader-core
uv run python exemple_pdf_laoder.py
```

## Key beginner notes

- `loader.load()` returns a **list** of documents. A PDF usually gives one
  document per page.
- The text loader example creates a temporary `.txt` file, loads it, and then
  deletes it. You do not need to prepare anything.
- Loading is only the first step. Long documents still need to be cut into
  smaller pieces before embedding.

## Next step

Go to [Step 2 - Chunking](../02-chunking/README.md) to learn how documents are
split into small pieces.

Back to the [course start](../../../README.md).
