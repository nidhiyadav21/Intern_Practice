import os
from dotenv import load_dotenv
load_dotenv()
BASE_URL = os.getenv("BASE_URL")

from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from Rag import get_retriever

def create_qa_chain():
    retriever = get_retriever()
    llm = OllamaLLM(model="mistral-nemo", base_url=BASE_URL)

    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)


    rag_chain_from_docs = (
            RunnablePassthrough.assign(context=(lambda x: x["context"]))

            | prompt
            | llm
            | StrOutputParser()
    )

    rag_chain = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    return rag_chain


def ask_question(query: str):
    """Run a query through the chain and return answer + sources."""
    chain = create_qa_chain()

    # We pass the string directly to the chain
    result = chain.invoke(query)


    answer = result["answer"]


    sources = list(set([doc.metadata.get("source", "Unknown") for doc in result["context"]]))

    return answer, sources


