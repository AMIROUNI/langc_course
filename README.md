# langc-course

Hands-on LangChain course: document loaders, chunking strategies, embeddings, and model clients.

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

## Requirements

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/)
- Ollama (optional, for local models)

## Setup

```bash
uv sync
```

Create a `.env` file in the project root with the API keys you need:

```dotenv
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

`.env` is gitignored — never commit real keys. See `.env.exemple` for the expected variables.

## Running the examples

```bash
uv run python src/langc_course/01-docment-loader-core/exempleTextLoader.py
```

The PDF example uses the relative path `./pdf/Lettre_motivation_.pdf`, so run it from its own folder:

```bash
cd src/langc_course/01-docment-loader-core
uv run python exemple_pdf_laoder.py
```

## Notes

- `exemple.md` in `01-docment-loader-core` summarizes the core document loaders and when to use each PDF loader.
- The chunking folder contains diagrams only; the embedding folder contains starter code.
