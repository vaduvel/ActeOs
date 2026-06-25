===
# Event Card — ro.life.bought_new_vehicle

| Câmp | Valoare |
|---|---|
| `batch_id` | `B14_BOUGHT_NEW_VEHICLE` |
| `alias_event_type_id` | `ro.life.bought_new_vehicle` |
| `event_type_id` | `life.bought_new_vehicle` |
| `title_ro` | Am cumpărat un vehicul nou și vreau să îl înmatriculez |
| `category_id` | `vehicles_mobility` |
| `reference_date` | `2026-06-25` |
| `geographic_scope` | național; pilot local Timiș / Timișoara |
| `publication_status` | `research_inbox_pending_snapshot_and_human_review` |

## Declanșator

Utilizatorul a cumpărat în România un vehicul nou și urmărește declararea fiscală și prima înmatriculare.

## Fapte de rutare

| Fact | Tip | Semnificație |
|---|---|---|
| `applicant_type` | `enum` | individual | company |
| `applicant_county` | `string` | TM pentru pilot; alt județ produce gap local |
| `representation_type` | `enum` | self | lawyer | authorized_individual | company_delegate |
| `ownership_document_registered_local_tax` | `boolean` | actul de proprietate este în evidența fiscală locală |
| `payment_via_snep` | `boolean` | controlează dovada plății |
| `acquisition_form` | `enum` | sale | leasing |
| `plate_choice` | `enum` | standard | preferential |
| `plate_type` | `enum` | A | B | C |

## Rezultat urmărit

Vehiculul este declarat fiscal și înmatriculat pe numele proprietarului, cu documentele și plățile aplicabile.

## Afirmații și reguli

| Element | Număr |
|---|---:|
| source claims | 14 |
| reguli deterministe | 24 |
| golden fixtures | 22 |
| gaps explicite | 4 |

## Acoperire verificată

- Dosarul național pentru vehicul nou este susținut de lista oficială MAI.
- Vehiculul nou este exceptat de la certificatul de autenticitate.
- Pilotul Timiș include clarificarea fiscală din 4 martie 2026 și canalul DFMT Atlas.

## Limitări controlate

- Lista exactă DFMT depinde de selecția interactivă.
- Canalele din alte județe rămân verified_with_local_gap.

## Politica de adevăr

- Nicio taxă, listă de acte, competență sau termen nu este activat fără `source_claim_ids`.
- O informație locală din afara pilotului Timiș/Timișoara produce confirmare, nu extrapolare.
- Un gap juridic ori operațional rămâne vizibil și nu este convertit automat în cerință obligatorie.

===
