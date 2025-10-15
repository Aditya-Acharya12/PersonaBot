from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
from src.services.embedding_service import generate_text_embeddings

router = APIRouter()

class EmbeddingRequest(BaseModel):
    chunks : List[str]

@router.get("/")
def test_embeddings():
    return {"message": "Embeddings route is working!"}

@router.post("/")
def generate_embeddings_route(req: EmbeddingRequest):
    """
    Generates embeddings for a list of text chunks.
    """
    embeddings = generate_text_embeddings(req.chunks)
    return {"num_embeddings": len(embeddings), "sample_embedding": embeddings[0]}