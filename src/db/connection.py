from motor.motor_asyncio import AsyncIOMotorClient
from src.config.settings import get_settings

settings = get_settings()

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DB_NAME]

def get_database():
    return db