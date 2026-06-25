# Event Card — ro.life.documents_lost_abroad

- `batch_id`: `B02_DOCUMENTS_LOST_ABROAD`
- `reference_date`: `2026-06-25`
- `pilot_jurisdiction`: `ro.tm.timisoara`
- `research_status`: `in_review`
- `trigger_ro`: Mi-am pierdut, mi s-a furat ori mi s-a distrus un document în străinătate și trebuie să-mi protejez identitatea și să pot continua sau încheia călătoria.

## Fapte de dezambiguizare

| fact | tip | valori / domeniu | obligatoriu | scop |
|---|---|---|---|---|
| `document_type` | `enum` | `passport` / `national_id` / `driving_licence` / `residence_permit` / `other` | da | alege emitentul și procedura |
| `loss_kind` | `enum` | `lost` / `stolen` / `destroyed` / `found_after_report` | da | determină raportarea și nulitatea |
| `current_region` | `enum` | `eu` / `outside_eu` | da | protecție consulară UE |
| `romanian_mission_available` | `boolean` | `true` / `false` | da | misiune proprie sau alt stat UE |
| `travel_need` | `enum` | `return_to_ro` / `urgent_continue` / `no_immediate_travel` | da | document de călătorie și urgență |
| `local_report_status` | `enum` | `obtained` / `not_obtained` / `not_applicable` | da | dovada furtului |

## Graf de proceduri

| intent_id | obligație | când | depends_on | rezultat |
|---|---|---|---|---|
| `ro.identity.loss.secure` | `mandatory` | mereu | — | identitate protejată și emitent contactat |
| `ro.passport.loss.declare_abroad` | `conditional` | pașaport pierdut/distrus | ro.identity.loss.secure | declarație consulară |
| `ro.passport.theft.report_local` | `conditional` | furt | ro.identity.loss.secure | dovadă poliție locală |
| `ro.travel.emergency_document.assess` | `conditional` | întoarcere sau urgență | ro.passport.loss.declare_abroad | document/rută confirmată de misiune |
| `eu.consular.protection.request` | `conditional` | în afara UE și România nereprezentată | — | asistență de la alt stat UE |

## Canale oficiale

| channel_id | nivel | utilizare | verificare |
|---|---|---|---|
| `ch.romanian_mission` | `consular` | declarare și document de călătorie | competența teritorială se confirmă |
| `ch.local_police` | `foreign_local` | raportarea furtului | oficial local |
| `ch.other_eu_mission` | `eu` | protecție consulară când România nu este reprezentată | oficial UE |

## Limite deterministe

- Motorul nu promite îmbarcarea, tranzitul sau intrarea doar pentru că a fost emis un document de urgență.
- Pașaportul temporar nu este prescris automat; misiunea verifică urgența și actele disponibile.
- Pentru documentele non-pașaport este declanșată o rută specifică emitentului, nu o copie a procedurii pașaportului.

## Politica de activare

`effective_from` din `rules.yaml` este data activării acestui ruleset de cercetare (2026-06-25), nu o afirmație despre data intrării în vigoare a fiecărui act normativ. Promovarea din `in_review` cere validare umană și reverificarea surselor cu freshness `critical`.
