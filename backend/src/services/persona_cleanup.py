from bson import ObjectId
from src.db.connection import get_db

db = get_db()
transcript_collection = db["transcripts"]
chunk_collection = db["chunks"]

def delete_all_persona_data(persona_id: str) -> dict:
    persona_obj = ObjectId(persona_id)

    deleted_transcripts = transcript_collection.delete_many({"persona_id": persona_obj}).deleted_count
    deleted_chunks = chunk_collection.delete_many({"persona_id": persona_obj}).deleted_count

    return {
        "deleted_transcripts" : deleted_transcripts,
        "deleted_chunks" : deleted_chunks
    }