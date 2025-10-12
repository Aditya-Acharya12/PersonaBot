from fastapi import FastAPI
from src.routes import transcribe, process_chunks, generate_embeddings, query

app = FastAPI()

app.include_router(transcribe.router, prefix="/transcribe", tags=["Transcription"])
app.include_router(process_chunks.router, prefix="/process_chunks", tags=["Chunk Processing"])
app.include_router(generate_embeddings.router, prefix="/generate_embeddings", tags=["Embeddings"])
app.include_router(query.router, prefix="/query", tags=["Query Engine"])

@app.get("/")
def root():
    return {"message": "Welcome to PersonaBot API"}