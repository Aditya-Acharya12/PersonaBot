from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import List
from src.services.transcription_service import transcribe_multiple,get_transcripts_for_persona,delete_transcript

router = APIRouter(prefix="/tarnscribe", tags=["Transcription"])

@router.get("/")
def list_all_transcripts(persona_id: str = Query(...)):
    transcripts = get_transcripts_for_persona(persona_id)
    return {"status": "success", "data": transcripts}

@router.post("/")
def transcribe_audio_route(persona_id:str = Query(..., description = "Persona ID (Mongo ObjectId as a string) "),files: List[UploadFile] = File(...)):
    """
    Accept multiple audio files, transcribe them, and return the results.
    """
    results = transcribe_multiple(files, persona_id)
    return {"status": "success", "count": len(results), "data": results}

@router.delete("/{file_name}")
def delete_transcript_route(file_name: str, persona_id: str = Query(...)):
    deleted = delete_transcript(file_name, persona_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transcript not found for this persona")
    return {"status": "success", "message": f"Transcript {file_name} deleted for persona {persona_id}"}