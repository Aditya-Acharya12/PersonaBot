import api from "@/lib/api";

export type Transcript = {
  filename: string;
  status: "processing" | "completed" | string;
};

export const uploadAndTranscribe = async (
  personaId: string,
  files: File[]
) => {
  const formData = new FormData();
  files.forEach((f) => formData.append("files", f));

  const res = await api.post(
    `/personas/${personaId}/transcribe`,
    formData,
    {
      headers: { "Content-Type": "multipart/form-data" },
    }
  );

  return res.data;
};

export const getTranscripts = async (
  personaId: string
): Promise<Transcript[]> => {
  const res = await api.get(
    `/personas/${personaId}/transcripts`
  );
  return res.data.data;
};

export const deleteTranscript = async (
  personaId: string,
  fileName: string
) => {
  const res = await api.delete(
    `/personas/${personaId}/transcripts/${fileName}`
  );
  return res.data;
};
