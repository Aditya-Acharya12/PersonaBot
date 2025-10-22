"""
Handles embedding generation logic
"""

from sentence_transformers import SentenceTransformer
from src.db.connection import get_db

db = get_db()
chunk_collection = db["chunks"]

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_new_chunks():
    print("Generating embeddings for new chunks...\n")
    count = 0

    for doc in chunk_collection.find({"embedding": None}):
        text = doc["text"]
        chunk_id = doc["chunk_id"]

        embedding = model.encode(text).tolist()

        chunk_collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"embedding" : embedding}}
        )

        print(f"✅ Embedded chunk {chunk_id}")
        count += 1
    return count

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