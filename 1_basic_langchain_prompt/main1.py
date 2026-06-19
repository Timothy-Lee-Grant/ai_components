from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3")

response = llm.invoke(
    "Explain how AI works."
)

print(response.content)