from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# Initialize model
llm = ChatOllama(
    model="llama3.2:latest",  # or mistral, phi, etc.
    temperature=0.7,
    base_url="http://ai:11434",
)

# Chat
response = llm.invoke([
    HumanMessage(content="Explain transformers in simple terms")
])

print(response.content)