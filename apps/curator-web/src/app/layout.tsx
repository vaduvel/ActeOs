import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ActeOS Curator Portal",
  description: "Content curation and review for ActeOS",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ro">
      <body className="min-h-screen bg-gray-50 text-gray-900 antialiased">
        {children}
      </body>
    </html>
  );
}
