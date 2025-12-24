from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    MONGO_URI: str
    DB_NAME: str = "audio_transcriber"

    MAX_PERSONAS_PER_USER: int = 3
    MAX_MEDIA_PER_PERSONA: int = 10

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    AWS_REGION: str | None = "ap-south-1"
    S3_BUCKET_NAME: str | None = None

    GEMINI_API_KEY: str | None = None

    WHISPER_MODEL: str = "base"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance so we don't re-parse .env on every import.
    """
    return Settings()