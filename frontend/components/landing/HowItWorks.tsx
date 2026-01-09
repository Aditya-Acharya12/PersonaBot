"use client";
import { motion } from "framer-motion";
import { Upload, FileAudio, MessageCircle } from "lucide-react";

const steps = [
  {
    number: "01",
    icon: Upload,
    title: "Upload audio or video",
    description: "Drag and drop your recordings, lectures, meetings, or interviews. We support all major formats.",
  },
  {
    number: "02",
    icon: FileAudio,
    title: "Transcribe & process",
    description: "Your content is automatically transcribed, chunked, and embedded for intelligent retrieval.",
  },
  {
    number: "03",
    icon: MessageCircle,
    title: "Ask questions",
    description: "Query your knowledge base and get accurate, grounded answers from your own content.",
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.5,
      ease: [0.4, 0, 0.2, 1] as const,
    },
  },
};

export const HowItWorks = () => {
  return (
    <section className="relative py-24 bg-linear-to-b from-slate-900/40 to-background">

      <div className="section-container">
        <div className="pointer-events-none absolute top-0 left-0 right-0 h-24 bg-linear-to-b from-transparent via-background/70 to-background"/>
        <div className="pointer-events-none absolute inset-0 -z-10 bg-linear-to-br from-blue-500/10 via-transparent to-cyan-400/10 blur-2xl" />
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
            How it works
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            From raw media to queryable knowledge in three simple steps.
          </p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="grid md:grid-cols-3 gap-8 lg:gap-12"
        >
          {steps.map((step, index) => (
            <motion.div
              key={step.number}
              variants={itemVariants}
              className="relative"
            >
              {/* Connector line */}
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-12 left-[60%] w-[80%] h-px bg-border" />
              )}
              
              <div className="
  rounded-xl p-8 h-full
  bg-white/10
  backdrop-blur-md
  border border-white/10
  shadow-[0_8px_32px_rgba(0,0,0,0.25)]
">
                <div className="flex items-start gap-4 mb-6">
                  <div className="
  flex items-center justify-center 
  w-12 h-12 rounded-xl
  bg-white/10 
  backdrop-blur-md
  border border-white/20
  text-primary
  shadow-[0_0_0_1px_rgba(255,255,255,0.05)]
">
  <step.icon className="w-6 h-6" />
</div>

                  <span className="text-sm font-mono text-muted-foreground mt-3">
                    {step.number}
                  </span>
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-3">
                  {step.title}
                </h3>
                <p className="text-muted-foreground leading-relaxed">
                  {step.description}
                </p>
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};
