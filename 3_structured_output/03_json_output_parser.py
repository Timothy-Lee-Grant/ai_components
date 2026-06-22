"""
03 · JsonOutputParser — when you want a dict and explicit prompt control
------------------------------------------------------------------------
with_structured_output is great, but sometimes you want to see and control the
formatting instructions, or you just want a plain dict. JsonOutputParser does
that: it injects format instructions into your prompt and parses the JSON the
model returns (handling ```json fences for you).

Run:  python 03_json_output_parser.py
"""
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_ollama import ChatOllama


class Movie(BaseModel):
    title: str = Field(description="the movie title")
    year: int = Field(description="release year")
    genres: list[str] = Field(description="list of genres")


parser = JsonOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_template(
    "Extract structured info about a movie from the text.\n"
    "{format_instructions}\n\n"
    "Text: {text}"
).partial(format_instructions=parser.get_format_instructions())

llm = ChatOllama(model="llama3", temperature=0)
chain = prompt | llm | parser

# Note: JsonOutputParser returns a plain dict (not a Pydantic object).
result = chain.invoke({"text": "The 1999 sci-fi action film The Matrix."})
print(result)
print("title:", result["title"], "| year:", result["year"])
