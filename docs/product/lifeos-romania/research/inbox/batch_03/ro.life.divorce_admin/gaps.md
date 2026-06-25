# Research gaps — B03_DIVORCE_ADMIN

| # | Gap | Status | De confirmat | Sursa țintă |
|---|---|---|---|---|
| 1 | Taxa de divorț administrativ Timișoara în 2026 | `needs_confirmation` | cuantumul și actul local în vigoare | HCL taxe locale 2026 + pagina oficială de plată |
| 2 | Ruta notarială când există copii minori | `not_started` | condiții, documente, costuri și competență | Legea notarilor / UNNPR / notar competent |
| 3 | Ruta judiciară când nu există acord | `not_started` | instanță, taxă, cerere și documente | Codul de procedură civilă + portal.just.ro |
| 4 | Durata operațională din alt UAT | `verified_with_local_gap` | termenul de emitere și programarea locală | serviciul de stare civilă al UAT-ului |
| 5 | Actualizarea pașaportului/permisului/vehiculului după divorț | `needs_confirmation` | reguli și termene specifice | DGP + DGPCI |

## Politica truth-guard

Eligibilitatea și documentele rutei administrative sunt ancorate în sursa oficială Timișoara, iar termenul actului de identitate în OUG nr. 97/2005. Taxa arhivată nu este tratată ca taxă actuală.

## Gate de promovare

Nicio regulă critică bazată pe un claim `needs_confirmation`, `conflicting`, `stale` sau fără locator oficial nu poate deveni `active`. Promovarea cere snapshot, hash, validare de schemă, golden fixtures verzi și reviewer independent.
