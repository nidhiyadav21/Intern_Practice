import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from tavily import TavilyClient

# ------------------ LOAD ENV ------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")



# ------------------ TAVILY CLIENT ------------------
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)



# ------------------ TOOL ------------------
@tool("SearchEngine", description="Search queries on the web")
def internet_search(query: str):
    response = tavily_client.search(query=query)

    # Extract top results safely
    results = response.get("results", [])
    content = "\n".join([r.get("content", "") for r in results[:3]])

    return content if content else "No results found"



# ------------------ LLM ------------------
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0.3
)

# Bind tool to model
model = llm.bind_tools([internet_search])



# ------------------ CHAT FUNCTION ------------------
def chatbot():
    print("Tool-based Chatbot (type 'exit' to stop)\n")

    chat_history = []

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Bot: Goodbye")
            break

        # Step 1: Ask model
        chat_history.append(HumanMessage(content=user_input))

        # Step 2: Check if tool call needed
        response = model.invoke(user_input)
        chat_history.append(response)

        while response.tool_calls:
            for tool_call in response.tool_calls:

            # Execute tool manually
                 tool_output = internet_search.invoke(tool_call["args"])

            # Send tool result back to model
                 tool_message = ToolMessage(
                    content=str(tool_output),
                    tool_call_id=tool_call["id"]
                 )
                 chat_history.append(tool_message)

            response = model.invoke(chat_history)
            chat_history.append(response)

        print("Bot:",response.content)



if __name__ == "__main__":
    chatbot()























