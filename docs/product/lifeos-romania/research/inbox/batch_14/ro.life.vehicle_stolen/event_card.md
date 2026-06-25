===
# Event Card — ro.life.vehicle_stolen

| Câmp | Valoare |
|---|---|
| `batch_id` | `B14_VEHICLE_STOLEN` |
| `alias_event_type_id` | `ro.life.vehicle_stolen` |
| `event_type_id` | `life.vehicle_stolen` |
| `title_ro` | Mi-a fost furat vehiculul |
| `category_id` | `vehicles_mobility` |
| `reference_date` | `2026-06-25` |
| `geographic_scope` | național; pilot local Timiș / Timișoara |
| `publication_status` | `research_inbox_pending_snapshot_and_human_review` |

## Declanșator

Utilizatorul vrea să sesizeze furtul, să obțină dovada autorității competente și, după caz, să radieze vehiculul.

## Fapte de rutare

| Fact | Tip | Semnificație |
|---|---|---|
| `theft_status` | `enum` | in_progress | discovered_not_in_progress |
| `desired_outcome` | `enum` | police_report_only | deregister | both |
| `applicant_county` | `string` | județul competent; TM este pilotul local |
| `applicant_role` | `enum` | owner | legal_heir | other; necesar pentru radiere |
| `registration_certificate_with_vehicle` | `boolean` | document indisponibil odată cu vehiculul |
| `registration_plates_with_vehicle` | `boolean` | plăcuțe indisponibile odată cu vehiculul |
| `deregistration_date` | `date` | ancoră pentru declarația fiscală ulterioară |

## Rezultat urmărit

Furtul este sesizat pe canalul potrivit, iar radierea și actualizarea fiscală sunt parcurse numai dacă utilizatorul le urmărește și are dovezile necesare.

## Afirmații și reguli

| Element | Număr |
|---|---:|
| source claims | 8 |
| reguli deterministe | 22 |
| golden fixtures | 22 |
| gaps explicite | 5 |

## Acoperire verificată

- Urgența este separată de sesizarea fără urgență; 112 este indicat numai pentru urgență.
- Furtul declarat este un temei verificat de radiere pentru proprietar sau moștenitor legal.
- Dosarul de radiere acceptă documente ori dovezi substitutive, iar declarația fiscală ulterioară are termen de 30 de zile.

## Limitări controlate

- Canalul exact al sesizării fără urgență și documentul poliției trebuie confirmate local.
- Termenul asigurătorului și efectul recuperării vehiculului nu sunt universalizate.

## Politica de adevăr

- Nicio taxă, listă de acte, competență sau termen nu este activat fără `source_claim_ids`.
- O informație locală din afara pilotului Timiș/Timișoara produce confirmare, nu extrapolare.
- Un gap juridic ori operațional rămâne vizibil și nu este convertit automat în cerință obligatorie.

===
