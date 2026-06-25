# 08 — Specificația aprofundată a motorului (transplant din v2)

> Această specificație extinde `05_RULE_ENGINE_SPEC.md`. Part A (motorul determinist) și Part B (orchestratorul de eveniment cu graf `depends_on`) rămân valabile. Aici adoptăm, ca donator din pachetul v2, modelul aprofundat de predicate, efecte, jurisdicție, temporalitate, conflict și prospețime. Implementarea rămâne `packages/rule-engine` (`wb_rule_engine`), fără I/O și fără LLM la runtime.

## 1. Contractul de intrare

```json
{
  "event_type_id": "life.moved",
  "reference_date": "2026-06-25",
  "timezone": "Europe/Bucharest",
  "jurisdiction_path": ["eu", "ro", "ro.tm", "ro.tm.timisoara"],
  "subject": { "role": "self" },
  "facts": { "new_address_occupancy": "owner", "owns_vehicle": true },
  "ruleset_version": "ro.tm.timisoara@2026.06.25.1"
}
```

Câmpurile lipsă nu se ghicesc; motorul returnează `missing_facts`.

## 2. Contractul de ieșire

Statusuri: `resolved`, `needs_facts`, `needs_confirmation`, `conflicting`, `blocked`, `no_active_ruleset`. Ieșirea conține `journey`, `missing_facts`, `warnings`, `conflicts` și `explanation` (`included_rule_ids`, `excluded_rule_ids`, `facts_hash`, `engine_version`).

## 3. Predicate DSL (AST tipat)

Condițiile sunt un AST JSON restricționat (vezi `contracts/predicate.schema.json`). Fără cod arbitrar sau text liber executabil.

- **Logici:** `all`, `any`, `not`, `const`.
- **Comparație:** `eq`, `neq`, `in`, `not_in`, `lt`, `lte`, `gt`, `gte`, `exists`, `missing`, `contains`, `matches_enum`.
- **Temporali:** `date_before`, `date_after`, `date_between`, `age_on_date_gte`, `age_on_date_lt`, `days_between_lte`, `within_window`, `deadline_relative_to`.
- **Jurisdicție:** `jurisdiction_is`, `jurisdiction_descends_from`, `institution_is`, `authority_scope_contains`.

## 4. Efectele unei reguli

`include_step`, `exclude_step`, `include_requirement`, `set_requirement_obligation`, `set_deadline`, `attach_channel`, `emit_warning`, `block`, `require_confirmation`, `trigger_child_event`, `set_freshness_state`. Efectele sunt declarative; o regulă nu poate executa I/O.

> Nota orchestratorului (Part B): graful de obligații cu `depends_on` din `05` se exprimă prin `trigger_child_event` și prin muchii explicite între noduri; `event_plan_hash` rămâne hash-ul planului agregat.

## 5. Pipeline de rezolvare

1. validează schema; 2. normalizează date/enum; 3. selectează ruleset activ (eveniment + dată + jurisdicție); 4. verifică integritatea claim-urilor și prospețimea; 5. calculează faptele cerute; 6. `needs_facts` dacă lipsesc; 7. evaluează gate-urile; 8. include/exclude; 9. construiește graful; 10. detectează cicluri/referințe inexistente; 11. sortare topologică stabilă; 12. atașează cerințe/canale/termene/claims; 13. aplică politica de conflict și prospețime; 14. materializează journey + trace; 15. calculează hash-ul.

## 6. Jurisdiction Resolver

Arbore `EU → RO → județ → UAT → instituție`. Selecție: elimină reguli inactive temporal → elimină reguli din afara teritoriului → verifică competența emitentului → aplică norma obligatorie de rang superior → aplică norma locală doar în spațiul permis → dacă rămân două efecte incompatibile, creează conflict. Override-urile se declară și se aprobă în metadata regulii. **Specific nu înseamnă automat superior.**

## 7. Temporal Engine

Intervale half-open `[effective_from, effective_to)`. Datele fără oră se evaluează în `Europe/Bucharest`. Tipuri de deadline: `fixed_instant`, `fixed_window`, `relative_business_days`, `relative_calendar_days`, `institution_schedule`, `unknown_pending_publication`. Nu convertim „zile lucrătoare" în calendaristice. Calendarul sărbătorilor e versionat separat.

## 8. Model de conflict

Conflictul conține regulile/claim-urile implicate, câmpul/efectul incompatibil, rangul și competența fiecărei surse, perioada comună, impactul (`informational`/`operational`/`critical`), acțiunea (`warn`/`needs_confirmation`/`block`) și textul pentru utilizator. Un conflict nu poate fi „rezolvat" de scorul de încredere dacă ambele surse sunt oficiale și active.

## 9. Freshness

Claim-uri: `fresh`, `stale`, `hard_expired`, `source_unavailable`, `withdrawn`/`superseded`. Politica pe clase: vezi `config/freshness_policy.yaml`. Pentru `critical`, hard expiry **blochează** efectul.

## 10. Stări

- **Journey:** `draft → active → needs_review → completed | cancelled | archived`.
- **Step:** `locked → available → in_progress → ready_to_submit → submitted → completed` (+`blocked`, `needs_confirmation`, `failed`, `skipped_not_applicable`).
- **Requirement:** `missing`, `provided`, `needs_review`, `ready`, `expired`, `rejected`, `not_applicable`.

## 11. Determinism și proprietăți testabile

Același input canonic + aceleași artefacte versionate ⇒ același hash. Interzis: ordine DB fără `ORDER BY`, timp citit intern, UUID random în hash semantic, seturi neordonate, LLM/rețea, timezone implicită.

Proprietăți: idempotență; missing facts monoton; no orphan step; journey aciclic; critical evidence (orice efect critic are claim activ); temporal boundary la `effective_to`; conflict visibility; no test leakage.

## 12. Coduri de eroare

Vezi `config/error_codes.yaml`. Relevante motorului: `RULESET_NOT_FOUND`, `RULESET_INTEGRITY_FAILED`, `MISSING_REQUIRED_FACTS`, `RULE_CLAIM_MISSING`, `CLAIM_HARD_EXPIRED`, `RULE_CONFLICT_CRITICAL`, `JOURNEY_GRAPH_CYCLE`, `JOURNEY_REFERENCE_MISSING`, `JURISDICTION_UNRESOLVED`, `TEMPORAL_WINDOW_INVALID`.
