# Strategia de testare și porțile de calitate

## 1. Principiul de bază

Produsul poate produce pagubă fără să „crape”: poate rula perfect și recomanda un document greșit. De aceea testarea are două axe independente:

1. **corectitudinea software** — cod, contracte, securitate, performanță;
2. **corectitudinea procedurală** — surse, aplicabilitate, temporalitate, jurisdicție și ramuri.

Un release trece numai dacă ambele axe sunt verzi.

## 2. Tipurile de teste

### T0 — Validare statică

- format, lint, type-check strict;
- OpenAPI lint + breaking-change check;
- SQL lint și migrații reversibile;
- JSON Schema validation pentru reguli, fixture-uri și bundle manifest;
- detecție secrete și licențe;
- link checker pentru documentația internă.

### T1 — Unit

**Rule engine:**

- fiecare operator de predicate;
- logică `all`, `any`, `not` și `unknown`;
- intervale de timp și timezone Europe/Bucharest;
- moștenire națională + regulă locală validă;
- conflict de rang/competență;
- sortare topologică stabilă;
- detectarea ciclurilor;
- canonicalizare și hash;
- freshness gates;
- alegerea bundle-ului.

**Document readiness:**

- dată expirată/neexpirată;
- câmp lipsă;
- pagină lipsă;
- imagine nelizibilă;
- semnătură: `detected`, `not_detected`, `unable_to_check`;
- document nepotrivit pentru cerință;
- fără verdict de autenticitate.

### T2 — Property-based și metamorphic

Cu Hypothesis/Kotest property testing:

- reordonarea faptelor nu schimbă `route_hash`;
- serializarea/deserializarea nu schimbă hash-ul;
- adăugarea unui fapt nereferențiat nu schimbă ruta;
- aceeași dată și același bundle produc același output;
- modificarea datei peste o limită de aplicare schimbă ruta exact unde este așteptat;
- graful publicabil este aciclic;
- orice cerință critică are cel puțin un `source_claim_id`;
- regula locală fără competență explicită nu poate suprascrie baza națională;
- orice `unknown` relevant produce întrebare sau stare de confirmare, nu trece tăcut.

### T3 — Contract

- FastAPI răspunde conform `08_API_SPEC.yaml`;
- modelele generate pentru Kotlin/TypeScript sunt compatibile;
- erorile folosesc `application/problem+json` și coduri stabile;
- toate mutațiile suportă idempotency unde contractul o cere;
- snapshot test pentru payloaduri publice, fără PII.

### T4 — Integration

- API + Postgres + worker + object storage;
- fetch local fixture → snapshot → diff → draft → review → publish;
- publicare atomică și rollback;
- journey create → facts → route → checklist → recalculate;
- rotația cheilor și decriptarea datelor;
- task retry/backoff și dead-letter;
- integrarea cu conectori externi este simulată prin servere contractuale; testele CI nu lovesc instituții publice.

### T5 — Android UI și on-device

- Compose UI tests pentru fiecare ecran E01–E16;
- proces death și restoration;
- offline mode;
- import PDF/imagine prin SAF;
- anulare permisiuni;
- font scale 200%, TalkBack, touch target;
- screenshot tests pe viewport-uri reprezentative;
- benchmark pentru OCR și baza locală;
- nicio imagine sau OCR raw în loguri ori analytics.

### T6 — Portal curator

- RBAC și separarea rolurilor;
- diff raw + semantic;
- editare structurată fără text liber executabil;
- reviewerul nu poate aproba propria schimbare critică;
- two-person rule pentru high/critical;
- impact analysis înainte de publish;
- rollback și audit.

### T7 — End-to-end

#### Grădiniță

- înscriere nouă, program prelungit, ambii părinți lucrează;
- program normal;
- reînscriere;
- părinte unic/reprezentare specială;
- criteriu special aplicabil;
- document medical solicitat prea devreme;
- etapa principală ratată → recalculare;
- informație locală lipsă → confirmare, nu blocaj fals.

#### Clasa pregătitoare

- copil care împlinește 6 ani până la 31 august;
- copil care împlinește 6 ani între 1 septembrie și 31 decembrie;
- a frecventat / nu a frecventat grădinița;
- școala de circumscripție;
- altă școală cu păstrarea opțiunii de circumscripție;
- cerere online care necesită validare conform regulii curente.

### T8 — Conținut procedural

Fiecare rule bundle are:

- golden route fixtures;
- negative fixtures;
- boundary dates;
- jurisdiction mismatch;
- missing facts;
- stale source;
- conflict source;
- provenance coverage report;
- human sign-off.

### T9 — Securitate și confidențialitate

- SAST, dependency scan, container scan, secret scan;
- DAST pe staging;
- MASVS 2.1 checklist pentru Android;
- ASVS 5.0 checklist pentru API/portal;
- authz tests pe fiecare endpoint curator;
- IDOR/BOLA, rate limit, SSRF în fetcher, path traversal, malicious PDF/image, decompression bomb;
- backup restore drill;
- export/ștergere date;
- log scrubbing tests.

### T10 — Performanță și reziliență

- 100 RPS route resolve pe bundle cald;
- p95 < 400 ms și p99 < 900 ms în profilul R1;
- cold path p95 < 1.5 s;
- workerul tolerează timeout, 429, 5xx și schimbare de content type;
- circuit breaker pentru conectori;
- API public funcționează cu conectorii externi căzuți;
- chaos test: Postgres failover, queue restart, storage timeout.

## 3. Fixture policy

- `TEST_ONLY` în nume și metadata pentru toate datele fictive.
- Nu se folosesc CNP-uri reale, acte reale sau imagini cu persoane reale în repository.
- Fixture-urile de conținut oficial pot reproduce numai fragmente scurte necesare testului, cu URL și data accesării.
- Nu se testează pe URL-uri periculoase sau documente malițioase reale în CI; se folosesc payloaduri controlate.

## 4. Coverage gates

- rule engine: 95% statements și 100% branch pe conflict/freshness/temporalitate;
- API/domain: 90% statements;
- worker/content pipeline: 85%;
- Android domain/data: 85%;
- UI: toate flows critice au test;
- rule bundle: 100% cerințe critice cu provenance și cel puțin un test pozitiv + unul negativ.

Coverage nu înlocuiește testele de proprietate și review-ul uman.

## 5. CI pipelines

### Pull request

1. changed-files scope;
2. format/lint/typecheck;
3. schema + OpenAPI validation;
4. unit/property;
5. contract/integration cu containere;
6. Android test + assembleDebug;
7. portal test + build;
8. secret/dependency/SAST;
9. generated artifacts clean check.

### Main

- toate cele de mai sus;
- migration dry-run pe copie de staging;
- image build + SBOM + signing;
- deploy staging;
- smoke + DAST light;
- canary intern.

### Production

- aprobare umană;
- backup verificat;
- migrație expand/contract;
- canary 5%;
- health/error/route-hash monitoring;
- promovare sau rollback automat.

## 6. Release blockers

Release-ul este blocat dacă:

- există regulă critică expirată expusă;
- o cerință critică nu are provenance;
- un test de golden route eșuează;
- apare un breaking API change neversionat;
- migrarea nu are strategie rollback/forward fix;
- există secret sau vulnerabilitate critică/high fără acceptare formală;
- logurile conțin PII;
- publish/rollback nu este reproductibil;
- TalkBack nu permite finalizarea traseului R1.
