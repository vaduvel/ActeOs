# Research gaps — B13_VAT_REGISTRATION

| # | Gap | Status | De confirmat | Sursa țintă |
|---|---|---|---|---|
| 1 | Plafonul TVA aplicabil la data și activitatea contribuabilului | `needs_confirmation` | valoarea, baza de calcul și momentul depășirii | Codul fiscal consolidat + ghid ANAF 2026 |
| 2 | Termenul exact de depunere pentru fiecare temei | `needs_confirmation` | data de la care curge și excepțiile | Codul fiscal/OPANAF aplicabil |
| 3 | Data efectivă a înregistrării | `needs_confirmation` | regula aplicabilă opțiunii, plafonului sau regimului special | ANAF + Codul fiscal |
| 4 | Documentele suplimentare și validările formularului 700 | `needs_confirmation` | versiunea curentă și anexele pentru situația concretă | pagina oficială ANAF formular 700 |
| 5 | Ruta specială pentru achiziții/servicii intracomunitare | `needs_confirmation` | formularul de înregistrare și obligațiile 301 aplicabile | ANAF + Codul fiscal |

## Politica truth-guard

Formularul și canalul sunt verificate; eligibilitatea materială, plafonul și data efectivă rămân blocate până la confirmarea sursei fiscale aplicabile.

## Gate de promovare

Nicio regulă critică bazată pe un claim `needs_confirmation`, `conflicting`, `stale`, `expired` sau fără locator oficial nu poate deveni `active`. Promovarea cere snapshot, hash, validare de schemă, golden fixtures verzi și reviewer independent.
