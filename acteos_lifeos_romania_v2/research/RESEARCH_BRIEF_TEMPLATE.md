# Deep Research Brief Template

## Role

Researcher de politici publice și analist de date oficiale. Livrează date atomice și trasabile, nu recomandări generale și nu cod.

## Product context

ActeOS transformă evenimente în reguli deterministe. Nicio informație critică nu poate fi inventată sau preluată din Tier 4 ca adevăr.

## Scope

- `event_type_id`:
- territory:
- reference date/year:
- personas/variants:
- exclusions:

## Source hierarchy

Tier 1 normative → Tier 2 official operational → Tier 3 documented official confirmation → Tier 4 signal only.

## Required output

1. executive summary;
2. jurisdiction tree and official identifiers;
3. facts/questions;
4. eligibility gates;
5. ordered steps and dependencies;
6. requirements with forms/validity/readiness;
7. deadlines/calendars;
8. official channels and integration status;
9. atomic source claims;
10. source registry;
11. conflict matrix;
12. gap registry;
13. freshness recommendations;
14. JSON conforming to contracts;
15. snapshot SHA-256 and package checksums.

## Atomic claim fields

`id, source_id, snapshot_id, statement, URL, publisher, authority_level, legal_rank, territory, competence_scope, exact_excerpt, locator, published_at, accessed_at, effective_from/to, confidence, freshness_class, review_due_at, hard_expiry_at, contradictions`.

## Non-negotiables

- exact quotes for critical assertions;
- no invented deadlines/fees/forms/channels;
- conflicts listed, not silently resolved;
- local rules require local source;
- pending publication marked explicitly;
- one claim per independently changeable assertion;
- no production status; research output enters inbox.
