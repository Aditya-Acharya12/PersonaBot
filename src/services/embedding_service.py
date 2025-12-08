"""
Handles embedding generation logic
"""

from sentence_transformers import SentenceTransformer
from bson import ObjectId

from src.db.connection import get_db
from src.config.settings import get_settings

settings = get_settings()
db = get_db()
chunk_collection = db["chunks"]

model = SentenceTransformer(settings.EMBEDDING_MODEL)

def embed_new_chunks(persona_id: str) -> dict:
    print("Generating embeddings for new chunks...\n")
    persona_obj_id = ObjectId(persona_id)

    docs = list(chunk_collection.find({
        "persona_id": persona_obj_id,
        "embedding": None
    }))

    if not docs: 
        return {
            "embedded_count":  0,
            "message" : "No new chunks to embed."
        }

    count = 0

    for doc in docs:
        text = doc["text"]
        chunk_id = doc["chunk_id"]

        embedding = model.encode(text).tolist()

        chunk_collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"embedding" : embedding}}
        )

        print(f"✅ Embedded chunk {chunk_id}")
        count += 1
    return {
        "embedded_count": count,
        "message" : "Embedding generation for persona."
    }

def total_chunks():
    return chunk_collection.count_documents({})

def total_embedded_chunks():
    return chunk_collection.count_documents({"embedding": {"$ne": None}})

def clear_all_embeddings():
    result = chunk_collection.update_many(
        {},
        {"$set": {"embedding": None}}
    )
    return result.modified_count 