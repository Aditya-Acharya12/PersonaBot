from sentence_transformers import SentenceTransformer, util 
import torch 
from src.db.connection import get_db

db = get_db()
chunk_collection = db["chunks"]

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_top_chunks(query, top_k=5):
    query_embedding = model.encode(query, convert_to_tensor=True)
    docs = list(chunk_collection.find({"embedding": {"$ne": None}}))

    similarities = []
    for doc in docs:
        embedding_tensor = torch.tensor(doc["embedding"])
        score = util.cos_sim(query_embedding, embedding_tensor).item()
        similarities.append((doc["text"],score))

    similarities.sort(key=lambda x: x[1], reverse=True)
    top_chunks = [text for text, _ in similarities[:top_k]]

    return top_chunks 