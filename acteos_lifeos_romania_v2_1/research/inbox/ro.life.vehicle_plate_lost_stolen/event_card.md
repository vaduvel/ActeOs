===
# Event Card — ro.life.vehicle_plate_lost_stolen

| Câmp | Valoare |
|---|---|
| `batch_id` | `B14_VEHICLE_PLATE_LOST_STOLEN` |
| `alias_event_type_id` | `ro.life.vehicle_plate_lost_stolen` |
| `event_type_id` | `life.vehicle_plate_lost_stolen` |
| `title_ro` | Am pierdut sau mi s-au furat plăcuțele de înmatriculare |
| `category_id` | `vehicles_mobility` |
| `reference_date` | `2026-06-25` |
| `geographic_scope` | național; pilot local Timiș / Timișoara |
| `publication_status` | `research_inbox_pending_snapshot_and_human_review` |

## Declanșator

Utilizatorul trebuie să înlocuiască una sau mai multe plăcuțe pierdute, furate, deteriorate ori reținute în străinătate.

## Fapte de rutare

| Fact | Tip | Semnificație |
|---|---|---|
| `plate_issue_reason` | `enum` | lost | stolen | damaged | retained_abroad | other |
| `plate_type` | `enum` | A | B | C | D |
| `plates_affected` | `enum` | one | pair |
| `incident_date` | `date` | ancoră pentru termenul de 30 zile |
| `applicant_county` | `string` | TM pilot |
| `payment_via_snep` | `boolean` | controlează dovada plății |

## Rezultat urmărit

Sunt emise plăcuțele de înlocuire, cu dovada incidentului și plata aplicabilă, în termenul procedural.

## Afirmații și reguli

| Element | Număr |
|---|---:|
| source claims | 12 |
| reguli deterministe | 24 |
| golden fixtures | 22 |
| gaps explicite | 4 |

## Acoperire verificată

- Termenul verificat este de 30 de zile de la incident.
- Sunt modelate separat pierderea, furtul, deteriorarea și reținerea externă.
- Tarifele A/B/C și tariful D publicat în Timiș sunt legate de configurația declarată, fără extrapolare automată.

## Limitări controlate

- Sancțiunea pentru întârziere și configurațiile neuzuale B/C/D rămân de confirmat.
- Pentru furt fără urgență nu este inventat un canal unic de plângere.

## Politica de adevăr

- Nicio taxă, listă de acte, competență sau termen nu este activat fără `source_claim_ids`.
- O informație locală din afara pilotului Timiș/Timișoara produce confirmare, nu extrapolare.
- Un gap juridic ori operațional rămâne vizibil și nu este convertit automat în cerință obligatorie.

===
