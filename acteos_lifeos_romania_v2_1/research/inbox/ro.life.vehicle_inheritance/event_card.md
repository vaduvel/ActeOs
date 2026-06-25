===
# Event Card — ro.life.vehicle_inheritance

| Câmp | Valoare |
|---|---|
| `batch_id` | `B14_VEHICLE_INHERITANCE` |
| `alias_event_type_id` | `ro.life.vehicle_inheritance` |
| `event_type_id` | `life.vehicle_inheritance` |
| `title_ro` | Am moștenit un vehicul |
| `category_id` | `vehicles_mobility` |
| `reference_date` | `2026-06-25` |
| `geographic_scope` | național; pilot local Timiș / Timișoara |
| `publication_status` | `research_inbox_pending_snapshot_and_human_review` |

## Declanșator

Utilizatorul urmărește să păstreze, să vândă sau să radieze un vehicul dobândit prin moștenire.

## Fapte de rutare

| Fact | Tip | Semnificație |
|---|---|---|
| `intended_action` | `enum` | keep_and_use | sell | deregister |
| `succession_status` | `enum` | not_opened | in_progress | completed |
| `applicant_role` | `enum` | legal_heir | other |
| `submission_mode` | `enum|null` | counter | online; diferențiază documentul fiscal Timiș la transcriere |
| `legal_acquisition_date_confirmed` | `boolean` | permite calculul termenului de transcriere |
| `acquisition_date` | `date` | data juridică confirmată a dobândirii |
| `co_heirs` | `boolean` | există mai mulți moștenitori |
| `minor_heir` | `boolean` | un moștenitor este minor |
| `applicant_county` | `string` | TM este pilotul local |

## Rezultat urmărit

Vehiculul este gestionat potrivit opțiunii utilizatorului, numai după dovedirea dreptului succesoral și îndeplinirea cerințelor fiscale și de evidență aplicabile.

## Afirmații și reguli

| Element | Număr |
|---|---:|
| source claims | 12 |
| reguli deterministe | 33 |
| golden fixtures | 22 |
| gaps explicite | 6 |

## Acoperire verificată

- Moștenitorii legali sunt eligibili expres pentru radierea vehiculului.
- Păstrarea și utilizarea vehiculului conduce la traseul de transcriere, cu CIV, ITP și RCA valabile.
- Termenul de 90 de zile este calculat numai dintr-o dată juridică a dobândirii confirmată.

## Limitări controlate

- Documentul succesoral exact, co-moștenitorii, minorii și traseul de vânzare necesită verificare pe speță.
- Particularitățile fiscale din afara Timișoarei rămân gap local verificabil.

## Politica de adevăr

- Nicio taxă, listă de acte, competență sau termen nu este activat fără `source_claim_ids`.
- O informație locală din afara pilotului Timiș/Timișoara produce confirmare, nu extrapolare.
- Un gap juridic ori operațional rămâne vizibil și nu este convertit automat în cerință obligatorie.

===
