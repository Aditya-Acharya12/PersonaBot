"""
Handles audio transcription logic (Whisper)
"""
import whisper
import os
from pathlib import Path
from datetime import datetime, UTC
from bson import ObjectId

from src.db.connection import get_db
from src.utils.mongo import serialize_docs

db = get_db()
collection = db["transcripts"]
chunk_collection = db["chunks"]

model = whisper.load_model("base")


def is_already_transcribed(file_name: str, persona_id: str) -> bool:
    return collection.find_one({
        "file_name": file_name,
        "persona_id": ObjectId(persona_id)
    }) is not None


def save_to_db(file_name: str, language: str, duration: float, transcription: str, persona_id: str):
    doc = {
        "file_name": file_name,
        "language": language,
        "duration": duration,
        "transcription": transcription,
        "persona_id": ObjectId(persona_id),
        "timestamp": datetime.now(UTC).isoformat()
    }
    collection.insert_one(doc)
    print(f"[DB] Saved transcript for {file_name}")


def transcribe_audio(file_path: str):
    result = model.transcribe(file_path)
    transcript = result["text"]
    language = result["language"]
    duration = result["segments"][-1]["end"] if result["segments"] else 0.0
    return transcript, language, duration


def transcribe_multiple(file_paths: list[str], persona_id: str):
    """
    BACKGROUND TASK ENTRYPOINT
    Receives file paths (strings), not UploadFile objects
    """
    results = []

    for path in file_paths:
        path = Path(path)
        file_name = path.name

        if is_already_transcribed(file_name, persona_id):
            print(f"[SKIP] {file_name} already transcribed")
            continue

        try:
            transcript, language, duration = transcribe_audio(str(path))
            save_to_db(file_name, language, duration, transcript, persona_id)

            results.append({
                "file_name": file_name,
                "language": language,
                "duration": duration,
                "status": "new"
            })
        except Exception as e:
            print(f"[ERROR] Transcribing {file_name}: {e}")

        finally:
            # cleanup
            if path.exists():
                path.unlink()

    return results


def get_transcripts_for_persona(persona_id: str):
    docs = list(collection.find({"persona_id": ObjectId(persona_id)}))
    return serialize_docs(docs)


def delete_transcript(file_name: str, persona_id: str):
    persona_obj_id = ObjectId(persona_id)

    result = collection.delete_one({
        "file_name": file_name,
        "persona_id": persona_obj_id
    })

    if result.deleted_count == 0:
        return False

    # cascade delete chunks
    chunk_collection.delete_many({
        "file_name": file_name,
        "persona_id": persona_obj_id
    })

    return True