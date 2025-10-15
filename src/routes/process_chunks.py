from fastapi import APIRouter
from pydantic import BaseModel
from src.services.chunk_service import create_chunks

router = APIRouter()

class ChunkRequest(BaseModel):
    text: str
    chunk_size: int = 500
    overlap: int = 50

@router.get("/")
def test_process():
    return {"message": "Process Chunks route is working!"}

@router.post("/")
def process_chunks_route(req: ChunkRequest):
    """
    Splits text into overlapping chunks.
    """
    chunks = create_chunks(req.text, req.chunk_size, req.overlap)
    return {"num_chunks": len(chunks), "chunks": chunks[:3]}  # only show few for now