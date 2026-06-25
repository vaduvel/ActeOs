# Strategie de test — LifeOS România

## Niveluri

1. **Contracte.** Validare JSON Schema (`contracts/*.schema.json`) și OpenAPI (`09_API_SPEC.yaml`).
2. **Motor (unit).** Operatori predicat, logică tri-valued, canonicalizare, `route_hash` stabil.
3. **Orchestrator (unit).** Aplicabilitate tri-valued, graf de dependențe, detecție de cicluri, sortare topologică stabilă, `event_plan_hash`.
4. **Golden hashes.** Fixture-uri din `seed/r1_route_fixtures.yaml` produc rute și planuri cu hash-uri așteptate, fixe.
5. **Negative.** Fapt lipsă → `NEEDS_FACTS`; regulă critică fără claim → invalid (în afară de fixture demo marcat); ciclu → `conflicting`.
6. **Integrare API.** Flux complet interpret → session → facts → resolve → route.
7. **Impact analysis.** Înainte de publicare: compară `route_hash`/`event_plan_hash` și grafurile între bundle curent și candidat; blochează la cicluri, claim-uri pierdute sau creștere de conflicte.

## Reguli

- Niciun test nu folosește rețea la runtime.
- Fixture-urile demo sunt marcate `demo_mode: true` și nu pot ajunge în producție.
- CI rulează toate nivelurile; golden hashes se actualizează doar deliberat, cu review.
