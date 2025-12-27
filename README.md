
# PersonaBot 🧠🎙️  
*A Persona-Aware Conversational AI Backend*

PersonaBot is a **production-style backend system** that turns raw audio recordings into a **persona-aware conversational AI**.  
Each persona behaves like a distinct individual, grounded entirely in *their own spoken content*.

This project is not a demo wrapper around an LLM — it is a **full AI pipeline** with authentication, authorization, background processing, and clean system boundaries.

---

## ✨ What PersonaBot Does

- Accepts **audio uploads** for a specific persona
- Transcribes audio using **OpenAI Whisper**
- Chunks transcripts with overlap for semantic coherence
- Generates vector embeddings for each chunk
- Retrieves the most relevant chunks at query time
- Generates **first-person responses** using an LLM
- Enforces **strict persona ownership & data isolation**
- Handles long-running AI workloads asynchronously

---

## 🏗️ System Architecture

```
Audio Upload
     ↓
Whisper Transcription (Background Task)
     ↓
Transcript Storage (MongoDB)
     ↓
Chunking with Overlap
     ↓
Embedding Generation (Sentence Transformers)
     ↓
Vector Retrieval (Cosine Similarity)
     ↓
LLM Response (Persona-Aware)
```

Each step is independently testable and replaceable.

---

## 🔐 Authentication & Authorization

- JWT-based authentication (OAuth2 password flow)
- Secure password hashing (bcrypt via passlib)
- Persona-level ownership checks on **every route**
- No persona data can be accessed across users

---

## 🧠 Design Philosophy

This project is intentionally built to reflect **real-world AI system design**, not a demo stitched together around an LLM API.

The core ideas behind PersonaBot are:

- **Persona isolation by design**  
  Each persona has its own transcripts, chunks, and embeddings. Data never bleeds across personas — enforced at DB, service, and route layers.

- **Explicit AI pipelines**  
  Transcription, chunking, embedding, retrieval, and generation are separate stages with clear responsibilities.

- **Asynchronous-first thinking**  
  Whisper, chunking, and embedding run as background tasks to keep the API responsive.

- **Backend correctness over UI polish**  
  The project prioritizes architecture, authorization, and correctness over surface-level features.

- **Security as a first-class concern**  
  Ownership checks are explicit — no implicit trust, no shortcuts.

PersonaBot is designed to show **how AI systems should be engineered**, not just how they can be called.

---

## 🧪 Tech Stack

### Backend
- **FastAPI**
- **MongoDB (Atlas-ready)**
- **JWT + OAuth2**
- **Pydantic**
- **Uvicorn**

### AI / ML
- **OpenAI Whisper**
- **Sentence Transformers**
- **Cosine similarity retrieval**
- **LLM (Gemini / OpenAI-compatible)**

### Infra & Patterns
- Background tasks for long-running workloads
- Clean service–route separation
- Persona-scoped data modeling

---

## 📦 Key Features

- Persona-based conversational memory
- Background transcription & embedding
- Secure multi-user architecture
- Clean, extensible pipeline
- Ready for frontend or API consumers

---

## 🚀 What This Project Demonstrates

- Designing AI systems beyond prompt engineering
- Handling real-world constraints (latency, ownership, scale)
- Building production-ready APIs for AI workloads
- Strong backend engineering fundamentals

---

## 🔮 Future Work

- Frontend dashboard (Next.js)
- Streaming responses
- Rate limiting & usage quotas
- Job status endpoints
- Cloud storage for media (S3/GCS)
- Vector DB integration (FAISS / Pinecone)

---

## 📄 License

MIT License
