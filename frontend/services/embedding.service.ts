import api from "@/lib/api";

export const startEmbedding = async (personaId: string) => {
  const res = await api.post(
    `/generate_embeddings/?persona_id=${personaId}`
  );
  return res.data;
};

export const getEmbeddingStats = async () => {
  const res = await api.get("/generate_embeddings/");
  return res.data;
};
