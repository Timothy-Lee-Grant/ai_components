"""
02 · Nested models and lists
----------------------------
Structured output isn't limited to flat fields. You can nest models and use
lists, and the model will populate the whole tree.

Run:  python 02_nested_and_lists.py
"""
from typing import List
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama


class Ingredient(BaseModel):
    name: str = Field(description="ingredient name")
    quantity: str = Field(description="amount, e.g. '2 cups'")


class Recipe(BaseModel):
    title: str
    servings: int
    ingredients: List[Ingredient] = Field(description="list of ingredients")
    steps: List[str] = Field(description="ordered preparation steps")


llm = ChatOllama(model="llama3", temperature=0)
recipe = llm.with_structured_output(Recipe).invoke(
    "Give me a simple recipe for grilled cheese."
)

print(f"{recipe.title} (serves {recipe.servings})")
print("\nIngredients:")
for ing in recipe.ingredients:
    print(f"  - {ing.quantity} {ing.name}")
print("\nSteps:")
for i, step in enumerate(recipe.steps, 1):
    print(f"  {i}. {step}")
