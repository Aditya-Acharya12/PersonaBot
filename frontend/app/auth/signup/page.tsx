"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import Link from "next/link";

import { signup } from "@/services/auth.service";
import { setToken } from "@/lib/auth";

export default function SignupPage() {
  const router = useRouter();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSignup = async () => {
  setError("");

  try {
    await signup(name, email, password);

    // optional UX choice:
    // either auto-login or send to login page
    router.push("/auth/login");
  } catch (err: any) {
    if (err.response?.status === 400) {
      setError("user already exists");
    } else {
      setError("signup failed");
    }
  }
};

  return (
    <div className="relative min-h-screen flex items-center justify-center px-4 bg-background overflow-hidden">
      {/* Animated background */}
      <motion.div
        aria-hidden
        className="
          absolute inset-0
          bg-linear-to-br
          from-blue-500/10
          via-cyan-500/5
          to-transparent
        "
        animate={{ opacity: [0.4, 0.6, 0.4] }}
        transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
      />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.4, 0, 0.2, 1] }}
        className="relative z-10 w-full max-w-md"
      >
        {/* Card */}
        <div
          className="
            rounded-xl p-8
            bg-white/10
            backdrop-blur-lg
            border border-white/15
            shadow-[0_8px_32px_rgba(0,0,0,0.25)]
            transition-all duration-300
            hover:border-blue-400/40
            hover:shadow-[0_12px_40px_rgba(59,130,246,0.25)]
          "
        >
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-2xl font-semibold text-foreground">
              Create your account
            </h1>
            <p className="text-sm text-muted-foreground mt-2">
              Start building your PersonaBot workspace
            </p>
          </div>

          {/* Form */}
          <div className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">
                Name
              </label>
              <Input
                placeholder="Your name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="
                  h-11
                  bg-white/5
                  border-white/15
                  focus:border-blue-400/50
                  focus:ring-2
                  focus:ring-blue-500/20
                  transition-all
                "
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">
                Email
              </label>
              <Input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="
                  h-11
                  bg-white/5
                  border-white/15
                  focus:border-blue-400/50
                  focus:ring-2
                  focus:ring-blue-500/20
                  transition-all
                "
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">
                Password
              </label>
              <Input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="
                  h-11
                  bg-white/5
                  border-white/15
                  focus:border-blue-400/50
                  focus:ring-2
                  focus:ring-blue-500/20
                  transition-all
                "
              />
            </div>

            {error && (
              <motion.p
                initial={{ opacity: 0, y: -5 }}
                animate={{ opacity: 1, y: 0 }}
                className="
                  text-sm
                  text-red-400
                  bg-red-500/10
                  border border-red-500/20
                  rounded-md
                  px-3 py-2
                "
              >
                {error}
              </motion.p>
            )}

            <Button
              onClick={handleSignup}
              className="
                w-full h-11
                bg-linear-to-r from-blue-500 to-cyan-500
                hover:from-blue-400 hover:to-cyan-400
                text-white
                shadow-[0_6px_20px_rgba(59,130,246,0.35)]
                transition-all duration-300
              "
            >
              Create account
            </Button>
          </div>

          {/* Footer */}
          <div className="mt-6 text-center text-sm text-muted-foreground">
            Already have an account?{" "}
            <Link
              href="/auth/login"
              className="text-primary font-medium hover:text-blue-400 transition-colors"
            >
              Sign in
            </Link>
          </div>
        </div>

        {/* Back to home */}
        <div className="text-center mt-6">
          <Link
            href="/"
            className="text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            ← Back to home
          </Link>
        </div>
      </motion.div>
    </div>
  );
}