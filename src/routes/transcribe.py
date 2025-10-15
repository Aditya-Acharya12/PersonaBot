from fastapi import APIRouter, UploadFile, File
from src.services.transcription_service import transcribe_audio

router = APIRouter()

@router.get("/")
def test_transcribe():
    return {"message": "Transcribe route is working!"}

@router.post("/")
async def transcribe_audio_route(file: UploadFile = File(...)):
    """
    Accepts an audio file and returns its transcription.
    """
    # temporary save file
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    result = await transcribe_audio(file_path)
    return {"status": "success", "data": result}