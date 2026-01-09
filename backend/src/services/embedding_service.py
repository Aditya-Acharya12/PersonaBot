"""
Handles embedding generation logic
BACKGROUND TASK SAFE
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
    persona_obj_id = ObjectId(persona_id)
    print(f"🔹 Generating embeddings for persona {persona_id}")

    docs = list(
        chunk_collection.find(
            {
                "persona_id": persona_obj_id,
                "embedding": None,
            }
        )
    )

    if not docs:
        return {"embedded_count": 0, "message": "No new chunks to embed."}

    count = 0

    for doc in docs:
        embedding = model.encode(doc["text"]).tolist()

        chunk_collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"embedding": embedding}},
        )

        count += 1
        print(f"✅ Embedded chunk {doc.get('chunk_id', doc['_id'])}")

    return {
        "embedded_count": count,
        "message": "Embedding generation completed.",
    }


def total_chunks_for_persona(persona_id: str) -> int:
    return chunk_collection.count_documents(
        {"persona_id": ObjectId(persona_id)}
    )


def total_embedded_chunks_for_persona(persona_id: str) -> int:
    return chunk_collection.count_documents(
        {
            "persona_id": ObjectId(persona_id),
            "embedding": {"$ne": None},
        }
    )

def clear_all_embeddings():
    result = chunk_collection.update_many(
        {}, {"$set": {"embedding": None}}
    )
    return result.modified_count