from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel

class TechSummary(BaseModel):
    technology: str
    difficulty: str


llm = ChatOllama(model="llama3")

structured_llm = llm.with_structured_output(
    TechSummary
)

result = structured_llm.invoke(
    "Docker is used for containers"
)

print(result.result)