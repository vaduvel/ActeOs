# Upgrade guide — v2.0.0 → v2.1.0

## De ce există versiunea 2.1

Research-ul de produs a clarificat modelul mental al utilizatorului: omul nu pornește de la „ce i s-a întâmplat”, ci de la ce are nevoie să rezolve. V2.1 introduce un Discovery Layer intent-first fără să schimbe motorul administrativ determinist.

## Ce rămâne neschimbat

- evidence-gated rules;
- temporal/jurisdiction resolver;
- Journey, Step și Requirement;
- source governance și content operations;
- local-first documents;
- OpenAPI-first și modular monolith;
- Event Atlas ca strat intern pentru bundle-uri și recomandări.

## Ce se adaugă

- Intent Atlas;
- dual navigation: search + categories;
- deterministic Intent Resolver;
- Romanian query normalization;
- ranking/disambiguation/no-result;
- discovery API și persistence;
- privacy-safe discovery analytics;
- Codex stories și test fixtures.

## Breaking conceptual change

`intent_type_id` devine identificatorul public obligatoriu când se creează un caz nou. `event_type_id` rămâne context opțional și compatibilitate internă. Deoarece implementarea baseline nu este încă în producție, schimbarea se aplică înainte de bootstrap, nu prin compatibilitate artificială în UI.
