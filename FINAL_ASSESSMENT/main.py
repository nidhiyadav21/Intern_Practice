from dotenv import load_dotenv

from FINAL_ASSESSMENT.db import memory
from RAG import get_retriever

from langchain_ollama.chat_models import ChatOllama
from langchain.agents import create_agent
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
llm = ChatOllama(model="mistral-nemo", base_url=BASE_URL)

def retrieve_context(query:str, vector_store=None):
    """Retrieves information to help answer a query"""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        ( f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs

    )
    return serialized, retrieved_docs



def chat():
    print("RAG BASED ChatBot(type 'exit' to exit)")
    while True:
        query = input("You:")
        if query.lower() == "exit":
            break

        config = {"configurable": {"thread_id": "user_session_1"}}

        agent = create_agent(
            llm,
            tools=[get_retriever],
            checkpointer=memory,
            system_prompt="You are a helpful assistant"
        )

        response = agent.invoke(
            {"messages": [{"role": "user", "content": query}]},
            config=config,
        )
        print("AI:", response["messages"][-1].content)


if __name__ == "__main__":
    chat()
