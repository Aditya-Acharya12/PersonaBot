# PersonaBot 🧠🎙️  
*A Production-Grade Persona-Aware Conversational AI System*

PersonaBot is a **production-deployed, end-to-end AI system** that transforms raw audio recordings into **persona-aware conversational agents**.

Each persona behaves like a distinct individual, grounded strictly in *their own spoken content*.  
PersonaBot enforces this at the **data, service, and authorization layers** — not just through prompts.

This project is **not a demo wrapper around an LLM**.  
It is a **real-world AI backend** with authentication, authorization, background processing, cloud deployment, and a cleanly engineered AI pipeline.

---

## 🚀 Live Deployment

- **Backend API (FastAPI + Swagger)**  
  👉 `https://<your-railway-backend>.up.railway.app/docs`

- **Frontend (Next.js)**  
  👉 `https://persona-bot-gamma.vercel.app`

---

## ✨ What PersonaBot Does

- Accepts **audio / video uploads** per persona  
- Transcribes media asynchronously using **OpenAI Whisper**  
- Stores transcripts in **MongoDB**  
- Chunks transcripts with overlap for semantic coherence  
- Generates vector embeddings for each chunk  
- Retrieves the most relevant chunks at query time  
- Produces **first-person, persona-aware responses**  
- Enforces **strict persona ownership & data isolation**  
- Handles long-running AI workloads using **background tasks**  
- Supports secure multi-user access with JWT-based authentication  

---

## 🏗️ System Architecture

```
Client (Web / API)
     ↓
Authenticated Upload (JWT)
     ↓
FastAPI Backend
     ↓
Background Tasks
     ├── Whisper Transcription
     ├── Text Chunking
     └── Embedding Generation
     ↓
MongoDB (Persona-Scoped Data)
     ↓
Semantic Retrieval (Cosine Similarity)
     ↓
LLM Response (Persona-Aware)
```

Each stage is:
- Explicit  
- Independently testable  
- Replaceable without breaking the system  

---

## 🔐 Authentication & Authorization

- OAuth2 password flow  
- JWT-based stateless authentication  
- Secure password hashing using **bcrypt (passlib)**  
- Persona-level ownership checks on **every protected route**  
- Zero cross-user or cross-persona data leakage  

Authorization is enforced **both at route-level and service-level**, ensuring defense in depth.

---

## 🧠 AI Pipeline Design

PersonaBot intentionally exposes the **entire AI lifecycle** instead of hiding it behind a single API call.

### Pipeline Stages

1. **Transcription** – OpenAI Whisper  
2. **Chunking** – Overlapping windows for semantic continuity  
3. **Embedding** – Sentence Transformers (CPU-friendly)  
4. **Retrieval** – Cosine similarity over persona-scoped vectors  
5. **Generation** – Persona-conditioned LLM responses  

### Key Properties

- No hallucinated memory  
- Responses are grounded only in user-provided content  
- Persona isolation is structural, not prompt-based  

---

## ⚙️ Backend Architecture & Engineering

- Clear separation of routes, services, models, and utilities  
- Long-running workloads handled via **FastAPI BackgroundTasks**  
- Explicit error handling and validation  
- Modular design suitable for scaling and extension  
- Identical behavior between **local and production environments**  

---

## 🧪 Tech Stack

### Backend
- FastAPI  
- Uvicorn  
- MongoDB  
- JWT + OAuth2  
- Pydantic v2  
- Passlib (bcrypt)  

### AI / ML
- OpenAI Whisper  
- Sentence Transformers  
- Cosine similarity retrieval  
- LLM (Gemini / OpenAI-compatible)  

### Frontend
- Next.js  
- TypeScript  
- Vercel  

### Infrastructure
- Docker  
- Railway  
- CORS-safe cross-origin auth  
- CPU-only inference  

---

## 📦 Key Features

- Persona-scoped conversational memory  
- Secure multi-user architecture  
- Background transcription & embedding pipelines  
- Clean, extensible AI workflow  
- Swagger-documented APIs  
- Frontend-ready backend  

---

## 🚀 What This Project Demonstrates

- Designing **AI systems**, not just calling AI APIs  
- Handling real-world constraints (latency, auth, deployment)  
- Debugging production issues across Docker, cloud, and ML stacks  
- Strong backend and system engineering fundamentals  
- End-to-end ownership: ML → backend → infra → deployment  

---

## 🔮 Future Work

- Job status & progress tracking endpoints  
- Streaming LLM responses  
- Rate limiting & usage quotas  
- Cloud object storage (S3 / GCS)  
- Vector DB integration (FAISS / Pinecone)  
- Background workers (Celery / Redis)  

---

## 📄 License

MIT License
