import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "./providers";
import AppBackground from "@/components/layout/AppBackground";

export const metadata: Metadata = {
  title: "PersonaBot",
  description: "Persona-aware conversational AI for your knowledge",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased relative">
        <Providers>
          <AppBackground />
          {children}
        </Providers>
      </body>
    </html>
  );
}
