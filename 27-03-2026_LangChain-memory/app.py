from agent import get_agent
from memory import save_message

agent = get_agent()


def chat(user_input):

    config = {"configurable": {"thread_id": "user_session_1"}}

    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        config=config,
    )


    ai_output = response["messages"][-1].content


    save_message(user_input, ai_output)

    return ai_output


if __name__ == "__main__":

    print("--- Local Llama 3.2 1B Agent (Ollama) Ready ---")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                break

            answer = chat(user_input)
            print(f"AI: {answer}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")




