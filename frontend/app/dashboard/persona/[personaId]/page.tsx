"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getPersonaById, Persona } from "@/services/persona.service";

export default function PersonaDetailPage() {
  const { personaId } = useParams();
  const [persona, setPersona] = useState<Persona | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!personaId || typeof personaId !== "string") return;

    const loadPersona = async () => {
      try {
        const data = await getPersonaById(personaId);
        if (!data) {
          setError("persona not found");
        } else {
          setPersona(data);
        }
      } catch {
        setError("failed to load persona");
      } finally {
        setLoading(false);
      }
    };

    loadPersona();
  }, [personaId]);

  if (loading) return <p>loading...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!persona) return null;

  return (
    <div style={{ padding: 24 }}>
      <h1>{persona.name}</h1>
      <p>{persona.description}</p>

      <hr />

      <section style={{ marginTop: 24 }}>
        <h2>Upload Media</h2>
        <p>media upload UI goes here</p>
      </section>

      <section style={{ marginTop: 24 }}>
        <h2>Chat</h2>
        <p>chat UI goes here</p>
      </section>
    </div>
  );
}
