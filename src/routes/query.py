from fastapi import APIRouter
from pydantic import BaseModel
from src.services.retrieval_service import retrieve_relevant_chunks
from src.services.llm_service import generate_llm_response

router = APIRouter()

class QueryRequest(BaseModel):
    query : str

@router.get("/")
def test_query():
    return {"message": "query route is working!"}

@router.post("/")
def query_route(req: QueryRequest):
    """
    Performs retrieval + LLM response generation.
    """
    query_embedding = [0.1] * 384  # placeholder for now
    relevant_chunks = retrieve_relevant_chunks(query_embedding)
    response = generate_llm_response(req.query, relevant_chunks)

    return {
        "query": req.query,
        "context": relevant_chunks,
        "response": response
    }