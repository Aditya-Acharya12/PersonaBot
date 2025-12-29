from fastapi import APIRouter, Depends
from src.services.persona_cleanup import delete_all_persona_data
from src.routes.auth import get_current_user
from src.utils.authz import verify_persona_ownership

router = APIRouter(prefix="/persona", tags=["Persona Management"])

@router.delete("/{persona_id}/data")
def delete_persona_data(persona_id: str, current_user: dict = Depends(get_current_user)):
    verify_persona_ownership(persona_id, current_user["id"])
    result = delete_all_persona_data(persona_id)
    return {"status": "success", "message":result}