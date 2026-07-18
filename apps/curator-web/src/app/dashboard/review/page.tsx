"use client";

import { useState } from "react";
import { DashboardShell } from "@/components/DashboardShell";

interface RuleVersion {
  id: string;
  title: string;
  author: string;
  status: string;
  reviews_required: number;
  reviews_received: number;
  is_critical: boolean;
  created_at: string;
}

const MOCK_RULES: RuleVersion[] = [
  {
    id: "rv-1",
    title: "Permis conducere — documente necesare",
    author: "curator1",
    status: "in_review",
    reviews_required: 2,
    reviews_received: 1,
    is_critical: true,
    created_at: "2026-07-15T10:00:00Z",
  },
  {
    id: "rv-2",
    title: "Certificat naștere — termen eliberare",
    author: "curator2",
    status: "in_review",
    reviews_required: 1,
    reviews_received: 0,
    is_critical: false,
    created_at: "2026-07-16T14:00:00Z",
  },
  {
    id: "rv-3",
    title: "Cazier judiciar — valabilitate",
    author: "curator1",
    status: "changes_requested",
    reviews_required: 2,
    reviews_received: 1,
    is_critical: true,
    created_at: "2026-07-14T09:00:00Z",
  },
];

function StatusBadge({ status }: { status: string }) {
  const colors: Record<string, string> = {
    draft: "bg-gray-100 text-gray-800",
    in_review: "bg-blue-100 text-blue-800",
    changes_requested: "bg-yellow-100 text-yellow-800",
    approved: "bg-green-100 text-green-800",
    rejected: "bg-red-100 text-red-800",
    published: "bg-purple-100 text-purple-800",
  };
  return (
    <span className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${colors[status] || ""}`}>
      {status.replace("_", " ")}
    </span>
  );
}

export default function ReviewPage() {
  const [rules] = useState<RuleVersion[]>(MOCK_RULES);
  const [selectedRule, setSelectedRule] = useState<string | null>(null);
  const [rationale, setRationale] = useState("");

  return (
    <DashboardShell>
      <h1 className="mb-6 text-2xl font-bold">Review Reguli</h1>

      <div className="mb-4 rounded-md bg-blue-50 p-3 text-sm text-blue-700">
        <strong>Regula celor două persoane:</strong> Modificările critice necesită
        aprobarea a doi reviewer-i distincți. Autorul nu își poate aproba propria modificare.
      </div>

      <div className="space-y-4">
        {rules.map((rule) => (
          <div key={rule.id} className="rounded-lg border border-gray-200 bg-white p-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold">{rule.title}</h3>
                <p className="text-sm text-gray-500">
                  Autor: {rule.author} · Creat: {new Date(rule.created_at).toLocaleDateString("ro-RO")}
                </p>
              </div>
              <div className="flex items-center space-x-3">
                <StatusBadge status={rule.status} />
                {rule.is_critical && (
                  <span className="rounded-full bg-red-100 px-2 py-1 text-xs font-medium text-red-800">
                    CRITIC
                  </span>
                )}
                <span className="text-sm text-gray-500">
                  {rule.reviews_received}/{rule.reviews_required} review-uri
                </span>
              </div>
            </div>

            {selectedRule === rule.id && (
              <div className="mt-4 border-t border-gray-200 pt-4">
                <textarea
                  className="block w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
                  rows={3}
                  placeholder="Raționament (min. 10 caractere)..."
                  value={rationale}
                  onChange={(e) => setRationale(e.target.value)}
                />
                <div className="mt-2 flex space-x-2">
                  <button className="rounded-md bg-green-600 px-4 py-2 text-sm text-white hover:bg-green-700">
                    Aprobă
                  </button>
                  <button className="rounded-md bg-yellow-600 px-4 py-2 text-sm text-white hover:bg-yellow-700">
                    Cere modificări
                  </button>
                  <button className="rounded-md bg-red-600 px-4 py-2 text-sm text-white hover:bg-red-700">
                    Respinge
                  </button>
                  <button
                    onClick={() => setSelectedRule(null)}
                    className="rounded-md bg-gray-200 px-4 py-2 text-sm text-gray-700 hover:bg-gray-300"
                  >
                    Anulează
                  </button>
                </div>
              </div>
            )}

            {selectedRule !== rule.id && (
              <button
                onClick={() => setSelectedRule(rule.id)}
                className="mt-3 rounded-md bg-blue-50 px-3 py-1 text-sm text-blue-600 hover:bg-blue-100"
              >
                Review
              </button>
            )}
          </div>
        ))}
      </div>
    </DashboardShell>
  );
}
