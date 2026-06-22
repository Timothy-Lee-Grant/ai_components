# 00 · Setup

Everything in this repo runs locally against [Ollama](https://ollama.com). No API keys.

## 1. Install Ollama

- **macOS / Windows:** download the installer from https://ollama.com/download
- **Linux:** `curl -fsSL https://ollama.com/install.sh | sh`

After installing, the Ollama server runs in the background. You can verify it's up:

```bash
ollama --version
curl http://localhost:11434/api/tags   # should return JSON, not an error
```

If `curl` fails, start the server manually with `ollama serve`.

## 2. Pull the models

This course uses two models:

```bash
ollama pull llama3            # the chat/instruct model used everywhere
ollama pull nomic-embed-text  # the embedding model used in module 4 (RAG)
```

`llama3` is ~4.7 GB. `nomic-embed-text` is small (~275 MB).

Confirm they're installed:

```bash
ollama list
```

> **Tip:** Any instruct model works (e.g. `llama3.1`, `mistral`, `qwen2.5`). If you
> swap, just change the `model=` argument in the scripts. Tool-calling examples
> (module 5) work best with a model that supports native tool calling, such as
> `llama3.1` or `qwen2.5`.

## 3. Python environment

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 4. Smoke test

```bash
python - << 'PY'
from langchain_ollama import ChatOllama
llm = ChatOllama(model="llama3")
print(llm.invoke("Say 'setup works' and nothing else.").content)
PY
```

If you see a sentence containing "setup works", you're ready. Move on to
[`01_concepts.md`](01_concepts.md) or jump straight into module 2.

## Common setup gotchas

- **`ConnectionError` / `Connection refused`** → the Ollama server isn't running. Run `ollama serve`.
- **`model 'llama3' not found`** → you didn't pull it. Run `ollama pull llama3`.
- **Slow first response** → the model is being loaded into memory. Subsequent calls are faster.
- **Out of memory** → try a smaller model (`ollama pull llama3.2:3b`) and update `model=` in the scripts.
