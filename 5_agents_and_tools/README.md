# Module 5 · Agents & Tools

So far the model only *talks*. **Tools** let it *act* — call functions to do math, look
things up, hit APIs. An **agent** is a model that decides, step by step, which tools to
call to reach a goal. This module builds that idea from a single tool up to a full
reasoning loop, and adds conversational memory.

> **Model note:** native tool calling depends on the model. Examples `02`–`04` work best
> with `llama3.1` or `qwen2.5` (`ollama pull llama3.1`). Example `06` uses the ReAct
> prompt pattern and works on **any** model, including plain `llama3`.

## The core idea: the model requests, you execute

A model never runs code itself. It returns a *request*: "call `multiply` with
`{a:6, b:7}`." Your code runs the function and feeds the result back. An agent just does
this in a loop until it can answer.

```
model ──requests──► tool call ──you run it──► result ──fed back──► model ──► … ──► answer
```

## The examples (in order)

### `01_define_a_tool.py` — what a tool is
The `@tool` decorator turns a function into a tool. Its name, type hints, and
**docstring** become what the model sees — so the docstring is part of the interface,
not just documentation. Shows the generated schema and that a tool is still callable
normally.

### `02_bind_tools.py` — the request handshake
`llm.bind_tools([...])` makes the model aware of tools. Asking "what is 6 times 7?"
returns a `.tool_calls` request, *not* an answer. The example then executes the
requested call by hand — the fundamental move behind every agent.

### `03_tool_loop.py` — an agent, built by hand ⭐
The whole agent loop with no framework: invoke → run requested tools → append results →
repeat until the model gives a final answer, with an iteration cap. Build this once and
agents stop being magic. Handles a two-step problem (add, then multiply).

### `04_agent_executor.py` — let the framework run the loop
`create_tool_calling_agent` + `AgentExecutor` do exactly what `03` does, but managed,
with `verbose=True` tracing. Note the required prompt layout with `agent_scratchpad`.
This is what you'd actually use day to day.

### `05_memory_chatbot.py` — remembering the conversation
Each call is stateless by default. `RunnableWithMessageHistory` keeps a per-session
message history and replays it via a `MessagesPlaceholder`, so the bot remembers earlier
turns. Keyed by `session_id` so multiple conversations stay separate.

### `06_react_prompt_agent.py` — agents on any model
A compact ReAct agent that needs **no** native tool calling. It prompts the model to
emit `Thought / Action / Action Input`, parses the action out, runs the tool, appends
the `Observation`, and loops. This is how agents worked before tool calling APIs — and
it still runs on plain `llama3`.

## Native tool calling vs. ReAct prompting

| | Native (`02`–`04`) | ReAct prompt (`06`) |
|---|---|---|
| Model support | needs a tool-calling model | any instruct model |
| Reliability | higher (structured) | depends on formatting |
| Transparency | structured `tool_calls` | plain-text steps you parse |
| When to use | model supports it | older/smaller models |

## Safety note

`06` uses `eval` for its calculator inside a stripped-down namespace **for demonstration
only**. Never `eval` untrusted input in real code — use a safe math parser (e.g. the
`ast` module or `numexpr`) and treat tool inputs as untrusted.

## Try this

1. Add a `subtract` tool to `03` and ask a three-step question.
2. Give `05` a third turn that references something from the first — confirm it remembers.
3. Add a `reverse_string` tool to `06`'s `TOOLS` dict and its system prompt.

## You've finished the path

Loop back to the [top-level README](../README.md) for the cheatsheet and glossary, or
remix these patterns: a RAG tool (module 4) handed to an agent (module 5) is a powerful,
very common combination.
