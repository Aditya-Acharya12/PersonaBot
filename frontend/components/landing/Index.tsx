import { Hero } from "@/components/landing/Hero";
import { HowItWorks } from "@/components/landing/HowItWorks";
import { UseCases } from "@/components/landing/UseCases";
import { WhyPersonaBot } from "@/components/landing/WhyPersonaBot";
import { Footer } from "@/components/landing/Footer";

const Index = () => {
  return (
    <main className="min-h-screen">
      <Hero />
      <HowItWorks />
      <UseCases />
      <WhyPersonaBot />
      <Footer />
    </main>
  );
};

export default Index;