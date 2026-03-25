import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

# Setup
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

# 1. Load PDF
loader = PyPDFLoader("SRS-BECS-2007.pdf")
docs = loader.load()

llm = ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL, temperature=0.3)

# 2. Extract Text
context = " ".join([doc.page_content for doc in docs])[:25000]


def generate_requirements(text_context):
    prompt = f"""
    You are a Systems Analyst. Based on the following text, extract:
    # 1. Functional Requirements
    # 2. Non-Functional Requirements

    Format the output as a clean Markdown list.
    ---
    Context: {text_context}
    """
    return llm.invoke(prompt).content


def generate_user_stories(reqs):
    prompt = f"""
    You are a Product Owner. Convert these requirements into detailed Agile User Stories.

    For each story, use this EXACT Markdown format:

    ## [Title of the Story]
    **Description:** As a [user], I want [feature], so that [benefit].
    
    **Acceptance Criteria:**
    - [ ] Criterion 1
    - [ ] Criterion 2
    - [ ] Criterion 3

    ---
    Requirements to convert: {reqs}
    """
    return llm.invoke(prompt).content


def generate_tasks(stories):
    prompt = f"""
    Convert these User Stories into a technical Task Checklist for developers.
    Format:
    # Tasks
    ## [Feature Name]
    - [ ] Main Task
      - Subtask

    Stories: {stories}
    """
    return llm.invoke(prompt).content


# 3. Execution
requirements = generate_requirements(context)
user_stories = generate_user_stories(requirements)
tasks = generate_tasks(user_stories)

# 4. Save to files
files = {
    "requirements.md": requirements,
    "user_stories.md": user_stories,
    "tasks.md": tasks
}

for filename, content in files.items():
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully generated: {filename}")























