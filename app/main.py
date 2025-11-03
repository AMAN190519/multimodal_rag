from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
import shutil

from app.ingestion import process_file
from app.query_handler import answer_query

app = FastAPI(title="Multimodal RAG System", version="2.0")

# ✅ Enable CORS (for Streamlit frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Ensure uploads folder exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/file")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save file locally
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process the uploaded file
        result = process_file(file_path)

        if result.get("status") == "error":
            return result

        # ✅ Prepare metadata
        metadata = {
            "file_name": file.filename,
            "file_type": file.filename.split(".")[-1],
            "upload_time": datetime.now().isoformat(),
            "source_path": file_path,
        }

        return {
            "status": "success",
            "full_text": result["full_text"],
            "content_sample": result["content_sample"],
            "metadata": metadata,
        }

    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@app.post("/query")
async def query_data(query: str = Form(...)):
    """
    Handles user queries and retrieves summarized answers from FAISS.
    """
    result = answer_query(query)
    return result


@app.get("/")
async def home():
    return {"message": "🚀 Multimodal RAG API is running successfully!"}