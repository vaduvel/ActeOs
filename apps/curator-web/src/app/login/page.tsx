"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { parseToken } from "@/lib/auth";

export default function LoginPage() {
  const [token, setToken] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    const user = parseToken(token);
    if (!user) {
      setError("Token invalid. Format: Bearer <curator_id>:<scope1,scope2>");
      return;
    }
    // Store token in sessionStorage (not localStorage for security)
    sessionStorage.setItem("curator_token", token);
    router.push("/dashboard/sources");
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <div className="w-full max-w-md rounded-lg bg-white p-8 shadow-md">
        <h1 className="mb-6 text-2xl font-bold text-gray-900">
          ActeOS Curator Portal
        </h1>
        <p className="mb-4 text-sm text-gray-600">
          Introduceți token-ul de curator pentru a accesa portalul.
        </p>
        <form onSubmit={handleLogin}>
          <label className="block text-sm font-medium text-gray-700">
            Bearer Token
            <textarea
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
              rows={3}
              value={token}
              onChange={(e) => setToken(e.target.value)}
              placeholder="Bearer curator1:sources:read,sources:write,rules:review"
            />
          </label>
          {error && (
            <p className="mt-2 text-sm text-red-600">{error}</p>
          )}
          <button
            type="submit"
            className="mt-4 w-full rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Autentificare
          </button>
        </form>
        <div className="mt-6 rounded-md bg-gray-50 p-3 text-xs text-gray-500">
          <p className="font-medium">Scopes disponibile:</p>
          <ul className="mt-1 list-inside list-disc">
            <li>sources:read — vizualizare registry</li>
            <li>sources:write — creare/editare surse</li>
            <li>rules:write — editare drafturi</li>
            <li>rules:review — aprobare/respingere</li>
            <li>rules:publish — publicare/rollback</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
