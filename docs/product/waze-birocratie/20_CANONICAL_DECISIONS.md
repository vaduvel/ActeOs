# Canonical architecture decisions

These decisions are accepted defaults. Codex creates formal ADR files while implementing them.

| ADR | Decision | Rationale | Revisit trigger |
|---|---|---|---|
| ADR-001 | Android native, Kotlin + Compose | local document processing, accessibility, platform security | iOS/web citizen client roadmap |
| ADR-002 | FastAPI modular monolith for R1 | speed with explicit boundaries; avoids premature microservices | independent scaling/team boundaries |
| ADR-003 | PostgreSQL canonical store | transactions, JSONB, auditability | measured scale/graph limitation |
| ADR-004 | Rules as immutable canonical JSON + relational metadata | deterministic bundle artifacts and easy diff | authoring/performance data proves otherwise |
| ADR-005 | No LLM in route runtime | reproducibility and safety | never for legal decision; only bounded explanation may be evaluated separately |
| ADR-006 | Local-first documents | minimization and trust | explicit user sync or official validation integration |
| ADR-007 | Account optional for citizen | lower friction and privacy | cross-device sync remains optional |
| ADR-008 | OIDC/RBAC for curators | strong organizational access control | provider change |
| ADR-009 | Bundle publication independent from app deploy | urgent content updates/rollback | none expected |
| ADR-010 | Deep-link before API integration | honest capability and lower coupling | formal partnership/API access |
| ADR-011 | Critical stale data fail closed | prevent confident wrong guidance | threshold tuning with evidence |
| ADR-012 | Two-person rule for high/critical content | reduce single-editor risk | audited risk model change |
| ADR-013 | Docker-first, provider-agnostic deployment | reproducibility and portability | platform-specific optimization with ADR |
| ADR-014 | EU-region managed services | GDPR/data-risk baseline | legal assessment |
| ADR-015 | No partner ranking in route | product neutrality | never without manifest change and governance approval |
