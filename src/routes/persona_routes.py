from fastapi import APIRouter
from src.services.persona_cleanup import delete_all_persona_data

router = APIRouter(prefix="/persona", tags=["Persona Management"])

@router.delete("/{persona_id}/data")
def delete_persona_data(persona_id: str):
    result = delete_all_persona_data(persona_id)
    return {"status": "success", "message":result}