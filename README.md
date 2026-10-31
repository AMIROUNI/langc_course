# langc-course

Hands-on LangChain course: document loaders, chunking strategies, embeddings, and model clients.

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

The commands above add the Python packages. To run local models you also need the Ollama runtime installed from https://ollama.com/download.

### Already cloned this repo?

```powershell
uv sync
```

## Environment variables

Create a `.env` file in the project root with the API keys you need:

```dotenv
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

`.env` is gitignored — never commit real keys. See `.env.exemple` for the expected variables.

## Project structure

```
src/langc_course/
├── 01-docment-loader-core/   # Document loaders (TextLoader, PyPDFLoader)
│   ├── pdf/                  # Sample PDF used by the examples
│   ├── exemple.md            # Loader notes and cheat sheet
│   ├── exempleTextLoader.py  # TextLoader example
│   └── exemple_pdf_laoder.py # PyPDFLoader example
├── 02-chunking/              # Chunking strategy reference images
├── 03-embedding/             # Embedding examples
├── clients/                  # Ollama and embedding clients
├── check_models.py
└── main.py
```

## Running the examples

```powershell
uv run python src/langc_course/01-docment-loader-core/exempleTextLoader.py
```

The PDF example uses the relative path `./pdf/Lettre_motivation_.pdf`, so run it from its own folder:

```powershell
cd src/langc_course/01-docment-loader-core
uv run python exemple_pdf_laoder.py
```

## Notes

- `exemple.md` in `01-docment-loader-core` summarizes the core document loaders and when to use each PDF loader.
- The chunking folder contains diagrams only; the embedding folder contains starter code.
