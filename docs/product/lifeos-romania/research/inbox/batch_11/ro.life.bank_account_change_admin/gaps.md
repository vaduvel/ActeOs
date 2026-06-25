# Research gaps — ro.life.bank_account_change_admin

| id | Gap | Status | Ce trebuie confirmat | Sursa țintă | Impact runtime |
|---|---|---|---|---|---|
| `G-BA-01` | Anexele formularului CNPP | `verified_with_local_gap` | documentul de cont, actul de identitate, reprezentarea | CNPP/CJP Timiș | cerințele nu devin obligatorii până la confirmare |
| `G-BA-02` | Data de efect și cutoff lunar | `needs_confirmation` | când se aplică noul cont | CJP competentă | nu se afișează termen inventat |
| `G-BA-03` | Plăți administrate de alte instituții | `needs_confirmation` | formulare și canale AJPIS/ANAF/UAT | instituția plătitoare | router, nu procedură generică |
| `G-BA-04` | Cont străin și cont terț | `needs_confirmation` | condițiile oficiale și documentele | CNPP plăți internaționale | blocare/hand-off |

## Regula de promovare

Un claim `needs_confirmation`, `conflicting`, `expired` sau fără snapshot aprobat nu poate susține o regulă critică `active`. Promovarea cere sursă oficială accesibilă, locator și citat verificate, reviewer independent și toate golden fixtures verzi.
