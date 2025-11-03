# Multimodal RAG System (FastAPI + FAISS + Streamlit)

# Overview
This project is a *Multimodal Retrieval-Augmented Generation (RAG) System* that allows you to upload text, PDF, and image files, extracts their content (via OCR for images), stores them in a **FAISS vector database**, and answers natural language questions using *local LLM-based summarization*.

# Features

- Upload & process multiple file types (`.txt`, `.pdf`, `.png`, `.jpg`, `.jpeg`)  
- OCR-based text extraction for images  
- Store embeddings locally using **FAISS** 
- Use **Sentence Transformers** for semantic search  
- Summarize & answer queries using **Hugging Face models**  
- Frontend built with **Streamlit** for easy interaction  
- Clean, modular **FastAPI backend**  

---

## Project Structure
```
multimodal_rag/
├ app/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry point
│   ├── ingestion.py         # File reading, OCR, and text extraction
│   ├── query_handler.py     # Query logic: retrieval + summarization
│   ├── retrieval.py         # FAISS vector search
│   ├── database.py          # Vector store and document handling
│   └── utils.py             # Helper functions
│
├── frontend_app.py          # Streamlit interface
├── uploads/                 # Uploaded files
├── vector_store/            # FAISS index and embeddings
├── requirements.txt
├── README.md
└── .gitignore
```

---

##  Installation & Setup

### Create and Activate Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate     # Windows
```

### 2 Install Required Packages
```bash
pip install -r requirements.txt
```

###  Install Tesseract (for OCR)
- Download from: https://github.com/UB-Mannheim/tesseract/wiki  
- Install in default path (e.g. `C:\Program Files\Tesseract-OCR\`)
- Then set the path in `app/ingestion.py`:
```python
import pytesseract, os
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata\\"
```

---

## ▶ How to Run

### Run Backend (FastAPI)
```bash
uvicorn app.main:app --reload
```
It runs by default at: `http://127.0.0.1:8000`

###  Run Frontend (Streamlit)
In a new terminal:
```bash
streamlit run frontend_app.py
```
It runs at: `http://localhost:8501`

---

##  API Endpoints

###  **POST /upload/file**
**Purpose:** Upload and process a file  
**Request:**  
`multipart/form-data` with a field: `file`  

**Response:**
```json
{
  "status": "success",
  "file_name": "Resume_Data_Analyst.pdf",
  "file_type": "pdf",
  "source_path": "uploads/Resume_Data_Analyst.pdf",
  "content_sample": "Analytical professional with a strong foundation..."
}
```

---

###  **POST /query**
**Purpose:** Ask a question about the uploaded data  

**Request:**
```json
{ "query": "What are Aman's top skills?" }
```

**Response:**
```json
{
  "status": "success",
  "generated_answer": "Aman's top skills include Python, SQL, Excel, Power BI, and Machine Learning.",
  "top_results": [
    {
      "source": "Resume_Data_Analyst.pdf",
      "relevance": 1.23,
      "snippet": "Skilled in Python, SQL, Excel, Power BI..."
    }
  ]
}
```

---

##  How It Works

1. **Ingestion**  
   - Extracts text from files (PDF, TXT, Images with OCR)
   - Splits text into chunks
   - Generates embeddings using `sentence-transformers/all-MiniLM-L6-v2`
   - Stores vectors in FAISS

2. **Query**  
   - Embeds user query and retrieves top-matching chunks from FAISS
   - Summarizes using a lightweight model like `flan-t5-base` or `bart-large-cnn`
   - Returns a concise, contextual answer

---

##  Tech Stack

| Component | Tool |
|------------|------|
| Backend | FastAPI |
| Frontend | Streamlit |
| Embeddings | Sentence Transformers |
| Vector Store | FAISS |
| Summarization | Hugging Face Transformers |
| OCR | Tesseract |
| Language | Python 3.10+ |

---

##  Example Queries

- “What is the candidate’s email ID?”
- “Where is Aman based?”
- “List all technical skills.”
- “Summarize the resume in 3 lines.”
- “Which tools has he used for data analysis?”

---

##  Future Improvements
- Multi-turn chat context memory  
- Cross-encoder reranking for better results  
- Hybrid (dense + keyword) search  
- Deployment on **Render / Railway / Streamlit Cloud**

---



 amant55726@gmail.com
 (https://github.com/AMAN190519)


