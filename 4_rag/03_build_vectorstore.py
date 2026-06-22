"""
03 · Build a vector store (the index)
-------------------------------------
A vector store holds embeddings and supports "find the most similar chunks"
queries. Here we load our docs, split them, embed each chunk, and store them in
Chroma — persisted to disk so we don't rebuild every run.

Run:  python 03_build_vectorstore.py
(Run this BEFORE 04 and 05.)
"""
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
PERSIST_DIR = str(HERE / "chroma_db")

# 1. Load every markdown file in data/ as Documents.
docs = []
for path in sorted(DATA.glob("*.md")):
    loaded = TextLoader(str(path)).load()
    for d in loaded:
        d.metadata["source"] = path.name   # remember where each chunk came from
    docs.extend(loaded)
print(f"loaded {len(docs)} documents")

# 2. Split into chunks.
splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=60)
chunks = splitter.split_documents(docs)
print(f"split into {len(chunks)} chunks")

# 3. Embed + store in Chroma, persisted to disk.
emb = OllamaEmbeddings(model="nomic-embed-text")
store = Chroma.from_documents(chunks, embedding=emb, persist_directory=PERSIST_DIR)
print(f"indexed into {PERSIST_DIR}")

# 4. Quick sanity check: a semantic search (no LLM yet).
hits = store.similarity_search("how many vacation days do I get?", k=2)
print("\nTop match for 'vacation days':")
print(hits[0].page_content[:200], f"\n(source: {hits[0].metadata.get('source')})")
