from fastapi import HTTPException
from bson import ObjectId
from src.db.connection import get_db

db = get_db()
personas_col = db["personas"]

def verify_persona_ownership(persona_id: str, user_id: str):
    """
    Ensures that the persona belongs to the authenticated user.
    This is the core 3h authorization check.
    """
    try:
        persona_obj_id = ObjectId(persona_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid persona_id")

    persona = personas_col.find_one({
        "_id": persona_obj_id,
        "user_id": ObjectId(user_id)
    })

    if not persona:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this persona"
        )

    return persona
