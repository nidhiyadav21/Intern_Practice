from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_core.tools import tool

@tool
def get_retriever():
    """ Loaded Documents and splitting into chunks and stored in vectorDb"""
    all_docs = []

    files = ["Data/file1.pdf",
             "Data/file2.pdf",
             "Data/file3.pdf"
    ]
    for file in files:
        loader = PyPDFLoader(file)
        docs = loader.load()
        all_docs.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
         chunk_size=500,
         chunk_overlap=100
    )
    chunks = splitter.split_documents(all_docs)

    embeddings = OllamaEmbeddings(model= "nomic-embed-text", base_url="http://172.16.1.224:11434")

    vector_store = InMemoryVectorStore.from_documents(chunks, embeddings)
    return vector_store.as_retriever()



