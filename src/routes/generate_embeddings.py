from fastapi import APIRouter
router = APIRouter()

@router.get("/")
def test_embeddings():
    return {"message": "Embeddings route is working!"}
