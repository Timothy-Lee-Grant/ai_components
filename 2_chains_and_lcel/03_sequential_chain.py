"""
03 · Sequential chains (output of one step feeds the next)
----------------------------------------------------------
Sometimes you need two model calls in a row: generate something, then transform
it. You can pipe one full chain into another.

Here: (1) brainstorm a product name, then (2) write a tagline for that name.
Run:  python 03_sequential_chain.py
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3", temperature=0.7)
parser = StrOutputParser()

# Step 1: idea -> a single product name
name_chain = (
    ChatPromptTemplate.from_template(
        "Invent a single catchy product name for: {idea}. "
        "Reply with ONLY the name, no punctuation."
    )
    | llm
    | parser
)

# Step 2: name -> tagline. We feed step 1's string output in as {name}.
tagline_chain = (
    ChatPromptTemplate.from_template("Write a 6-word tagline for a product called {name}.")
    | llm
    | parser
)

# Compose: the dict adapts step 1's string output into the {name} key step 2 expects.
full_chain = name_chain | (lambda name: {"name": name}) | tagline_chain

idea = "an app that waters your plants automatically"
print("Idea:", idea)
print("Tagline:", full_chain.invoke({"idea": idea}))
