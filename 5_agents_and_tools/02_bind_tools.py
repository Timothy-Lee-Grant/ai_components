"""
02 · Letting the model REQUEST a tool call
------------------------------------------
llm.bind_tools([...]) tells the model which tools exist. The model doesn't run
them — it returns a structured request (.tool_calls) saying which tool to call
with which arguments. YOU execute it. This example shows that handshake.

Best with a tool-calling model:  ollama pull llama3.1   (then model="llama3.1")
Run:  python 02_bind_tools.py
"""
from langchain_core.tools import tool
from langchain_ollama import ChatOllama


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b


# llama3.1 / qwen2.5 support native tool calling; plain llama3 may not.
llm = ChatOllama(model="llama3.1", temperature=0)
llm_with_tools = llm.bind_tools([multiply])

response = llm_with_tools.invoke("What is 6 times 7?")

print("content:", repr(response.content))
print("tool_calls:", response.tool_calls)

# The model asked us to call a tool; now we actually run it:
if response.tool_calls:
    call = response.tool_calls[0]
    result = multiply.invoke(call["args"])
    print(f"\nexecuted {call['name']}({call['args']}) = {result}")
else:
    print("\nThis model didn't request a tool call. Try model='llama3.1' or 'qwen2.5'.")
