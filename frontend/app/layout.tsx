import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI SDR Crew",
  description: "A crew that qualifies accounts and drafts grounded outreach, with human approval to send.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="mx-auto max-w-5xl px-6 py-6">
          <header className="mb-8 flex items-center justify-between border-b border-edge pb-4">
            <Link href="/" className="flex items-center gap-2">
              <span className="text-lg font-semibold text-white">AI SDR Crew</span>
              <span className="pill bg-slate-800 text-slate-400">grounded · human-approved</span>
            </Link>
            <a href="https://github.com/tahasiddiquii/ai-sdr-crew" className="text-sm text-slate-400 hover:text-white">
              source
            </a>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
