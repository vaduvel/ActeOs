# 19 — Risk Register

| ID | Risc | Prob. | Impact | Trigger | Mitigare | Owner |
|---|---|---:|---:|---|---|---|
| R-01 | Regulă administrativă greșită | M | Critic | respingere confirmată | evidence gate, review, rollback | Content Ops |
| R-02 | Rule rot neobservat | H | Critic | source diff/expiry | monitor, hard expiry | Content Ops |
| R-03 | Conflict oficial ascuns | M | Critic | efecte incompatibile | conflict state, block | Policy Lead |
| R-04 | Cost de mentenanță nesustenabil | H | Mare | backlog stale crește | scope local, scoring, automation | Founder |
| R-05 | Acoperire largă superficială | H | Mare | multe events fără claims | release gates | Product |
| R-06 | LLM decide implicit ruta | M | Critic | prompt output folosit direct | architecture tests | Tech Lead |
| R-07 | PII în logs/analytics | M | Critic | scanner/report | allowlist telemetry | Security |
| R-08 | Expunere documente cloud | L/M | Critic | storage/auth incident | local default, encryption, RLS | Security |
| R-09 | Dispozitiv pierdut | M | Mare | vault local accesibil | secure storage, app lock | Mobile Lead |
| R-10 | Account takeover admin | M | Critic | anomalous publish | MFA, RBAC, approvals | Security |
| R-11 | Supply-chain compromise | M | Mare | dependency alert | lockfiles, SBOM, scans | Tech Lead |
| R-12 | Source fetcher SSRF/malware | M | Mare | malicious URL/file | egress controls, sandbox | Security |
| R-13 | Partener influențează ruta | M | Mare | ranking anomaly | neutrality audit | Product |
| R-14 | Utilizatorul crede că garantăm | H | Mare | copy/support feedback | explicit limits, UX | Content Design |
| R-15 | OCR fals pozitiv | H | Mediu/Mare | readiness dispute | confidence/limitations | ML Lead |
| R-16 | Autenticitate sugerată greșit | M | Critic | copy says valid/authentic | prohibited language tests | Product |
| R-17 | Integrare oficială indisponibilă | H | Mediu | timeout | deep-link fallback | Platform |
| R-18 | OpenAPI drift | M | Mare | client/backend mismatch | generated client/CI | Tech Lead |
| R-19 | Migration corupe date | L/M | Critic | deploy failure | expand-contract, backups | Platform |
| R-20 | Notification greșit temporizată | M | Mare | timezone/DST bug | temporal tests | Backend |
| R-21 | Low retention | H | Mare | no return events | household, expiry, traction scope | Product |
| R-22 | Monetizare slabă | M/H | Mare | low conversion | case/family experiments | Founder |
| R-23 | Research legal restriction | M | Mare | terms/robots | manual source process | Policy Lead |
| R-24 | Local staff practice differs | H | Mare | user reports | confirm/gap workflow | Content Ops |
| R-25 | Accessibility exclusion | M | Mare | audit/user test | WCAG gates | Design |
| R-26 | Fake/typosquatted official link | M | Critic | domain change | domain registry, DNS checks | Security |
| R-27 | Overengineering delays value | H | Mare | infra grows before events | modular monolith ADR | Tech Lead |
| R-28 | Vendor lock-in | M | Mediu | adapter bypass | ports/adapters | Architecture |
| R-29 | User shares household improperly | M | Mare | access complaint | granular consent/revoke | Product/Security |
| R-30 | Research input mistaken as approved | M | Critic | inbox data imported | environment and status gates | Content Ops |

## Review

Riscurile se revizuiesc la fiecare release gate și după orice incident. Acceptarea unui risc Critic necesită Founder + Security/Policy owner și termen de remediere; nu poate fi acceptată implicit prin backlog.
