"""
Handles embedding generation logic
"""

def generate_text_embeddings(chunks: list[str]) -> list[list[float]]:
    """
    Converts text chunks into embeddings.
    """
    # TODO: integrate SentenceTransformer or Gemini embeddings
    return [[0.1] * 384 for _ in chunks]
