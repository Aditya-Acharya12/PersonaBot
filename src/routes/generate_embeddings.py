from fastapi import APIRouter, Query
from typing import List
from src.services.embedding_service import embed_new_chunks, total_chunks, total_embedded_chunks, clear_all_embeddings

router = APIRouter(prefix="/generate_embeddings", tags=["Embeddings"])

@router.get("/")
def count_embeddings():
    total = total_chunks()
    embedded = total_embedded_chunks()
    return {"total_chunks": total, "embedded_chunks": embedded}

@router.post("/")
def generate_embeddings_route(persona_id: str = Query(..., description = "Persona ID (Mongo ObjectId string)")):
    count = embed_new_chunks(persona_id)
    if count == 0:
        return {"message": "No new chunks to embed."}
    return {"message": f"Generated embeddings for {count} new chunks."}

@router.delete("/")
def clear_embeddings():
    cleared_count = clear_all_embeddings()
    return {"message": f"Cleared embeddings for {cleared_count} chunks."}