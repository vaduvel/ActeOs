# Arhitectura tehnică

## 1. Principii

- Android nativ, offline-first pentru datele deja descărcate.
- Backend modular monolith în R1, cu limite clare; evităm microservicii premature.
- Worker separat pentru ingestie și jobs lungi.
- Motor determinist ca pachet pur, fără I/O în evaluare.
- Reguli imutabile și publicare atomică.
- Documentele rămân local implicit.
- Integrările sunt capabilități feature-gated, nu promisiuni în UI.
- Provider-neutral în domeniu; adaptoare pentru infrastructură.

## 2. Structura monorepo

```text
/
├── AGENTS.md
├── README.md
├── IMPLEMENTATION_STATUS.md
├── Makefile
├── docker-compose.yml
├── apps/
│   ├── android/
│   │   ├── app/
│   │   ├── core-model/
│   │   ├── core-network/
│   │   ├── core-database/
│   │   ├── core-designsystem/
│   │   ├── core-security/
│   │   ├── feature-home/
│   │   ├── feature-journey/
│   │   ├── feature-dossier/
│   │   ├── feature-document-scan/
│   │   ├── feature-sources/
│   │   └── feature-settings/
│   └── curator-web/
├── services/
│   ├── api/
│   └── worker/
├── packages/
│   ├── rule-engine/
│   ├── contracts/
│   ├── source-ingestion/
│   └── observability/
├── data/
│   ├── source-registry/
│   ├── verified-rules/
│   └── test-fixtures/
├── infra/
│   ├── docker/
│   ├── migrations/
│   └── deployment/
├── docs/
│   ├── adr/
│   ├── runbooks/
│   └── threat-model/
└── .github/workflows/
```

## 3. Stack baseline verificat la data workbookului

### Android

- Android Gradle Plugin 9.2.x, patch stabil curent;
- Kotlin 2.4.0;
- JDK 17;
- Jetpack Compose BOM stabil compatibil, blocat în `libs.versions.toml`;
- Navigation Compose;
- Hilt sau DI manuală pe interfețe — alegerea se documentează în ADR;
- Room;
- WorkManager;
- Retrofit/OkHttp + kotlinx.serialization;
- CameraX + ML Kit document scanner/text recognition;
- DataStore;
- Android Keystore pentru chei;
- minSdk 26.

Nu se folosesc dependency versions alpha/beta pentru componente critice fără ADR.

### Backend

- Python 3.13;
- FastAPI 0.138.x;
- Pydantic v2;
- SQLAlchemy 2.x async;
- Alembic;
- PostgreSQL 17;
- httpx;
- structlog;
- OpenTelemetry;
- pytest + hypothesis;
- `uv` pentru lockfile și reproducibilitate.

### Portal curator

- Next.js 16.2.x patch stabil;
- React 19.2.x patch securizat;
- TypeScript strict;
- server components numai unde aduc valoare;
- client-side forms cu validare Zod;
- Playwright pentru E2E;
- componente accesibile și design tokens comune.

### Storage și jobs

- PostgreSQL pentru metadata și queue R1 (`FOR UPDATE SKIP LOCKED`);
- storage S3-compatibil pentru snapshots și uploaduri opt-in;
- MinIO local;
- Redis este opțional, nu dependență inițială.

## 4. Componente backend

### API

- auth/session;
- catalog intenții;
- jurisdiction registry;
- route resolver;
- dossier metadata;
- source/provenance read API;
- feedback;
- admin/curation;
- signed rule bundle distribution.

### Worker

- scheduler;
- fetch adapters;
- parser/normalizer;
- diff engine;
- AI extraction adapter;
- schema validator;
- notification jobs;
- staleness monitor;
- cleanup/retention.

### Rule engine package

Pur Python, fără FastAPI/SQLAlchemy. Primește obiecte validate și returnează obiecte. Testele rulează fără DB.

## 5. Android architecture

- single activity + Compose;
- UDF/MVI light: `UiState`, `UiAction`, `UiEffect`;
- domain use cases;
- repository interfaces;
- Room cache pentru intents, bundles, routes și metadata documente;
- fișiere sensibile în internal storage criptat;
- document image bytes nu intră în analytics/logs;
- WorkManager pentru refresh și reminders;
- network boundary cu DTO separat de domain model;
- route bundle signature/hash verificat înainte de activare.

## 6. Portal curator

Pagini:

- dashboard;
- sources;
- source snapshots și diff;
- extraction drafts;
- claims review;
- rules editor cu predicate builder, nu text liber;
- impact analysis;
- publish/rollback;
- conflicts;
- feedback incidents;
- stale rules;
- audit log;
- users/roles.

## 7. Ingestion AI

LLM-ul este adaptor schimbabil. Contract:

```json
{
  "source_snapshot_id": "uuid",
  "claims": [
    {
      "statement": "...",
      "source_locator": {"page": 2, "start": 120, "end": 264},
      "proposed_type": "required_document",
      "confidence": 0.82
    }
  ],
  "proposed_rule_patch": {},
  "warnings": []
}
```

Outputul este draft, nu producție. Promptul interzice completarea golurilor. Modelul nu primește documente de utilizator.

## 8. Autentificare

### Cetățean

- anonymous device session implicit;
- cont opțional prin magic link/OIDC provider configurabil;
- ROeID numai după acord formal și adaptor dedicat;
- document upload/sync separat de simpla autentificare.

### Curator

- OIDC enterprise;
- MFA obligatoriu;
- RBAC și audit;
- sesiuni scurte și reautentificare pentru publish/rollback.

## 9. Caching

- bundles publicate: cache lung, invalidare prin version/hash;
- source snapshots: imutabile;
- route outputs: cache local keyed by bundle+facts+reference_date;
- informațiile volatile au TTL propriu;
- clasa A stale nu este ascunsă sub cache.

## 10. Observabilitate

- trace ID de la client la worker;
- metrics: route latency, bundle load, fetch errors, stale count, review SLA, conflict count;
- logs structurate cu redacție;
- error reporting fără raw user facts;
- audit events separat de logs operaționale;
- alerte pentru source critical unreachable, publish failure și route resolver invariant breach.

## 11. Deployment de referință

- Android: Play Console internal → closed → production;
- curator web: Vercel EU sau container echivalent;
- API și worker: container host cu long-running process în regiune UE;
- Postgres/storage: regiune UE;
- CDN numai pentru assets publice și bundles semnate;
- secrets în secret manager;
- staging separat de production, cu date distincte.

FastAPI nu se pune într-un runtime exclusiv serverless dacă workerul și conexiunile persistente nu pot fi operate corect.

## 12. ADR-uri obligatorii

- ADR-001 deterministic rule engine;
- ADR-002 Android-native first;
- ADR-003 local-first documents;
- ADR-004 immutable rule versions;
- ADR-005 human approval gate;
- ADR-006 PostgreSQL job queue in R1;
- ADR-007 deep-link before formal integration;
- ADR-008 deployment provider choice;
- ADR-009 authentication provider;
- ADR-010 analytics provider/no-provider.
