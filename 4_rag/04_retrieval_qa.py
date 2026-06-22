"""
04 · Retrieval-Augmented Generation (the full RAG chain)
--------------------------------------------------------
RAG = retrieve relevant chunks, stuff them into the prompt as context, then let
the model answer FROM that context. This grounds answers in your data and cuts
hallucination.

The chain shape (note the passthrough pattern from module 2!):
    { context: retriever, question: passthrough } -> prompt -> llm -> str

Prereq: run 03_build_vectorstore.py first.
Run:    python 04_retrieval_qa.py
"""
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma

PERSIST_DIR = str(Path(__file__).resolve().parent / "chroma_db")

emb = OllamaEmbeddings(model="nomic-embed-text")
store = Chroma(persist_directory=PERSIST_DIR, embedding_function=emb)
retriever = store.as_retriever(search_kwargs={"k": 3})


def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)


prompt = ChatPromptTemplate.from_template(
    "Answer the question using ONLY the context below. "
    "If the answer isn't in the context, say you don't know.\n\n"
    "Context:\n{context}\n\nQuestion: {question}\nAnswer:"
)

llm = ChatOllama(model="llama3", temperature=0)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

for q in [
    "How many vacation days do full-time employees get?",
    "What is the AquaBot 3000's water tank capacity?",
    "How many approvals are needed to change the billing service?",
]:
    print(f"Q: {q}\nA: {rag_chain.invoke(q)}\n")
