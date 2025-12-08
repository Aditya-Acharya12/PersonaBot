from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime
import hashlib

from src.db.connection import get_db
from src.config.settings import get_settings
from src.models.user_models import UserCreate, UserOut, PersonaCreate, PersonaOut

router = APIRouter(prefix = "/users", tags=["Users"])

settings = get_settings()
db=get_db()
users_col = db["users"]
personas_col = db["personas"]

def hash_password(password: str)-> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

@router.post("/", response_model = UserOut)
def create_user(user_in: UserCreate):
    existing = users_col.find_one({"email": user_in.email})
    if existing: 
        raise HTTPException(status_code= 400, detail="User already exists with this email")
    
    doc = {
        "name": user_in.name,
        "email": user_in.email,
        "password": hash_password(user_in.password),
        "persona_limit": settings.MAX_PERSONAS_PER_USER,
        "created_at": datetime.utcnow()
    }

    result = users_col.insert_one(doc)

    return UserOut(
        id=str(result.inserted_id),
        name=user_in.name,
        email=user_in.email
    )


@router.post("{user_id}/personas", response_model=PersonaOut)
def create_persona(user_id: str, persona_in: PersonaCreate):
    try:
        user_obj_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    
    user = users_col.find_one({"_id":user_obj_id})
    if not user:
        raise HTTPException(status_code = 400, detail = "User not fund")
    
    persona_count = personas_col.count_documents({"user_id":user_obj_id})
    if persona_count >= user.get("persona_limit", settings.MAX_PERSONAS_PER_USER):
        raise HTTPException(status_code=400, detail="Persona limit reached for this user")
    
    persona_doc = {
        "user_id": user_obj_id,
        "name": persona_in.name,
        "description": persona_in.description,
        "max_iploads": settings.MAX_MEDIA_PER_PERSONA,
        "upload_count": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }


    result = personas_col.insert_one(persona_doc)

    return PersonaOut(
        id = str(result.inserted_id),
        user_id = str(user_obj_id),
        name = persona_in.name,
        description=persona_in.description,
    )

@router.get("/{user_id}/personas", response_model = list[PersonaOut])
def list_personas(user_id: str):
    try:
        user_obj_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    
    user = users_col.find_one({"_id": user_obj_id})
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    personas = list(personas_col.find({"user_id": user_obj_id}))

    return [
        PersonaOut(
            id = str(p["_id"]),
            user_id=str(p["user_id"]),
            name=p["name"],
            description = p.get("description"),
        )
        for p in personas
    ]