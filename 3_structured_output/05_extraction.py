"""
05 · Information extraction — a real-world use case
---------------------------------------------------
Structured output shines for pulling data out of messy text. Here we extract a
list of people and their roles from a paragraph into typed objects you could
drop straight into a database.

Run:  python 05_extraction.py
"""
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama


class Person(BaseModel):
    name: str = Field(description="full name")
    role: Optional[str] = Field(default=None, description="their job/title if mentioned")
    organization: Optional[str] = Field(default=None, description="their org if mentioned")


class People(BaseModel):
    people: List[Person] = Field(description="everyone mentioned in the text")


text = (
    "At the summit, CEO Dana Lin of Northwind opened the keynote. "
    "She introduced Raj Patel, the lead engineer, and Maria Gomez from Acme Corp, "
    "who heads product."
)

llm = ChatOllama(model="llama3", temperature=0)
extracted = llm.with_structured_output(People).invoke(
    f"Extract every person mentioned and their role/org:\n\n{text}"
)

for p in extracted.people:
    print(f"- {p.name} | role: {p.role} | org: {p.organization}")
