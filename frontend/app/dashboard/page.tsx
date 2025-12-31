"use client";

import { useEffect, useState } from "react";
import {
  getPersonas,
  createPersona,
  deletePersona,
  Persona,
} from "@/services/persona.service";

export default function DashboardPage() {
  const [personas, setPersonas] = useState<Persona[]>([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadPersonas = async () => {
    try {
      const data = await getPersonas();
      setPersonas(data);
    } catch {
      setError("failed to load personas");
    }
  };

  useEffect(() => {
    loadPersonas();
  }, []);

  const handleCreate = async () => {
    if (!name.trim()) return;

    setLoading(true);
    setError("");

    try {
      await createPersona(name, description);
      setName("");
      setDescription("");
      await loadPersonas();
    } catch {
      setError("failed to create persona");
    }

    setLoading(false);
  };

  const handleDelete = async (personaId: string) => {
    try {
      await deletePersona(personaId);
      await loadPersonas();
    } catch {
      setError("failed to delete persona");
    }
  };

  return (
    <div style={{ padding: 24 }}>
      <h1>Dashboard</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <div style={{ marginBottom: 24 }}>
        <input
          placeholder="persona name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <br />
        <input
          placeholder="description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <br />
        <button onClick={handleCreate} disabled={loading}>
          {loading ? "creating..." : "create persona"}
        </button>
      </div>

      <hr />

      <ul>
        {personas.map((p) => (
          <li key={p.id} style={{ marginBottom: 12 }}>
            <strong
              style={{ cursor: "pointer", textDecoration: "underline" }}
              onClick={() => {
                window.location.href = `/dashboard/persona/${p.id}`;
              }}
            >
              {p.name}
            </strong>
            <p>{p.description}</p>
            <button onClick={() => handleDelete(p.id)}>delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
