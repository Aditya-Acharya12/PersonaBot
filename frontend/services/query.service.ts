import api from "@/lib/api";

export const queryPersona = async (
  personaId: string,
  query: string,
  history: { role: "user" | "assistant"; content: string }[] = []
) => {
  const res = await api.post(
    `/personas/${personaId}/query`,
    {
      query,
      history,
    }
  );

  return res.data;
};
