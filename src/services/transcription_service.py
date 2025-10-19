"""
Handles audio transcription logic (e.g., Whisper)
"""
import whisper
import os 
from datetime import datetime, UTC 
from src.db.connection import get_db

db = get_db()
collection = db["transcripts"]

model = whisper.load_model("base")

def is_already_transcribed(file_name: str) -> bool:
    return collection.find_one({"file_name": file_name}) is not None

def save_to_db(file_name: str, language: str, duration: float, transcription: str):
    doc = {
        "file_name": file_name,
        "language": language,
        "duration": duration,
        "transcription": transcription,
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

def transcribe_multiple(files):
    """
    Accepts a list of uploaded audio files (FastAPI UploadFile),
    transcribes each, stores results in DB, and returns metadata.
    """
    results = []

    for file in files:
        file_name = file.filename
        local_path = f"temp/{file_name}"

        # ensure temp folder exists
        os.makedirs("temp", exist_ok=True)

        # save locally
        with open(local_path, "wb") as f:
            f.write(file.file.read())

        if is_already_transcribed(file_name):
            doc = collection.find_one({"file_name": file_name})
            results.append({
                "file_name": file_name,
                "language": doc["language"],
                "duration": doc["duration"],
                "transcript": doc["transcription"],
                "status": "already_exists"
            })
            continue

        # perform transcription
        transcript, language, duration = transcribe_audio(local_path)
        save_to_db(file_name, language, duration, transcript)

        results.append({
            "file_name": file_name,
            "language": language,
            "duration": duration,
            "transcript": transcript,
            "status": "new"
        })

        os.remove(local_path)

    return results

def get_all_transcripts():
    docs = collection.find({}, {"_id": 0})  # exclude internal MongoDB ID
    return list(docs)


def delete_transcript(file_name: str):
    result = collection.delete_one({"file_name": file_name})
    return result.deleted_count > 0