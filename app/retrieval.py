from app.database import search_in_vector_db

def retrieve_relevant_text(query: str, top_k: int = 3):
    """
    Retrieve top-k relevant text chunks and sources for a query.
    """
    try:
        results = search_in_vector_db(query, top_k=top_k)
        if not results:
            return []

        formatted = []
        for res in results:
            formatted.append({
                "content": res["content"][:500],
                "relevance_score": round(res["relevance_score"], 3),
                "source": res["metadata"].get("file_name", "Unknown")
            })

        return formatted
    except Exception as e:
        print(f" Retrieval error: {str(e)}")
        return []