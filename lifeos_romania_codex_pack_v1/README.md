# LifeOS Romania / ActeOS - Codex Execution Pack v1

Acest pachet transforma noua pozitionare a produsului intr-un set executabil pentru Codex: event-driven LifeOS, nu o lista de proceduri.

## Ce construiesti
- Mobile app React Native/Expo.
- Backend FastAPI.
- Postgres schema + rule engine determinist.
- Curator portal minimal.
- Event taxonomy + demo-safe route bundles.

## Regula de aur
Nu inventa reguli administrative reale. In demo folosesti seed-uri marcate `demo_mode: true`. Pentru productie, fiecare regula critica trebuie sa aiba `source_claim_ids` aprobate.
