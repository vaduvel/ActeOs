===
# Event Card — ro.life.vehicle_registration_certificate_lost

| Câmp | Valoare |
|---|---|
| `batch_id` | `B14_VEHICLE_REGISTRATION_CERTIFICATE_LOST` |
| `alias_event_type_id` | `ro.life.vehicle_registration_certificate_lost` |
| `event_type_id` | `life.vehicle_registration_certificate_lost` |
| `title_ro` | Am pierdut, deteriorat sau mi s-a furat certificatul de înmatriculare |
| `category_id` | `vehicles_mobility` |
| `reference_date` | `2026-06-25` |
| `geographic_scope` | național; pilot local Timiș / Timișoara |
| `publication_status` | `research_inbox_pending_snapshot_and_human_review` |

## Declanșator

Utilizatorul nu mai poate folosi certificatul și cere un duplicat de la autoritatea care a înmatriculat vehiculul.

## Fapte de rutare

| Fact | Tip | Semnificație |
|---|---|---|
| `replacement_reason` | `enum` | lost | stolen | damaged | retained_abroad | other |
| `applicant_role` | `enum` | registered_owner | mandated_holder | other |
| `applicant_county` | `string` | județul autorității competente |
| `submission_mode` | `enum` | counter | online |
| `civ_valid` | `boolean` | CIV valabilă |
| `payment_via_snep` | `boolean` | controlează dovada plății |

## Rezultat urmărit

Este emis un nou certificat de înmatriculare pe baza motivului și documentelor doveditoare aplicabile.

## Afirmații și reguli

| Element | Număr |
|---|---:|
| source claims | 8 |
| reguli deterministe | 21 |
| golden fixtures | 22 |
| gaps explicite | 4 |

## Acoperire verificată

- Sunt modelate pierderea, furtul, deteriorarea și reținerea în străinătate.
- Solicitanții verificați sunt proprietarul înscris și deținătorul mandatat.
- În pilotul Timiș, canalul online pentru duplicat este modelat distinct de ghișeu.

## Limitări controlate

- Termenul de emitere și canalele altor județe nu sunt presupuse.
- Cazurile reziduale cer confirmare.

## Politica de adevăr

- Nicio taxă, listă de acte, competență sau termen nu este activat fără `source_claim_ids`.
- O informație locală din afara pilotului Timiș/Timișoara produce confirmare, nu extrapolare.
- Un gap juridic ori operațional rămâne vizibil și nu este convertit automat în cerință obligatorie.

===
