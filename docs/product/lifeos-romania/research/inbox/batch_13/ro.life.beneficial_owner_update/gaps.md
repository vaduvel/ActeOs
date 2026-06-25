# Research gaps — B13_BENEFICIAL_OWNER_UPDATE

| # | Gap | Status | De confirmat | Sursa țintă |
|---|---|---|---|---|
| 1 | Lista curentă a jurisdicțiilor din art. 56 alin. (1^3) | `needs_confirmation` | încadrarea exactă a fiecărei entități din lanț | listele actualizate publicate de ONRC/organismele internaționale |
| 2 | Formularul și fluxul tehnic ONRC valabile la data depunerii | `needs_confirmation` | versiunea formularului și cerințele portalului | ONRC — beneficiari reali |
| 3 | Forma exactă a reprezentării în situația concretă | `needs_confirmation` | dată certă, notar, avocat sau altă formă | Legea nr. 129/2019 art. 56 alin. (6) + ONRC |
| 4 | Aplicarea etapelor ulterioare sancțiunii | `needs_confirmation` | stadiul sancțiunii și riscul de dizolvare în dosarul concret | Legea nr. 129/2019 art. 57 + ONRC/instanță |

## Politica truth-guard

Motorul aplică 15 zile numai când triggerul este confirmat. Lista jurisdicțiilor și efectele post-sancțiune cer verificare punctuală.

## Gate de promovare

Nicio regulă critică bazată pe un claim `needs_confirmation`, `conflicting`, `stale`, `expired` sau fără locator oficial nu poate deveni `active`. Promovarea cere snapshot, hash, validare de schemă, golden fixtures verzi și reviewer independent.
