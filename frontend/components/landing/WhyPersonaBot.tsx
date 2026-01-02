"use client";
import { motion } from "framer-motion";
import { Shield, Target, Database } from "lucide-react";

const features = [
  {
    icon: Target,
    title: "Grounded accuracy",
    description: "Answers come directly from your uploaded content. No hallucinations, no generic responses—just your knowledge.",
  },
  {
    icon: Shield,
    title: "Your data, your control",
    description: "Each persona is isolated. Your content stays private and is only used to answer your questions.",
  },
  {
    icon: Database,
    title: "Persona-specific answers",
    description: "Create multiple personas for different contexts. Query the right knowledge base for the right task.",
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.15,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, x: -20 },
  visible: {
    opacity: 1,
    x: 0,
    transition: {
      duration: 0.5,
      ease: [0.4, 0, 0.2, 1] as const,
    },
  },
};

export const WhyPersonaBot = () => {
  return (
    <section className="py-24 bg-background">
      <div className="section-container">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-20 items-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
              Why PersonaBot?
            </h2>
            <p className="text-lg text-muted-foreground leading-relaxed mb-6">
              Unlike generic chatbots, PersonaBot only uses your content to answer questions. 
              This means every response is traceable back to something you provided.
            </p>
            <p className="text-muted-foreground leading-relaxed">
              Whether you're a student, researcher, or professional—build knowledge bases 
              that actually understand your domain.
            </p>
          </motion.div>

          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            className="space-y-6"
          >
            {features.map((feature) => (
              <motion.div
                key={feature.title}
                variants={itemVariants}
                className="flex gap-5"
              >
                <div className="shrink-0 flex items-center justify-center w-11 h-11 rounded-lg bg-primary/10 text-primary">
                  <feature.icon className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-foreground mb-1.5">
                    {feature.title}
                  </h3>
                  <p className="text-muted-foreground leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  );
};
