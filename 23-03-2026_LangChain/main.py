import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
# Initialize model
llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # or mistral, phi, etc.
    temperature=0.7,
    api_key = API_KEY
)

# Chat
response = llm.invoke([
    HumanMessage(content="Explain LangChain in Simple terms")
])

print(response.content)
