"""
06 · ReAct agent without native tool calling (works on ANY model)
-----------------------------------------------------------------
Not every local model supports native tool calling. The ReAct pattern gets
around that: you PROMPT the model to alternate "Thought / Action / Action Input
/ Observation" in plain text, and parse those actions out. This is how agents
worked before native tool calling existed — and it still works on plain llama3.

This is a compact, transparent implementation so you can see the mechanism.
Run:  python 06_react_prompt_agent.py
"""
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# --- our "tools": plain functions ---
def calculator(expr: str) -> str:
    try:
        return str(eval(expr, {"__builtins__": {}}, {}))  # tiny sandbox; demo only
    except Exception as e:
        return f"error: {e}"

def string_length(s: str) -> str:
    return str(len(s.strip()))

TOOLS = {"calculator": calculator, "string_length": string_length}

SYSTEM = """You are a reasoning agent. You can use these tools:
- calculator: evaluates a math expression, e.g. "3 * (4 + 1)"
- string_length: returns the length of a string

Respond using EXACTLY this format, one step at a time:
Thought: <your reasoning>
Action: <tool name, one of: calculator, string_length>
Action Input: <the input to the tool>

When you have the final answer, respond with:
Thought: <reasoning>
Final Answer: <the answer>
"""

llm = ChatOllama(model="llama3", temperature=0)
prompt = ChatPromptTemplate.from_messages([("system", SYSTEM), ("human", "{scratchpad}")])

def run(question: str, max_steps: int = 5) -> str:
    scratchpad = f"Question: {question}\n"
    for _ in range(max_steps):
        text = (prompt | llm).invoke({"scratchpad": scratchpad}).content

        if "Final Answer:" in text:
            return text.split("Final Answer:", 1)[1].strip()

        action = re.search(r"Action:\s*(.+)", text)
        action_input = re.search(r"Action Input:\s*(.+)", text)
        if not (action and action_input):
            return "(could not parse an action) " + text.strip()

        tool_name = action.group(1).strip()
        tool_arg = action_input.group(1).strip().strip('"')
        observation = TOOLS.get(tool_name, lambda x: "unknown tool")(tool_arg)

        # Append our step + the observation, then loop so the model continues.
        scratchpad += f"{text.strip()}\nObservation: {observation}\n"
    return "(stopped: hit step cap)"

print(run("What is 12 * 9, and how many characters are in the word 'banana'?"))
