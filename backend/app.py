import os
import shutil
import traceback
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from utils.parser import load_pdf
from utils.embedder import embed_docs
from utils.retriever import answer_question

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static folder and upload folder exist
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "..", "frontend", "static")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = load_pdf(file_path)
        embed_docs([text])

        return {"message": f"{file.filename} uploaded and embedded successfully."}
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

@app.post("/ask")
async def ask_question(question: str = Form(...)):
    try:
        print("Received question:", question)
        answer = answer_question(question)
        print("Answer:", answer)
        return {"answer": answer}
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

@app.get("/uploads")
async def list_uploads():
    try:
        files = os.listdir(UPLOAD_DIR)
        # Filter only files (exclude directories)
        file_list = [f for f in files if os.path.isfile(os.path.join(UPLOAD_DIR, f))]
        return {"files": file_list}
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}
