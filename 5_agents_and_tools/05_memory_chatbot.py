"""
05 · Adding memory — a chatbot that remembers
---------------------------------------------
By default each .invoke() is independent; the model forgets prior turns. To hold
a conversation, you keep a history of messages and replay it each turn.
RunnableWithMessageHistory automates this, keyed by a session id so you can have
multiple separate conversations.

Run:  python 05_memory_chatbot.py
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3", temperature=0.3)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly assistant. Keep replies short."),
    MessagesPlaceholder("history"),   # past turns get injected here
    ("human", "{input}"),
])

chain = prompt | llm | StrOutputParser()

# A tiny in-memory store mapping session_id -> its message history.
_store: dict[str, InMemoryChatMessageHistory] = {}

def get_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in _store:
        _store[session_id] = InMemoryChatMessageHistory()
    return _store[session_id]

chatbot = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="input",
    history_messages_key="history",
)

cfg = {"configurable": {"session_id": "demo-1"}}

# Turn 1 establishes a fact; turn 2 relies on remembering it.
print("U: My name is Sam and I love hiking.")
print("A:", chatbot.invoke({"input": "My name is Sam and I love hiking."}, config=cfg))

print("\nU: What's my name and one hobby you know I enjoy?")
print("A:", chatbot.invoke({"input": "What's my name and one hobby you know I enjoy?"}, config=cfg))
