from fastapi import APIRouter
from src.services.llm_service import generate_answer

router = APIRouter(prefix="/query", tags=["Query Engine"])

@router.post("/")
async def query_llm(payload: dict):
    query = payload.get("query")
    if not query:
        return {"error": "Query text missing"}

    answer = generate_answer(query)
    return {"query": query, "answer": answer}