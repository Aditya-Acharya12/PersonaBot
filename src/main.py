from fastapi import FastAPI
from src.routes import transcribe, process_chunks, generate_embeddings, query
from src.config.settings import get_settings

app = FastAPI()
settings = get_settings()

app.include_router(transcribe.router, prefix="/transcribe", tags=["Transcription"])
app.include_router(process_chunks.router, prefix="/process_chunks", tags=["Chunk Processing"])
app.include_router(generate_embeddings.router, prefix="/generate_embeddings", tags=["Embeddings"])
app.include_router(query.router, prefix="/query", tags=["Query Engine"])

@app.get("/")
def root():
    return {"message": "Welcome to PersonaBot API"}