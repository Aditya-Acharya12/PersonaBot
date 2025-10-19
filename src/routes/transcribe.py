from fastapi import APIRouter, UploadFile, File
from typing import List
from src.services.transcription_service import transcribe_multiple

router = APIRouter(prefix="/tarnscribe", tags=["Transcription"])

@router.get("/")
def test_transcribe():
    return {"message": "Transcribe route is working!"}

@router.post("/")
async def transcribe_audio_route(files: List[UploadFile] = File(...)):
    """
    Accept multiple audio files, transcribe them, and return the results.
    """

    results = transcribe_multiple(files)
    return {"status": "success", "count": len(results), "data": results}