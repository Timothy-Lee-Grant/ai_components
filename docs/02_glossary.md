# 02 · Glossary

Plain-English definitions of every term used in this repo.

**Agent** — A setup where the model decides, step by step, which tools to call to
accomplish a goal, instead of following a fixed script. See module 5.

**Batch** — Running a runnable over many inputs at once (`.batch([...])`), often
parallelized for speed.

**Chain** — Two or more runnables connected so output flows from one to the next.
Built with the `|` operator in LCEL.

**Chat model** — A model that takes a list of role-tagged messages and returns an AI
message. `ChatOllama` is the one used here.

**Chunk / chunking** — Splitting a long document into smaller pieces so each fits in
the model's context and can be embedded/retrieved independently. See module 4.

**Context window** — The maximum amount of text (measured in tokens) a model can read
at once.

**Embedding** — A list of numbers (a vector) representing the meaning of a piece of
text. Similar meanings produce nearby vectors. The basis of semantic search.

**Fallback** — An alternate runnable to use automatically if the primary one fails.
`primary.with_fallbacks([backup])`.

**Few-shot** — Including example input/output pairs in the prompt to show the model the
pattern you want.

**LCEL (LangChain Expression Language)** — The `|` pipe syntax for composing runnables.
Not a separate language — just operator overloading.

**LLM** — Large Language Model. In this repo, accessed via Ollama.

**Message** — A unit of conversation with a role: System, Human, or AI.

**Ollama** — A tool that runs open models locally and exposes them over a local HTTP
API. Everything here talks to it.

**Output parser** — A runnable that converts a model's reply into a usable type: a
string, a dict, or a validated object.

**Prompt template** — A reusable prompt with `{placeholders}` filled at call time.

**Pydantic** — A Python library for declaring data schemas as classes and validating
data against them. Used to define the shape of structured output.

**RAG (Retrieval-Augmented Generation)** — Fetching relevant documents and inserting
them into the prompt so the model can answer from your data. Module 4.

**ReAct** — An agent pattern: the model alternates **Reasoning** ("I should look this
up") and **Acting** (calling a tool) until it can answer.

**Retriever** — A runnable that, given a query, returns the most relevant documents
(usually from a vector store).

**Runnable** — Any object with `.invoke()` / `.batch()` / `.stream()`. The universal
building block; everything composable in LangChain is one.

**RunnableLambda** — A wrapper that turns a plain Python function into a runnable so it
can sit inside a chain.

**RunnableParallel** — A runnable that fans one input out to several runnables at once
and collects their results into a dict. Often written as a plain `{}` dict in a chain.

**RunnablePassthrough** — A runnable that returns its input unchanged; used to carry a
value forward while other branches transform it.

**Streaming** — Receiving the model's output incrementally, token by token, via
`.stream()`.

**Structured output** — Model output forced into a specific schema (e.g. a Pydantic
class) rather than free-form text. Module 3.

**System prompt** — The instruction/persona message that sets the model's behavior for
the whole conversation.

**Token** — The unit models read and generate text in — roughly a word-piece. Context
windows and speed are measured in tokens.

**Tool** — A Python function the model can choose to call (e.g. a calculator, a search,
an API). Defined with the `@tool` decorator. Module 5.

**Tool calling** — The mechanism by which a model requests that a specific tool be run
with specific arguments.

**Vector store** — A database of embeddings that supports "find the most similar"
queries. Chroma is used here.
