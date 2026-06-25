# 10A — Discovery API Contract

## 1. Principii

- API-ul servește numai intenturi publicate.
- Căutarea este idempotentă și nu creează caz.
- `POST /v1/intents/resolve-query` nu poate returna un ID care nu există în catalogul activ.
- Pornirea cazului este operațiune separată și cere confirmarea clientului.
- Răspunsurile includ `catalog_version` și `resolver_version`.

## 2. Endpoint-uri

### `GET /v1/discovery/home`

Returnează categorii, quick actions, feature availability și versiunea catalogului. Datele personale precum cazurile active sunt compuse local sau prin endpoint-urile autentificate existente.

### `GET /v1/categories`

Filtre: locale, jurisdiction hint. Returnează numai categorii cu minimum un intent disponibil.

### `GET /v1/intents`

Filtre: `query`, `category_id`, `jurisdiction_id`, `cursor`, `limit`. Pentru query gol poate returna catalogul categoriei.

### `POST /v1/intents/resolve-query`

Request: `query`, `locale`, `jurisdiction_hint`, `category_hint`, `client_catalog_version`, `allow_semantic_fallback`.

Response: maximum trei candidați, `resolution_state`, `catalog_version`, `resolver_version`, `normalization_version`, `fallback_used`, `request_id`.

### `GET /v1/intents/{intent_type_id}`

Returnează fișa publică a intentului și availability. Nu returnează reguli administrative nepublicate.

### `POST /v1/cases`

`intent_type_id` este obligatoriu în v2.1. `event_type_id` devine context opțional de compatibilitate; `event_context_ids` poate conține bundle-ul sursă.

## 3. Error codes

- `INTENT_QUERY_TOO_SHORT`;
- `INTENT_NOT_FOUND`;
- `INTENT_AMBIGUOUS` este stare de succes în response, nu 4xx;
- `INTENT_NOT_AVAILABLE_IN_JURISDICTION`;
- `INTENT_WITHDRAWN`;
- `CATALOG_VERSION_MISMATCH`;
- `DISCOVERY_INDEX_UNAVAILABLE`;
- `SEMANTIC_FALLBACK_DISABLED`;
- `UNKNOWN_INTENT_ID_FROM_ADAPTER`.

## 4. Caching

- catalog/categories: cache public cu ETag și versiune;
- resolve-query: cache privat/ephemeral, fără query brut în CDN logs dacă infrastructura nu poate garanta redaction;
- intent detail: cache public numai pentru câmpurile publice;
- availability este variabilă după jurisdicție și intră în cache key.

## 5. Compatibility

Endpoint-urile vechi `/v1/life-events*` rămân în contract pentru compatibilitate internă, dar `classify` este deprecated. Noul client mobil nu îl folosește pentru discovery.
