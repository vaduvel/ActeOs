# Event Card — ro.life.residence_right_ro

- `batch_id`: `B02_RESIDENCE_RIGHT_RO`
- `reference_date`: `2026-06-25`
- `pilot_jurisdiction`: `ro.tm.timisoara`
- `research_status`: `in_review`
- `trigger_ro`: Sunt cetățean străin și trebuie să obțin sau să prelungesc dreptul de ședere în România.

## Fapte de dezambiguizare

| fact | tip | valori / domeniu | obligatoriu | scop |
|---|---|---|---|---|
| `citizen_group` | `enum` | `romanian` / `eu_see_ch` / `third_country` | da | separă regimul juridic |
| `request_stage` | `enum` | `first_entry` / `temporary_extension` / `long_term` / `family_card` / `protection_or_special` | da | procedura aplicabilă |
| `residence_purpose` | `enum` | `work` / `studies` / `family` / `commercial` / `other` | da | condițiile speciale |
| `current_status_valid` | `boolean` | `true` / `false` | da | menținerea dreptului până la decizie |
| `cross_border_worker` | `boolean` | `true` / `false` | da | excepția locativă |
| `timis_residence` | `boolean` | `true` / `false` | da | competența teritorială pilot |

## Graf de proceduri

| intent_id | obligație | când | depends_on | rezultat |
|---|---|---|---|---|
| `ro.immigration.regime.classify` | `mandatory` | mereu | — | regim UE/străin/român selectat |
| `ro.immigration.temporary_extension.apply` | `conditional` | stat terț + prelungire | ro.immigration.regime.classify | cerere IGI depusă |
| `ro.immigration.purpose.requirements.collect` | `conditional` | prelungire temporară | ro.immigration.temporary_extension.apply | dosar pe scop |
| `ro.immigration.other_stage.route` | `conditional` | termen lung/familie/protecție | ro.immigration.regime.classify | procedură separată |

## Canale oficiale

| channel_id | nivel | utilizare | verificare |
|---|---|---|---|
| `ch.igi_national` | `national` | norme și proceduri de ședere | OUG 194 + IGI |
| `ch.igi_timis` | `ro.tm` | depunere la reședința din Timiș | oficial IGI Timiș |

## Limite deterministe

- Regimul UE este separat de regimul resortisanților statelor terțe.
- Motorul nu inventează cuantumul taxelor, al mijloacelor de întreținere sau documentele speciale ale fiecărui scop.
- Menținerea dreptului până la decizie este afișată numai dacă șederea era legală la depunere.

## Politica de activare

`effective_from` din `rules.yaml` este data activării acestui ruleset de cercetare (2026-06-25), nu o afirmație despre data intrării în vigoare a fiecărui act normativ. Promovarea din `in_review` cere validare umană și reverificarea surselor cu freshness `critical`.
