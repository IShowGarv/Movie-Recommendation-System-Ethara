import type { Metadata } from "next";
import "./globals.css";
import AppShell from "@/components/AppShell";

export const metadata: Metadata = {
  title: "CinemaAI — Movie Recommendations",
  description: "AI-powered movie recommendation platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased bg-[#0d0d0d] text-white">
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
