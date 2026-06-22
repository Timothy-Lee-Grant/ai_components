"""
02 · Streaming tokens
---------------------
Any chain supports .stream(), which yields output incrementally instead of
waiting for the whole response. Great for responsive UIs and long answers.

Run:  python 02_streaming.py
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3", temperature=0.3)

prompt = ChatPromptTemplate.from_template(
    "Write a short paragraph about why {topic} matters."
)
chain = prompt | llm | StrOutputParser()

# Each chunk is a piece of the string. Print as they arrive.
for chunk in chain.stream({"topic": "local language models"}):
    print(chunk, end="", flush=True)
print()  # final newline
