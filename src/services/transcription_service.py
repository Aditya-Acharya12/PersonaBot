"""
Handles audio transcription logic (e.g., Whisper)
"""
import whisper
import os 
from datetime import datetime, UTC 
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Mongo setup
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["personabot"]
collection = db["transcripts"]

model = whisper.load_model("base")

def is_already_transcribed(file_name: str) -> bool:
    # return collection.find_one({"file_name": file_name}) is not None
    return False

def save_to_db(file_name: str, language: str, duration: float, transcription: str):
    # doc = {
    #     "file_name": file_name,
    #     "language": language,
    #     "duration": duration,
    #     "transcription": transcription,
    #     "timestamp": datetime.now(UTC).isoformat()
    # }
    # collection.insert_one(doc)
    print(f"[Mock] Saved transcript for {file_name} to DB")

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