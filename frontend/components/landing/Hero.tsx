"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

export const Hero = () => {
  return (
    <section className="relative min-h-[85vh] flex items-center justify-center overflow-hidden bg-slate-950">
      {/* Subtle gradient overlay */}
      <div
        className="absolute inset-0 opacity-40"
        style={{
          background:
            "radial-gradient(ellipse 80% 50% at 50% -20%, hsl(221 83% 53% / 0.3), transparent)",
        }}
      />

      <div className="section-container relative z-10 text-center py-24">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={{
            visible: {
              transition: { staggerChildren: 0.15 },
            },
          }}
          className="max-w-3xl mx-auto"
        >
          <motion.div
            variants={fadeUp}
            transition={{ duration: 0.6, ease: "easeOut" }}
          >
            <span className="inline-block px-4 py-1.5 mb-6 text-sm font-medium text-slate-300 bg-slate-800/60 rounded-full border border-slate-700/50">
              Knowledge-grounded AI for your content
            </span>
          </motion.div>

          <motion.h1
            variants={fadeUp}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-primary-foreground mb-6"
          >
            Talk to your knowledge.
          </motion.h1>

          <motion.p
            variants={fadeUp}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="text-lg sm:text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed"
          >
            Upload audio and video. PersonaBot transcribes, processes, and lets you
            query your content with persona-aware answers grounded in what you've shared.
          </motion.p>

          <motion.div
            variants={fadeUp}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4"
          >
            <Link href="/auth/signup">
              <Button
  size="lg"
  className="
    h-12 px-8 text-base font-medium
    bg-linear-to-r from-blue-500 to-cyan-500
    hover:from-blue-400 hover:to-cyan-400
    text-white
    shadow-[0_8px_30px_rgba(59,130,246,0.35)]
    transition-all duration-300
  "
>

                Get Started
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>

            <Link href="/auth/login">
              <Button
                variant="outline"
                size="lg"
                className="
  h-12 px-8 text-base font-medium
  bg-white/5
  border border-white/20
  text-slate-200
  hover:bg-white/10
  backdrop-blur-md
"
              >
                Login
              </Button>
            </Link>
          </motion.div>
        </motion.div>
      </div>

      <div
  className="
    pointer-events-none
    absolute bottom-0 left-0 right-0
    h-40
    bg-linear-to-b
    from-transparent
    via-slate-900/60
    to-background
    backdrop-blur-sm
  "
/>
    </section>
  );
};
