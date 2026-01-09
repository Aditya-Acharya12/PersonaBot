import api from "@/lib/api";

export const queryPersona = async (
  personaId: string,
  query: string
) => {
  const res = await api.post(
    `/personas/${personaId}/query`,
    { query }
  );
  return res.data;
};