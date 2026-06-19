from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3")

prompt = ChatPromptTemplate.from_template(
    """
    You are a professional architect.

    Explain how {topic} works to a curious young adult.
    """
)

chain = prompt | llm

response = chain.invoke({
    "topic": "The Summit building in NYC"
})

print(response.content)