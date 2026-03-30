import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = ChatOllama(model = "llama3.2:1b")

memory = MemorySaver()

agent = create_agent(
     llm,
     tools=[],
     checkpointer=memory,

    middleware=[
        SummarizationMiddleware(
            model=llm,
            trigger=("messages",6),
            keep=("messages",4),
        ),
    ],
)

while True:
    user_input = input("You: ")

    if user_input == "exit":
        break
    response = agent.invoke(
        {
            "messages": [{"role": "user","content": user_input}]
        },
        config={
            "configurable": {
                "thread_id": "user_1"
            }
        },
    )
    print("AI:",response["messages"][-1].content)