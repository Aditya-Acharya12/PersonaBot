import api from "@/lib/api";

export const uploadAndTranscribe = async (
  personaId: string,
  files: File[]
) => {
  const formData = new FormData();
  files.forEach((f) => formData.append("files", f));

  const res = await api.post(
    `/tarnscribe/?persona_id=${personaId}`,
    formData,
    {
      headers: { "Content-Type": "multipart/form-data" },
    }
  );

  return res.data;
};

export const getTranscripts = async (personaId: string) => {
  const res = await api.get(`/tarnscribe/?persona_id=${personaId}`);
  return res.data.data;
};

export const deleteTranscript = async (
  personaId: string,
  fileName: string
) => {
  const res = await api.delete(
    `/tarnscribe/${fileName}?persona_id=${personaId}`
  );
  return res.data;
};
