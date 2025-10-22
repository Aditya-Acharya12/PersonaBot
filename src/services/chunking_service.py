import nltk
from nltk.tokenize import word_tokenize
import hashlib
from src.db.connection import get_db

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

def process_transcripts():
    """
    Fetches all transcripts, chunks them, and stores results in 'chunks' collection.
    Avoids duplicates via unique chunk_id.
    """
    print("🔹 Starting transcript chunking...")
    docs = list(source_collection.find())

    if not docs:
        print("⚠️ No transcripts found.")
        return {"status": "empty"}

    total_inserted = 0
    for doc in docs:
        file_name = doc.get("file_name")
        text = doc.get("transcription")

        if not text or len(text.strip().split()) < 10:
            print(f"⚠️ Skipping {file_name} — transcription too short.")
            continue

        chunks = chunk_text_with_overlap(text)
        inserted = 0

        for idx, chunk in enumerate(chunks):
            chunk_id = generate_chunk_id(chunk, file_name, idx)
            if chunk_collection.find_one({"chunk_id": chunk_id}):
                continue

            chunk_doc = {
                "chunk_id": chunk_id,
                "file_name": file_name,
                "text": chunk,
                "embedding": None
            }
            chunk_collection.insert_one(chunk_doc)
            inserted += 1

        total_inserted += inserted
        print(f"✅ {file_name}: inserted {inserted} chunks")

    print(f"🏁 Done. Total inserted: {total_inserted}")
    return {"status": "success", "inserted": total_inserted}

def get_all_chunks():
    docs = chunk_collection.find({}, {"_id": 0})  # exclude internal MongoDB ID
    return list(docs)

def delete_chunks():
    result = chunk_collection.delete_many({})
    return result.deleted_count
