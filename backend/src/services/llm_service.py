from typing import List, Dict, Union
from src.services.retrieval_service import retrieve_top_chunks
from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class ChatMessage(BaseModel):
    role: str
    content: str


def format_chat_history(
    history: List[Union[Dict, ChatMessage]]
) -> str:
    """
    Safely formats chat history whether messages are dicts or Pydantic objects.
    """
    lines = []

    for msg in history:
        if isinstance(msg, dict):
            role = msg.get("role")
            content = msg.get("content")
        else:
            role = msg.role
            content = msg.content

        speaker = "User" if role == "user" else "Assistant"
        lines.append(f"{speaker}: {content}")

    return "\n".join(lines)

def generate_answer(
    query: str,
    persona_id: str,
    history: List[Dict] | None = None,
    top_k: int = 5,
) -> str:
    history = history or []

    top_chunks = retrieve_top_chunks(query, persona_id, top_k=top_k)

    if not top_chunks:
        return "I don't have enough information yet to answer that for this persona."

    context_text = "\n\n".join(top_chunks)
    history_block = format_chat_history(history)

    conversation_section = ""
    if history_block:
        conversation_section = f"""
Conversation so far:
{history_block}
"""

    prompt = f"""
You are now acting as the person whose words were transcribed from their video recordings.

The following context contains excerpts of what they've said across multiple clips.
Use ONLY this context to answer.

Speak in the first person.
Be natural, conversational, and authentic.
Do not mention transcripts, clips, or context explicitly.

{conversation_section}
---
Relevant context:
{context_text}

---
User question:
{query}

Answer (in first person):
"""

    try:
        print("🧠 Sending prompt to Gemini...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        print("✅ Gemini responded")
        return response.text.strip()

    except Exception as e:
        import traceback
        print("❌ Gemini generation error:", e)
        traceback.print_exc()
        return "Something went wrong while generating the answer."