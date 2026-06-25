# Event Card — ro.life.consular_service

- `batch_id`: `B02_CONSULAR_SERVICE`
- `reference_date`: `2026-06-25`
- `pilot_jurisdiction`: `ro.tm.timisoara`
- `research_status`: `in_review`
- `trigger_ro`: Sunt în străinătate sau am nevoie de un serviciu al unei misiuni române și trebuie să identific procedura consulară exactă.

## Fapte de dezambiguizare

| fact | tip | valori / domeniu | obligatoriu | scop |
|---|---|---|---|---|
| `service_category` | `enum` | `passport_travel` / `civil_status` / `citizenship` / `renunciation` / `emergency_lost_docs` / `notarial_legalisation` / `visa` / `other` | da | selectează serviciul |
| `applicant_status` | `enum` | `romanian_citizen` / `foreign_citizen` / `dual_or_uncertain` | da | eligibilitate consulară |
| `current_region` | `enum` | `eu` / `outside_eu` | da | protecție consulară UE |
| `romanian_mission_available` | `boolean` | `true` / `false` | da | misiune proprie sau alt stat UE |
| `legal_basis` | `enum` | `art8_1` / `art10` / `art11` / `other` / `not_applicable` / `unknown` | da | ruta de cetățenie |

## Graf de proceduri

| intent_id | obligație | când | depends_on | rezultat |
|---|---|---|---|---|
| `ro.consular.service.classify` | `mandatory` | mereu | — | serviciu și misiune identificate |
| `ro.consular.passport.request` | `conditional` | pașaport/călătorie | ro.consular.service.classify | rută DGP consulară |
| `ro.consular.civil_status.request` | `conditional` | stare civilă | ro.consular.service.classify | operațiune exactă selectată |
| `ro.consular.citizenship.request` | `conditional` | temei eligibil | ro.consular.service.classify | depunere consulară |
| `eu.consular.protection.request` | `conditional` | stat terț fără misiune română | — | misiune alternativă UE |

## Canale oficiale

| channel_id | nivel | utilizare | verificare |
|---|---|---|---|
| `ch.romanian_mission_passports` | `consular` | pașapoarte și documente de călătorie | DGP + misiune |
| `ch.romanian_mission_civil_status` | `consular` | stare civilă | Legea 119 + misiune |
| `ch.romanian_mission_citizenship` | `consular` | cetățenie și renunțare | Legea 21 + misiune |
| `ch.romanian_mission_emergency` | `consular` | urgențe/documente pierdute | DGP + misiune |
| `ch.other_eu_mission` | `eu` | protecție consulară nereprezentată | oficial UE |
| `ch.evisa_mae` | `national` | verificare și cerere de viză pentru România | portal oficial MAE |

## Limite deterministe

- Evenimentul este un router; nu combină toate serviciile consulare într-un checklist universal.
- Taxele, programarea, competența teritorială și lista de documente se confirmă în catalogul live al misiunii.
- Depunerea consulară a cetățeniei este inclusă doar pentru bazele ancorate explicit în lege.

## Politica de activare

`effective_from` din `rules.yaml` este data activării acestui ruleset de cercetare (2026-06-25), nu o afirmație despre data intrării în vigoare a fiecărui act normativ. Promovarea din `in_review` cere validare umană și reverificarea surselor cu freshness `critical`.
