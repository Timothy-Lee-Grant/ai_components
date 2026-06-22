"""
01 · Embeddings 101 — turning text into vectors
-----------------------------------------------
An embedding is a list of numbers representing the MEANING of text. Similar
meanings -> nearby vectors. This is the engine behind semantic search and RAG.

We embed a few sentences and compute cosine similarity to see that related
sentences score higher than unrelated ones.

Requires:  ollama pull nomic-embed-text
Run:       python 01_embeddings_basics.py
"""
import math
from langchain_ollama import OllamaEmbeddings

emb = OllamaEmbeddings(model="nomic-embed-text")

sentences = [
    "How do I water my plants automatically?",   # query
    "The AquaBot waters your plants on a schedule.",  # related
    "The stock market fell three percent today.",     # unrelated
]

vectors = emb.embed_documents(sentences)
print("each embedding has", len(vectors[0]), "dimensions\n")


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb)


query = vectors[0]
for sent, vec in zip(sentences[1:], vectors[1:]):
    print(f"{cosine(query, vec):.3f}  <-  {sent}")
# The related sentence should score noticeably higher than the unrelated one.
