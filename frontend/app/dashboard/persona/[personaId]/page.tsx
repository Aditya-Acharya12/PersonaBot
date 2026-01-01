"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getPersonaById, Persona } from "@/services/persona.service";
import { queryPersona } from "@/services/query.service";

import {
  uploadAndTranscribe,
  getTranscripts,
} from "@/services/transcription.service";

import {
  startChunking,
  getChunks,
} from "@/services/chunking.service";

import {
  startEmbedding,
  getEmbeddingStats,
} from "@/services/embedding.service";

export default function PersonaDetailPage() {
  const { personaId } = useParams();
  const [persona, setPersona] = useState<Persona | null>(null);

  const [files, setFiles] = useState<File[]>([]);
  const [transcripts, setTranscripts] = useState<any[]>([]);
  const [chunks, setChunks] = useState<any[]>([]);
  const [embeddingStats, setEmbeddingStats] = useState<any>(null);

  const [msg, setMsg] = useState("");

  // 🔹 QUERY STATE
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [asking, setAsking] = useState(false);
  const [queryError, setQueryError] = useState("");

  useEffect(() => {
    if (!personaId || typeof personaId !== "string") return;

    getPersonaById(personaId).then(setPersona);
    refreshAll();
  }, [personaId]);

  const refreshAll = async () => {
    if (!personaId || typeof personaId !== "string") return;

    try {
      const t = await getTranscripts(personaId);
      setTranscripts(t);

      const c = await getChunks(personaId);
      setChunks(c);

      const e = await getEmbeddingStats();
      setEmbeddingStats(e);
    } catch {}
  };

  const handleQuery = async () => {
    if (!persona || !question.trim()) return;

    setAsking(true);
    setQueryError("");
    setAnswer("");

    try {
      const res = await queryPersona(persona.id, question);
      setAnswer(res.answer);
    } catch {
      setQueryError("failed to get answer");
    }

    setAsking(false);
  };

  if (!persona) return <p>loading...</p>;

  return (
    <div style={{ padding: 24 }}>
      <h1>{persona.name}</h1>
      <p>{persona.description}</p>

      <hr />

      {/* STEP 1: TRANSCRIPTION */}
      <section>
        <h2>1. Transcription</h2>

        <input
          type="file"
          multiple
          accept="audio/*,video/*"
          onChange={(e) =>
            setFiles(Array.from(e.target.files || []))
          }
        />

        <br />

        <button
          onClick={async () => {
            if (!personaId || typeof personaId !== "string") return;
            await uploadAndTranscribe(personaId, files);
            setMsg("transcription started");
            refreshAll();
          }}
        >
          upload & transcribe
        </button>

        <p>transcripts: {transcripts.length}</p>
      </section>

      <hr />

      {/* STEP 2: CHUNKING */}
      <section>
        <h2>2. Chunking</h2>

        <button
          disabled={transcripts.length === 0}
          onClick={async () => {
            if (!personaId || typeof personaId !== "string") return;
            await startChunking(personaId);
            setMsg("chunking started");
            refreshAll();
          }}
        >
          process chunks
        </button>

        <p>chunks: {chunks.length}</p>
      </section>

      <hr />

      {/* STEP 3: EMBEDDINGS */}
      <section>
        <h2>3. Embeddings</h2>

        <button
          disabled={chunks.length === 0}
          onClick={async () => {
            if (!personaId || typeof personaId !== "string") return;
            await startEmbedding(personaId);
            setMsg("embedding started");
            refreshAll();
          }}
        >
          generate embeddings
        </button>

        {embeddingStats && (
          <p>
            embedded {embeddingStats.embedded_chunks} /{" "}
            {embeddingStats.total_chunks}
          </p>
        )}
      </section>

      <hr />

      {/* STEP 4: QUERY */}
      <section>
        <h2>4. Query Persona</h2>

        <input
          style={{ width: "100%" }}
          placeholder="ask a question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <br />

        <button
          disabled={
            asking ||
            !question.trim() ||
            !embeddingStats ||
            embeddingStats.embedded_chunks === 0
          }
          onClick={handleQuery}
        >
          {asking ? "thinking..." : "ask"}
        </button>

        {queryError && (
          <p style={{ color: "red" }}>{queryError}</p>
        )}

        {answer && (
          <div style={{ marginTop: 16 }}>
            <strong>Answer</strong>
            <p>{answer}</p>
          </div>
        )}
      </section>

      <hr />

      {msg && <p>{msg}</p>}
    </div>
  );
}
