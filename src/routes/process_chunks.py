from fastapi import APIRouter
router = APIRouter()

@router.get("/")
def test_process():
    return {"message": "Process Chunks route is working!"}
