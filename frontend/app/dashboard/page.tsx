"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Plus, Trash2, ArrowRight, User, FileText, LogOut } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import {
  getPersonas,
  createPersona,
  deletePersona,
  Persona,
} from "@/services/persona.service";

export default function DashboardPage() {
  const router = useRouter();

  const [personas, setPersonas] = useState<Persona[]>([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const nameInputRef = useRef<HTMLInputElement>(null);

  const loadPersonas = async () => {
    try {
      const data = await getPersonas();
      setPersonas(data);
    } catch {
      setError("failed to load personas");
    }
  };

  useEffect(() => {
    loadPersonas();
  }, []);

  const handleCreate = async () => {
    if (!name.trim()) return;
    setLoading(true);
    setError("");

    try {
      await createPersona(name, description);
      setName("");
      setDescription("");
      await loadPersonas();
    } catch {
      setError("failed to create persona");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (personaId: string) => {
    try {
      await deletePersona(personaId);
      await loadPersonas();
    } catch {
      setError("failed to delete persona");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    router.push("/auth/login");
  };

  return (
    <div className="relative min-h-screen flex flex-col overflow-hidden">
      {/* ===== Global Background ===== */}
      <div className="absolute inset-0 -z-10 bg-[#020617]" />
      <div className="absolute inset-0 -z-10 bg-[radial-gradient(60%_40%_at_50%_0%,rgba(59,130,246,0.22),transparent)]" />
      <div className="absolute inset-0 -z-10 bg-[radial-gradient(40%_30%_at_80%_20%,rgba(14,165,233,0.15),transparent)]" />

      {/* ===== Header ===== */}
      <header className="border-b border-white/10 bg-[#020617]/80 backdrop-blur-md">
        <div className="section-container py-5 flex items-center justify-between">
          <div
            className="flex items-center gap-2 cursor-pointer"
            onClick={() => router.push("/dashboard")}
          >
            <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center font-semibold text-white">
              P
            </div>
            <span className="text-lg font-semibold text-white">
              <a href="/">PersonaBot</a>
            </span>
          </div>

          <Button
            onClick={handleLogout}
            variant="outline"
            className="
              border-white/20
              bg-white/5
              text-slate-200
              hover:bg-white/10
              hover:text-white
              flex items-center gap-2
            "
          >
            <LogOut className="h-4 w-4" />
            Logout
          </Button>
        </div>
      </header>

      {/* ===== Main Content ===== */}
      <main className="flex-1">
        <div className="mx-auto max-w-6xl px-6 py-10">
          {/* Page Intro */}
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="mb-10"
          >
            <h1 className="text-3xl font-semibold text-white tracking-tight">
              Dashboard
            </h1>
            <p className="mt-2 text-slate-400">
              Manage your personas and knowledge bases
            </p>
          </motion.div>

          {/* Error */}
          {error && (
            <div className="mb-6 rounded-lg border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-400">
              {error}
            </div>
          )}

          <div className="grid gap-8 lg:grid-cols-3">
            {/* Create Persona */}
            <Card className="bg-white/10 backdrop-blur-md border border-white/10 shadow-[0_12px_40px_rgba(0,0,0,0.35)]">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-white">
                  <Plus className="h-5 w-5 text-blue-400" />
                  Create Persona
                </CardTitle>
                <CardDescription className="text-slate-400">
                  Add a new persona to your collection
                </CardDescription>
              </CardHeader>

              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-300">
                    Name
                  </label>
                  <Input
                    ref={nameInputRef}
                    placeholder="e.g. Research Assistant"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="bg-white/5 border-white/10 text-white placeholder:text-slate-500"
                  />
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-300">
                    Description
                  </label>
                  <Input
                    placeholder="Optional description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    className="bg-white/5 border-white/10 text-white placeholder:text-slate-500"
                  />
                </div>
              </CardContent>

              <CardFooter>
                <Button
                  onClick={handleCreate}
                  disabled={loading}
                  className="
                    w-full
                    bg-gradient-to-r from-blue-500 to-cyan-500
                    hover:from-blue-400 hover:to-cyan-400
                    text-white
                    shadow-[0_10px_30px_rgba(59,130,246,0.35)]
                  "
                >
                  {loading ? "Creating..." : "Create Persona"}
                </Button>
              </CardFooter>
            </Card>

            {/* Personas */}
            <div className="lg:col-span-2">
              <h2 className="mb-4 text-lg font-medium text-white">
                Your Personas
              </h2>

              {personas.length === 0 ? (
                <Card className="bg-white/5 border border-white/10">
                  <CardContent className="flex flex-col items-center justify-center py-16 text-center">
                    <div className="mb-4 rounded-full bg-white/10 p-4">
                      <User className="h-8 w-8 text-slate-400" />
                    </div>
                    <h3 className="text-lg font-medium text-white">
                      No personas yet
                    </h3>
                    <p className="mt-1 max-w-sm text-sm text-slate-400">
                      Create your first persona to start building your knowledge base.
                    </p>
                    <Button
                      variant="outline"
                      className="mt-6 border-white/20 text-slate-200 hover:bg-white/10"
                      onClick={() => nameInputRef.current?.focus()}
                    >
                      <Plus className="mr-2 h-4 w-4" />
                      Create your first persona
                    </Button>
                  </CardContent>
                </Card>
              ) : (
                <div className="grid gap-4 sm:grid-cols-2">
                  {personas.map((p) => (
                    <Card
                      key={p.id}
                      className="
                        bg-white/10
                        backdrop-blur-md
                        border border-white/10
                        transition-all
                        hover:-translate-y-1
                        hover:border-blue-400/40
                        hover:shadow-[0_20px_40px_rgba(59,130,246,0.15)]
                      "
                    >
                      <CardHeader className="pb-2">
                        <div className="flex items-center gap-3">
                          <div className="rounded-lg bg-blue-500/20 p-2 border border-blue-400/30">
                            <FileText className="h-4 w-4 text-blue-300" />
                          </div>
                          <CardTitle className="text-base text-white">
                            {p.name}
                          </CardTitle>
                        </div>
                      </CardHeader>

                      <CardContent className="pb-2">
                        <p className="text-sm text-slate-400">
                          {p.description || "No description provided"}
                        </p>
                      </CardContent>

                      <CardFooter className="flex justify-between">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleDelete(p.id)}
                          className="text-slate-400 hover:text-red-400 hover:bg-red-500/10"
                        >
                          <Trash2 className="mr-1 h-4 w-4" />
                          Delete
                        </Button>

                        <Button
                          size="sm"
                          onClick={() =>
                            router.push(`/dashboard/persona/${p.id}`)
                          }
                          className="bg-white/10 text-white hover:bg-white/20"
                        >
                          Open
                          <ArrowRight className="ml-1 h-4 w-4" />
                        </Button>
                      </CardFooter>
                    </Card>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      {/* ===== Footer ===== */}
      <footer className="border-t border-white/10 bg-[#020617]/80 backdrop-blur-md">
        <div className="mx-auto max-w-6xl px-6 py-6 text-sm text-slate-400 flex justify-between">
          <span>© {new Date().getFullYear()} PersonaBot</span>
          <span>Built with FastAPI & Next.js</span>
        </div>
      </footer>
    </div>
  );
}
