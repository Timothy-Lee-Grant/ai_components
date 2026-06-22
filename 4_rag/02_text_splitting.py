"""
02 · Splitting documents into chunks
------------------------------------
Long documents don't fit neatly into a prompt and embed poorly as one blob.
We split them into overlapping chunks so each piece is focused and retrievable.
Overlap keeps sentences from being cut awkwardly between chunks.

Run:  python 02_text_splitting.py
"""
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

doc = Path(__file__).resolve().parent.parent / "data" / "company_handbook.md"
text = doc.read_text()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,      # target characters per chunk
    chunk_overlap=50,    # characters shared between neighbours
)
chunks = splitter.split_text(text)

print(f"split into {len(chunks)} chunks\n")
for i, c in enumerate(chunks[:3]):
    print(f"--- chunk {i} ({len(c)} chars) ---\n{c}\n")
# Try changing chunk_size to 600 and watch the chunk count drop.
