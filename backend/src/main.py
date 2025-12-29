from fastapi import FastAPI
from src.routes import transcribe, process_chunks, generate_embeddings, query, user_management, persona_routes, auth
from src.config.settings import get_settings

app = FastAPI()
settings = get_settings()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(user_management.router, prefix="/users", tags=["Users"])
app.include_router(persona_routes.router, prefix="/persona", tags=["Persona Management"])

app.include_router(transcribe.router, prefix="/transcribe", tags=["Transcription"])
app.include_router(process_chunks.router, prefix="/process_chunks", tags=["Chunk Processing"])
app.include_router(generate_embeddings.router, prefix="/generate_embeddings", tags=["Embeddings"])
app.include_router(query.router, prefix="/query", tags=["Query Engine"])

@app.get("/")
def root():
    return {"message": "Welcome to PersonaBot API"}