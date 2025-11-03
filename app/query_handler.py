import os
import re
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline

# ✅ Load embedding model (same one used in ingestion)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ✅ Load summarizer for context-aware answers
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-large")

# ✅ Helper function to load FAISS vector store
def load_vector_store():
    if os.path.exists("vector_store"):
        return FAISS.load_local("vector_store", embedding_model, allow_dangerous_deserialization=True)
    return None

# ✅ Clean the text before using it
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'http\S+', '', text)
    return text.strip()

# ✅ Main function that handles query answering
async def answer_query(query: str):
    vector_store = load_vector_store()
    if vector_store is None:
        return {"status": "error", "answer": "No vector store found. Please upload a file first."}

    # 🔹 Retrieve top chunks from FAISS
    docs_and_scores = vector_store.similarity_search_with_score(query, k=5)
    if not docs_and_scores:
        return {"status": "error", "answer": "No relevant content found."}

    # 🔹 Combine top retrieved chunks
    context = " ".join([clean_text(doc.page_content) for doc, _ in docs_and_scores])
    context = context[:5000]  # Avoid overload

    # 🔹 Construct prompt for smart answering
    prompt = (
        f"You are an intelligent assistant. "
        f"Use the provided context to answer the user's question accurately, concisely, and relevantly.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        f"Answer:"
    )

    # 🔹 Generate answer using LLM
    try:
        response = qa_pipeline(prompt, max_length=200, temperature=0.3, num_return_sequences=1)
        generated_answer = response[0]['generated_text']
    except Exception as e:
        generated_answer = f"(Error while generating answer: {e})"

    # 🔹 Prepare top results for inspection
    top_results = []
    for doc, score in docs_and_scores:
        top_results.append({
            "source": doc.metadata.get("source", "Unknown"),
            "relevance": float(score),
            "snippet": clean_text(doc.page_content[:250])
        })

    # 🔹 Return structured output
    return {
        "status": "success",
        "query": query,
        "generated_answer": clean_text(generated_answer),
        "top_results": top_results
    }