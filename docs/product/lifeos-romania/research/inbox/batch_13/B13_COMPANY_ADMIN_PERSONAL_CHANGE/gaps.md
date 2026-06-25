# Research gaps — B13_COMPANY_ADMIN_PERSONAL_CHANGE

| # | Gap | Status | De confirmat | Sursa țintă |
|---|---|---|---|---|
| 1 | Lista exactă de documente pentru fiecare formă juridică și calitate | `needs_confirmation` | act constitutiv actualizat, specimen, avize și declarații aplicabile | pagina ONRC aferentă formei juridice + ORCT |
| 2 | Cuantumul tarifului de publicitate/poștal | `needs_confirmation` | nota de calcul curentă pentru cererea concretă | ONRC / ORCT |
| 3 | Consecințele depunerii după termenul general de 15 zile | `needs_confirmation` | sancțiunea sau remediul aplicabil situației | Legea nr. 265/2022 consolidată + ORCT |
| 4 | Autorizări sectoriale pentru anumite tipuri de societăți | `verified_with_local_gap` | avizul autorității de reglementare competente | autoritatea sectorială oficială |

## Politica truth-guard

Dosarul de bază, canalele și termenul general sunt ancorate în ghidurile ONRC. Motorul nu deduce forma juridică, tariful ori avizele speciale.

## Gate de promovare

Nicio regulă critică bazată pe un claim `needs_confirmation`, `conflicting`, `stale`, `expired` sau fără locator oficial nu poate deveni `active`. Promovarea cere snapshot, hash, validare de schemă, golden fixtures verzi și reviewer independent.
