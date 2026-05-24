from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def embed_docs(docs, persist_path="chroma_store/"):
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma.from_texts(docs, embedding=embedding, persist_directory=persist_path)
    vectordb.persist()
    return vectordb
 