# 08 — Architecture Blueprint

## 1. Decizia principală

R1 folosește un **modular monolith**, nu microservicii. Există patru procese/deployables cu limite clare:

1. aplicația mobilă;
2. portalul admin;
3. API-ul FastAPI;
4. workerul pentru ingestie, freshness, notificări și jobs.

API și worker împart pachetele de domeniu și baza PostgreSQL, dar rulează separat. Rule engine este bibliotecă pură, fără dependențe de framework.

## 2. Stack de referință la 25 iunie 2026

- Mobile: Expo SDK 56, React Native 0.85, React 19.2, TypeScript, Expo Router;
- Admin: Next.js 16.2, TypeScript;
- API: Python 3.13, FastAPI 0.138.x, Pydantic v2, SQLAlchemy 2;
- DB: PostgreSQL 18.x;
- API contract: OpenAPI 3.1.1;
- local mobile data: Expo SQLite + SecureStore;
- object storage cloud: adapter, referință Supabase Storage EU;
- deployment reference: mobile EAS, admin Vercel, API/worker container EU, database Supabase EU.

Versiunile exacte sunt blocate în lockfiles. Upgrade-ul este schimbare controlată.

## 3. Monorepo

```text
apps/
  mobile/
  admin/
services/
  api/
  worker/
packages/
  contracts/
  design-tokens/
  mobile-domain/
  generated-api-client/
python/
  acteos_domain/
  acteos_rule_engine/
  acteos_application/
  acteos_adapters/
  acteos_tests/
infra/
research/
docs/
```

## 4. Module backend

- `identity_access`: auth, sessions, RBAC;
- `catalog`: intents, aliases, categories, life-event contexts, facts și jurisdicții;
- `cases`: instanțe pentru intenturi confirmate, contexte de eveniment opționale și answers;
- `rules`: rulesets, evaluator, trace;
- `journeys`: materialization și progress;
- `documents`: metadata și readiness, fără presupunere de cloud;
- `channels`: registry și linkuri oficiale;
- `content_ops`: sources, snapshots, claims, review, publish;
- `notifications`: deadlines, expiry, rule changes;
- `feedback`: rejection reports și correction loop;
- `audit`: security/admin audit;
- `jobs`: queue PostgreSQL și workers.

Modulele comunică prin interfețe/application services, nu prin acces arbitrar la tabelele altui modul.

## 4A. Modul Discovery

`discovery` conține normalizerul român, alias index, ranking, availability filters și semantic adapter boundary. Produce numai `intent_type_id` candidate și trace. Nu importă rule engine și nu citește documente personale. Indexul local mobil este derivat din catalogul publicat.

## 5. Flux de rezolvare

```text
Mobile -> API /cases -> facts -> /resolve
                         |
                         v
                 Rule Engine (pure)
                         |
             active immutable ruleset
                         |
                         v
              Journey + ResolutionTrace
                         |
                  local mobile cache
```

Nicio sursă externă nu este accesată sincron pentru a decide ruta. Conectorii pot actualiza registry-ul înainte, prin content pipeline.

## 6. Flux de conținut

```text
Official source -> snapshot/hash -> AI extraction candidate
 -> curator edits -> reviewer approves -> rule simulation
 -> publish immutable ruleset -> journeys affected queued for review
```

AI extraction este offline/asynchronous și nu poate publica.

## 7. Local-first mobile

Pe dispozitiv:

- event drafts;
- facts și journey cache;
- progress;
- document metadata;
- fișierele documentelor, implicit;
- outbox pentru sincronizare;
- chei și tokenuri în secure storage.

Serverul primește doar datele necesare rezolvării. Pentru modul anonim se poate folosi un `installation_id` rotabil și cazurile pot rămâne exclusiv locale dacă ruleset-urile relevante sunt sincronizate.

## 8. Cloud document options

- `LOCAL_ONLY` — implicit;
- `ENCRYPTED_BACKUP` — client-side envelope encryption, serverul nu poate analiza conținutul;
- `CLOUD_PROCESSING_CONSENTED` — upload temporar pentru procesare explicită, retenție scurtă;
- `HUMAN_REVIEW_CONSENTED` — flux separat, audit și acces limitat.

Aceste moduri nu se combină implicit.

## 9. Database și tenancy

Un singur cluster PostgreSQL R1, separate schemas logical: `app`, `content`, `audit`. RLS protejează datele utilizatorului; operațiunile admin folosesc service role izolat. Rulesets și source claims sunt global/public read prin API, nu direct DB din mobile.

## 10. Queue fără infrastructură prematură

R1 folosește tabel de jobs cu `FOR UPDATE SKIP LOCKED`, retry/backoff și dead-letter state. Redis/Kafka intră doar dacă volumele sau latența o cer și prin ADR.

## 11. Integrații

Fiecare integrare are adapter și status:

- `SOURCE_ONLY` — folosim ca dovadă;
- `DEEP_LINK` — conducem utilizatorul;
- `ENROLMENT_REQUIRED` — integrarea cere proces formal;
- `SANDBOX`;
- `ACTIVE`;
- `SUSPENDED`.

Nu marcăm o integrare `ACTIVE` doar pentru că există documentație publică.

## 12. Resilience

- timeout scurt și bounded retries;
- circuit breaker pentru conectori;
- idempotency keys pentru mutații;
- outbox pattern pentru notificări și audit;
- snapshot ruleset local în API/worker;
- graceful degradation: journey existent rămâne disponibil;
- feature flags pentru clasificare AI, cloud vault și parteneri;
- kill switch pentru sursă, regulă, event family și integrare.

## 13. Security boundaries

- mobile este client neîncrezător;
- admin necesită MFA și device/session controls;
- rule publish este operațiune cu approval distinct;
- object storage nu este public;
- signed URLs au durată scurtă și scope;
- PII este exclusă din telemetry;
- secret manager, nu `.env` în producție;
- dependencies scanate și SBOM la release.

## 14. Scalare

R1 optimizează corectitudinea și operabilitatea. Scalarea verticală și read replicas sunt suficiente inițial. Se separă serviciile numai când există:

- profil de scalare incompatibil;
- boundary de securitate obligatoriu;
- echipă/ciclu de release distinct;
- indisponibilitate cauzată demonstrabil de coupling.

## 15. Deployment topology de referință

- `admin`: Vercel EU, fără acces direct la service role în browser;
- `api`: container regional EU;
- `worker`: container regional EU, autoscaling limitat;
- `db/storage/auth`: Supabase project EU;
- `observability`: vendor EU-compatible sau self-hosted, cu redaction;
- `mobile`: EAS builds, channels dev/staging/production.

Acestea sunt adapters și pot fi înlocuite fără schimbarea domeniului.
