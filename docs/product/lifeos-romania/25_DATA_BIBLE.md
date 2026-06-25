# 25 — Data Bible (transplant din v2)

## Principii

Separă definiția canonică de instanța utilizatorului; păstrează lineage pentru orice rezultat; nu stoca text liber dacă o valoare tipată e suficientă; evită duplicarea PII în audit/analytics; date temporale cu timezone sau UTC; rulesets publicate imutabile; istoricul traseului reproductibil, dar documentele ștergibile independent.

## Clasificarea datelor

| Clasă | Exemple | Regim |
|---|---|---|
| Public | event types, reguli aprobate, canale | cacheabil, versionat |
| Intern | draft rules, gap registry, review notes | RBAC, audit |
| Personal | journey progress, preferințe | RLS, retenție |
| Sensibil | CNP, adresă exactă, relații familiale | minimizare, criptare |
| Document | imagini/PDF, câmpuri extrase | local implicit, acces strict |
| Security | tokens, audit admin, incident | segregare, retenție controlată |

## Identificatori

- entități operaționale: UUIDv7;
- IDs canonice de domeniu: `life.moved`, `identity.change_domicile` (convenția super-book; vezi `27_V2_DONOR_INTEGRATION.md` pentru maparea către `ro.life.*` din v2);
- rule revision: UUID + `canonical_rule_id` stabil;
- ruleset: `scope@YYYY.MM.DD.revision` + UUID intern;
- source claim: ID stabil doar pentru aceeași afirmație;
- step semantic key: stabil între rulesets dacă acțiunea e aceeași.

## Entități publice

`life_event_types`, `fact_definitions`, `jurisdictions`, `sources`, `source_snapshots`, `source_claims`, `rules`/`rule_revisions`, `rule_sets`, `official_channels`.

## Entități utilizator

`households`, `household_members` (CNP nu e cheie și nu e obligatoriu), `assets`, `cases`, `fact_values` (provenance: user_entered/derived/document_extracted/registry_verified), `journeys`, `journey_steps`/`journey_requirements`, `documents`, `document_readiness_runs`, `notifications`, `feedback_reports`.

## Stări și invariants

- **Ruleset:** `draft → validating → approved → active → superseded | withdrawn`. Un scope/event/date nu are două rulesets active simultan.
- **Claim:** `draft → in_review → approved → active → stale → hard_expired | withdrawn | superseded`. Un efect critic nu referă claim non-activ/non-fresh.
- **Case/Journey:** case poate exista fără journey până când faptele sunt suficiente; journey păstrează ruleset-ul folosit.

## Date sensibile, retenție, ștergere

Numele complet e evitat în engine (rol/subject id); CNP doar pentru prefill explicit, preferabil local; adresa normalizată în componente, fără coordonate implicite; OCR brut cu retenție scurtă. Retenție machine-readable în `config/retention_policy.yaml`. Ștergerea documentului elimină obiect, thumbnails, OCR brut și cheile; auditul păstrează doar evenimentul „document deleted".

## Lineage

Orice cerință critică păstrează: `rule_revision_id → rule_claim_link → source_claim_id → source_snapshot_id → source URL/hash`. Legarea nu se rupe când sursa se schimbă; o revizie nouă creează lineage nou.

## Migrații

Alembic; expand → migrate → contract; nimic destructiv într-un singur release; indexes mari `CONCURRENTLY`; fiecare migrație are risk note.
