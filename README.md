# langc-course

Hands-on LangChain course: document loaders, chunking strategies, embeddings,
vector stores, metadata filtering, and a small RAG system.

## Start here

New to RAG and LangChain? Follow the folders in this order. Every folder has its
own `README.md` with a simple explanation and the exact command to run.

| Step | Folder | What you learn |
| --- | --- | --- |
| 1 | [01-docment-loader-core](src/langc_course/01-docment-loader-core/README.md) | Load text and PDF files into LangChain documents. |
| 2 | [02-chunking](src/langc_course/02-chunking/README.md) | Cut long documents into small, meaningful chunks. |
| 3 | [03-embedding](src/langc_course/03-embedding/README.md) | Turn text into vectors (lists of numbers). |
| 4 | [vector_db_using_chroma](src/langc_course/vector_db_using_chroma/README.md) | Store vectors in Chroma and search them by meaning. |
| 5 | [metadata_filtering](src/langc_course/metadata_filtering/README.md) | Filter search results using document metadata. |
| 6 | [build_a_basic_rag_system](src/langc_course/build_a_basic_rag_system/README.md) | Put everything together into a RAG pipeline. |

After the main path, read:

- [The 5 RAG failure modes](src/langc_course/the_5_rag_failure_modes/README.md) -
  what goes wrong in RAG and how to recognise it.
- [Clients](src/langc_course/clients/README.md) - the shared Ollama client used by
  the examples (reference, not a lesson step).

The big picture:

```text
file -> load -> chunk -> embed -> store -> retrieve -> LLM answer
        step 1  step 2  step 3  step 4   step 5/6
```

## Installation (Windows)

### 1. Install Astral `uv`

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart the terminal afterwards and check with `uv --version`.

### 2. Initialize the project

```powershell
uv init
```

### 3. Create the virtual environment

```powershell
uv venv
```

### 4. Activate the environment

```powershell
.venv\Scripts\activate
```

### 5. Install the LangChain dependencies

```powershell
uv add langchain langchain-core langgraph langchain-openai langchain-anthropic python-dotenv
```

### 6. Install the Ollama packages

```powershell
uv add ollama langchain-ollama
```

The commands above add the Python packages. To run local models you also need the
Ollama runtime installed from https://ollama.com/download.

### Already cloned this repo?

```powershell
uv sync
```

## Environment variables

Create a `.env` file in the project root with your Ollama Cloud key:

```dotenv
OLLAMA_API_KEY=your_key_here
```

`.env` is gitignored - never commit real keys. See `.env.exemple` for the
expected variable.

## Project structure

```text
src/langc_course/
├── 01-docment-loader-core/    # Step 1: load text and PDF files
│   ├── pdf/                   # Sample PDF used by the examples
│   ├── exemple.md             # Loader notes and cheat sheet
│   ├── exempleTextLoader.py   # TextLoader example
│   └── exemple_pdf_laoder.py  # PyPDFLoader example
├── 02-chunking/               # Step 2: chunking diagrams
├── 03-embedding/              # Step 3: embeddings
├── vector_db_using_chroma/    # Step 4: store and search vectors with Chroma
├── metadata_filtering/        # Step 5: filter search results with metadata
├── build_a_basic_rag_system/  # Step 6: complete RAG pipeline
├── the_5_rag_failure_modes/   # Reference: what goes wrong in RAG
├── clients/                   # Shared Ollama client code
├── check_models.py
└── main.py
```

## Running the examples

Each folder README lists its exact command. A few examples:

```powershell
uv run python src/langc_course/01-docment-loader-core/exempleTextLoader.py
uv run python src/langc_course/03-embedding/raw_emb.py
uv run python src/langc_course/vector_db_using_chroma/vector_stores.py
uv run python src/langc_course/build_a_basic_rag_system/rag_pipeline.py
```

The PDF example uses the relative path `./pdf/Lettre_motivation_.pdf`, so run it
from its own folder:

```powershell
cd src/langc_course/01-docment-loader-core
uv run python exemple_pdf_laoder.py
```

## Notes

- `exemple.md` in `01-docment-loader-core` summarizes the core document loaders
  and when to use each PDF loader.
- The chunking folder contains diagrams only; the runnable splitter demo is in
  `the_5_rag_failure_modes/bad_chunking/text_splitters.py`.
- Generated folders such as `chroma_db/` are not committed.
