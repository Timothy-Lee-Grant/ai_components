"""
08 · Configuring chains at call time
------------------------------------
You can tweak a runnable per-call with .with_config(...) — handy for changing
behavior (like model temperature via configurable fields) or attaching tags/
run names for tracing without rebuilding the chain.

This example shows the simplest, always-available form: naming a run and
passing it through. It also demonstrates max_concurrency on batch.

Run:  python 08_config_and_tags.py
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3", temperature=0)
chain = ChatPromptTemplate.from_template("Give a one-word category for: {item}") | llm | StrOutputParser()

# Tag a single run (useful when you later add tracing/observability).
out = chain.with_config(run_name="categorize", tags=["demo"]).invoke({"item": "banana"})
print("single:", out.strip())

# Limit how many run in parallel during a batch (protect a small local server).
items = [{"item": x} for x in ["banana", "hammer", "violin", "python", "comet"]]
results = chain.batch(items, config={"max_concurrency": 2})
for i, r in zip(items, results):
    print(f"{i['item']:>8} -> {r.strip()}")
