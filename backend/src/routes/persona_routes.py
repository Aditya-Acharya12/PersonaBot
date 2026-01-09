from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from src.db.connection import get_db
from src.services.persona_cleanup import delete_all_persona_data
from src.routes.auth import get_current_user
from src.utils.authz import verify_persona_ownership

router = APIRouter(
    prefix="/personas",
    tags=["Persona Management"],
)

db = get_db()
personas_col = db["personas"]
transcripts_col = db["transcripts"]
chunks_col = db["chunks"]

@router.get("/{persona_id}")
def get_persona(
    persona_id: str,
    current_user: dict = Depends(get_current_user),
):
    verify_persona_ownership(persona_id, current_user["id"])

    persona = personas_col.find_one({"_id": ObjectId(persona_id)})
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")

    return {
        "id": str(persona["_id"]),
        "user_id": str(persona["user_id"]),
        "name": persona["name"],
        "description": persona.get("description"),
    }

@router.delete("/{persona_id}/data")
def delete_persona_data(
    persona_id: str,
    current_user: dict = Depends(get_current_user),
):
    verify_persona_ownership(persona_id, current_user["id"])
    result = delete_all_persona_data(persona_id)
    return {"status": "success", "message": result}

@router.get("/{persona_id}/status")
def get_persona_status(
    persona_id: str,
    current_user: dict = Depends(get_current_user),
):
    verify_persona_ownership(persona_id, current_user["id"])

    persona_obj_id = ObjectId(persona_id)

    transcript_count = transcripts_col.count_documents(
        {"persona_id": persona_obj_id}
    )

    chunk_count = chunks_col.count_documents(
        {"persona_id": persona_obj_id}
    )

    embedded_count = chunks_col.count_documents(
        {
            "persona_id": persona_obj_id,
            "embedding": {"$ne": None},
        }
    )

    return {
        "persona_id": persona_id,
        "transcripts": transcript_count,
        "chunks": chunk_count,
        "embedded_chunks": embedded_count,
        "is_ready": embedded_count > 0,
    }
