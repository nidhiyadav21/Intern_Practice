from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize the Ollama model

llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0,
)

# 2. A very simple tool for the agent to use
@tool()
def print_message(message: str) -> str:
    """Print a message to the console."""
    print(f"\n[Agent Tool Execution]: {message}")
    return "Message printed successfully."

# 3. Create the agent with TodoListMiddleware
# This middleware helps the agent track its progress on the list
agent = create_agent(
    model=llm,
    tools=[print_message],
    system_prompt="You are a helpful assistant. Use your tools to complete tasks.",
    middleware=[TodoListMiddleware()],
)

# 4. Invoke with a multi-step request
response = agent.invoke(
    input={"messages": [{"role": "user",
                         "content": "First, print 'Hello'. Second, print 'Working on it'. Finally, print 'Done'."}]}
)

print("\n--- Final Response ---")
print(response["messages"][-1].content)
