# 10 — API Contract Guide

Contractul normativ este `contracts/openapi.yaml`.

## 1. Convenții

- base path: `/v1`;
- JSON UTF-8;
- timestamps RFC 3339 UTC;
- date fără oră: `YYYY-MM-DD`;
- IDs UUID string sau canonical id documentat;
- enumurile sunt lowercase snake_case;
- toate mutațiile acceptă `Idempotency-Key` unde dublarea ar produce efect;
- toate răspunsurile includ `X-Request-ID`;
- `ETag`/`If-Match` pentru resurse editabile și publish;
- pagination cursor-based;
- `application/problem+json` nu este folosit; avem envelope stabil documentat.

## 2. Error envelope

```json
{
  "error": {
    "code": "MISSING_REQUIRED_FACTS",
    "message": "Mai sunt necesare informații pentru calcularea traseului.",
    "details": {"fact_ids": ["new_address_occupancy"]},
    "request_id": "...",
    "retryable": false
  }
}
```

Mesajul este sigur pentru utilizator. Detaliile tehnice rămân în logurile interne redactate.

## 3. Autentificare

- endpoint-urile de catalog pot fi publice cu rate limit;
- case/journey anonymous folosesc token de instalare cu scope restrâns;
- conturile folosesc JWT issuer configurat;
- admin folosește JWT + MFA assurance + RBAC;
- service-to-service folosește identitate workload, nu API key comun.

## 4. Versionare

- `/v1` se schimbă compatibil;
- câmpuri noi sunt opționale;
- enumuri noi necesită client tolerant și release note;
- breaking change creează `/v2` sau negotiation explicit;
- schema ruleset are versiune independentă de API.

## 5. Endpoint families

### Catalog

- `GET /life-events`
- `POST /life-events/classify`
- `GET /life-events/{event_type_id}`
- `GET /jurisdictions/search`

### Case și resolver

- `POST /cases`
- `GET /cases/{case_id}`
- `PUT /cases/{case_id}/facts`
- `POST /cases/{case_id}/resolve`

### Journey

- `GET /journeys/{journey_id}`
- `POST /journeys/{journey_id}/recalculate`
- `PUT /journeys/{journey_id}/steps/{step_id}/status`
- `PUT /journeys/{journey_id}/requirements/{requirement_id}/status`

### Documents

- `POST /documents/metadata`
- `POST /documents/{document_id}/processing-session`
- `POST /documents/{document_id}/readiness`
- `DELETE /documents/{document_id}`

### Household și active

- `POST /households`
- `POST /households/{household_id}/members`
- `POST /assets`

### Channels și notifications

- `GET /official-channels`
- `GET/PUT /notification-preferences`

### Feedback

- `POST /feedback/rejections`
- `POST /feedback/source-issue`

### Content admin

- sources, snapshots, claims, rules, simulation, conflicts, gaps, publish și withdraw.

## 6. Resolve semantics

`POST /cases/{id}/resolve` nu este long-running pentru ruleset local. Răspunde:

- `200 resolved`;
- `200 needs_facts` cu fact definitions;
- `409 conflicting` numai dacă clientul cere strict resolution; implicit conflictul poate fi reprezentat în 200 status object;
- `422` pentru input invalid;
- `503` pentru ruleset indisponibil, fără fallback inventat.

## 7. Document upload

API-ul separă metadata de bytes. Pentru local-only nu există upload. Pentru cloud processing:

1. client cere processing session;
2. server returnează signed upload URL și expiry;
3. upload direct în storage;
4. worker procesează;
5. obiectul este șters conform retention;
6. rezultatele sunt returnate cu limitări și engine version.

## 8. Concurrency

- facts update folosește `version`/`If-Match`;
- progress update este idempotent și last-write-safe;
- publish ruleset cere manifest hash și approval id;
- recalculation nu suprascrie journey vechi; creează revision și migration result.

## 9. Generated clients

OpenAPI generează client TypeScript pentru mobile/admin. Codul generat nu se editează manual. Backend tests verifică răspunsurile against schema; CI rulează breaking-change detection.
