"use client";

import { useEffect, useState, useRef, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import {
  Upload,
  Send,
  ArrowLeft,
  Settings,
  FileAudio,
  Loader2,
  MessageCircle,
  Bot,
  User,
  CheckCircle2,
  Clock,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";

import { getPersonaById, Persona } from "@/services/persona.service";
import { queryPersona } from "@/services/query.service";
import {
  uploadAndTranscribe,
  getTranscripts,
} from "@/services/transcription.service";
import api from "@/lib/api";
import { Footer } from "@/components/landing/Footer";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
}

interface Transcript {
  filename?: string;
  file_name?: string;
  original_filename?: string;
  status: string;
}

interface PersonaStatus {
  transcripts: number;
  chunks: number;
  embedded_chunks: number;
  is_ready: boolean;
}

const glassCard =
  "rounded-xl p-8 bg-white/10 backdrop-blur-lg border border-white/15 " +
  "shadow-[0_8px_32px_rgba(0,0,0,0.25)] transition-all duration-300 " +
  "hover:border-blue-400/40 hover:shadow-[0_12px_40px_rgba(59,130,246,0.25)]";

export default function PersonaWorkspace() {
  const { personaId } = useParams<{ personaId: string }>();
  const router = useRouter();

  const [persona, setPersona] = useState<Persona | null>(null);
  const [status, setStatus] = useState<PersonaStatus | null>(null);
  const [transcripts, setTranscripts] = useState<Transcript[]>([]);

  const [files, setFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [question, setQuestion] = useState("");
  const [asking, setAsking] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!personaId) return;
    loadPersona();
    loadTranscripts();
    loadStatus();
  }, [personaId]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const loadPersona = async () => {
    const data = await getPersonaById(personaId!);
    setPersona(data);
  };

  const loadTranscripts = async () => {
    const t = await getTranscripts(personaId!);
    setTranscripts(t);
  };

  const loadStatus = async () => {
    const res = await api.get(`/personas/${personaId}/status`);
    setStatus(res.data);
  };

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(e.type === "dragenter" || e.type === "dragover");
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const dropped = Array.from(e.dataTransfer.files).filter(
      (f) => f.type.startsWith("audio/") || f.type.startsWith("video/")
    );
    setFiles((prev) => [...prev, ...dropped]);
  }, []);


  const handleUpload = async () => {
    if (!personaId || files.length === 0) return;
    setUploading(true);
    await uploadAndTranscribe(personaId, files);
    setFiles([]);
    await loadTranscripts();
    await loadStatus();
    setUploading(false);
  };

  const handleQuery = async () => {
    if (!personaId || !question.trim()) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      content: question.trim(),
    };

    setMessages((m) => [...m, userMsg]);
    setQuestion("");
    setAsking(true);

    try {
      const res = await queryPersona(personaId, userMsg.content);
      setMessages((m) => [
        ...m,
        {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: res.answer,
        },
      ]);
    } finally {
      setAsking(false);
    }
  };

  if (!persona || !status) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-950">
        <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-slate-100">
      {/* Header */}
      <header className="border-b border-white/10 bg-slate-950/80 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => router.push("/dashboard")}
            className="text-slate-300 hover:text-white"
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Dashboard
          </Button>

          <div>
            <h1 className="text-lg font-semibold">{persona.name}</h1>
            {persona.description && (
              <p className="text-sm text-slate-400">{persona.description}</p>
            )}
          </div>

          <Button
  variant="outline"
  size="sm"
  onClick={() =>
    router.push(`/dashboard/persona/${personaId}/settings`)
  }
  className="border-white/20 text-slate-200 hover:bg-white/10"
>
  <Settings className="mr-2 h-4 w-4" />
  Advanced
