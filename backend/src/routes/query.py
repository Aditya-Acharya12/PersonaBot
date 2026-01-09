from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.services.llm_service import generate_answer
from src.routes.auth import get_current_user
from src.utils.authz import verify_persona_ownership

router = APIRouter(
    prefix="/personas/{persona_id}",
    tags=["Query Engine"],
)
class QueryRequest(BaseModel):
    query: str
@router.post("/query")
def query_persona(
    persona_id: str,
    req: QueryRequest,
    current_user: dict = Depends(get_current_user),
):
    verify_persona_ownership(persona_id, current_user["id"])
    answer = generate_answer(req.query, persona_id)
    return {
        "persona_id": persona_id,
        "query": req.query,
        "answer": answer,
    }