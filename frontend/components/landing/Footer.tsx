"use client";
import { motion } from "framer-motion";

export const Footer = () => {
  return (
    <motion.footer
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
      className="py-12 bg-slate-950 border-t border-slate-800"
    >
      <div className="section-container">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
              <span className="text-primary-foreground font-bold text-sm">P</span>
            </div>
            <span className="text-lg font-semibold text-slate-200">PersonaBot</span>
          </div>

          <nav className="flex items-center gap-8">
            <a
              href="/auth/login"
              className="text-sm text-slate-400 hover:text-slate-200 transition-colors"
            >
              Login
            </a>
            <a
              href="/auth/signup"
              className="text-sm text-slate-400 hover:text-slate-200 transition-colors"
            >
              Get Started
            </a>
          </nav>
        </div>

        <div className="mt-8 pt-8 border-t border-slate-800">
          <p className="text-sm text-slate-500 text-center">
            © {new Date().getFullYear()} PersonaBot. Built for knowledge workers.
          </p>
        </div>
      </div>
    </motion.footer>
  );
};
