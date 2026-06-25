# Research gaps — B13_TAX_DECISION_CONTEST

| # | Gap | Status | De confirmat | Sursa țintă |
|---|---|---|---|---|
| 1 | Termenul exact al contestației | `needs_confirmation` | numărul de zile, punctul de pornire și situațiile speciale | Codul de procedură fiscală, articolul aplicabil |
| 2 | Organul de depunere și organul de soluționare | `needs_confirmation` | competența pentru ANAF și organ fiscal local | Codul de procedură fiscală + instrucțiunea din act |
| 3 | Conținutul obligatoriu al contestației | `needs_confirmation` | semnătură, obiect, motive și dovezi | Codul de procedură fiscală |
| 4 | Calea pentru actele de executare | `needs_confirmation` | contestație la executare și instanța competentă | Codul de procedură fiscală |
| 5 | Suspendarea executării | `needs_confirmation` | temei, instanță/autoritate, cauțiune și efecte | Codul de procedură fiscală + Legea contenciosului |
| 6 | Canalele operaționale ANAF și DFMT | `verified_with_local_gap` | SPV, registratură, e-mail și cerințe de semnare | procedurile oficiale ale emitentului |

## Politica truth-guard

Evenimentul rămâne deliberat conservator: clasifică și pregătește, dar blochează termenul și destinatarul până la verificare juridică punctuală.

## Gate de promovare

Nicio regulă critică bazată pe un claim `needs_confirmation`, `conflicting`, `stale`, `expired` sau fără locator oficial nu poate deveni `active`. Promovarea cere snapshot, hash, validare de schemă, golden fixtures verzi și reviewer independent.
