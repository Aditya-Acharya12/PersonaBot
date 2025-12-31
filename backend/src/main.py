from fastapi import FastAPI
from src.routes import transcribe, process_chunks, generate_embeddings, query, user_management, persona_routes, auth
from src.config.settings import get_settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(user_management.router, tags=["Users"])
app.include_router(persona_routes.router, tags=["Persona Management"])

app.include_router(transcribe.router, tags=["Transcription"])
app.include_router(process_chunks.router, tags=["Chunk Processing"])
app.include_router(generate_embeddings.router, tags=["Embeddings"])
app.include_router(query.router, prefix="/query", tags=["Query Engine"])

@app.get("/")
def root():
    return {"message": "Welcome to PersonaBot API"}