# Research gaps — B13_TAX_RETURN_INDIVIDUAL

| # | Gap | Status | De confirmat | Sursa țintă |
|---|---|---|---|---|
| 1 | Consecințele depunerii D212 după 25 mai 2026 | `needs_confirmation` | sancțiuni, dobânzi și procedura de conformare pentru cazul concret | Codul de procedură fiscală + comunicare ANAF |
| 2 | Calculul impozitului, CAS și CASS | `needs_confirmation` | baza, pragurile și cumulul veniturilor | Codul fiscal consolidat + instrucțiunile D212 |
| 3 | Bonificația de 3% și condițiile ei | `needs_confirmation` | eligibilitate, termen 15 aprilie 2026 și aplicarea efectivă | actul normativ și ghidul ANAF 2026 |
| 4 | Corectarea după anularea rezervei verificării ulterioare | `needs_confirmation` | temeiul art. 105 alin. (6) aplicabil situației | Codul de procedură fiscală + instrucțiunile D212 |
| 5 | Ani fiscali diferiți de 2025 | `needs_confirmation` | formular, termen și versiune aplicabilă | arhiva oficială ANAF |

## Politica truth-guard

Motorul poate indica formularul și termenul publicat pentru 2025, dar nu produce calcule fiscale sau consecințe de întârziere fără claims normative distincte.

## Gate de promovare

Nicio regulă critică bazată pe un claim `needs_confirmation`, `conflicting`, `stale`, `expired` sau fără locator oficial nu poate deveni `active`. Promovarea cere snapshot, hash, validare de schemă, golden fixtures verzi și reviewer independent.
