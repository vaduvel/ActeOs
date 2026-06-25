# Event Card — ro.life.renounce_citizenship

- `batch_id`: `B02_RENOUNCE_CITIZENSHIP`
- `reference_date`: `2026-06-25`
- `pilot_jurisdiction`: `ro.tm.timisoara`
- `research_status`: `in_review`
- `trigger_ro`: Vreau să renunț legal la cetățenia română și să știu când produce efecte.

## Fapte de dezambiguizare

| fact | tip | valori / domeniu | obligatoriu | scop |
|---|---|---|---|---|
| `age` | `number` | ani împliniți | da | majorat |
| `other_citizenship_status` | `enum` | `acquired` / `applied_with_assurance` / `none` / `unknown` | da | evitarea apatridiei |
| `criminal_status` | `enum` | `clear` / `suspect_or_accused` / `sentence_to_execute` / `unknown` | da | impedimentul penal |
| `debts_status` | `enum` | `none` / `paid` / `secured` / `unresolved` / `unknown` | da | condiția privind debitele |
| `serious_reason_status` | `enum` | `declared` / `missing` / `unknown` | da | motivele temeinice |
| `residence_location` | `enum` | `romania` / `abroad` | da | canalul de depunere |
| `minors_affected` | `boolean` | `true` / `false` | da | efectele asupra copiilor |

## Graf de proceduri

| intent_id | obligație | când | depends_on | rezultat |
|---|---|---|---|---|
| `ro.citizenship.renunciation.eligibility` | `mandatory` | mereu | — | condiții evaluate |
| `ro.citizenship.renunciation.file` | `conditional` | condiții preliminar îndeplinite | ro.citizenship.renunciation.eligibility | cerere depusă |
| `ro.citizenship.renunciation.complete` | `conditional` | Comisia cere completări | ro.citizenship.renunciation.file | dosar susținut |
| `ro.citizenship.renunciation.certificate` | `conditional` | ordin aprobat | ro.citizenship.renunciation.file | adeverință eliberată și cetățenie pierdută |

## Canale oficiale

| channel_id | nivel | utilizare | verificare |
|---|---|---|---|
| `ch.anc` | `national` | depunere pentru domiciliu în România | Legea 21/1991, art. 31 |
| `ch.romanian_mission` | `external` | depunere și adeverință pentru domiciliu/reședință în străinătate | Legea 21/1991, art. 31 |

## Limite deterministe

- Ordinul de aprobare și pierderea efectivă a cetățeniei sunt momente juridice distincte.
- Motorul nu afirmă că minorii pierd automat cetățenia odată cu un părinte.
- Cuantumul taxei nu este introdus fără o sursă operațională oficială curentă.

## Politica de activare

`effective_from` din `rules.yaml` este data activării acestui ruleset de cercetare (2026-06-25), nu o afirmație despre data intrării în vigoare a fiecărui act normativ. Promovarea din `in_review` cere validare umană și reverificarea surselor cu freshness `critical`.
