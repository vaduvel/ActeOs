# ADR-015 — v2.1 pack ca sursă unică de adevăr; migrarea activelor existente

- **Status:** Accepted
- **Date:** 2026-06-25
- **Owners:** Product + Architecture

## Context

Înainte de pachetul v2.1 existau deja livrabile reale în repo:

- un authoring/rule engine determinist în `packages/rule-engine/wb_rule_engine/authoring` (predicate AST tipat, `evaluate_ruleset` cu deadline-uri, conflicte, override și precedență de status, golden runner, validator JSON-schema, orchestrator multi-event);
- 19 batch-uri de research R1 în `docs/product/lifeos-romania/research/inbox`;
- doctrină de produs și contracte (`docs/product/lifeos-romania/`, ex. D6 conflict-never-hidden, freshness, source claims).

Pachetul `acteos_lifeos_romania_v2_1/` este un Master Execution Pack complet, cu plan de execuție fazat (M0–M9), contracte OpenAPI/JSON Schema, taxonomie de intenturi și skill-uri operaționale. Engine-ul existent se mapează aproape integral pe contractul motorului din `docs/05_RULE_ENGINE_SPEC.md` (statusuri `resolved/needs_facts/needs_confirmation/conflicting/blocked`, același DSL de predicate).

## Decision

Pachetul **v2.1 devine sursa unică de adevăr** pentru produs, arhitectură, contracte și execuție. Activele existente **se migrează**, nu se aruncă și nu se reconstruiesc de la zero:

1. Rule engine-ul existent se migrează în `python/acteos_rule_engine` (+ `python/acteos_domain`) conform repository map din `codex/EXECUTION_PLAN.md`, păstrând testele golden și validatorul; reconciliere de contract: câmpuri namespaced (`facts.*`, `context.*`), `engine_version = 2.1.0`, modelul de conflict v2.1.
2. Cele 19 batch-uri de research se importă în `research/inbox` al pack-ului prin skill-ul `acteos-research-import`, rămânând neaprobate până la gate-uri.
3. Doctrina și contractele din `docs/product/lifeos-romania/` devin material donor; conținutul canonic se consolidează în docs-urile v2.1, fără duplicare conflictuală.
4. Convențiile de ID se aliniază la v2.1: stratul public `ro.intent.*`, contextul intern `ro.life.*`, `journey_template_id`; vechiul `life.*` se remapează la import.

v2.1 se promovează ca rădăcină de lucru a monorepo-ului; structurile vechi rămân temporar pentru trasabilitate și se retrag după ce migrarea trece gate-urile.

## Consequences

- M2 (deterministic resolver) pornește de la engine migrat, nu de la zero.
- M8 (research import) refolosește batch-urile existente.
- Apare un strat nou obligatoriu: Intent Atlas + Intent Resolver (discovery), peste engine.
- Reconcilierea de contract (namespaced fields, conflict model, no `flag_conflict` în lista v2.1 de efecte) se tratează explicit la migrarea engine-ului.
- Trasabilitatea (requirement/story/ADR IDs) leagă activele migrate de planul v2.1.

## Revisit triggers

- migrarea engine-ului dezvăluie o divergență de contract ireconciliabilă;
- costul de întreținere a două structuri în paralel depășește beneficiul;
- product owner decide alt scope pentru R1.
