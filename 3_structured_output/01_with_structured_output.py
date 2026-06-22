"""
01 · with_structured_output — the easy, preferred way
-----------------------------------------------------
Define the shape you want as a Pydantic model, then call
llm.with_structured_output(Model). LangChain handles prompting the model to
produce matching data and parsing it back into a typed Python object.

Run:  python 01_with_structured_output.py
"""
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama


class TechSummary(BaseModel):
    """A structured summary of a technology."""
    technology: str = Field(description="the name of the technology")
    one_liner: str = Field(description="a single sentence describing it")
    difficulty: str = Field(description="one of: beginner, intermediate, advanced")


llm = ChatOllama(model="llama3", temperature=0)
structured_llm = llm.with_structured_output(TechSummary)

result = structured_llm.invoke("Summarize Docker for someone new to DevOps.")

# `result` is a real TechSummary object — attribute access, not string parsing.
print(type(result).__name__)
print("technology:", result.technology)
print("one_liner: ", result.one_liner)
print("difficulty:", result.difficulty)
