"""
Handles text chunking logic
"""

def create_chunks(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Splits a large text into overlapping chunks.
    """
    # TODO: replace with proper chunking in utils later
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size - overlap)]
