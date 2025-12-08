from fastapi import APIRouter, Query
from pydantic import BaseModel
from src.services.llm_service import generate_answer

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/")
def query_route(
    req: QueryRequest,
    persona_id: str = Query(..., description="Persona ID (Mongo ObjectId string)"),
):
    answer = generate_answer(req.query, persona_id)
    return {
        "query": req.query,
        "persona_id": persona_id,
        "answer": answer,
    }