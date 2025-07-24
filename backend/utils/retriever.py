from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

def get_qa_bot():
    vectordb = Chroma(
        persist_directory="chroma_store/",
        embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    )

    llm = HuggingFaceEndpoint(
        repo_id="google/flan-t5-base",
        task="text2text-generation",
        model_kwargs={"temperature": 0.3, "max_new_tokens": 256}
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever()
    )

    return qa_chain

