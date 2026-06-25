===
# Event Card — ro.life.import_vehicle_non_eu

| Câmp | Valoare |
|---|---|
| `batch_id` | `B14_IMPORT_VEHICLE_NON_EU` |
| `alias_event_type_id` | `ro.life.import_vehicle_non_eu` |
| `event_type_id` | `life.import_vehicle_non_eu` |
| `title_ro` | Import un vehicul din afara UE și vreau să îl înmatriculez |
| `category_id` | `vehicles_mobility` |
| `reference_date` | `2026-06-25` |
| `geographic_scope` | național; pilot local Timiș / Timișoara |
| `publication_status` | `research_inbox_pending_snapshot_and_human_review` |

## Declanșator

Utilizatorul aduce un vehicul dintr-un stat terț și trebuie să coordoneze vama, RAR, fiscalitatea locală și înmatricularea.

## Fapte de rutare

| Fact | Tip | Semnificație |
|---|---|---|
| `vehicle_condition` | `enum` | new | used |
| `customs_clearance_status` | `enum` | completed | pending | unknown | relief_claimed |
| `ownership_document_registered_local_tax` | `boolean` | declararea fiscală locală |
| `applicant_county` | `string` | TM pilot |
| `foreign_registration_documents_available` | `boolean` | pentru vehicul utilizat |
| `representation_type` | `enum` | self | lawyer | authorized_individual | company_delegate |

## Rezultat urmărit

Vehiculul are situația vamală și TVA clarificate, documentația RAR obținută, este declarat fiscal și înmatriculat.

## Afirmații și reguli

| Element | Număr |
|---|---:|
| source claims | 9 |
| reguli deterministe | 24 |
| golden fixtures | 22 |
| gaps explicite | 5 |

## Acoperire verificată

- Vehiculul din afara UE intră, în principiu, în vamă și TVA la import.
- Înmatricularea folosește dosarul național pentru vehicul nou sau uzat importat.
- Calculul exact este separat de traseul administrativ și nu este ghicit.

## Limitări controlate

- Tariful vamal, scutirile, EORI și formalitățile de reprezentare vamală sunt lăsate needs_confirmation.
- Tarifele RAR și traducerile nu sunt presupuse.

## Politica de adevăr

- Nicio taxă, listă de acte, competență sau termen nu este activat fără `source_claim_ids`.
- O informație locală din afara pilotului Timiș/Timișoara produce confirmare, nu extrapolare.
- Un gap juridic ori operațional rămâne vizibil și nu este convertit automat în cerință obligatorie.

===
