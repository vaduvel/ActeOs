"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { parseToken, type CuratorUser } from "@/lib/auth";
import { Nav } from "./Nav";

export function DashboardShell({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<CuratorUser | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const token = sessionStorage.getItem("curator_token");
    if (!token) {
      router.push("/login");
      return;
    }
    const parsed = parseToken(token);
    if (!parsed) {
      sessionStorage.removeItem("curator_token");
      router.push("/login");
      return;
    }
    setUser(parsed);
    setLoading(false);
  }, [router]);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-gray-500">Se încarcă...</p>
      </div>
    );
  }

  if (!user) return null;

  return (
    <div>
      <Nav userScopes={user.scopes} />
      <main className="mx-auto max-w-7xl px-4 py-6">{children}</main>
    </div>
  );
}
