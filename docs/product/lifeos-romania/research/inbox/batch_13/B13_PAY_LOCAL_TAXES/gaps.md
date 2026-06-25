# Research gaps — B13_PAY_LOCAL_TAXES

| # | Gap | Status | De confirmat | Sursa țintă |
|---|---|---|---|---|
| 1 | Bonificația Timișoara pentru plata anticipată în 2026 | `conflicting` | procent, beneficiari și termen | HCL Timișoara 2026 + pagina DFMT 2026 |
| 2 | Regula sumelor de până la 50 lei în 2026 | `needs_confirmation` | prag și termen aplicabil | Codul fiscal + HCL Timișoara 2026 |
| 3 | Cuantumurile și indexările 2026 | `needs_confirmation` | suma pe fiecare obiect fiscal | HCL și evidența fiscală curentă |
| 4 | Metodele, IBAN-urile și beneficiarii | `needs_confirmation` | canal online, transfer și casierie | pagina DFMT «Modalități de plată» |
| 5 | Accesoriile pentru plata după scadență | `needs_confirmation` | dobândă, penalitate și sold la zi | Codul de procedură fiscală + evidența DFMT |
| 6 | Alte UAT | `verified_with_local_gap` | termene, bonificații, conturi și platforme locale | site-ul UAT competent |

## Politica truth-guard

Scadențele de pe pagina DFMT pot ghida ruta, dar plata este blocată până când utilizatorul confirmă suma și contul din evidența fiscală curentă.

## Gate de promovare

Nicio regulă critică bazată pe un claim `needs_confirmation`, `conflicting`, `stale`, `expired` sau fără locator oficial nu poate deveni `active`. Promovarea cere snapshot, hash, validare de schemă, golden fixtures verzi și reviewer independent.
