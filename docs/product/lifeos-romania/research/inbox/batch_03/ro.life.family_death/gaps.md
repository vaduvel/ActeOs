# Research gaps — B03_FAMILY_DEATH

| # | Gap | Status | De confirmat | Sursa țintă |
|---|---|---|---|---|
| 1 | Cuantumul ajutorului de deces 2026 | `needs_confirmation` | valoarea curentă pentru fiecare categorie | CNPP + legea bugetului asigurărilor sociale 2026 |
| 2 | Dovada exactă pentru membrul de familie neasigurat | `verified_with_local_gap` | documentele și persoana de la care derivă dreptul | CNPP / casa teritorială de pensii |
| 3 | Canalul local în afara Timișoarei | `verified_with_local_gap` | programare și serviciu competent | UAT/SPCLEP competent |
| 4 | Ajutoare locale de înmormântare | `not_started` | existență, condiții și cuantum | DAS Timișoara / UAT competent |
| 5 | Contracte, conturi și obligații private ale persoanei decedate | `out_of_scope` | procedura fiecărei entități | canalele oficiale ale furnizorilor |

## Politica truth-guard

Regulile de stare civilă și condiția dovezii cheltuielilor sunt oficial ancorate. Cuantumul ajutorului și ajutoarele locale nu sunt completate fără actul 2026.

## Gate de promovare

Nicio regulă critică bazată pe un claim `needs_confirmation`, `conflicting`, `stale` sau fără locator oficial nu poate deveni `active`. Promovarea cere snapshot, hash, validare de schemă, golden fixtures verzi și reviewer independent.
