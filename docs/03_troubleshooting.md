# 03 · Troubleshooting

Common errors across all modules and how to fix them.

## Connection & server

**`ConnectionError` / `httpx.ConnectError` / "Connection refused"**
The Ollama server isn't running. Start it: `ollama serve`. Verify with
`curl http://localhost:11434/api/tags`.

**Requests hang forever**
First call after boot loads the model into RAM and can take 10–30s. If it never
returns, the model may be too big for your memory — try `llama3.2:3b`.

## Models

**`model 'llama3' not found, try pulling it first`**
Run `ollama pull llama3`. List what you have with `ollama list`.

**RAG: `model 'nomic-embed-text' not found`**
Run `ollama pull nomic-embed-text`. Embeddings use a separate model from chat.

**Tool calling does nothing / model ignores tools**
Not all local models support native tool calling. Use `llama3.1` or `qwen2.5`:
`ollama pull llama3.1`, then set `model="llama3.1"`. Module 5 also shows a
prompt-based fallback that works on any model.

## Imports & packages

**`ModuleNotFoundError: No module named 'langchain_ollama'`**
Activate your venv and `pip install -r requirements.txt`.

**`ModuleNotFoundError: langchain_chroma` (module 4)**
`pip install langchain-chroma chromadb`.

**Deprecation warnings about `langchain.xxx` imports**
Modern LangChain split into packages. Import from `langchain_core`,
`langchain_community`, and `langchain_ollama` as the examples do.

## Structured output (module 3)

**`OutputParserException` / "Could not parse output"**
The local model returned text that doesn't match the schema. Fixes, in order:
1. Use `with_structured_output(...)` instead of hand-parsing.
2. Wrap the parser with `OutputFixingParser` or add a retry (see `04_retry_validation.py`).
3. Lower `temperature=0` for more deterministic formatting.
4. Simplify the schema — fewer/flatter fields parse more reliably on small models.

**Model wraps JSON in ```` ```json ```` fences**
The `JsonOutputParser` and `with_structured_output` handle this. If hand-parsing,
strip fences first.

## RAG (module 4)

**Answers ignore my documents**
Check retrieval in isolation: print `retriever.invoke("your question")`. If the
chunks are irrelevant, your splitting or query is off — adjust `chunk_size` or
`k` (number of chunks retrieved).

**Chroma persistence errors / stale data**
Delete the persisted directory (e.g. `rm -rf 4_rag/chroma_db`) and re-run to rebuild
the index from scratch.

## General

**Output is inconsistent between runs**
Set `temperature=0` for reproducible, deterministic-ish output. Default temperature
introduces randomness.

**It's just slow**
Local inference is CPU/GPU-bound. Use a smaller model for iteration, keep the server
warm, and prefer `.batch()` over a Python loop for multiple inputs.
