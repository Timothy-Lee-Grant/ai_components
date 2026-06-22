# ai_components

A hands-on, runnable course for building AI components with **LangChain** and **local Ollama models**. Every example runs offline against a model on your own machine — no API keys, no cloud bills.

This repo is organized as a numbered learning path. Work through the folders in order, or jump to the topic you need.

## Learning path

| # | Module | What you'll learn |
|---|--------|-------------------|
| 1 | [`1_basic_langchain_prompt/`](1_basic_langchain_prompt/) | Calling a model, prompt templates, first taste of structured output |
| 2 | [`2_chains_and_lcel/`](2_chains_and_lcel/) | LCEL pipe syntax, runnables, sequential & parallel chains, fallbacks |
| 3 | [`3_structured_output/`](3_structured_output/) | Pydantic schemas, output parsers, JSON mode, validation & retries |
| 4 | [`4_rag/`](4_rag/) | Loaders, splitting, embeddings, vector stores, retrieval QA |
| 5 | [`5_agents_and_tools/`](5_agents_and_tools/) | Tool calling, custom tools, ReAct agents, memory & chatbots |

## Documentation

- [`docs/00_setup.md`](docs/00_setup.md) — install Ollama + Python deps, pull models, sanity-check
- [`docs/01_concepts.md`](docs/01_concepts.md) — the mental model: messages, runnables, LCEL, the core abstractions
- [`docs/02_glossary.md`](docs/02_glossary.md) — plain-English definitions of every term used here
- [`docs/03_troubleshooting.md`](docs/03_troubleshooting.md) — common errors and how to fix them
- [`docs/04_cheatsheet.md`](docs/04_cheatsheet.md) — copy-paste snippets for the patterns you'll reuse most

## Quick start

```bash
# 1. Install Ollama (see docs/00_setup.md), then pull the models used here:
ollama pull llama3
ollama pull nomic-embed-text     # for the RAG module

# 2. Create a virtualenv and install Python deps:
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Run any example:
python 2_chains_and_lcel/01_pipe_basics.py
```

## How each module is laid out

Every module folder contains:

- Numbered `NN_*.py` scripts — small, focused, runnable examples. Read them top to bottom.
- A `README.md` walkthrough — the narrative: what each example shows, why it matters, and what to try next.

Start each module by reading its `README.md`, then run the scripts in order.

## Conventions used in the examples

- The model is always `llama3` via `langchain_ollama` unless noted.
- Each script is self-contained and runnable on its own (`python path/to/script.py`).
- Comments explain the *why*, not just the *what*.
- Where a feature depends on model capabilities (e.g. native tool calling), the script says so and falls back gracefully.
