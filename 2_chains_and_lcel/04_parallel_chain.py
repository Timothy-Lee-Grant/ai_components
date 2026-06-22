"""
04 · Parallel chains (fan-out, then collect)
--------------------------------------------
RunnableParallel runs several runnables on the SAME input at once and collects
their results into a dict. Useful for getting multiple perspectives in one shot.

Run:  python 04_parallel_chain.py
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3", temperature=0)
parser = StrOutputParser()

def branch(instruction: str):
    return ChatPromptTemplate.from_template(instruction + " Topic: {topic}") | llm | parser

# A plain dict inside a chain is automatically treated as RunnableParallel.
analysis = RunnableParallel(
    pros=branch("List 2 pros, comma-separated."),
    cons=branch("List 2 cons, comma-separated."),
    summary=branch("Summarize in under 12 words."),
)

result = analysis.invoke({"topic": "using a monorepo"})
for key, value in result.items():
    print(f"\n## {key}\n{value}")
