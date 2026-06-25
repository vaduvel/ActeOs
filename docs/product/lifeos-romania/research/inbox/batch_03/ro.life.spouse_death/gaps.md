# Research gaps — B03_SPOUSE_DEATH

| # | Gap | Status | De confirmat | Sursa țintă |
|---|---|---|---|---|
| 1 | Cuantumul ajutorului de deces în 2026 | `needs_confirmation` | valoarea legală aferentă anului și statutului persoanei decedate | CNPP + legea bugetului asigurărilor sociale 2026 |
| 2 | Pragul de venit pentru pensia de urmaș | `needs_confirmation` | valoarea curentă și modul de verificare | CNPP / act normativ 2026 |
| 3 | Documentele complete pe fiecare profil de pensie de urmaș | `verified_with_local_gap` | documentele medicale, școlare și de venit aplicabile | CNPP / casa teritorială de pensii |
| 4 | Înregistrarea decesului în alt UAT | `verified_with_local_gap` | programarea și canalul local | serviciul de stare civilă competent |
| 5 | Contracte private, conturi, utilități și asigurări ale soțului decedat | `out_of_scope` | procedura fiecărei entități | canalele oficiale ale furnizorilor |

## Politica truth-guard

Termenul de 3 zile și cazurile speciale sunt ancorate în Legea nr. 119/1996. CNPP susține ajutorul și rutele de pensie, dar cuantumurile și pragurile dinamice rămân necompletate.

## Gate de promovare

Nicio regulă critică bazată pe un claim `needs_confirmation`, `conflicting`, `stale` sau fără locator oficial nu poate deveni `active`. Promovarea cere snapshot, hash, validare de schemă, golden fixtures verzi și reviewer independent.
