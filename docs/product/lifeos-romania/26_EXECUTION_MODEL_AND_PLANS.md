# 26 — Model de execuție & convenția ExecPlan (transplant din v2)

## ExecPlan

Un ExecPlan este planul viu prin care un agent execută o schimbare semnificativă fără context ascuns. Obligatoriu când: schimbarea traversează ≥2 module; modifică OpenAPI/JSON Schema/SQL/RLS/contracte; schimbă un ruleset, resolverul sau politica de prospețime; cere migrare/backfill/rollout/rollback; implică integrare externă, documente, auth sau PII; depășește un PR simplu; pregătește un release.

Proprietăți obligatorii: self-contained, outcome-first, executable, testable, living document, safe to resume, reversible, traceable.

Structura minimă: Purpose & user-visible outcome; Context & repo map; Scope/non-scope; Constraints & invariants; Milestones, dependencies & gates; Implementation steps; Validation commands & evidence; Migration/rollout/rollback; Security/privacy/a11y checks; Progress checklist; Surprises; Decision log; Outcomes.

## Gate universal de milestone

Nu e complet până când: cod + contracte + docs sincronizate; lint/typecheck/teste verzi; contracte/migrații validate; a11y/privacy/security aplicabile trecute; observabilitate și failure states există; rollback posibil sau justificat; status și plan viu actualizate.

## Skills repo-scoped (vezi `skills/`)

- **acteos-rule-authoring** — dovezi oficiale → reguli atomice tipate, publicate cu four-eyes.
- **acteos-vertical-slice** — outcome cap-coadă fără a sparge contract-first/determinism/trasabilitate.
- **acteos-research-import** — import guvernat în `research/inbox/`, promovare doar a claim-urilor validate independent.
- **acteos-release-certification** — release gradual, observabil și reversibil; condiții automate de no-go.

## Adaptare la stack-ul nostru

Milestone-urile M0–M9 din v2 sunt valabile, cu o singură înlocuire de stack: **mobile = Android nativ Kotlin** (nu Expo/RN), iar API/motor = `services/api` (`wb_api`) + `packages/rule-engine` (`wb_rule_engine`) existente. Vezi `27_V2_DONOR_INTEGRATION.md`.
