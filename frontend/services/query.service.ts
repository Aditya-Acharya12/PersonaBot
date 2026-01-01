import api from "@/lib/api";

export const queryPersona = async (
  personaId: string,
  query: string
) => {
  const res = await api.post(
    `/query?persona_id=${personaId}`,
    { query }
  );
  return res.data;
};