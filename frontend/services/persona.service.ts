import api from "@/lib/api";

export interface Persona {
  id: string;
  user_id: string;
  name: string;
  description?: string;
}

export const getPersonas = async (): Promise<Persona[]> => {
  const res = await api.get("/users/me/personas");
  return res.data;
};

export const createPersona = async (
  name: string,
  description?: string
): Promise<Persona> => {
  const res = await api.post("/users/me/personas", {
    name,
    description,
  });
  return res.data;
};

export const deletePersona = async (personaId: string) => {
  const res = await api.delete(`/users/me/personas/${personaId}`);
  return res.data;
};

export const getPersonaById = async (
  personaId: string
): Promise<Persona | null> => {
  const res = await api.get("/users/me/personas");
  const personas: Persona[] = res.data;
  return personas.find((p) => p.id === personaId) || null;
};