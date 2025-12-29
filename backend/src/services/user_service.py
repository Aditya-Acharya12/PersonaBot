from datetime import datetime
from bson import ObjectId
from src.db.connection import get_db
from src.utils.mongo import serialize_doc, serialize_docs
from src.utils.security import hash_password, verify_password

db = get_db()
users_col = db["users"]
personas_col = db["personas"]
transcripts_col = db["transcripts"]
chunks_col = db["chunks"]

def create_user(email: str, password: str, name: str | None = None):
    if users_col.find_one({"email": email}):
        return None
    user_doc = {
        "email": email,
        "password_hash": hash_password(password),
        "name": name,
        "created_at":  datetime.utcnow()
    }
    res = users_col.insert_one(user_doc)
    user_doc["_id"] = res.inserted_id
    return serialize_doc(user_doc)

def authenticate_user(email: str, password: str):
    user = users_col.find_one({"email": email})
    if not user:
        return None
    if not verify_password(password, user.get("password_hash", "")):
        return None
    user = serialize_doc(user)
    user["id"] = user.pop("_id",None)
    return user

def get_user_by_id(user_id: str):
    doc = users_col.find_one({"_id": ObjectId(user_id)})
    if not doc:
        return None
    return serialize_doc(doc)


def get_all_users():
    """
    Return all users (no passwords, etc.).
    """
    docs = list(users_col.find({}))
    cleaned = []
    for doc in docs:
        doc = serialize_doc(doc)
        doc.pop("password_hash", None)
        cleaned.append(doc)
    return cleaned


def get_user_personas(user_id: str):
    """
    Return all personas for a given user_id from the personas collection.
    """
    user_obj = ObjectId(user_id)
    docs = list(personas_col.find({"user_id": user_obj}))
    return serialize_docs(docs)


def delete_persona(user_id: str, persona_id: str) -> dict:
    """
    Delete a persona document belonging to a user and
    delete all transcripts + chunks for that persona.
    """
    user_obj = ObjectId(user_id)
    persona_obj = ObjectId(persona_id)

    persona_res = personas_col.delete_one(
        {"_id": persona_obj, "user_id": user_obj}
    )

    if persona_res.deleted_count == 0:
        return {
            "deleted": False,
            "reason": "Persona not found for this user"
        }

    deleted_transcripts = transcripts_col.delete_many(
        {"persona_id": persona_obj}
    ).deleted_count

    deleted_chunks = chunks_col.delete_many(
        {"persona_id": persona_obj}
    ).deleted_count

    return {
        "deleted": True,
        "deleted_transcripts": deleted_transcripts,
        "deleted_chunks": deleted_chunks,
    }

def delete_user(user_id: str)-> dict:

    user_obj = ObjectId(user_id)

    res_user = users_col.delete_one({"_id": user_obj})
    if res_user.deleted_count == 0:
        return {"deleted": False, "reason": "User not found"}
    
    persona_ids = [p["_id"] for p in personas_col.find({"user_id": user_obj})]

    deleted_personas = personas_col.delete_many({"user_id": user_obj}).deleted_count

    deleted_transcripts = 0
    deleted_chunks = 0

    for pid in persona_ids:
        deleted_transcripts += transcripts_col.delete_many({"perosna_id": pid}).deleted_count
        deleted_chunks += chunks_col.delete_many({"persona_id": pid}).deleted_count

    return {
        "deleted": True,
        "deleted_personas": deleted_personas,
        "deleted_transcripts": deleted_transcripts,
        "deleted_chunks": deleted_chunks,
    }