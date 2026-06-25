---
name: acteos-intent-authoring
description: Author or change canonical intents, aliases, category placement, intent-event links, discovery ranking fixtures and publication status.
---

# ActeOS Intent Authoring

Use this skill whenever a task changes `intent_type`, aliases, category discovery, query ranking, disambiguation or intent-event links.

## Mandatory sequence

1. Read `docs/03A_DISCOVERY_INTENT_ATLAS.md` and `contracts/intent_ranking.yaml`.
2. Decide whether the request is a new canonical intent, an alias, a bundle, or a journey/rule change.
3. Never create a new intent only for a spelling variant or synonym.
4. Add/update `data/intent_taxonomy.yaml` and mapping files.
5. Add positive, ambiguous and negative fixtures.
6. Run schema and taxonomy validation.
7. Confirm no administrative obligation was embedded in aliases/outcome copy.
8. Update catalog version and changelog.
9. For a published intent, ensure a usable Journey/ruleset exists or availability remains `not_available`.

## Prohibited

- AI-generated IDs not present in the catalog;
- paid ranking boosts;
- aliases containing unverified deadlines, fees or required acts;
- raw sensitive queries in analytics;
- automatic case creation without user confirmation.

## Evidence to attach

- taxonomy diff;
- fixture results;
- duplicate/alias collision report;
- API/schema validation;
- accessibility copy review for public labels.
