# Definition of Done — LifeOS România

O fază/un livrabil este „gata" doar dacă:

- Cod tipat, fără TODO pe căi critice.
- Teste verzi: contracte, unit motor, unit orchestrator, golden hashes, negative, integrare API.
- Migrări DB rulabile și reversibile.
- Determinism dovedit: același input canonic ⇒ același `route_hash`/`event_plan_hash`.
- Zero reguli critice de producție fără `source_claim_ids`.
- `demo_mode` absent din căile de producție (doar fixture de test).
- Trasabilitate înapoi la super-book (`23_TRACEABILITY_MATRIX.csv`) și la surse.
- Containerizat și pornit prin `docker-compose`/Makefile; healthcheck verde.
- Accesibilitate verificată pe ecranele cheie (font scaling, limbaj simplu).
