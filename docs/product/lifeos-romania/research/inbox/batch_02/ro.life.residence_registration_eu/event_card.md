# Event Card — ro.life.residence_registration_eu

- `batch_id`: `B02_RESIDENCE_REGISTRATION_EU`
- `reference_date`: `2026-06-25`
- `pilot_jurisdiction`: `ro.tm.timisoara`
- `research_status`: `in_review`
- `trigger_ro`: Sunt cetățean UE/SEE/Elveția sau membru de familie și vreau să locuiesc în România peste perioada scurtă de ședere.

## Fapte de dezambiguizare

| fact | tip | valori / domeniu | obligatoriu | scop |
|---|---|---|---|---|
| `citizen_group` | `enum` | `eu_see_ch` / `non_eu_family_member` / `romanian` | da | regimul juridic |
| `stay_over_3_months` | `boolean` | `true` / `false` | da | formalitatea de înregistrare |
| `residence_basis` | `enum` | `employment` / `self_employed` / `means` / `studies` / `eu_family` / `romanian_family` / `volunteer` / `religious` / `other` | da | checklistul de bază |
| `family_member_citizenship` | `enum` | `eu_see_ch` / `non_eu` / `not_applicable` | da | certificat versus carte de rezidență |
| `timis_residence` | `boolean` | `true` / `false` | da | canalul local pilot |
| `continuous_legal_residence_years` | `number` | `>=0` | da | rezidență permanentă |

## Graf de proceduri

| intent_id | obligație | când | depends_on | rezultat |
|---|---|---|---|---|
| `ro.immigration.eu.registration.assess` | `mandatory` | cetățean UE/SEE/CH | — | necesitatea certificatului stabilită |
| `ro.immigration.eu.registration.apply` | `conditional` | peste trei luni | ro.immigration.eu.registration.assess | certificat de înregistrare |
| `ro.immigration.eu.family_card.apply` | `conditional` | membru de familie non-UE | — | carte de rezidență |
| `ro.immigration.eu.permanent.assess` | `optional` | minimum cinci ani | — | eligibilitate permanentă evaluată |

## Canale oficiale

| channel_id | nivel | utilizare | verificare |
|---|---|---|---|
| `ch.igi_national_eu` | `national` | reguli și liste de documente | oficial IGI |
| `ch.igi_timis` | `ro.tm` | depunere/programare pentru domiciliul din Timiș | oficial IGI Timiș |

## Limite deterministe

- Motorul folosește pragul legal «peste trei luni», nu îl transformă arbitrar într-un număr de zile.
- Cetățeanul UE și membrul de familie non-UE nu primesc același document.
- Cuantumul mijloacelor și checklisturile operative se reverifică la IGI înainte de depunere.

## Politica de activare

`effective_from` din `rules.yaml` este data activării acestui ruleset de cercetare (2026-06-25), nu o afirmație despre data intrării în vigoare a fiecărui act normativ. Promovarea din `in_review` cere validare umană și reverificarea surselor cu freshness `critical`.
