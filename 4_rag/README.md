# Module 4 · RAG (Retrieval-Augmented Generation)

A model only knows what it was trained on. **RAG** lets it answer from *your* data:
retrieve the relevant chunks, put them in the prompt as context, then let the model
answer from that context. It's the most common pattern for docs Q&A, support bots, and
"chat with your files."

This module uses two small sample documents in [`../data/`](../data/) — a company
handbook and a product FAQ — so the examples are concrete and verifiable.

> Requires the embedding model: `ollama pull nomic-embed-text`
> Install the vector store: `pip install langchain-chroma chromadb`

## The RAG pipeline, end to end

```
documents ─► split into chunks ─► embed each chunk ─► store in vector DB
                                                              │
question ─► embed ─► similarity search ◄──────────────────────┘
                          │
              top-k chunks ─► prompt (context + question) ─► model ─► grounded answer
```

## Run order

The examples build on each other. **Run `03` before `04`/`05`** — it creates the index
the others read.

### `01_embeddings_basics.py` — what an embedding is
Embeds three sentences and computes cosine similarity. You'll see the related sentence
score higher than the unrelated one. This is the whole basis of retrieval, shown with
no magic.

### `02_text_splitting.py` — chunking
Splits the handbook into overlapping chunks with `RecursiveCharacterTextSplitter`.
Explains why `chunk_size` and `chunk_overlap` matter. Try changing them and watch the
chunk count move.

### `03_build_vectorstore.py` — build the index ⭐ run first
Loads both markdown files, splits them, embeds the chunks, and stores them in Chroma,
persisted to `chroma_db/`. Ends with a pure similarity search (no LLM) so you can see
retrieval working on its own. It also tags each chunk with its `source` filename.

### `04_retrieval_qa.py` — the full RAG chain
The payoff. Wires `retriever → prompt → llm → parser` using the **passthrough pattern
from module 2**. The prompt instructs the model to answer *only* from context and admit
when it doesn't know. Asks three questions spanning both documents.

### `05_rag_with_sources.py` — citing sources
Production RAG must be auditable. Uses `RunnableParallel` to return both the answer and
the list of source files it drew from, so users can verify.

## Knobs that matter

| Knob | Effect | Where |
|------|--------|-------|
| `chunk_size` | bigger = more context per chunk, fewer chunks | `02`, `03` |
| `chunk_overlap` | prevents losing info at chunk boundaries | `02`, `03` |
| `k` (in `search_kwargs`) | how many chunks to retrieve | `04`, `05` |
| prompt wording | controls grounding / "I don't know" behavior | `04` |

## Debugging retrieval

If answers are wrong, **check retrieval in isolation first**:
`store.similarity_search("your question", k=3)`. If the returned chunks are irrelevant,
no model can save the answer — fix chunking or `k` before blaming the prompt. See
[`../docs/03_troubleshooting.md`](../docs/03_troubleshooting.md).

## Try this

1. Add your own `.md` file to `../data/`, re-run `03`, and ask about it.
2. In `04`, lower `k` to 1 and find a question that now fails — see why context matters.
3. Ask `04` something not in the docs and confirm it says "I don't know" instead of guessing.

## Next

Module 5 lets the model *act*: choose and call tools in a loop to accomplish tasks.
