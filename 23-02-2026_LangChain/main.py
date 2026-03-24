import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage


# Initialize model
llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # or mistral, phi, etc.
    temperature=0.7,
    api_key = "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"
)

# Chat
response = llm.invoke([
    HumanMessage(content="Explain LangChain in Simple terms")
])

print(response.content)
