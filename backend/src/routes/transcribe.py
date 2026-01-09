from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
from typing import List
from bson import ObjectId

from src.services.transcription_service import (
    get_transcripts_for_persona,
    delete_transcript,
)
from src.services.pipeline_service import run_ingestion_pipeline
from src.routes.auth import get_current_user
from src.utils.authz import verify_persona_ownership
from src.utils.file_utils import save_uploads_to_disk

router = APIRouter(
    prefix="/personas/{persona_id}",
    tags=["Transcription"],
)

@router.get("/transcripts")
def list_transcripts(
    persona_id: str,
    current_user: dict = Depends(get_current_user),
):
    verify_persona_ownership(persona_id, current_user["id"])
    transcripts = get_transcripts_for_persona(persona_id)
    return {"status": "success", "data": transcripts}

@router.post("/transcribe")
def transcribe_audio(
    persona_id: str,
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    current_user: dict = Depends(get_current_user),
):
    verify_persona_ownership(persona_id, current_user["id"])

    saved_paths = save_uploads_to_disk(files, persona_id)

    background_tasks.add_task(
        run_ingestion_pipeline,
        saved_paths,
        persona_id,
    )

    return {
        "status": "success",
        "message": f"Ingestion started for {len(saved_paths)} file(s)",
    }

@router.delete("/transcripts/{file_name}")
def delete_transcript_route(
    persona_id: str,
    file_name: str,
    current_user: dict = Depends(get_current_user),
):
    verify_persona_ownership(persona_id, current_user["id"])

    deleted = delete_transcript(file_name, persona_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Transcript not found for this persona",
        )

    return {
        "status": "success",
        "message": f"Transcript {file_name} deleted",
    }
