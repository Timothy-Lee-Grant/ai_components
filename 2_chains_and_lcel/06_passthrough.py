"""
06 · RunnablePassthrough — keep the original input around
---------------------------------------------------------
Often a later step needs BOTH a transformed value and the original input.
`RunnablePassthrough.assign(...)` adds new keys to the input dict while keeping
the existing ones. This is the exact pattern RAG uses (module 4): keep the
question, and add retrieved context alongside it.

Run:  python 06_passthrough.py
"""
from operator import itemgetter

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3", temperature=0)
parser = StrOutputParser()

# A small sub-chain that looks up a fact for the given question.
# itemgetter("question") pulls the question string out of the input dict.
fact_lookup = (
    {"q": itemgetter("question")}
    | ChatPromptTemplate.from_template("State one concise fact relevant to: {q}")
    | llm
    | parser
)

# .assign() runs fact_lookup and stores its result under a new "fact" key,
# while the original "question" key is passed through untouched.
chain = (
    RunnablePassthrough.assign(fact=fact_lookup)
    | ChatPromptTemplate.from_template(
        "Question: {question}\nKnown fact: {fact}\n"
        "Answer the question in one sentence using the fact."
    )
    | llm
    | parser
)

print(chain.invoke({"question": "Why is the sky blue?"}))
