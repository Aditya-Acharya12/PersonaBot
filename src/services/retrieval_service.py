from sentence_transformers import SentenceTransformer, util
import torch
from bson import ObjectId
from bson.errors import InvalidId

from src.db.connection import get_db
from src.config.settings import get_settings

settings = get_settings()
db = get_db()
chunk_collection = db["chunks"]

# load embedding model once
model = SentenceTransformer(settings.EMBEDDING_MODEL)


def retrieve_top_chunks(query: str, persona_id: str, top_k: int = 5):
    """
    Retrieve top-k most similar chunks for a given persona.
    Returns a list of chunk texts ordered by similarity.
    """
    try:
        persona_obj_id = ObjectId(persona_id)
    except InvalidId:
        print("Invalid persona_id passed to retrieve_top_chunks:", persona_id)
        return []

    # only chunks for this persona with non-null embeddings
    docs = list(
        chunk_collection.find(
            {"persona_id": persona_obj_id, "embedding": {"$ne": None}},
            {"text": 1, "embedding": 1},
        )
    )

    print(f"🔎 Found {len(docs)} chunks with embeddings for persona {persona_id}")

    if not docs:
        return []

    # encode query once
    query_embedding = model.encode(query, convert_to_tensor=True)

    similarities = []
    for doc in docs:
        embedding_tensor = torch.tensor(doc["embedding"])
        score = util.cos_sim(query_embedding, embedding_tensor).item()
        similarities.append((doc["text"], score))

    similarities.sort(key=lambda x: x[1], reverse=True)

    top_chunks = [text for text, _ in similarities[:top_k]]
    print(f"✅ Returning {len(top_chunks)} top chunks")
    return top_chunks
