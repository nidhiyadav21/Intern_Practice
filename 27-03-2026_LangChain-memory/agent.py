import os
from dotenv import load_dotenv
from pymongo import MongoClient

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph.checkpoint.mongodb import MongoDBSaver
from tools import get_user_info

load_dotenv()

# 2. Setup Local Ollama LLM (Llama 3.2 1B)
llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0.3
)

# 3. Setup MongoDB Connection
client = MongoClient(os.getenv("MONGO_URI"))
checkpointer = MongoDBSaver(client, db_name="agent_memory")

# 4. Create Agent using Ollama
def get_agent():


    # Note: langgraph's create_react_agent is preferred for checkpointers
    return create_agent(
        llm,
        tools=[get_user_info],
        checkpointer=checkpointer
    )






















