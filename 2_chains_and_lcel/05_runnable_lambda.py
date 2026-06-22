"""
05 · RunnableLambda — put your own Python in a chain
----------------------------------------------------
Any function can become a chain step. Wrap it in RunnableLambda (or just use a
plain lambda where LCEL can infer it). Great for pre/post-processing.

Run:  python 05_runnable_lambda.py
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3", temperature=0)

# A pre-processing step: normalize the user's input before it hits the prompt.
def clean_input(data: dict) -> dict:
    return {"topic": data["topic"].strip().lower()}

# A post-processing step: add metadata around the model's answer.
def add_word_count(text: str) -> dict:
    return {"answer": text, "word_count": len(text.split())}

chain = (
    RunnableLambda(clean_input)
    | ChatPromptTemplate.from_template("Define {topic} in one line.")
    | llm
    | StrOutputParser()
    | RunnableLambda(add_word_count)
)

print(chain.invoke({"topic": "   Idempotency  "}))
