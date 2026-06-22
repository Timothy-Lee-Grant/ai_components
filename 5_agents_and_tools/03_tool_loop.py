"""
03 · The full tool-calling loop (a mini agent, by hand)
-------------------------------------------------------
A real agent loops: the model requests tools, we run them, we feed the RESULTS
back, and the model continues until it can answer. Building this loop by hand
(no framework) is the best way to understand what an "agent" actually is.

Loop:
  1. send messages to the model (with tools bound)
  2. if it requested tool calls -> run them, append ToolMessages, go to 1
  3. else -> it's the final answer, stop

Best with:  ollama pull llama3.1   (model="llama3.1")
Run:        python 03_tool_loop.py
"""
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_ollama import ChatOllama


@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


tools = {"add": add, "multiply": multiply}
llm = ChatOllama(model="llama3.1", temperature=0).bind_tools(list(tools.values()))

messages = [HumanMessage("What is 3 plus 4, and then that result multiplied by 5?")]

for step in range(5):  # cap iterations so we never loop forever
    ai = llm.invoke(messages)
    messages.append(ai)

    if not ai.tool_calls:
        print("\nFINAL ANSWER:", ai.content)
        break

    for call in ai.tool_calls:
        chosen = tools[call["name"]]
        result = chosen.invoke(call["args"])
        print(f"  step {step}: {call['name']}({call['args']}) -> {result}")
        # Feed the result back so the model can use it on the next turn.
        messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
else:
    print("\nStopped: hit the iteration cap.")
