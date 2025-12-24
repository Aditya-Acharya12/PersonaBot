from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Depends
from typing import List
from src.services.transcription_service import transcribe_multiple,get_transcripts_for_persona,delete_transcript
from src.routes.auth import get_current_user
from src.utils.authz import verify_persona_ownership

router = APIRouter(prefix="/tarnscribe", tags=["Transcription"])

@router.get("/")
def list_all_transcripts(persona_id: str = Query(...), current_user: dict = Depends(get_current_user)):
    verify_persona_ownership(persona_id, current_user["id"])
    transcripts = get_transcripts_for_persona(persona_id)
    return {"status": "success", "data": transcripts}

@router.post("/")
def transcribe_audio_route(persona_id:str = Query(..., description = "Persona ID (Mongo ObjectId as a string) "),files: List[UploadFile] = File(...), current_user : dict = Depends(get_current_user)):
    """
    Accept multiple audio files, transcribe them, and return the results.
    """
    verify_persona_ownership(persona_id=persona_id, user_id= current_user["id"])
    results = transcribe_multiple(files, persona_id)
    return {"status": "success", "count": len(results), "data": results}

@router.delete("/{file_name}")
def delete_transcript_route(file_name: str, persona_id: str = Query(...), current_user: dict = Depends(get_current_user)):
    verify_persona_ownership(persona_id, current_user["id"])
    deleted = delete_transcript(file_name, persona_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transcript not found for this persona")
    return {"status": "success", "message": f"Transcript {file_name} deleted for persona {persona_id}"}