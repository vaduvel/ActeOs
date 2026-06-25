===
# Event Card — ro.life.temporary_vehicle_authorisation

| Câmp | Valoare |
|---|---|
| `batch_id` | `B14_TEMPORARY_VEHICLE_AUTHORISATION` |
| `alias_event_type_id` | `ro.life.temporary_vehicle_authorisation` |
| `event_type_id` | `life.temporary_vehicle_authorisation` |
| `title_ro` | Vreau numere provizorii pentru un vehicul |
| `category_id` | `vehicles_mobility` |
| `reference_date` | `2026-06-25` |
| `geographic_scope` | național; pilot local Timiș / Timișoara |
| `publication_status` | `research_inbox_pending_snapshot_and_human_review` |

## Declanșator

Utilizatorul are nevoie să circule temporar înaintea înmatriculării și trebuie verificată durata cumulată, RCA și proveniența vehiculului.

## Fapte de rutare

| Fact | Tip | Semnificație |
|---|---|---|
| `vehicle_origin` | `enum` | domestic | foreign |
| `previously_registered_abroad` | `boolean` | activează actele străine |
| `foreign_registration_documents_available` | `boolean` | activează excepția de 5 zile |
| `requested_days` | `integer` | durata solicitată |
| `total_days_after_request` | `integer` | cumulul tuturor autorizațiilor |
| `rca_valid` | `boolean` | RCA pe numele proprietarului |

## Rezultat urmărit

Este emisă autorizația provizorie și plăcuțele aferente pentru perioada legal posibilă, numai pe teritoriul României.

## Afirmații și reguli

| Element | Număr |
|---|---:|
| source claims | 7 |
| reguli deterministe | 19 |
| golden fixtures | 22 |
| gaps explicite | 4 |

## Acoperire verificată

- Limita cumulată verificată este de 90 de zile.
- Fără actele străine, excepția verificată este de maximum 5 zile și cel mult până la expirarea RCA.
- Autorizația este valabilă numai în România.

## Limitări controlate

- Costul exact al plăcuțelor și cerința tranzitorie dealer/leasing rămân de confirmat.
- Canalele din alte județe sunt local gap.

## Politica de adevăr

- Nicio taxă, listă de acte, competență sau termen nu este activat fără `source_claim_ids`.
- O informație locală din afara pilotului Timiș/Timișoara produce confirmare, nu extrapolare.
- Un gap juridic ori operațional rămâne vizibil și nu este convertit automat în cerință obligatorie.

===
