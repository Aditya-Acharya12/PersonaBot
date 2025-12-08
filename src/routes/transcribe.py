from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import List
from src.services.transcription_service import transcribe_multiple,get_all_transcripts,delete_transcript

router = APIRouter(prefix="/tarnscribe", tags=["Transcription"])

@router.get("/")
def list_all_transcripts():
    transcripts = get_all_transcripts()
    return {"status": "success", "data": transcripts}

@router.post("/")
def transcribe_audio_route(persona_id:str = Query(..., description = "Persona ID (Mongo ObjectId as a string) "),files: List[UploadFile] = File(...)):
    """
    Accept multiple audio files, transcribe them, and return the results.
    """
    results = transcribe_multiple(files, persona_id)
    return {"status": "success", "count": len(results), "data": results}

@router.delete("/{file_name}")
def delete_transcript_route(file_name: str):
    deleted = delete_transcript(file_name)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transcript not found")
    return {"status": "success", "message": f"Transcript {file_name} deleted."}