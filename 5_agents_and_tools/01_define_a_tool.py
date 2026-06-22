"""
01 · Defining tools
-------------------
A "tool" is just a Python function the model is allowed to call. The @tool
decorator turns a function into one. The function's name, type hints, and
docstring become the description the model uses to decide when to call it — so
write a clear docstring!

Run:  python 01_define_a_tool.py
"""
from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """Add two integers together and return the sum."""
    return a + b


@tool
def word_count(text: str) -> int:
    """Count the number of words in a piece of text."""
    return len(text.split())


# Tools expose the metadata the model sees:
for t in (add, word_count):
    print(f"name: {t.name}")
    print(f"  description: {t.description}")
    print(f"  args schema: {t.args}")
    print()

# You can also just call a tool directly (it's still a normal function):
print("add.invoke({'a': 2, 'b': 3}) =", add.invoke({"a": 2, "b": 3}))
