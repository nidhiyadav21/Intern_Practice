import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyMuPDFLoader
from prompt import load_prompt

load_dotenv()
#API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0.3
)

#PDF
def extract_pdf(file_path):
    loader = PyMuPDFLoader(file_path)
    docs = loader.load()
    return "\n".join([doc.page_content for doc in docs])


#PROMPTS
req_prompt = PromptTemplate.from_template(load_prompt("requirement"))
us_prompt = PromptTemplate.from_template(load_prompt("user_story"))
task_prompt = PromptTemplate.from_template(load_prompt("generate_task"))

requirement_chain = req_prompt | llm
user_stories_chain = us_prompt | llm
tasks_chain = task_prompt | llm


#TOOLS
@tool
def generate_requirements(text: str):
    """Generates a list of requirements from the provided text."""
    return requirement_chain.invoke({"text": text}).content


@tool
def generate_user_stories(requirements: str):
    """Converts business requirements into structured user stories."""
    return user_stories_chain.invoke({"requirements": requirements}).content


@tool
def generate_task(user_stories: str,max_chars: int = 1500):
    """Breaks down user stories into specific actionable tasks."""
    return tasks_chain.invoke({"user_stories": user_stories, "max_chars": max_chars}).content


tools = [generate_requirements, generate_user_stories, generate_task]

#AGENT
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=load_prompt("agent_prompt")
)


if __name__ == "__main__":
    pdf_path = "SRS-BECS-2007.pdf"

    print("Extracting PDF...")
    text = extract_pdf(pdf_path)[:8000]

    print("Running Agent...")

    result = agent.invoke({
         "input": text,
        "max_chars": 1500

    })

    print("\n===== FINAL TASKS =====\n")
    print(result["messages"][-1].content)






















