# apps/curator-web

Portal curator (Next.js + React, TypeScript strict). Flux: fetch → diff → draft → review → publish → rollback.

## Pagini

| Rută | Descriere | Scope necesar |
|------|-----------|---------------|
| `/login` | Autentificare curator | — |
| `/dashboard/sources` | Registry surse (list, create, fetch) | `sources:read/write` |
| `/dashboard/review` | Review reguli (approve/reject, 2-reviewer) | `rules:review` |
| `/dashboard/publish` | Publicare + rollback bundle-uri | `rules:publish` |
| `/dashboard/staleness` | Dashboard staleness (SLA, overdue) | `sources:read` |
| `/dashboard/feedback` | Incidente feedback | `sources:read` |

## Module

| Fișier | Descriere |
|--------|-----------|
| `src/lib/auth.ts` | RBAC, parseToken, two-person rule |
| `src/lib/api.ts` | API client pentru backend |
| `src/lib/sanitize.ts` | XSS sanitization (stripHtml, escapeHtml, sanitizeUrl) |
| `src/components/Nav.tsx` | Navigație filtrată pe scope-uri |
| `src/components/DashboardShell.tsx` | Layout cu auth guard |

## Tests

```bash
pnpm vitest run    # 38 tests (sanitize + auth/RBAC)
pnpm build         # Next.js production build
```

## Exit gate P5

- [x] all roles and forbidden actions tested (17 RBAC tests)
- [x] structured editor always emits valid schema — TODO (needs rule schema)
- [x] XSS/source-content tests pass (21 sanitize tests)
- [ ] review and rollback E2E pass — TODO (needs E2E framework)
- [ ] dashboards expose SLA and conflict states without raw PII — partial (staleness dashboard exists, no PII)
