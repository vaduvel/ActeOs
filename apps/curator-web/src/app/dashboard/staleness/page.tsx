"use client";

import { DashboardShell } from "@/components/DashboardShell";

interface StalenessItem {
  source_id: string;
  url: string;
  publisher: string;
  level: string;
  hours_since_fetch: number | null;
  fetch_interval_hours: number;
  overdue_by_hours: number | null;
}

const MOCK_STALENESS: StalenessItem[] = [
  {
    source_id: "s-1",
    url: "https://www.primariatm.ro/acte",
    publisher: "Primăria Timișoara",
    level: "critical",
    hours_since_fetch: 400,
    fetch_interval_hours: 24,
    overdue_by_hours: 376,
  },
  {
    source_id: "s-2",
    url: "https://legislatie.just.ro",
    publisher: "Monitorul Oficial",
    level: "stale",
    hours_since_fetch: 50,
    fetch_interval_hours: 24,
    overdue_by_hours: 26,
  },
  {
    source_id: "s-3",
    url: "https://www.cnas.ro",
    publisher: "CNAS",
    level: "due",
    hours_since_fetch: 26,
    fetch_interval_hours: 24,
    overdue_by_hours: 2,
  },
  {
    source_id: "s-4",
    url: "https://www.drpciv.ro",
    publisher: "DRPCIV",
    level: "fresh",
    hours_since_fetch: 12,
    fetch_interval_hours: 24,
    overdue_by_hours: null,
  },
];

function LevelBadge({ level }: { level: string }) {
  const colors: Record<string, string> = {
    fresh: "bg-green-100 text-green-800",
    due: "bg-yellow-100 text-yellow-800",
    stale: "bg-orange-100 text-orange-800",
    critical: "bg-red-100 text-red-800",
  };
  const labels: Record<string, string> = {
    fresh: "Fresh",
    due: "Due",
    stale: "Stale",
    critical: "CRITIC",
  };
  return (
    <span className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${colors[level] || ""}`}>
      {labels[level] || level}
    </span>
  );
}

export default function StalenessPage() {
  return (
    <DashboardShell>
      <h1 className="mb-6 text-2xl font-bold">Staleness Dashboard</h1>

      <div className="mb-6 grid grid-cols-4 gap-4">
        {(["critical", "stale", "due", "fresh"] as const).map((level) => {
          const count = MOCK_STALENESS.filter((s) => s.level === level).length;
          const colors: Record<string, string> = {
            critical: "border-red-300 bg-red-50",
            stale: "border-orange-300 bg-orange-50",
            due: "border-yellow-300 bg-yellow-50",
            fresh: "border-green-300 bg-green-50",
          };
          return (
            <div key={level} className={`rounded-lg border-2 p-4 ${colors[level]}`}>
              <p className="text-2xl font-bold">{count}</p>
              <p className="text-sm capitalize">{level}</p>
            </div>
          );
        })}
      </div>

      <div className="overflow-hidden rounded-lg border border-gray-200 bg-white">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">Sursă</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">Status</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">Ore de la fetch</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">Interval</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">Depășit cu</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {MOCK_STALENESS.map((item) => (
              <tr key={item.source_id} className="hover:bg-gray-50">
                <td className="px-4 py-3">
                  <p className="text-sm font-medium">{item.publisher}</p>
                  <p className="text-xs text-gray-500">{item.url}</p>
                </td>
                <td className="px-4 py-3"><LevelBadge level={item.level} /></td>
                <td className="px-4 py-3 text-sm">
                  {item.hours_since_fetch !== null ? `${item.hours_since_fetch}h` : "Niciodată"}
                </td>
                <td className="px-4 py-3 text-sm">{item.fetch_interval_hours}h</td>
                <td className="px-4 py-3 text-sm font-medium text-red-600">
                  {item.overdue_by_hours !== null ? `+${item.overdue_by_hours}h` : "—"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </DashboardShell>
  );
}
