"use client";
import { motion } from "framer-motion";
import { GraduationCap, Users, Mic2, Brain } from "lucide-react";

const useCases = [
  {
    icon: GraduationCap,
    title: "Learning from lectures",
    description: "Upload course recordings and study by asking questions directly to your lecture content.",
  },
  {
    icon: Users,
    title: "Meeting summaries",
    description: "Turn hours of meetings into queryable knowledge. Find decisions and action items instantly.",
  },
  {
    icon: Mic2,
    title: "Interview preparation",
    description: "Create personas from interview recordings and practice with context-aware Q&A.",
  },
  {
    icon: Brain,
    title: "Personal knowledge base",
    description: "Build a searchable archive of podcasts, voice notes, and ideas you can query anytime.",
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.4,
      ease: [0.4, 0, 0.2, 1] as const,
    },
  },
};

export const UseCases = () => {
  return (
    <section className="py-24 bg-muted/50">
      <div className="section-container">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
            Built for real use cases
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            PersonaBot adapts to how you work and learn.
          </p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6"
        >
          {useCases.map((useCase) => (
            <motion.div
              key={useCase.title}
              variants={itemVariants}
              className="group bg-card rounded-xl p-6 border border-border shadow-card hover:shadow-md transition-shadow duration-300"
            >
              <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary/10 text-primary mb-5 group-hover:bg-primary/15 transition-colors">
                <useCase.icon className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-semibold text-foreground mb-2">
                {useCase.title}
              </h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {useCase.description}
              </p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};
