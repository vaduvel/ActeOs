# Research gaps — B01_CIVIL_STATUS_DUPLICATE

| # | Gap | Status | De confirmat | Sursa țintă | Impact |
|---|---|---|---|---|---|
| G1 | Canalul electronic efectiv în SIIEASC | `conflicting` | portal, autentificare, formate și acoperire teritorială | DGEP / HUB MAI | `critical` |
| G2 | Pagina locală curentă Timișoara | `needs_confirmation` | programare, adresă, acte și canale | Primăria Timișoara | `critical` |
| G3 | Taxa curentă Timișoara | `conflicting` | HCL aplicabilă în 2026 și cuantum | Consiliul Local Timișoara | `critical` |
| G4 | Termene locale după migrarea SIIEASC | `needs_confirmation` | 5/30 zile versus timpi HUB | DGEP / Primăria Timișoara | `operational` |

## Claim-uri nepromovabile

| claim_id | confidence | status | afirmație | sursă |
|---|---|---|---|---|
| `claim.civil.electronic_allowed_law` | `conflicting` | `conflicting` | Începând cu 31 martie 2025, certificatele și extrasele multilingve se pot emite, transmite și semna electronic. | https://legislatie.just.ro/Public/DetaliiDocument/8624 |
| `claim.civil.hub_no_electronic` | `conflicting` | `conflicting` | Pagina HUB pentru acest serviciu declară că nu primește și nu transmite documente în format electronic. | https://hub.mai.gov.ro/serviciu/view?id=99 |
| `claim.civil.fee_ambiguity_hub` | `conflicting` | `conflicting` | Pagina HUB afișează 0 lei în tabel, dar precizează că taxele diferă și se stabilesc prin hotărâre a consiliului local. | https://hub.mai.gov.ro/serviciu/view?id=99 |
| `claim.civil.tm_docs_archived` | `needs_confirmation` | `in_review` | Pagina arhivată Timișoara indică actul de identitate, certificatul vechi la preschimbare, actul de modificare a statutului, procura și dovada rudeniei pentru deces, după caz. | https://servicii.primariatm.ro/duplicate-stare-civila |
| `claim.civil.tm_presence_no_email_archived` | `needs_confirmation` | `in_review` | Pagina arhivată Timișoara afirmă că identitatea se verifică în prezență și că cererile prin e-mail sau poștă nu pot fi soluționate favorabil. | https://servicii.primariatm.ro/duplicate-stare-civila |
| `claim.civil.tm_appointment_archived` | `needs_confirmation` | `in_review` | Pagina arhivată Timișoara cere programare online pentru depunerea cererii. | https://servicii.primariatm.ro/duplicate-stare-civila |
| `claim.civil.tm_timing_archived` | `needs_confirmation` | `in_review` | Pagina arhivată Timișoara indică 5 zile pentru acte înregistrate local și 30 de zile pentru acte înregistrate în altă localitate. | https://servicii.primariatm.ro/duplicate-stare-civila |
| `claim.civil.tm_no_fee_archived` | `conflicting` | `conflicting` | Pagina arhivată Timișoara afirmă că nu se percep taxe pentru eliberarea certificatului la cerere. | https://servicii.primariatm.ro/duplicate-stare-civila |

## Politica de promovare

Niciun claim `needs_confirmation` sau `conflicting` nu poate activa o regulă critică. Regula rămâne `in_review`, produce `require_confirmation` ori este blocată până la reconcilierea sursei.
