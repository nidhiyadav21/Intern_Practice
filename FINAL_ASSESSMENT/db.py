import os
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_ollama.chat_models import ChatOllama
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()

client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot"]
collection = db["messages"]
BASE_URL = os.getenv("BASE_URL")
llm = ChatOllama(model="mistral-nemo",base_url=BASE_URL)


memory = MongoDBSaver(client,collection="messages")





