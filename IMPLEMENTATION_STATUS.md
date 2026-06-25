# Implementation status

> Status viu al implementării. Se actualizează la finalul fiecărei faze cu: stories terminate, fișiere schimbate, comenzi + rezultate exacte, coverage, migrații, findings de securitate, limitări cunoscute, ADR-uri și poarta următoarei faze.

## Rezumat

| Fază | Subiect | Stories | Status |
|---|---|---|---|
| P0 | Fundație & reproductibilitate | WB-001…005 | 🟡 în lucru (schelet inițializat) |
| P1 | Contracte, persistență, cripto | WB-010…024 | ⬜ neopînit |
| P2 | Motor determinist de reguli | WB-030…035 | ⬜ neopînit |
| P3 | Ingestie surse & lifecycle | WB-040…045 | ⬜ neopînit |
| P4 | API & lifecycle călătorie | WB-050…055 | ⬜ neopînit |
| P5 | Portal curator | WB-060…065 | ⬜ neopînit |
| P6 | Android cetățean | WB-070…077 | ⬜ neopînit |
| P7 | Document readiness local | WB-080…085 | ⬜ neopînit |
| P8 | Conținut R1 verificat + routing | WB-090…103 | ⬜ neopînit |
| P9 | Securitate, privacy, observ., recovery | WB-110…124 | ⬜ neopînit |
| P10 | Deployment & release | WB-130…135 | ⬜ neopînit |

## P0 — Fundație & reproductibilitate

**Plan:** creează scheletul de monorepo conform `07_ARCHITECTURE.md`, root `Makefile`, `docker-compose.yml`, fundament CI și procesul ADR. Fără logică de produs.

**Realizat:**

- [x] arborele de directoare conform arhitecturii (`apps/`, `services/`, `packages/`, `data/`, `infra/`, `docs/`)
- [x] root `Makefile` cu țintele cerute (încă stub-uri)
- [x] `docker-compose.yml` (Postgres 17 + MinIO, doar dev)
- [x] fundament CI (`.github/workflows/ci.yml`)
- [x] proces ADR (`docs/adr/`)
- [x] `AGENTS.md` și `IMPLEMENTATION_STATUS.md`

**De făcut pentru a închide P0 (gate verde):**

- [ ] pin toolchains și commit lockfiles reale (Gradle/`libs.versions.toml`, `uv.lock`, `pnpm-lock.yaml`)
- [ ] `make doctor`, `make bootstrap`, `make up`, `make smoke-local` funcționale dintr-un checkout curat
- [ ] CI rulează un smoke minimal real

**Riscuri / limitări cunoscute:**

- Țintele `make` sunt momentan stub-uri care semnalează TODO; nu fac încă build real.
- Versiunile din workbook trebuie verificate împotriva disponibilității în mediu; orice deviație => ADR.
