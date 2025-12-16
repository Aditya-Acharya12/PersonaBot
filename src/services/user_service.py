# src/services/user_service.py

from bson import ObjectId
from src.db.connection import get_db
from src.utils.mongo import serialize_doc, serialize_docs

db = get_db()
users_col = db["users"]
personas_col = db["personas"]
transcripts_col = db["transcripts"]
chunks_col = db["chunks"]


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