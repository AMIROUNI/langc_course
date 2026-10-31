# Core Document Loaders

| Loader | Use it for |
| --- | --- |
| `PyPDFLoader` | PDF files (`.pdf`) |
| `TextLoader` | Plain text files (`.txt`) |
| `DirectoryLoader` | A directory of files (`.txt`, `.pdf`, `.docx`, `.csv`, `.json`, `.html`) |
| `WebBaseLoader` | Web pages (`.html`) |
| `UnstructuredFileLoader` | Unstructured data (`.txt`, `.pdf`, `.docx`, `.csv`, `.json`, `.html`) |

```python
loader = Loader("path/to/file.pdf")  # Replace with the actual file path
```

## PDF loading options

| # | Loader | Speed | Metadata | Best for |
| --- | --- | --- | --- | --- |
| 1 | `PyPDFLoader` | Good | Basic | Simple PDFs |
| 2 | `PyMuPDFLoader` | Best (faster) | Rich | PDFs where you need solid metadata quickly |
| 3 | `UnstructuredPDFLoader` | Slower | Detailed | Complex layouts, tables, and multi-column documents |

**Rule of thumb:** start with `PyPDFLoader` and switch only if you need more.

## Web loading

Single URL — one `Document` per page:

```
https://example.com  ==>  WebBaseLoader  ==>  Document
```

Multiple URLs — one `Document` per URL:

```
https://example.com/1  \
https://example.com/2  ==>  WebBaseLoader  ==>  Document1, Document2, Document3
https://example.com/3  /
```

```python
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader(["https://example.com/1", "https://example.com/2"])
documents = loader.load()
```

## Directory loading

```
docs/                          DirectoryLoader(
    report.pdf                     path="docs/",
    notes.txt                      glob="**/*.pdf",
    data.csv          ====>        loader_cls=PyPDFLoader
    guide.pdf                  )
    readme.txt
    summary.pdf
```

```python
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

loader = DirectoryLoader(
    "docs/",              # folder to scan
    glob="**/*.pdf",      # which files to load
    loader_cls=PyPDFLoader,  # loader used for each matching file
)
documents = loader.load()
```

How `glob` works:

- `glob="**/*.pdf"` matches every PDF in `docs/` **and** in all subdirectories, recursively.
- `glob="*.pdf"` matches only PDFs directly inside `docs/`, ignoring subfolders.
- Files that do not match the pattern (e.g. `notes.txt` when globbing `**/*.pdf`) are skipped.
- To load several extensions at once, use a generic loader such as `UnstructuredFileLoader`, or run one `DirectoryLoader` per pattern and combine the documents.

Notes:

- `loader_cls` is the loader class applied to each matching file (the original notes said `loader_ci`, which is a typo).
- `UnstructuredDataLoader` does not exist; use `UnstructuredFileLoader` (or `UnstructuredLoader`).
- For large folders, `use_multithreading=True` speeds up loading.
