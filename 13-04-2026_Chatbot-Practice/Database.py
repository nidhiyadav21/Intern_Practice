import os
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_ollama.chat_models import ChatOllama
from langgraph.checkpoint.mongodb import MongoDBSaver
from langchain.agents.middleware.summarization import SummarizationMiddleware

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

client = MongoClient("mongodb://localhost:27017/")
# db = client["chatbot"]
# collection = db["chatbot_history"]


memory = MongoDBSaver(client,db_name="chatbot_checkpoints")

llm = ChatOllama(model="mistral-nemo",base_url=BASE_URL)

summarization_middleware = (SummarizationMiddleware(
                            model =  llm,
                            trigger=("messages",6),
                            keep=("messages",2)
                           ))





