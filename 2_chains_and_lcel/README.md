# Module 2 · Chains & LCEL

**LCEL** (LangChain Expression Language) is the `|` pipe syntax for wiring runnables
together. This module builds it up from a single pipe to parallel branches and
fallbacks. If you only learn one thing in this repo, learn this: *everything composes
with `|`.*

> Prereq: read [`../docs/01_concepts.md`](../docs/01_concepts.md) first — it explains
> runnables and messages, which everything here builds on.

## The examples

Run them in order. Each is self-contained: `python 0N_name.py`.

### `01_pipe_basics.py` — the pipe operator
The core move: `prompt | llm | StrOutputParser()`. The output of each stage feeds the
next. Adding `StrOutputParser()` makes the chain return a clean string instead of an
`AIMessage`. You also get `.batch()` for free. **This is the shape of almost every
chain you'll write.**

### `02_streaming.py` — token streaming
The same chain supports `.stream()`, yielding text as it's generated. This is what
powers "typing" UIs. No code change to the chain — streaming is built into every
runnable.

### `03_sequential_chain.py` — chaining two model calls
Generate a product name, then feed that name into a second chain to write a tagline.
Shows how to adapt one step's output (a string) into the next step's input (a dict)
with a small lambda.

### `04_parallel_chain.py` — fan-out with RunnableParallel
Run several prompts on the *same* input simultaneously and collect them into a dict
(`pros`, `cons`, `summary`). A plain `{}` dict inside a chain becomes a
`RunnableParallel` automatically.

### `05_runnable_lambda.py` — your own Python as a step
Wrap ordinary functions with `RunnableLambda` to pre-process input (normalize text)
and post-process output (add a word count). Chains aren't limited to models and
prompts.

### `06_passthrough.py` — carrying values forward
`RunnablePassthrough.assign(...)` adds computed keys to the input dict while keeping
the originals. This is the precise pattern RAG uses to keep the user's question next
to retrieved context — so understanding it here pays off in module 4.

### `07_fallbacks.py` — graceful failure
`.with_fallbacks([backup])` automatically retries with a backup runnable when the
primary errors. The example points the primary at a non-existent model so you can see
the fallback take over.

### `08_config_and_tags.py` — per-call configuration
`.with_config(run_name=..., tags=...)` labels runs (useful once you add tracing), and
`config={"max_concurrency": N}` throttles `.batch()` so you don't overwhelm a small
local server.

## Mental model recap

```
.invoke(x)   run once
.batch([..]) run many (parallel)
.stream(x)   yield token-by-token

prompt | llm | parser          # sequential
{ "a": chainA, "b": chainB }   # parallel (RunnableParallel)
RunnablePassthrough.assign(k=…) # add a key, keep the rest
chain.with_fallbacks([backup]) # resilience
```

## Try this

1. In `04`, add a fourth branch that returns a one-word sentiment.
2. Turn `03` into a three-step chain: idea → name → tagline → slogan.
3. Make `07` fall back through *two* backups, and observe which one answers.

## Next

Module 3 makes the final parser return **validated, typed data** instead of free text.
