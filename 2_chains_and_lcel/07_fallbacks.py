"""
07 · Fallbacks — survive failures gracefully
--------------------------------------------
`.with_fallbacks([...])` gives a runnable one or more backups. If the primary
raises an error, LangChain automatically tries the next one. Use it to fall back
to a different (e.g. smaller, more available) model, or a simpler chain.

Run:  python 07_fallbacks.py
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

prompt = ChatPromptTemplate.from_template("Answer briefly: {q}")
parser = StrOutputParser()

# Primary points at a model that doesn't exist -> every call will fail.
primary = prompt | ChatOllama(model="this-model-does-not-exist") | parser

# Backup uses a model you actually pulled.
backup = prompt | ChatOllama(model="llama3", temperature=0) | parser

robust = primary.with_fallbacks([backup])

# The primary errors, the fallback answers — transparently.
print(robust.invoke({"q": "What is 2 + 2?"}))
