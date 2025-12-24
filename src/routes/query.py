from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel
from src.services.llm_service import generate_answer
from src.routes.auth import get_current_user
from src.utils.authz import verify_persona_ownership

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/")
def query_route(
    req: QueryRequest,
    persona_id: str = Query(..., description="Persona ID (Mongo ObjectId string)"),
    current_user: dict = Depends(get_current_user)
):
    verify_persona_ownership(persona_id, current_user["id"])
    answer = generate_answer(req.query, persona_id)
    return {
        "query": req.query,
        "persona_id": persona_id,
        "answer": answer,
    }