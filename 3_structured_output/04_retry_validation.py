"""
04 · Validation + retry — making small local models reliable
------------------------------------------------------------
Local models sometimes emit JSON that doesn't match your schema. Two defenses:

  1) Pydantic validators that enforce real constraints.
  2) OutputFixingParser, which sends malformed output BACK to the model with the
     error and asks it to fix it — automatically.

Run:  python 04_retry_validation.py
"""
from pydantic import BaseModel, Field, field_validator
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.output_parsers import OutputFixingParser
from langchain_ollama import ChatOllama


class Review(BaseModel):
    product: str
    rating: int = Field(description="integer 1-5")
    sentiment: str = Field(description="one of: positive, neutral, negative")

    @field_validator("rating")
    @classmethod
    def rating_in_range(cls, v: int) -> int:
        if not 1 <= v <= 5:
            raise ValueError("rating must be between 1 and 5")
        return v

    @field_validator("sentiment")
    @classmethod
    def known_sentiment(cls, v: str) -> str:
        allowed = {"positive", "neutral", "negative"}
        if v.lower() not in allowed:
            raise ValueError(f"sentiment must be one of {allowed}")
        return v.lower()


llm = ChatOllama(model="llama3", temperature=0)
base_parser = PydanticOutputParser(pydantic_object=Review)

# Wrap the base parser so that if validation fails, the LLM is asked to repair it.
fixing_parser = OutputFixingParser.from_llm(parser=base_parser, llm=llm)

prompt = ChatPromptTemplate.from_template(
    "Extract a product review as structured data.\n{format_instructions}\n\nReview: {text}"
).partial(format_instructions=base_parser.get_format_instructions())

chain = prompt | llm | fixing_parser

review = chain.invoke({
    "text": "The new headphones are amazing — crystal clear sound, worth every penny!"
})
print(review)
print("rating:", review.rating, "| sentiment:", review.sentiment)
