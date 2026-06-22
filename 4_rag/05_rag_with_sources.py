"""
05 · RAG that cites its sources
-------------------------------
A good RAG app shows WHERE its answer came from so users can verify it. We use
RunnableParallel to return both the generated answer and the retrieved source
documents from a single call.

Prereq: run 03_build_vectorstore.py first.
Run:    python 05_rag_with_sources.py
"""
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma

PERSIST_DIR = str(Path(__file__).resolve().parent / "chroma_db")

emb = OllamaEmbeddings(model="nomic-embed-text")
store = Chroma(persist_directory=PERSIST_DIR, embedding_function=emb)
retriever = store.as_retriever(search_kwargs={"k": 3})

prompt = ChatPromptTemplate.from_template(
    "Use ONLY this context to answer.\n\nContext:\n{context}\n\nQuestion: {question}"
)
llm = ChatOllama(model="llama3", temperature=0)


def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)


# answer_chain produces the text; we run it alongside the raw docs so we keep both.
answer_chain = (
    RunnablePassthrough.assign(context=lambda x: format_docs(x["docs"]))
    | prompt
    | llm
    | StrOutputParser()
)

chain = RunnableParallel(
    docs=retriever,
    question=RunnablePassthrough(),
) | RunnableParallel(
    answer=answer_chain,
    sources=lambda x: sorted({d.metadata.get("source", "?") for d in x["docs"]}),
)

out = chain.invoke("How much does the AquaBot cost and is there a subscription?")
print("ANSWER:\n", out["answer"])
print("\nSOURCES:", out["sources"])
