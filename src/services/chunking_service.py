import nltk
from nltk.tokenize import word_tokenize
import hashlib
from src.db.connection import get_db
from bson import ObjectId

db = get_db()
source_collection = db["transcripts"]
chunk_collection = db["chunks"]

# download punkt if missing
nltk.download("punkt", quiet=True)

def generate_chunk_id(text: str, file_name: str, index: int) -> str:
    base = f"{file_name}_{index}_{hashlib.md5(text.encode()).hexdigest()[:8]}"
    return base

def chunk_text_with_overlap(text: str, max_words: int = 250, overlap: int = 50):
    words = word_tokenize(text)
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + max_words, len(words))
        chunk_words = words[start:end]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)
        start += max_words - overlap

    return chunks

def process_transcripts(persona_id: str) -> dict:
    from bson.errors import InvalidId

    try:
        persona_obj_id = ObjectId(persona_id)
    except InvalidId:
        return {"status": "error", "message": "Invalid persona_id"}

    print("🔹 Starting transcript chunking...")
    docs = list(source_collection.find({"persona_id": persona_obj_id}))

    if not docs:
        return {
            "processed_files": 0,
            "total_chunks_inserted": 0,
            "message": "No transcripts found for this persona."
        }

    total_inserted = 0
    processed_files = 0

    for doc in docs:
        file_name = doc.get("file_name")
        text = doc.get("transcription")

        if not text or len(text.strip().split()) < 10:
            continue

        chunks = chunk_text_with_overlap(text)
        inserted = 0

        for idx, chunk in enumerate(chunks):
            chunk_id = generate_chunk_id(chunk, file_name, idx)

            if chunk_collection.find_one({"chunk_id": chunk_id, "persona_id": persona_obj_id}):
                continue

            chunk_doc = {
                "chunk_id": chunk_id,
                "file_name": file_name,
                "text": chunk,
                "persona_id": persona_obj_id,
                "embedding": None
            }
            chunk_collection.insert_one(chunk_doc)
            inserted += 1

        if inserted > 0:
            processed_files += 1
            total_inserted += inserted

    return {
        "processed_files": processed_files,
        "total_chunks_inserted": total_inserted,
        "message": "Chunking completed."
    }

def get_chunks_for_persona(persona_id: str):
    persona_obj_id = ObjectId(persona_id)
    docs = chunk_collection.find(
        {"persona_id": persona_obj_id},
        {"_id": 0}
    )
    return list(docs)

def delete_chunks():
    result = chunk_collection.delete_many({})
    return result.deleted_count
