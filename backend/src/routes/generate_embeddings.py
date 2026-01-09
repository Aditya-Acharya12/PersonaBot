from fastapi import APIRouter, Query, Depends, BackgroundTasks
from src.services.embedding_service import (
    embed_new_chunks,
    total_chunks_for_persona,
    total_embedded_chunks_for_persona,
    clear_all_embeddings,
)
from src.routes.auth import get_current_user
from src.utils.authz import verify_persona_ownership

router = APIRouter(prefix="/generate_embeddings", tags=["Embeddings"])

@router.get("/")
def count_embeddings(
    persona_id: str = Query(..., description="Persona ID"),
    current_user: dict = Depends(get_current_user),
):
    verify_persona_ownership(persona_id, current_user["id"])

    total = total_chunks_for_persona(persona_id)
    embedded = total_embedded_chunks_for_persona(persona_id)

    return {
        "total_chunks": total,
        "embedded_chunks": embedded,
    }

@router.post("/")
def generate_embeddings_route(
    background_tasks: BackgroundTasks,
    persona_id: str = Query(..., description="Persona ID"),
    current_user: dict = Depends(get_current_user),
):
    verify_persona_ownership(persona_id, current_user["id"])
    background_tasks.add_task(embed_new_chunks, persona_id)

    return {
        "status": "success",
        "message": f"Embedding generation task for persona {persona_id} has been started.",
    }

@router.delete("/")
def clear_embeddings():
    cleared_count = clear_all_embeddings()
    return {
        "status": "success",
        "message": f"Cleared embeddings for {cleared_count} chunks.",
    }