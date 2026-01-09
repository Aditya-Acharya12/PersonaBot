from src.services.transcription_service import transcribe_multiple
from src.services.chunking_service import process_transcripts
from src.services.embedding_service import embed_new_chunks


def run_ingestion_pipeline(saved_paths: list[str], persona_id: str):
    # 1. Transcribe
    transcribe_multiple(saved_paths, persona_id)

    # 2. Chunk
    process_transcripts(persona_id)

    # 3. Embed
    embed_new_chunks(persona_id)

    print(f"✅ Persona {persona_id} is ready")
