"""
Handles vector retrieval and FAISS / Mongo integration
"""

def retrieve_relevant_chunks(query_embedding: list[float], top_k: int = 3) -> list[dict]:
    """
    Retrieves top_k similar chunks from FAISS or DB.
    """
    # TODO: actual FAISS search logic later
    return [{"chunk": "mock context", "score": 0.95}]
