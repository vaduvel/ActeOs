===
event_id: ro.life.fishing_permit
title_ro: Obținerea permisului de pescuit recreativ
intent_id: ro.intent.obtain_fishing_permit
category_id: hobbies_permits
as_of: 2026-06-25
geography: rute speciale naționale și ARBDD; pilot teritorial ITPF Timișoara; gap pentru alți administratori
publication_status: research_verified_with_explicit_gaps
fixture_count: 22
rule_count: 14
claim_count: 7

## outcome_ro
Identificarea cumulului de permise și avize aplicabil apei alese și verificarea separată a restricțiilor curente.

## routing_facts
- `goal`
- `water_regime`
- `tourist_access_permit`
- `border_approval`
- `border_region`
- `restrictions_checked`

## deterministic_branches
| goal / branch | result_ro | confidence |
|---|---|---|
| `water_regime=delta_rbdd` | permis ARBDD + permis acces turist | verified |
| `water_regime=border/maritime` | aviz prealabil Poliția de Frontieră | verified |
| `water_regime=other` | administratorul apei trebuie confirmat | needs_confirmation |

## competent_authorities
| authority | role | territory |
|---|---|---|
| Administrația Rezervației Biosferei Delta Dunării | permis RBDD | RBDD |
| Poliția de Frontieră Română | aviz prealabil | ape de frontieră, ape maritime interioare, mare teritorială |
| ITPF Timișoara | canal teritorial pilot | zona de competență |

## stop_conditions
- Nu considera permisul ARBDD valabil singur dacă lipsește permisul de acces turist aplicabil.
- Nu omite avizul de frontieră pentru apele enumerate oficial.
- Nu afirma că permisul înlătură prohibițiile.
- Nu inventa emitentul pentru o apă al cărei administrator nu este confirmat.

## source_index
| claim_id | publisher | confidence | official_url |
|---|---|---|---|
| `b18.fishing_permit.delta_permit` | Administrația Rezervației Biosferei Delta Dunării | verified | https://permise.ddbra.ro/ |
| `b18.fishing_permit.border_approval` | Poliția de Frontieră Română | verified | https://www.politiadefrontiera.ro/ro/main/i-informatii-privind--activitatea-de-pescuit-recreativsportiv-in-zona-de-frontiera--39707.html |
| `b18.fishing_permit.border_channel` | Poliția de Frontieră Română | verified | https://www.politiadefrontiera.ro/ro/main/i-informatii-privind--activitatea-de-pescuit-recreativsportiv-in-zona-de-frontiera--39707.html |
| `b18.fishing_permit.border_term_validity` | Poliția de Frontieră Română | verified | https://www.politiadefrontiera.ro/ro/main/i-informatii-privind--activitatea-de-pescuit-recreativsportiv-in-zona-de-frontiera--39707.html |
| `b18.fishing_permit.border_no_file` | Poliția de Frontieră Română | verified | https://www.politiadefrontiera.ro/ro/main/pg-activitati-avizate-41.html |
| `b18.fishing_permit.administrator_route_gap` | Poliția de Frontieră Română | needs_confirmation | https://www.politiadefrontiera.ro/ro/main/i-informatii-privind--activitatea-de-pescuit-recreativsportiv-in-zona-de-frontiera--39707.html |
| `b18.fishing_permit.restrictions_gap` | Administrația Rezervației Biosferei Delta Dunării | needs_confirmation | https://permise.ddbra.ro/ |
===
