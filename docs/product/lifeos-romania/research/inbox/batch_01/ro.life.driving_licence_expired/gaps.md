# Research gaps — B01_DRIVING_LICENCE_EXPIRED

| # | Gap | Status | De confirmat | Sursa țintă | Impact |
|---|---|---|---|---|---|
| G1 | Lista exactă națională de documente | `needs_confirmation` | snapshot al paginii DGPCI document-details | DGPCI | `critical` |
| G2 | Regula medicală națională pentru nouă valabilitate | `verified_with_local_gap` | text național și excepții pe categorii | Ordin MAI 82/2024 / DGPCI | `critical` |
| G3 | Documentele și limitele reprezentării prin împuternicit | `needs_confirmation` | formă procură, fotografie, semnătură | DGPCI | `critical` |
| G4 | Program SPCRPCIV Timiș | `conflicting` | 19:00 sau 19:30 L-J | Prefectura Timiș | `operational` |

## Claim-uri nepromovabile

| claim_id | confidence | status | afirmație | sursă |
|---|---|---|---|---|
| `claim.dl.renew.program_conflict_a` | `conflicting` | `conflicting` | Pagina locală publică pentru permise program L-J 08:10-19:00 și V 08:30-18:00. | https://tm.prefectura.mai.gov.ro/permise-auto-si-inmatriculari/serviciul-regim-permise-si-inmatriculari-program/ |
| `claim.dl.renew.program_conflict_b` | `conflicting` | `conflicting` | Aceeași pagină publică pentru preschimbare L-J 08:10-19:30 și V 08:30-18:00. | https://tm.prefectura.mai.gov.ro/permise-auto-si-inmatriculari/serviciul-regim-permise-si-inmatriculari-program/ |
| `claim.dl.renew.exact_dossier` | `needs_confirmation` | `in_review` | Pagina HUB trimite la o pagină DGPCI pentru documentele exacte, dar lista nu este expusă în conținutul stabil verificat; dosarul exact rămâne de confirmat înainte de producție. | https://hub.mai.gov.ro/serviciu/view?id=69 |

## Politica de promovare

Niciun claim `needs_confirmation` sau `conflicting` nu poate activa o regulă critică. Regula rămâne `in_review`, produce `require_confirmation` ori este blocată până la reconcilierea sursei.
