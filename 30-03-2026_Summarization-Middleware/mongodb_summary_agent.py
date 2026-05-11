import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_mongodb import MongoDBChatMessageHistory
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

# Config
MONGO_URI = os.getenv("MONGO_URL")
MODEL = os.getenv("LLAMA_MODEL")

# LLM
llm = ChatOllama(model=MODEL, temperature=0)

# MongoDB (Long-term permanent memory)
mongo_memory = MongoDBChatMessageHistory(
    connection_string=MONGO_URI,
    session_id="user_simple",
    database_name="middleware_db",
    collection_name="history"
)

# Memory Checkpointer(It is necessary for maintaining short-term context)
checkpointer = MemorySaver()

#Agent with summarization
agent = create_agent(
    model=llm,
    checkpointer=checkpointer,  # Add a Checkpointer
    system_prompt="You are a helpful assistant with memory. Use the provided 'Old info' if it helps answer the user.",
    middleware=[
        SummarizationMiddleware(
            model=llm,
            trigger=("messages", 6),
            keep=("messages", 4)
        )
    ]
)


# Search from MongoDB
def get_old(query):
    # To check old messages from mongodb
    for m in reversed(mongo_memory.messages):
        if query.lower() in m.content.lower():
            return m.content
    return ""

#Chat loop
config = {"configurable": {"thread_id": "thread_1"}}  # Define a Thread ID

print("Chat started! Type 'exit' to stop.")

while True:
    user_input = input("\nUser: ")
    if user_input.lower() == "exit":
        break

    # 1. To retrieve context from mongodb
    old_context = get_old(user_input)
    final_query = user_input
    if old_context:
        final_query += f"\n(Context from long-term memory: {old_context})"

    # 2. Invoke Agent
    result = agent.invoke(
        {"messages": [HumanMessage(content=final_query)]},
        config=config
    )

    reply = result["messages"][-1].content
    print("AI:", reply)

    # 3. It save in mongodb permanently
    mongo_memory.add_user_message(user_input)
    mongo_memory.add_ai_message(reply)

