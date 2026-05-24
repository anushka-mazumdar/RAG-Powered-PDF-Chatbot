from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline
from dotenv import load_dotenv
import os

load_dotenv()

# Load local text-to-text model
local_model = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    device=-1  # Force CPU (even if GPU exists)
)

def get_relevant_context(question: str) -> str:
    vectordb = Chroma(
        persist_directory="chroma_store/",
        embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    )
    retriever = vectordb.as_retriever()
    docs = retriever.get_relevant_documents(question)
    context = "\n".join([doc.page_content for doc in docs][:3])
    return context

def answer_question(question: str) -> str:
    context = get_relevant_context(question)
    prompt = f"Answer the following question based on the context:\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"
    try:
        result = local_model(prompt, max_new_tokens=256, temperature=0.3)
        return result[0]['generated_text']
    except Exception as e:
        print("❌ Local model error:", e)
        return "Sorry, I couldn’t generate a response."
