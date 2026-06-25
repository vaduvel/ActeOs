# Research gaps — B01_DRIVING_LICENCE_LOST_STOLEN

| # | Gap | Status | De confirmat | Sursa țintă | Impact |
|---|---|---|---|---|---|
| G1 | Lista exactă de documente pentru duplicat | `needs_confirmation` | snapshot DGPCI document-details | DGPCI | `critical` |
| G2 | Proces-verbal/adeverință de furt pentru permis | `not_found` | dacă este obligatoriu sau doar util | DGPCI / Ordin MAI 82/2024 | `critical` |
| G3 | Semnătura/formatele acceptate pe e-mail | `needs_confirmation` | PDF, semnătură, dimensiune, subiect | fiecare SPCRPCIV | `operational` |
| G4 | Regula medicală națională vs pilot Timiș | `verified_with_local_gap` | aplicare uniformă și excepții | DGPCI / Ordin MAI 82/2024 | `critical` |

## Claim-uri nepromovabile

| claim_id | confidence | status | afirmație | sursă |
|---|---|---|---|---|
| `claim.dldup.exact_dossier` | `needs_confirmation` | `in_review` | Pagina HUB trimite la o pagină DGPCI pentru dosarul exact, dar lista stabilă nu este expusă în conținutul verificat. | https://hub.mai.gov.ro/serviciu/view?id=72 |

## Politica de promovare

Niciun claim `needs_confirmation` sau `conflicting` nu poate activa o regulă critică. Regula rămâne `in_review`, produce `require_confirmation` ori este blocată până la reconcilierea sursei.
