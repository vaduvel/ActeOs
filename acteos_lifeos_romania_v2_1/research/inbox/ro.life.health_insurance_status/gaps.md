# Research gaps — B06_HEALTH_INSURANCE_STATUS

| id | subiect | status | de confirmat | sursă țintă | comportament motor |
|---|---|---|---|---|---|
| HIS-G1 | Cuantum D212 2026 | needs_confirmation | baza, suma, termenele și formularul curent | ANAF / Codul fiscal consolidat | Arată doar perioada de 12 luni verificată; nu reutiliza exemplul 2022. |
| HIS-G2 | Corectarea rezultatului negativ | needs_confirmation | documentele și canalul pentru fiecare categorie | CAS teritorială / Ordinul 1549/2018 consolidat | Cere categoria înainte de listă. |
| HIS-G3 | Condițiile studentului 18–26 | needs_confirmation | pragurile de venit și excepțiile curente | Legea 95/2006 + Codul fiscal consolidat | Păstrează CI/document student; confirmă eligibilitatea. |
| HIS-G4 | Disponibilitatea/SLA SIUI | needs_confirmation | status tehnic și fallback curent | CNAS SIUI | Nu interpreta indisponibilitatea ca neasigurare. |

## Politică aplicată

- Nicio taxă, listă de documente, adresă sau durată neconfirmată nu este transformată în efect automat.
- `needs_confirmation` blochează doar afirmația critică nesusținută; pașii naționali verificați pot rămâne vizibili.
- `verified_with_local_gap` păstrează regula națională și cere verificarea canalului local din afara pilotului.
