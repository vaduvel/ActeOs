# Research gaps — B03_MARRIAGE_PLANNING

| # | Gap | Status | De confirmat | Sursa țintă |
|---|---|---|---|---|
| 1 | Procedura exactă pentru încheiere înainte de ziua 11 | `needs_confirmation` | autoritatea aprobatoare, cererea și dovada motivului temeinic | Legea nr. 119/1996 art. 27 + Primăria Timișoara |
| 2 | Ruta completă pentru persoana de 16–17 ani | `verified_with_local_gap` | documentele și instanța competentă în situația concretă | Codul civil consolidat + serviciul local de stare civilă |
| 3 | Forma documentelor pentru fiecare stat străin | `needs_confirmation` | apostilă, supralegalizare, scutire și certificatul de capacitate | MAE/eConsulat + Primăria Timișoara |
| 4 | Valabilitatea operațională curentă a certificatului medical în alt UAT | `verified_with_local_gap` | cerința locală din UAT-ul competent | serviciul de stare civilă al UAT-ului |
| 5 | Orice taxă locală sau cost conex | `not_found` | existență și cuantum 2026 | hotărârea de taxe locale / pagina oficială a UAT-ului |

## Politica truth-guard

Fereastra 11–30 zile și documentele de bază sunt ancorate în Legea nr. 119/1996. Detaliile locale, ruta minorului și forma actelor străine nu sunt extrapolate în afara sursei și rămân confirmabile.

## Gate de promovare

Nicio regulă critică bazată pe un claim `needs_confirmation`, `conflicting`, `stale` sau fără locator oficial nu poate deveni `active`. Promovarea cere snapshot, hash, validare de schemă, golden fixtures verzi și reviewer independent.
