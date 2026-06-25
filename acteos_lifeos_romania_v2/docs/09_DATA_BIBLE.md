# 09 — Data Bible

## 1. Principii

- separă definiția canonică de instanța utilizatorului;
- păstrează lineage pentru orice rezultat administrativ;
- nu stoca text liber dacă o valoare tipată este suficientă;
- evită duplicarea PII în audit și analytics;
- toate datele temporale au timezone sau sunt UTC;
- rulesets publicate sunt imutabile;
- istoricul traseului este reproductibil, dar documentele pot fi șterse independent.

## 2. Clasificarea datelor

| Clasă | Exemple | Regim |
|---|---|---|
| Public | event types, rules aprobate, canale oficiale | cacheabil, versionat |
| Intern | draft rules, gap registry, review notes | RBAC, audit |
| Personal | journey progress, preferences | RLS, retenție |
| Sensibil | CNP, adresă exactă, relații familiale | minimizare, criptare |
| Document | imagini/PDF-uri, extracted fields | local implicit, acces strict |
| Security | tokens, audit admin, incident data | segregare, retenție controlată |

## 3. Identificatori

- entități operaționale: UUIDv7;
- IDs canonice: `ro.life.moved_home`, `ro.doc.identity_card`;
- rule revision: UUID + `canonical_rule_id` stabil;
- ruleset: `scope@YYYY.MM.DD.revision` plus UUID intern;
- source claim: ID stabil doar pentru aceeași afirmație; schimbarea semantică creează claim nou;
- step semantic key: stabil între rulesets dacă acțiunea este aceeași.

## 4. Entități publice

### `life_event_types`

Taxonomie, sinonime, categorie, release wave, facts contract și status.

### `fact_definitions`

Tip, label, reason, sensitivity, validation și options. Nu conține răspunsuri.

### `jurisdictions`

Arbore EU/RO/județ/UAT/instituție, coduri oficiale, perioadă și sursă.

### `sources`

URL canonic, publisher, authority level, territory, source type și crawler policy.

### `source_snapshots`

Conținut capturat, hash, timestamp, HTTP metadata, storage pointer și diff status.

### `source_claims`

Afirmație atomică, excerpt, locator, effective interval, confidence, approval și snapshot.

### `rules` / `rule_revisions`

Condiție AST, efecte, severity, claims, jurisdiction, dates și review metadata.

### `rule_sets`

Colecție imutabilă publicată, manifest hash și engine compatibility.

### `official_channels`

Tip, URL/adresă/contact, jurisdiction, validitate, integration status și claims.

## 5. Entități utilizator

### `households`

Container opțional. Nu presupune că toți membrii au cont.

### `household_members`

Alias local, relație, date strict necesare. CNP nu este cheie și nu este obligatoriu.

### `assets`

Vehicul, proprietate, firmă. Atributele sunt JSON tipat prin schema de asset type.

### `cases`

Eveniment început de utilizator, subiect, reference date, jurisdiction și lifecycle.

### `fact_values`

Valori tipate și provenance: user_entered, derived, document_extracted, registry_verified.

### `journeys`

Materializare legată de ruleset, facts hash și resolution trace.

### `journey_steps` / `journey_requirements`

Snapshot-uri pentru reproducere; progresul utilizatorului este separat de template.

### `documents`

Metadata, ownership, storage mode, local reference, cloud object pointer opțional, retention și encryption envelope metadata.

### `document_readiness_runs`

Verificări individuale, rezultat, engine/model version, extracted fields redactate și limitări.

### `notifications`

Planificare, tip, payload fără PII, status și delivery provider id.

### `feedback_reports`

Respingere, cerință diferită, sursă neclară sau canal invalid; poate atașa dovadă doar cu consimțământ.

## 6. Stări și invariants

### Ruleset

`draft → validating → approved → active → superseded | withdrawn`

Invariant: un scope/event/date nu are două rulesets active decât dacă partition key diferă explicit.

### Claim

`draft → in_review → approved → active → stale → hard_expired | withdrawn | superseded`

Invariant: `critical` rule effect nu referă claim care nu este active/fresh conform politicii.

### Case/Journey

Case-ul poate exista fără Journey până când facts sunt suficiente. Journey-ul păstrează ruleset-ul folosit chiar după publicarea unei versiuni noi; recalcularea creează revizie nouă.

## 7. Date sensibile

- numele complet este evitat în rules engine; se folosește role/subject id;
- CNP este colectat numai pentru prefill explicit și preferabil procesat local;
- adresa se normalizează în componente, dar coordonatele nu sunt stocate implicit;
- extracted fields pot fi păstrate numai dacă utilizatorul salvează documentul;
- textul OCR brut are retenție mai scurtă decât documentul sau este eliminat imediat după checks;
- thumbnails nu sunt generate în cloud pentru local-only.

## 8. Retenție

Politica machine-readable: `contracts/retention_policy.yaml`.

Default-uri:

- anonymous server case: 24 h dacă nu este sincronizat;
- account case: până la ștergere sau 24 luni de inactivitate, cu notificare;
- cloud processing temporary object: maximum 24 h;
- human review object: maximum 30 zile sau până la închiderea review-ului;
- audit admin: conform politicii interne, minimum necesar investigației;
- source snapshots: termen lung, fiind evidență publică și lineage;
- analytics: agregate, fără raw PII.

## 9. Ștergere

Ștergerea documentului elimină obiectul, thumbnails, OCR raw și cheile asociate. Auditul păstrează doar evenimentul „document deleted”, fără conținut. Ștergerea contului anonimizează feedback-ul unde poate fi păstrat legitim și elimină profilul/journeys conform politicii.

## 10. Migrații

- Alembic este sursa pentru schema backend;
- nicio modificare destructivă într-un singur release;
- expand → migrate → contract;
- indexes mari se creează concurrently în producție;
- fiecare migration are risk note și verificare post-deploy;
- ruleset schemas au migration tool separat și backward compatibility explicită.

## 11. Query patterns și indexes

Critice:

- rules active după event + jurisdiction + date;
- journey by user/installation + status;
- source claims due for review;
- jobs ready by status/run_at;
- feedback open by impacted rule/event;
- audit by actor/entity/time;
- notifications by due_at/status.

SQL-ul de referință se află în `db/`.

## 12. Data lineage

Orice `journey_requirement` critic păstrează:

`rule_revision_id → rule_claim_link → source_claim_id → source_snapshot_id → source URL/hash`.

Această legătură nu se rupe când sursa se schimbă; o revizie nouă creează lineage nou.

## 13. Analytics model

Analytics folosește pseudonymous installation/account id, event taxonomy id, state codes și durations. Nu include:

- free-text input;
- fact values sensibile;
- document names sau OCR;
- adrese;
- phone/email;
- source excerpts accesate de utilizator asociate nominal.
