# 04 · Cheatsheet

Copy-paste snippets for the patterns you'll reuse most. All assume:

```python
from langchain_ollama import ChatOllama
llm = ChatOllama(model="llama3", temperature=0)
```

## Call a model

```python
llm.invoke("one-off question").content
```

## System + human messages

```python
from langchain_core.messages import SystemMessage, HumanMessage
llm.invoke([SystemMessage("Be terse."), HumanMessage("Define RAG.")]).content
```

## Prompt template → model → string

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("Explain {topic} in one sentence.")
chain = prompt | llm | StrOutputParser()
chain.invoke({"topic": "embeddings"})
```

## Run many inputs at once

```python
chain.batch([{"topic": "docker"}, {"topic": "kubernetes"}])
```

## Stream tokens

```python
for chunk in chain.stream({"topic": "vector stores"}):
    print(chunk, end="", flush=True)
```

## Structured output (preferred)

```python
from pydantic import BaseModel, Field

class Summary(BaseModel):
    title: str = Field(description="short title")
    score: int = Field(description="1-10")

structured = llm.with_structured_output(Summary)
structured.invoke("Rate and title: Docker simplifies deployment.")
```

## Run things in parallel, collect into a dict

```python
from langchain_core.runnables import RunnableParallel
fan = RunnableParallel(
    pros=ChatPromptTemplate.from_template("Pros of {x}?") | llm | StrOutputParser(),
    cons=ChatPromptTemplate.from_template("Cons of {x}?") | llm | StrOutputParser(),
)
fan.invoke({"x": "monorepos"})   # -> {"pros": ..., "cons": ...}
```

## Carry a value forward (passthrough)

```python
from langchain_core.runnables import RunnablePassthrough
chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm
```

## Wrap a plain function as a step

```python
from langchain_core.runnables import RunnableLambda
shout = RunnableLambda(lambda s: s.upper())
(chain | shout).invoke({"topic": "ai"})
```

## Fallback to a backup model/chain

```python
robust = primary_chain.with_fallbacks([backup_chain])
```

## Minimal RAG

```python
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

emb = OllamaEmbeddings(model="nomic-embed-text")
store = Chroma.from_texts(["fact one", "fact two"], embedding=emb)
retriever = store.as_retriever(search_kwargs={"k": 2})
retriever.invoke("query")
```

## Define a tool

```python
from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

llm_with_tools = llm.bind_tools([add])
llm_with_tools.invoke("what is 2 + 3?").tool_calls
```
