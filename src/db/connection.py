from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_db():
    mongo_uri =  os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client[os.getenv("DB_NAME")]
    return db

def get_collections():
    db = get_db()
    return {
        "users": db["users"],
        "personas": db["personas"],
        "media": db["media"]
    }