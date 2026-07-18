"use client";

import { DashboardShell } from "@/components/DashboardShell";

interface FeedbackIncident {
  id: string;
  type: string;
  message: string;
  status: string;
  journey_id: string | null;
  created_at: string;
}

const MOCK_FEEDBACK: FeedbackIncident[] = [
  {
    id: "f-1",
    type: "wrong_schedule",
    message: "Programul afișat pentru DGASPC nu corespunde cu realitatea",
    status: "new",
    journey_id: "j-123",
    created_at: "2026-07-17T14:00:00Z",
  },
  {
    id: "f-2",
    type: "extra_document_requested",
    message: "Mi s-a cerut și dovada domiciliului, nu era în listă",
    status: "triaged",
    journey_id: "j-456",
    created_at: "2026-07-16T10:00:00Z",
  },
];

function TypeBadge({ type }: { type: string }) {
  const labels: Record<string, string> = {
    extra_document_requested: "Document extra",
    wrong_schedule: "Program greșit",
    wrong_address: "Adresă greșită",
    broken_link: "Link rupt",
    accepted_first_time: "Acceptat din prima",
    other: "Altele",
  };
  return (
    <span className="inline-flex rounded-full bg-blue-100 px-2 py-1 text-xs font-medium text-blue-800">
      {labels[type] || type}
    </span>
  );
}

function StatusBadge({ status }: { status: string }) {
  const colors: Record<string, string> = {
    new: "bg-red-100 text-red-800",
    triaged: "bg-yellow-100 text-yellow-800",
    investigating: "bg-blue-100 text-blue-800",
    resolved: "bg-green-100 text-green-800",
    dismissed: "bg-gray-100 text-gray-800",
  };
  return (
    <span className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${colors[status] || ""}`}>
      {status}
    </span>
  );
}

export default function FeedbackPage() {
  return (
    <DashboardShell>
      <h1 className="mb-6 text-2xl font-bold">Feedback & Incidente</h1>

      <div className="mb-4 rounded-md bg-yellow-50 p-3 text-sm text-yellow-700">
        <strong>Notă:</strong> Feedback-ul nu modifică automat regulile.
        Fiecare incident creează un ticket de verificare pentru curatori.
      </div>

      <div className="space-y-4">
        {MOCK_FEEDBACK.map((item) => (
          <div key={item.id} className="rounded-lg border border-gray-200 bg-white p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <TypeBadge type={item.type} />
                <StatusBadge status={item.status} />
              </div>
              <p className="text-xs text-gray-500">
                {new Date(item.created_at).toLocaleDateString("ro-RO")}
              </p>
            </div>
            <p className="mt-2 text-sm text-gray-700">{item.message}</p>
            {item.journey_id && (
              <p className="mt-1 text-xs text-gray-500">
                Journey: {item.journey_id}
              </p>
            )}
          </div>
        ))}
      </div>
    </DashboardShell>
  );
}
