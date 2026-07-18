"use client";

import { useState } from "react";
import { DashboardShell } from "@/components/DashboardShell";

interface Bundle {
  id: string;
  bundle_hash: string;
  intent_id: string;
  channel: string;
  published_at: string;
  is_current: boolean;
}

const MOCK_BUNDLES: Bundle[] = [
  {
    id: "b-1",
    bundle_hash: "sha256:a1b2c3d4e5f6...",
    intent_id: "identity_card_first",
    channel: "production",
    published_at: "2026-07-10T12:00:00Z",
    is_current: true,
  },
  {
    id: "b-2",
    bundle_hash: "sha256:f6e5d4c3b2a1...",
    intent_id: "identity_card_first",
    channel: "canary",
    published_at: "2026-07-16T10:00:00Z",
    is_current: false,
  },
];

export default function PublishPage() {
  const [bundles] = useState<Bundle[]>(MOCK_BUNDLES);
  const [confirmRollback, setConfirmRollback] = useState<string | null>(null);

  return (
    <DashboardShell>
      <h1 className="mb-6 text-2xl font-bold">Publicare & Rollback</h1>

      <div className="mb-6 rounded-lg border border-gray-200 bg-white p-4">
        <h2 className="mb-3 text-lg font-semibold">Publică bundle nou</h2>
        <div className="flex space-x-4">
          <select className="rounded-md border border-gray-300 px-3 py-2 text-sm">
            <option value="canary">Canary (test)</option>
            <option value="production">Production</option>
          </select>
          <input
            type="text"
            placeholder="Motiv publicare (min. 10 caractere)"
            className="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm"
          />
          <button className="rounded-md bg-green-600 px-4 py-2 text-sm text-white hover:bg-green-700">
            Publică
          </button>
        </div>
      </div>

      <h2 className="mb-3 text-lg font-semibold">Bundle-uri publicate</h2>
      <div className="space-y-3">
        {bundles.map((bundle) => (
          <div key={bundle.id} className="rounded-lg border border-gray-200 bg-white p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-mono text-sm">{bundle.bundle_hash}</p>
                <p className="text-sm text-gray-500">
                  Intent: {bundle.intent_id} · Canal: {bundle.channel} ·
                  Publicat: {new Date(bundle.published_at).toLocaleDateString("ro-RO")}
                </p>
              </div>
              <div className="flex items-center space-x-2">
                {bundle.is_current && (
                  <span className="rounded-full bg-green-100 px-2 py-1 text-xs font-medium text-green-800">
                    CURRENT
                  </span>
                )}
                <span className={`rounded-full px-2 py-1 text-xs font-medium ${
                  bundle.channel === "production"
                    ? "bg-purple-100 text-purple-800"
                    : "bg-yellow-100 text-yellow-800"
                }`}>
                  {bundle.channel}
                </span>
                {!bundle.is_current && (
                  <button
                    onClick={() => setConfirmRollback(bundle.id)}
                    className="rounded-md bg-red-50 px-3 py-1 text-sm text-red-600 hover:bg-red-100"
                  >
                    Rollback aici
                  </button>
                )}
              </div>
            </div>

            {confirmRollback === bundle.id && (
              <div className="mt-3 rounded-md bg-red-50 p-3">
                <p className="text-sm text-red-700">
                  Sigur doriți rollback la acest bundle? Aceasta va muta pointerul de producție.
                </p>
                <textarea
                  className="mt-2 block w-full rounded-md border border-red-300 px-3 py-2 text-sm"
                  rows={2}
                  placeholder="Motiv rollback (min. 20 caractere)..."
                />
                <div className="mt-2 flex space-x-2">
                  <button className="rounded-md bg-red-600 px-4 py-2 text-sm text-white hover:bg-red-700">
                    Confirmă Rollback
                  </button>
                  <button
                    onClick={() => setConfirmRollback(null)}
                    className="rounded-md bg-gray-200 px-4 py-2 text-sm text-gray-700 hover:bg-gray-300"
                  >
                    Anulează
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </DashboardShell>
  );
}
