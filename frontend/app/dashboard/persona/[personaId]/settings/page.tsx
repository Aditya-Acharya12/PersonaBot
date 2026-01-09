"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import {
  ArrowLeft,
  Settings,
  FileText,
  Layers,
  Zap,
  RefreshCw,
  Loader2,
  AlertCircle,
  CheckCircle2,
  Play,
  Clock
} from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { getPersonaById, Persona } from "@/services/persona.service";
import { getTranscripts } from "@/services/transcription.service";
import api from "@/lib/api";

interface PersonaStatus {
  transcripts: number;
  chunks: number;
  embedded_chunks: number;
  is_ready: boolean;
}

interface Transcript {
  status: string;
}

export default function PersonaSettingsPage() {
  const { personaId } = useParams<{ personaId: string }>();
  const router = useRouter();

  const [persona, setPersona] = useState<Persona | null>(null);
  const [status, setStatus] = useState<PersonaStatus | null>(null);
  const [transcripts, setTranscripts] = useState<Transcript[]>([]);

  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [chunking, setChunking] = useState(false);
  const [embedding, setEmbedding] = useState(false);


  const loadAll = async () => {
    if (!personaId) return;
    setLoading(true);

    try {
      const [p, s, t] = await Promise.all([
        getPersonaById(personaId),
        api.get(`/personas/${personaId}/status`),
        getTranscripts(personaId),
      ]);

      setPersona(p);
      setStatus(s.data);
      setTranscripts(t);
    } catch (err) {
      console.error("settings load failed", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAll();
  }, [personaId]);

  const handleRefresh = async () => {
    setRefreshing(true);
    await loadAll();
    setRefreshing(false);
  };

  const handleChunking = async () => {
    if (!personaId) return;
    setChunking(true);
    await api.post(`/process_chunks?persona_id=${personaId}`);
    await loadAll();
    setChunking(false);
  };

  const handleEmbedding = async () => {
    if (!personaId) return;
    setEmbedding(true);
    await api.post(`/generate_embeddings?persona_id=${personaId}`);
    await loadAll();
    setEmbedding(false);
  };


  const completedTranscripts = transcripts.filter(
    (t) => t.status === "completed"
  ).length;

  const processingTranscripts = transcripts.filter(
    (t) => t.status === "processing"
  ).length;


  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-950">
        <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
      </div>
    );
  }

  if (!persona || !status) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center bg-slate-950 text-slate-300">
        <AlertCircle className="h-10 w-10 mb-4" />
        <p className="mb-4">Persona not found</p>
        <Button onClick={() => router.push("/dashboard")}>
          Back to Dashboard
        </Button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-slate-100">
      {/* Header */}
      <header className="border-b border-white/10 bg-slate-950/80 backdrop-blur">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={() =>
              router.push(`/dashboard/persona/${personaId}`)
            }
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Workspace
          </Button>

          <div className="flex items-center gap-2">
            <Settings className="h-5 w-5 text-blue-400" />
            Advanced Settings
          </div>

          <Button
            variant="outline"
            size="sm"
            onClick={handleRefresh}
            disabled={refreshing}
          >
            <RefreshCw className="mr-2 h-4 w-4" />
            Refresh
          </Button>
        </div>
      </header>

      <div className="mx-auto max-w-5xl px-6 py-8 space-y-6">
        {/* Transcriptions */}
        <Card className="bg-white/5 border border-white/10">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-4 w-4 text-blue-400" />
              Transcriptions
            </CardTitle>
            <CardDescription>
              Audio/video to text conversion
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
  {/* Status line */}
{transcripts.length === 0 ? (
  <p className="text-slate-400">No files uploaded yet</p>
) : processingTranscripts > 0 ? (
  <div className="flex items-center gap-2 text-amber-400">
    <Loader2 className="h-4 w-4 animate-spin" />
    {processingTranscripts} processing…
  </div>
) : (
  <div className="flex items-center gap-2 text-green-400">
    <CheckCircle2 className="h-4 w-4" />
    {transcripts.length} file(s) ready
  </div>
)}


  {/* ✅ TRANSCRIPT LIST */}
  {transcripts.length > 0 && (
    <div className="space-y-2">
      {transcripts.map((t, i) => {
        const name =
          (t as any).original_filename ||
          (t as any).filename ||
          (t as any).file_name ||
          "unknown file";

        return (
          <div
            key={i}
            className="flex items-center gap-3 rounded-lg bg-white/10 border border-white/10 px-3 py-2 text-sm"
          >
            <FileText className="h-4 w-4 text-blue-400 shrink-0" />

            <span className="flex-1 truncate text-slate-100">
              {name}
            </span>

            {t.status === "processing" ? (
              <Clock className="h-4 w-4 text-amber-400 shrink-0" />
            ) : (
              <CheckCircle2 className="h-4 w-4 text-green-400 shrink-0" />
            )}
          </div>
        );
      })}
    </div>
  )}
</CardContent>
        </Card>

        {/* Chunking */}
        <Card className="bg-white/5 border border-white/10">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Layers className="h-4 w-4 text-purple-400" />
              Chunking
            </CardTitle>
          </CardHeader>
          <CardContent className="flex justify-between items-center">
            <p>Chunks: {status.chunks}</p>
            <Button
              size="sm"
              onClick={handleChunking}
              disabled={chunking || completedTranscripts === 0}
            >
              <Play className="mr-2 h-4 w-4" />
              Re-run
            </Button>
          </CardContent>
        </Card>

        {/* Embeddings */}
        <Card className="bg-white/5 border border-white/10">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Zap className="h-4 w-4 text-green-400" />
              Embeddings
            </CardTitle>
          </CardHeader>
          <CardContent className="flex justify-between items-center">
            <p>
              Embedded: {status.embedded_chunks} / {status.chunks}
            </p>
            <Button
              size="sm"
              onClick={handleEmbedding}
              disabled={embedding || status.chunks === 0}
            >
              <Play className="mr-2 h-4 w-4" />
              Re-run
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}