# Research gaps — B13_TAX_REFUND_REQUEST

| # | Gap | Status | De confirmat | Sursa țintă |
|---|---|---|---|---|
| 1 | Canalul ANAF pentru fiecare categorie de sumă | `needs_confirmation` | formular, SPV, registratură și organ competent | ANAF — proceduri și formulare curente |
| 2 | Termenul de soluționare | `needs_confirmation` | articolul aplicabil și punctul de pornire | Codul de procedură fiscală consolidat |
| 3 | Prescripția dreptului de a cere restituirea | `needs_confirmation` | durata și evenimentul de la care curge | Codul de procedură fiscală consolidat |
| 4 | Ordinea compensării cu obligații restante | `needs_confirmation` | creanțele eligibile și ordinea legală | Codul de procedură fiscală consolidat |
| 5 | Documentele cererii de restituire Timișoara | `needs_confirmation` | lista completă și datele bancare | Atlas / DFMT Timișoara |
| 6 | Procedura altor UAT | `verified_with_local_gap` | formular, documente, canal și termen local | site-ul UAT competent |

## Politica truth-guard

Doar redirecționarea către Atlas și dovada cerută pentru compensarea Timișoara produc efecte ferme. Restul rămâne blocat ori cere confirmare.

## Gate de promovare

Nicio regulă critică bazată pe un claim `needs_confirmation`, `conflicting`, `stale`, `expired` sau fără locator oficial nu poate deveni `active`. Promovarea cere snapshot, hash, validare de schemă, golden fixtures verzi și reviewer independent.
