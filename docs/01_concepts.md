# 01 · Core concepts (the mental model)

You only need a handful of ideas to understand everything in this repo. Read this
once and the examples will click.

## Messages, not strings

Chat models think in **messages**, each with a role:

- **System** — instructions/persona ("You are a helpful architect.")
- **Human** — what the user says
- **AI** — what the model replies

When you call `llm.invoke("hello")` LangChain quietly wraps your string in a Human
message. When you need control (a system prompt, a conversation), you pass a list of
messages instead.

```python
from langchain_core.messages import SystemMessage, HumanMessage
llm.invoke([
    SystemMessage("You only answer in haiku."),
    HumanMessage("Describe the ocean."),
])
```

## Everything is a Runnable

This is the single most important idea in modern LangChain.

A **Runnable** is any object with an `.invoke()` method (plus `.batch()`, `.stream()`,
and async variants). Models are runnables. Prompt templates are runnables. Output
parsers are runnables. Retrievers are runnables. Even a plain Python function can be
turned into one.

Because they share this interface, you can **connect them with the `|` (pipe)
operator**, exactly like Unix pipes. The output of the left side becomes the input of
the right side:

```python
chain = prompt | llm | parser
chain.invoke({"topic": "docker"})
```

This is called **LCEL** — LangChain Expression Language. It's not a new language; it's
just operator overloading on the `|` symbol. Module 2 is dedicated to it.

## The three verbs every runnable understands

| Verb | What it does | When to use |
|------|--------------|-------------|
| `.invoke(x)` | run once, return the result | normal calls |
| `.batch([x, y])` | run many inputs (parallelized) | bulk processing |
| `.stream(x)` | yield the output token-by-token | live UIs, long answers |

Each also has an `a`-prefixed async twin: `.ainvoke`, `.abatch`, `.astream`.

## Prompt templates

A **prompt template** is a reusable string with `{placeholders}`. It's a runnable that
takes a dict and produces messages:

```python
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_template("Explain {topic} simply.")
prompt.invoke({"topic": "vector databases"})   # -> messages
```

## Output parsers

A model returns an AI message. An **output parser** turns that message into something
useful — a plain string, a Python dict, a validated Pydantic object. It's the last
stage of most chains. Module 3 goes deep here.

```python
from langchain_core.output_parsers import StrOutputParser
chain = prompt | llm | StrOutputParser()   # -> returns a str, not a message
```

## Putting it together: the shape of almost everything

```
input dict ──► prompt template ──► chat model ──► output parser ──► clean result
            (fills placeholders)  (generates)    (extracts/validates)
```

Once you see this pipeline, the four modules are just variations:

- **Module 2 (Chains/LCEL)** — composing these pipelines: in sequence, in parallel, with fallbacks.
- **Module 3 (Structured output)** — making the *parser* return validated, typed data.
- **Module 4 (RAG)** — inserting a *retrieval* step that fetches context before the prompt.
- **Module 5 (Agents)** — letting the *model* decide which tools to call in a loop.

## A note on local models

Local models (llama3 et al.) are smaller than frontier cloud models. They're great for
learning and many production tasks, but:

- They follow formatting instructions less reliably → output parsers with retries matter more (module 3).
- Native tool calling depends on the model → module 5 shows both native and prompt-based approaches.
- They're slower on first load → keep the Ollama server warm.

None of this changes the concepts — only your expectations of polish.
