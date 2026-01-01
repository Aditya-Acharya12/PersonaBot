import api from "@/lib/api";

export const startChunking = async (personaId: string) => {
  const res = await api.post(
    `/process_chunks/?persona_id=${personaId}`
  );
  return res.data;
};

export const getChunks = async (personaId: string) => {
  const res = await api.get(
    `/process_chunks/?persona_id=${personaId}`
  );
  return res.data.data;
};