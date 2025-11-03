import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Initialize embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Folder where FAISS index will be stored
FAISS_INDEX_DIR = "faiss_index"
os.makedirs(FAISS_INDEX_DIR, exist_ok=True)

# Load existing index if available, otherwise initialize new one
if os.path.exists(os.path.join(FAISS_INDEX_DIR, "index.faiss")):
    vector_db = FAISS.load_local(FAISS_INDEX_DIR, embedding_model, allow_dangerous_deserialization=True)
else:
    vector_db = FAISS.from_texts(["init"], embedding_model)

def add_to_vector_db(text, metadata):
    """Add new text + metadata to FAISS and persist."""
    if isinstance(text, list):
        texts = text
    else:
        texts = [text]

    if isinstance(metadata, list):
        metadatas = metadata
    else:
        metadatas = [metadata]

    # Add data to FAISS
    vector_db.add_texts(texts, metadatas=metadatas)

    # Save for persistence
    vector_db.save_local(FAISS_INDEX_DIR)

    return True


def search_in_vector_db(query, top_k=3):
    """Search similar text in FAISS vector DB."""
    # Ensure the most recent data is loaded
    if os.path.exists(os.path.join(FAISS_INDEX_DIR, "index.faiss")):
        db = FAISS.load_local(FAISS_INDEX_DIR, embedding_model, allow_dangerous_deserialization=True)
    else:
        db = vector_db

    results = db.similarity_search_with_score(query, k=top_k)

    formatted_results = []
    for doc, score in results:
        formatted_results.append({
            "content": doc.page_content,
            "metadata": doc.metadata,
            "relevance_score": float(score)
        })

    return formatted_results