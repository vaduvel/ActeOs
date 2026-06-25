# ActeOs — „Waze pentru birocrație"

> Un strat independent de **navigație, pregătire și verificare formală** între intenția cetățeanului și serviciul public din România. Spune-ne ce vrei să rezolvi — îți construim traseul administrativ aplicabil situației tale, îți verificăm dosarul și te conducem către canalul oficial. Când drumul se schimbă, recalculăm.

**Versiune pachet specificații:** 3.0.0 · **Statut:** spec canonică, implementare neînceput

---

## Ce este acest repo

În acest moment repo-ul conține **pachetul canonic de implementare** (specificații, contracte, arhitectură, reguli, backlog, teste și instrucțiuni de execuție), nu încă produsul construit. Pachetul se află în [`waze_birocratie_codex_pack/`](./waze_birocratie_codex_pack/) și trebuie citit în ordinea din [`README` al pachetului](./waze_birocratie_codex_pack/README.md).

Începe de la [`CODEX_START_HERE.md`](./waze_birocratie_codex_pack/CODEX_START_HERE.md).

## Formula produsului

**Intenție + context personal minim + jurisdicție + dată de referință + reguli publicate și versionate = traseu administrativ personalizat.**

Același input, aceeași jurisdicție, aceeași dată de evaluare și același bundle de reguli produc același traseu.

## Principii care nu se negociază

- **Regulile decid. AI-ul asistă.** Motorul determinist produce traseul; LLM-ul extrage drafturi, explică și clasifică, dar nu inventează obligații și nu decide la runtime.
- **Fiecare afirmație importantă are dovadă** — sursă oficială, autoritate, teritoriu, perioadă de aplicare, fragment justificativ și data verificării.
- **Incertitudinea se afișează** — o regulă neconfirmată, conflictuală sau expirată nu primește „haină verde".
- **Documentele rămân pe dispozitiv** în configurația implicită.
- **Canalul oficial este destinația** — aplicația conduce către platforma/ghișeul competent, nu creează o administrație paralelă.

## Release-uri

| Release | Verticală | Conținut |
|---|---|---|
| **R1** | Educație | Înscriere antepreșcolar/preșcolar + clasa pregătitoare (bază națională 2026-2027, override-uri locale Timiș/Timișoara). Admitere liceu implementată, ascunsă până la completarea datelor locale. |
| **R2** | Viață personală | Carte de identitate, pașaport, schimbare nume, stare civilă, beneficii copil. |
| **R3** | Proprietate / auto / fiscal | Taxe locale, certificat fiscal, înmatriculări, trasee ANAF. |

## Arhitectură (țintă)

- **Android nativ** — Kotlin + Jetpack Compose, offline-first, `minSdk 26`, OCR local (CameraX + ML Kit).
- **Backend** — Python 3.13 + FastAPI (modular monolith), Pydantic v2, SQLAlchemy async, PostgreSQL 17.
- **Worker** — ingestie surse, snapshot, diff semantic, AI extraction, monitorizare prospețime.
- **Rule engine** — pachet Python pur, determinist, fără I/O.
- **Portal curator** — Next.js + React, TypeScript strict; flux fetch → diff → draft → review → publish → rollback.
- **Storage** — PostgreSQL + S3-compatibil (MinIO local), găzduire în regiune UE (GDPR).

Detaliile complete sunt în [`07_ARCHITECTURE.md`](./waze_birocratie_codex_pack/07_ARCHITECTURE.md) și deciziile în [`20_CANONICAL_DECISIONS.md`](./waze_birocratie_codex_pack/20_CANONICAL_DECISIONS.md).

## Structura monorepo țintă

```text
/
├── apps/            # android/ + curator-web/
├── services/        # api/ + worker/
├── packages/        # rule-engine/ + contracts/ + source-ingestion/ + observability/
├── data/            # source-registry/ + verified-rules/ + test-fixtures/
├── infra/           # docker/ + migrations/ + deployment/
└── docs/            # adr/ + runbooks/ + threat-model/
```

## Status

Vezi `IMPLEMENTATION_STATUS.md` (creat la inițializarea monorepo-ului). Raport de validare al pachetului: [`VALIDATION_REPORT.md`](./waze_birocratie_codex_pack/VALIDATION_REPORT.md).
