"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV_ITEMS = [
  { href: "/dashboard/sources", label: "Surse", scope: "sources:read" },
  { href: "/dashboard/review", label: "Review", scope: "rules:review" },
  { href: "/dashboard/publish", label: "Publicare", scope: "rules:publish" },
  { href: "/dashboard/staleness", label: "Staleness", scope: "sources:read" },
  { href: "/dashboard/feedback", label: "Feedback", scope: "sources:read" },
];

export function Nav({ userScopes }: { userScopes: Set<string> }) {
  const pathname = usePathname();

  return (
    <nav className="border-b border-gray-200 bg-white">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
        <Link href="/dashboard/sources" className="text-lg font-bold text-blue-600">
          ActeOS Curator
        </Link>
        <div className="flex space-x-1">
          {NAV_ITEMS.filter((item) => userScopes.has(item.scope)).map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                pathname === item.href
                  ? "bg-blue-100 text-blue-700"
                  : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"
              }`}
            >
              {item.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}
