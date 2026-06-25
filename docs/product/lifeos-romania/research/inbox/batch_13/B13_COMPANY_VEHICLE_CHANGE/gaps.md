# Research gaps — B13_COMPANY_VEHICLE_CHANGE

| # | Gap | Status | De confirmat | Sursa țintă |
|---|---|---|---|---|
| 1 | Termenul și documentele declarației fiscale locale pentru fiecare tip de dobândire | `needs_confirmation` | formular, termen, anexele și eventualele sancțiuni | DFMT Timișoara / Codul fiscal și normele locale |
| 2 | Lista completă pentru import UE/non-UE și final de leasing | `verified_with_local_gap` | documentele după selecția cazului | serviciul oficial Timișoara + DGPCI |
| 3 | Aplicarea certificatului fiscal în alte județe/UAT | `verified_with_local_gap` | canalul și interconectarea locală | prefectura și organul fiscal local competente |
| 4 | Taxele de certificat, plăci și înmatriculare | `needs_confirmation` | cuantumul și contul de plată curent | DGPCI/Prefectura Timiș |
| 5 | Operațiuni exclusiv online disponibile la data cererii | `needs_confirmation` | funcționalitatea curentă DGPCI/HUB | DGPCI / HUB MAI |

## Politica truth-guard

Termenul național de 90 zile și pilotul Timiș sunt separate. Nicio cerință fiscală locală din Timișoara nu este generalizată automat la alt UAT.

## Gate de promovare

Nicio regulă critică bazată pe un claim `needs_confirmation`, `conflicting`, `stale`, `expired` sau fără locator oficial nu poate deveni `active`. Promovarea cere snapshot, hash, validare de schemă, golden fixtures verzi și reviewer independent.
