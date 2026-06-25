===
# Event Card — ro.life.import_vehicle_eu

| Câmp | Valoare |
|---|---|
| `batch_id` | `B14_IMPORT_VEHICLE_EU` |
| `alias_event_type_id` | `ro.life.import_vehicle_eu` |
| `event_type_id` | `life.import_vehicle_eu` |
| `title_ro` | Import un vehicul din UE și vreau să îl înmatriculez |
| `category_id` | `vehicles_mobility` |
| `reference_date` | `2026-06-25` |
| `geographic_scope` | național; pilot local Timiș / Timișoara |
| `publication_status` | `research_inbox_pending_snapshot_and_human_review` |

## Declanșator

Utilizatorul aduce în România un vehicul nou sau utilizat cumpărat dintr-un stat UE și urmărește RAR, fiscal și înmatriculare.

## Fapte de rutare

| Fact | Tip | Semnificație |
|---|---|---|
| `vehicle_condition` | `enum` | new | used |
| `vat_registered` | `boolean` | înregistrarea solicitantului în scopuri TVA |
| `rar_applicant_matches_acquirer` | `boolean` | solicitantul CIV este achizitorul intracomunitar sau reprezentant legal |
| `ownership_document_registered_local_tax` | `boolean` | actul de proprietate este declarat fiscal |
| `applicant_county` | `string` | TM pilot |
| `representation_type` | `enum` | self | lawyer | authorized_individual | company_delegate |

## Rezultat urmărit

Vehiculul este încadrat fiscal, verificat la RAR, declarat local și înmatriculat în România.

## Afirmații și reguli

| Element | Număr |
|---|---:|
| source claims | 14 |
| reguli deterministe | 25 |
| golden fixtures | 22 |
| gaps explicite | 4 |

## Acoperire verificată

- Importul din UE nu implică taxă vamală.
- Vehiculul utilizat necesită actele străine și plăcuțele, plus condițiile RAR/ITP/autenticitate.
- Solicitantul neînregistrat TVA are o cerință separată de certificat TVA.

## Limitări controlate

- Calculul TVA, formularul ANAF și traducerile nu sunt automatizate fără surse operaționale complete.
- Tarifele și programarea RAR locale rămân de confirmat.

## Politica de adevăr

- Nicio taxă, listă de acte, competență sau termen nu este activat fără `source_claim_ids`.
- O informație locală din afara pilotului Timiș/Timișoara produce confirmare, nu extrapolare.
- Un gap juridic ori operațional rămâne vizibil și nu este convertit automat în cerință obligatorie.

===
