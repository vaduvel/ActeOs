===
# Event Card — ro.life.vehicle_deregistration

| Câmp | Valoare |
|---|---|
| `batch_id` | `B14_VEHICLE_DEREGISTRATION` |
| `alias_event_type_id` | `ro.life.vehicle_deregistration` |
| `event_type_id` | `life.vehicle_deregistration` |
| `title_ro` | Vreau să radiez un vehicul |
| `category_id` | `vehicles_mobility` |
| `reference_date` | `2026-06-25` |
| `geographic_scope` | național; pilot local Timiș / Timișoara |
| `publication_status` | `research_inbox_pending_snapshot_and_human_review` |

## Declanșator

Utilizatorul urmărește radierea din circulație pentru un motiv legal și apoi actualizarea evidenței fiscale locale.

## Fapte de rutare

| Fact | Tip | Semnificație |
|---|---|---|
| `deregistration_reason` | `enum` | lawful_storage | scrapped | permanent_export | stolen | domestic_transfer | other |
| `applicant_role` | `enum` | owner | legal_heir | owner_not_on_last_certificate |
| `applicant_county` | `string` | TM pilot |
| `submission_mode` | `enum` | counter | online |
| `all_local_obligations_paid` | `boolean` | condiție fiscală la radierea la cerere |
| `deregistration_date` | `date|null` | ancoră pentru declarația fiscală în 30 zile |

## Rezultat urmărit

Vehiculul este radiat pentru un motiv admis și radierea este declarată fiscal în termenul aplicabil.

## Afirmații și reguli

| Element | Număr |
|---|---:|
| source claims | 10 |
| reguli deterministe | 23 |
| golden fixtures | 22 |
| gaps explicite | 4 |

## Acoperire verificată

- Motivele și dosarul de radiere sunt modelate explicit.
- Moștenitorii legali sunt eligibili să ceară radierea.
- Declarația fiscală post-radiere are termen verificat de 30 de zile.

## Limitări controlate

- Calitatea de moștenitor și temeiurile atipice cer confirmare.
- Radierea din oficiu este separată de radierea la cerere.

## Politica de adevăr

- Nicio taxă, listă de acte, competență sau termen nu este activat fără `source_claim_ids`.
- O informație locală din afara pilotului Timiș/Timișoara produce confirmare, nu extrapolare.
- Un gap juridic ori operațional rămâne vizibil și nu este convertit automat în cerință obligatorie.

===
