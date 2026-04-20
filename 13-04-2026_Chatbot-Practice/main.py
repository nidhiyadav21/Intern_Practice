import os
from dotenv import load_dotenv
from langchain_ollama.chat_models import ChatOllama
from langchain.agents import create_agent
from Rag import get_retriever
from Database import memory,summarization_middleware
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

load_dotenv()
BASE_URL= os.getenv("BASE_URL")

llm = ChatOllama(model="mistral-nemo",base_url=BASE_URL)

retriever = get_retriever.invoke({})
def retrieve_context(query:str):
    """Retrieves information to help answer a query"""
    docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in docs])

def summarization_invoke(state):
    return summarization_middleware.invoke(state)

def chat():
    print("RAG BASED ChatBot(type 'exit' to exit)")
    agent = create_agent(
        model=llm,
        tools=[retrieve_context],
        checkpointer=memory,
        system_prompt="You are a Professional assistant."
                      "Always use the 'retrieve_context' tool to verify facts about PDF chunking"
                      "or project implementation before answering from your own memory."
        )
    while True:
        query = input("You:")
        if query.lower() == "exit":
            break

        config = {"configurable":{"thread_id": "user_session_2"}}

        response = agent.invoke(
            {"messages": [{"role": "user","content": query}]},
            config=config,
        )
        print("AI:",response["messages"][-1].content)

if __name__ == "__main__":
    chat()







