import os
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver

#Initialize Ollama Model
llm = ChatOllama(model="llama3.2:1b", temperature=0)


# Simple tool
def delete_file(file_name: str) -> str:
    """Deletes a specified file."""
    return f"File '{file_name}' deleted successfully"

llm_with_tools = llm.bind_tools([delete_file])

#Create agent
agent = create_agent(
    model=llm_with_tools,
    tools=[delete_file],
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "delete_file": {
                    "allowed_decisions": ["approve", "reject"]
                }
            }
        )
    ],
)

#Running the Agent
config = {"configurable": {"thread_id": "session_1"}}
query = {"messages": [HumanMessage(content="Delete the file named 'old_data.txt'")]}


print("--- Agent is processing ---")
agent.invoke(query, config)


state = agent.get_state(config)

if state.next:
    print(f"\n[INTERRUPT]: Agent wants to call tool: {state.next}")


    decision = input("Type 'approve' to proceed or 'reject' to stop: ").strip().lower()

    if decision == "approve":
        print("Resuming execution...")

        final_result = agent.invoke(None, config)
        print("\nFinal Result:", final_result["messages"][-1].content)
    else:
        print("Action rejected. Stopping.")
