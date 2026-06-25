# Research gaps — ro.life.choose_family_doctor

| id | Gap | Status | Ce trebuie confirmat | Sursa țintă | Impact runtime |
|---|---|---|---|---|---|
| `G-CFD-01` | Capacitatea cabinetului | `verified_with_local_gap` | acceptă sau nu pacienți noi în ziua solicitării | cabinetul ales | confirmare obligatorie |
| `G-CFD-02` | Lista exactă CJAS Timiș | `verified_with_local_gap` | linkul operațional și actualizarea furnizorilor | CJAS Timiș | căutare locală cu prospețime |
| `G-CFD-03` | Modelul cererii Anexa 2A | `needs_confirmation` | URL direct și versiune completabilă | CNAS / CJAS | se furnizează numai după snapshot |
| `G-CFD-04` | Înscrierea persoanelor fără CNP sau în regim special | `needs_confirmation` | documentele și casa competentă | CNAS | review manual |

## Regula de promovare

Un claim `needs_confirmation`, `conflicting`, `expired` sau fără snapshot aprobat nu poate susține o regulă critică `active`. Promovarea cere sursă oficială accesibilă, locator și citat verificate, reviewer independent și toate golden fixtures verzi.
