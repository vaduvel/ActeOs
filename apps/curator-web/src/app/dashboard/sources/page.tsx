"use client";

import { useState } from "react";
import { DashboardShell } from "@/components/DashboardShell";
import { hasScope } from "@/lib/auth";
import { stripHtml, sanitizeUrl } from "@/lib/sanitize";

interface Source {
  id: string;
  canonical_url: string;
  publisher: string;
  authority_level: string;
  status: string;
  freshness_class: string;
  review_interval_days: number;
  last_verified_at: string | null;
}

// Mock data for development — will be replaced by API calls
const MOCK_SOURCES: Source[] = [
  {
    id: "1",
    canonical_url: "https://www.primariatm.ro/acte",
    publisher: "Primăria Timișoara",
    authority_level: "uat",
    status: "active",
    freshness_class: "operational",
    review_interval_days: 30,
    last_verified_at: "2026-07-15T10:00:00Z",
  },
  {
    id: "2",
    canonical_url: "https://legislatie.just.ro",
    publisher: "Monitorul Oficial",
    authority_level: "national_normative",
    status: "active",
    freshness_class: "critical",
    review_interval_days: 7,
    last_verified_at: "2026-07-17T08:00:00Z",
  },
  {
    id: "3",
    canonical_url: "https://www.cnas.ro",
    publisher: "CNAS",
    authority_level: "national_operational",
    status: "paused",
    freshness_class: "operational",
    review_interval_days: 14,
    last_verified_at: "2026-06-20T12:00:00Z",
  },
];

function StatusBadge({ status }: { status: string }) {
  const colors: Record<string, string> = {
    active: "bg-green-100 text-green-800",
    paused: "bg-yellow-100 text-yellow-800",
    retired: "bg-gray-100 text-gray-800",
  };
  return (
    <span className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${colors[status] || colors.retired}`}>
      {status}
    </span>
  );
}

function FreshnessBadge({ freshnessClass }: { freshnessClass: string }) {
  const colors: Record<string, string> = {
    critical: "bg-red-100 text-red-800",
    operational: "bg-blue-100 text-blue-800",
    explanatory: "bg-gray-100 text-gray-800",
  };
  return (
    <span className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${colors[freshnessClass] || ""}`}>
      {freshnessClass}
    </span>
  );
}

export default function SourcesPage() {
  const [sources] = useState<Source[]>(MOCK_SOURCES);
  const [showCreate, setShowCreate] = useState(false);

  return (
    <DashboardShell>
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold">Registry Surse</h1>
        <button
          onClick={() => setShowCreate(!showCreate)}
          className="rounded-md bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700"
        >
          + Sursă nouă
        </button>
      </div>

      {showCreate && (
        <div className="mb-6 rounded-lg border border-gray-200 bg-white p-4">
          <h2 className="mb-3 text-lg font-semibold">Sursă nouă</h2>
          <form className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">URL</label>
              <input type="url" className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm" placeholder="https://" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Editor</label>
              <input type="text" className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm" placeholder="Numele instituției" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Nivel autoritate</label>
              <select className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm">
                <option value="national_normative">Național normativ</option>
                <option value="national_operational">Național operațional</option>
                <option value="county">Județ</option>
                <option value="uat">UAT</option>
                <option value="institution">Instituție</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Clasă freshness</label>
              <select className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm">
                <option value="critical">Critic</option>
                <option value="operational">Operațional</option>
                <option value="explanatory">Explicativ</option>
              </select>
            </div>
            <div className="col-span-2">
              <button type="submit" className="rounded-md bg-green-600 px-4 py-2 text-sm text-white hover:bg-green-700">
                Creează sursa
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="overflow-hidden rounded-lg border border-gray-200 bg-white">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">URL</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Editor</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Autoritate</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Status</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Freshness</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Ultima verificare</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Acțiuni</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {sources.map((source) => (
              <tr key={source.id} className="hover:bg-gray-50">
                <td className="max-w-xs truncate px-4 py-3 text-sm">
                  {sanitizeUrl(source.canonical_url) ? (
                    <a
                      href={source.canonical_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      {source.canonical_url}
                    </a>
                  ) : (
                    <span className="text-red-600">URL nesigur</span>
                  )}
                </td>
                <td className="px-4 py-3 text-sm">{source.publisher}</td>
                <td className="px-4 py-3 text-sm">{source.authority_level}</td>
                <td className="px-4 py-3"><StatusBadge status={source.status} /></td>
                <td className="px-4 py-3"><FreshnessBadge freshnessClass={source.freshness_class} /></td>
                <td className="px-4 py-3 text-sm text-gray-500">
                  {source.last_verified_at
                    ? new Date(source.last_verified_at).toLocaleDateString("ro-RO")
                    : "Niciodată"}
                </td>
                <td className="px-4 py-3">
                  <button className="rounded bg-blue-50 px-2 py-1 text-xs text-blue-600 hover:bg-blue-100">
                    Fetch
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </DashboardShell>
  );
}
