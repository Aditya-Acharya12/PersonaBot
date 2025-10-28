from src.services.retrieval_service import retrieve_top_chunks
from google import genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_answer(query):
    top_chunks = retrieve_top_chunks(query, top_k=5)

    if not top_chunks:
        return "No relevant information found for this query."

    context_text = "\n\n".join(top_chunks)

    prompt = f"""
You are now acting as the person whose words were transcribed from their video recordings. 
The following context contains excerpts of what they’ve said in multiple clips. 

Use this context to answer the user's question in the first person, 
reflecting their natural speaking style, opinions, and tone.

Keep your answer conversational and authentic — as if you’re talking to your audience, not writing a script.
Here is the context you have to work with:

---
Context:
{context_text}

---
Question:
{query}

Answer (in first person):
"""

    try:
        print("🧠 Sending prompt to Gemini...")
        response = client.models.generate_content(model = "gemini-2.5-flash",contents = prompt)
        print("✅ Gemini responded:", response)
        return response.text.strip()
    except Exception as e:
        import traceback
        print("❌ Gemini generation error:", e)
        traceback.print_exc()
        return f"Error while generating answer: {e}"
