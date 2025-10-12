from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def test_transcribe():
    return {"message": "Transcribe route is working!"}
