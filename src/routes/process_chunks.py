from fastapi import APIRouter, Query, Depends
from src.services.chunking_service import process_transcripts,get_chunks_for_persona,delete_chunks
from src.routes.auth import get_current_user
from src.utils.authz import verify_persona_ownership

router = APIRouter(prefix="/process_chunks", tags=["Chunk Processing"])

@router.get("/")
def list_chunks(persona_id: str = Query(...), current_user: dict = Depends(get_current_user)):
    verify_persona_ownership(persona_id, current_user["id"])
    chunks = get_chunks_for_persona(persona_id)
    return {"status": "success", "data": chunks}

@router.post("/")
def process_chunks_route(persona_id: str = Query(..., description="Persona ID (Mongo ObjectId string)"), current_user: dict = Depends(get_current_user)):
    verify_persona_ownership(persona_id, current_user["id"])
    result = process_transcripts(persona_id)
    return result

@router.delete("/")
def clear_all_chunks():
    deleted_count = delete_chunks()
    return {"status": "success", "deleted_count": deleted_count}