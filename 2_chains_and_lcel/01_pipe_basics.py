"""
01 · The pipe operator (LCEL) basics
------------------------------------
The `|` operator connects runnables: the output of the left becomes the input
of the right. This is the foundation of everything else.

Pipeline shape:  prompt  ->  model  ->  string parser
Run:  python 01_pipe_basics.py
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3", temperature=0)

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in exactly one sentence."
)

# Without the parser, .invoke() returns an AIMessage (you'd need .content).
# StrOutputParser() makes the chain return a plain string — much nicer.
chain = prompt | llm | StrOutputParser()

result = chain.invoke({"topic": "a vector database"})
print(result)

# The same chain understands batch and stream for free:
print("\n--- batch ---")
for r in chain.batch([{"topic": "Docker"}, {"topic": "Kubernetes"}]):
    print("-", r)
