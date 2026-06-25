# Research gaps — B03_NAME_CHANGE_AFTER_MARRIAGE

| # | Gap | Status | De confirmat | Sursa țintă |
|---|---|---|---|---|
| 1 | Pașaport după schimbarea numelui | `needs_confirmation` | obligația, termenul, taxa și documentele curente | Direcția Generală de Pașapoarte / hub.mai.gov.ro |
| 2 | Permis de conducere după schimbarea numelui | `needs_confirmation` | termenul și lista oficială DGPCI | dgpci.mai.gov.ro |
| 3 | Certificat de înmatriculare după schimbarea numelui | `needs_confirmation` | termenul, documentele și tariful | dgpci.mai.gov.ro + act normativ consolidat |
| 4 | Canal CIS/CI pentru alt UAT | `verified_with_local_gap` | serviciul competent și programarea locală | SPCLEP al domiciliului |
| 5 | Interacțiuni cu bănci, angajator, asigurări și contracte private | `out_of_scope` | cerințele fiecărui furnizor | canalul oficial al fiecărei entități |

## Politica truth-guard

OUG nr. 97/2005 susține schimbarea actului și termenul de 15 zile. Pașaportul, permisul și vehiculul nu primesc termen sau taxă până la cercetarea sursei oficiale specifice.

## Gate de promovare

Nicio regulă critică bazată pe un claim `needs_confirmation`, `conflicting`, `stale` sau fără locator oficial nu poate deveni `active`. Promovarea cere snapshot, hash, validare de schemă, golden fixtures verzi și reviewer independent.
