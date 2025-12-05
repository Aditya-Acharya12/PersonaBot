from fastapi import APIRouter
from src.services.chunking_service import process_transcripts,get_all_chunks,delete_chunks

router = APIRouter(prefix="/process_chunks", tags=["Chunk Processing"])

@router.get("/")
def list_all_chunks():
    chunks = get_all_chunks()
    return {"status": "success", "data": chunks}

@router.post("/")
def process_chunks_route():
    result = process_transcripts()
    return result

@router.delete("/")
def clear_all_chunks():
    deleted_count = delete_chunks()
    return {"status": "success", "deleted_count": deleted_count}