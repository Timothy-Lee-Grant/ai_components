"""
04 · A real agent with AgentExecutor (the framework does the loop)
------------------------------------------------------------------
Example 03 showed the loop by hand. In practice you let LangChain run it for
you. create_tool_calling_agent + AgentExecutor handle the reason/act/observe
loop, including feeding tool results back, with verbose tracing.

Best with:  ollama pull llama3.1   (model="llama3.1")
Run:        python 04_agent_executor.py
"""
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain.agents import create_tool_calling_agent, AgentExecutor


@tool
def get_word_length(word: str) -> int:
    """Return the number of letters in a single word."""
    return len(word)


@tool
def reverse(text: str) -> str:
    """Reverse a string."""
    return text[::-1]


tools = [get_word_length, reverse]

# Tool-calling agents need this exact slot layout, including agent_scratchpad,
# which is where the framework records the intermediate tool calls.
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use tools when they help."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

llm = ChatOllama(model="llama3.1", temperature=0)
agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = executor.invoke({
    "input": "How many letters are in the word 'elephant', and what is it reversed?"
})
print("\nRESULT:", result["output"])