</Button>
        </div>
      </header>

      <div className="mx-auto grid max-w-6xl grid-cols-[320px_1fr] gap-6 px-6 py-8">
        {/* Knowledge */}
        <Card className={`${glassCard} text-slate-100`}>
          <CardContent className="space-y-4">
            <h2 className="flex items-center gap-2 font-medium">
              <Upload className="h-4 w-4 text-blue-400" />
              Knowledge
            </h2>

            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`cursor-pointer rounded-xl border-2 border-dashed p-6 text-center transition ${
                dragActive
                  ? "border-blue-400 bg-blue-500/10"
                  : "border-white/20 hover:border-blue-400/40"
              }`}
            >
              <Upload className="mx-auto mb-2 h-6 w-6 text-blue-400" />
              <p className="text-sm font-medium">Upload audio or video</p>
              <p className="text-xs text-slate-400">drag & drop or click</p>
              <input
                ref={fileInputRef}
                type="file"
                multiple
                accept="audio/*,video/*"
                className="hidden"
              />
            </div>

            {files.length > 0 && (
              <Button
                onClick={handleUpload}
                disabled={uploading}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white"
              >
                {uploading ? "Processing…" : "Upload & process"}
              </Button>
            )}

            {/* ✅ FIXED FILE LIST */}
            {transcripts.length > 0 && (
              <div className="space-y-2">
                {transcripts.map((t, i) => {
                  const displayName =
                    t.original_filename ||
                    t.filename ||
                    t.file_name ||
                    "unknown file";

                  return (
                    <div
                      key={i}
                      title={displayName}
                      className="flex items-center gap-3 rounded-lg bg-white/10 border border-white/15 px-3 py-2 text-sm transition hover:bg-white/15"
                    >
                      <FileAudio className="h-4 w-4 text-blue-400 shrink-0" />

                      <span className="flex-1 truncate font-medium text-slate-100">
                        {displayName}
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

            <div
              className={`flex items-center gap-2 rounded-md px-3 py-2 text-sm ${
                status.is_ready
                  ? "bg-green-500/10 text-green-300"
                  : "bg-amber-500/10 text-amber-300"
              }`}
            >
              {status.is_ready ? (
                <>
                  <CheckCircle2 className="h-4 w-4" />
                  Ready to chat
                </>
              ) : (
                <>
                  <Clock className="h-4 w-4" />
                  Processing knowledge…
                </>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Chat */}
        <Card className={`${glassCard} flex flex-col text-slate-100`}>
          <div className="border-b border-white/10 px-6 py-4 flex items-center gap-2">
            <MessageCircle className="h-5 w-5 text-blue-400" />
            Ask questions
          </div>

          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 ? (
              <div className="flex h-full flex-col items-center justify-center text-center">
                <Bot className="h-10 w-10 text-slate-400 mb-3" />
                <p className="text-sm text-slate-400">
                  {status.is_ready
                    ? "Ask anything about your uploaded content"
                    : "Upload content to start chatting"}
                </p>
              </div>
            ) : (
              messages.map((m) => (
                <div
                  key={m.id}
                  className={`flex gap-3 ${
                    m.role === "user" ? "justify-end" : ""
                  }`}
                >
                  {m.role === "assistant" && (
                    <div className="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center">
                      <Bot className="h-4 w-4 text-white" />
                    </div>
                  )}
                  <div
                    className={`max-w-[70%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                      m.role === "user"
                        ? "bg-gradient-to-r from-blue-600 to-blue-500 text-white"
                        : "bg-white/10 border border-white/10"
                    }`}
                  >
                    {m.content}
                  </div>
                  {m.role === "user" && (
                    <div className="h-8 w-8 rounded-full bg-white/20 flex items-center justify-center">
                      <User className="h-4 w-4 text-slate-200" />
                    </div>
                  )}
                </div>
              ))
            )}
            <div ref={chatEndRef} />
          </div>

          <div className="border-t border-white/10 p-4 flex gap-3">
            <Input
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              disabled={!status.is_ready || asking}
              placeholder={
                status.is_ready ? "Ask something…" : "Upload content first"
              }
              className="bg-white/10 border-white/15 text-slate-100 placeholder:text-slate-400"
            />
            <Button
              onClick={handleQuery}
              disabled={!status.is_ready || asking || !question.trim()}
              className="bg-blue-600 hover:bg-blue-700 text-white"
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </Card>
      </div>

      <Footer />
    </div>
  );
}
