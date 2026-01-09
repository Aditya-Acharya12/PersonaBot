from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from datetime import datetime

from src.db.connection import get_db
from src.config.settings import get_settings
from src.models.user_models import PersonaCreate, PersonaOut
from src.services.user_service import get_all_users, delete_persona, delete_user
from src.routes.auth import get_current_user
from src.utils.authz import verify_persona_ownership

router = APIRouter(prefix="/users", tags=["Users"])

settings = get_settings()
db = get_db()
users_col = db["users"]
personas_col = db["personas"]


@router.post("/me/personas", response_model=PersonaOut)
def create_persona(
    persona_in: PersonaCreate,
    current_user: dict = Depends(get_current_user),
):
    user_obj_id = ObjectId(current_user["id"])

    user = users_col.find_one({"_id": user_obj_id})
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    persona_count = personas_col.count_documents({"user_id": user_obj_id})
    if persona_count >= user.get("persona_limit", settings.MAX_PERSONAS_PER_USER):
        raise HTTPException(status_code=400, detail="Persona limit reached")

    persona_doc = {
        "user_id": user_obj_id,
        "name": persona_in.name,
        "description": persona_in.description,
        "max_iploads": settings.MAX_MEDIA_PER_PERSONA,
        "upload_count": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    result = personas_col.insert_one(persona_doc)

    return PersonaOut(
        id=str(result.inserted_id),
        user_id=str(user_obj_id),
        name=persona_in.name,
        description=persona_in.description,
    )


@router.get("/me/personas", response_model=list[PersonaOut])
def list_personas(current_user: dict = Depends(get_current_user)):
    user_obj_id = ObjectId(current_user["id"])

    personas = list(personas_col.find({"user_id": user_obj_id}))

    return [
        PersonaOut(
            id=str(p["_id"]),
            user_id=str(p["user_id"]),
            name=p["name"],
            description=p.get("description"),
        )
        for p in personas
    ]


@router.delete("/me/personas/{persona_id}")
def delete_persona_me(
    persona_id: str,
    current_user: dict = Depends(get_current_user),
):
    verify_persona_ownership(persona_id, current_user["id"])
    result = delete_persona(current_user["id"], persona_id)

    if not result["deleted"]:
        raise HTTPException(status_code=404, detail=result["reason"])

    return {"status": "success"}


@router.get("/")
def list_users():
    users = get_all_users()
    return {"status": "success", "data": users}


@router.delete("/{user_id}")
def delete_user_route(user_id: str):
    result = delete_user(user_id)

    if not result["deleted"]:
        raise HTTPException(status_code=404, detail=result["reason"])

    return {"status": "success"}

@router.get("/me/personas/{persona_id}", response_model=PersonaOut)
def get_persona_me(
    persona_id: str,
    current_user: dict = Depends(get_current_user),
):
    verify_persona_ownership(persona_id, current_user["id"])

    persona = personas_col.find_one({"_id": ObjectId(persona_id)})
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")

    return PersonaOut(
        id=str(persona["_id"]),
        user_id=str(persona["user_id"]),
        name=persona["name"],
        description=persona.get("description"),
    )
