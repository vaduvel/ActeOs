# Decizii de arhitectură canonice — LifeOS România (Super-Book)

ADR-001…015 din pachetul original `waze-birocratie` rămân valabile și se moștenesc integral (Android nativ, FastAPI monolith modular, PostgreSQL, reguli ca JSON canonic imutabil, fără LLM în runtime de rutare, local-first documents, cont opțional, OIDC/RBAC curatori, publicare bundle independentă, deep-link înainte de API, fail-closed pe stale critic, two-person rule, Docker-first, EU-region, fără ranking de parteneri).

ADR-016…021 (stratul de eveniment) rămân valabile: orchestrare LifeEvent deasupra procedurilor, plan determinist cu `event_plan_hash`, pilot teritorial Timiș, clasificator NL assist-only pe catalog controlat, claim pe dependențe, fapte partajate.

Deciziile de **fuziune** (vezi `MERGE_PROVENANCE.md`):

| ADR | Decizie | Raționament | Revisit trigger |
|-----|---------|-------------|-----------------|
| ADR-022 | Mobil = Android nativ Kotlin/Compose; React Native Expo respins | nu aruncăm munca nativă existentă; control fin pe accesibilitate/seniori | dacă apare nevoie cross-platform iOS prioritară |
| ADR-023 | Postură de producție; `demo_mode` doar fixture de test | regula de execuție a utilizatorului (totul real) | niciodată relaxat pentru date afișate utilizatorului |
| ADR-024 | Convenție ID canonică: `life.*` pentru evenimente, `<domain>.<action>` pentru obligații | deja cablată în seed/contracte/DB; descompunerea bogată se re-exprimă pe ea | migrare majoră de taxonomie |
| ADR-025 | Frecvență = high/medium/low; freshness = clasele A/B/C | eliminarea coliziunii de denumiri din pachetul B | — |
| ADR-026 | Un singur director canonic; pachetul GPT devine arhivă deprecată | un singur adevăr | — |

Codex creează fișiere ADR formale în `docs/adr/` la implementare.
