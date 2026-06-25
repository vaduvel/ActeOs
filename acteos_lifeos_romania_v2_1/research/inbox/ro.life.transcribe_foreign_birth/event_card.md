# Event Card — ro.life.transcribe_foreign_birth

- `batch_id`: `B02_TRANSCRIBE_FOREIGN_BIRTH`
- `reference_date`: `2026-06-25`
- `pilot_jurisdiction`: `ro.tm.timisoara`
- `research_status`: `in_review`
- `trigger_ro`: Am un certificat de naștere emis în străinătate și trebuie să obțin actul românesc prin transcriere.

## Fapte de dezambiguizare

| fact | tip | valori / domeniu | obligatoriu | scop |
|---|---|---|---|---|
| `subject_romanian_status` | `enum` | `romanian_at_birth` / `acquired_or_reacquired` / `not_romanian` / `uncertain` | da | aplicabilitatea art. 41 |
| `foreign_event_registered` | `boolean` | `true` / `false` | da | transcriere versus înregistrare inițială |
| `applicant_location` | `enum` | `romania` / `abroad` | da | canal local sau consular |
| `ever_domiciled_ro` | `boolean` | `true` / `false` | da | competența teritorială specială |
| `citizenship_basis` | `enum` | `birth` / `art10_11` / `other` | da | ruta specială art. 10/11 |
| `document_format` | `enum` | `standard` / `multilingual_vienna` / `electronic` / `incomplete` | da | formalități document |
| `issuing_country_group` | `enum` | `eu` / `hague_non_eu` / `non_hague` / `unknown` | da | apostilă/supralegalizare |
| `timisoara_connection` | `enum` | `domicile` / `last_domicile` / `none` | da | pilotul local |
| `subject_age` | `number` | ani împliniți | da | cine semnează/depune |

## Graf de proceduri

| intent_id | obligație | când | depends_on | rezultat |
|---|---|---|---|---|
| `ro.civil_status.birth.foreign.classify` | `mandatory` | mereu | — | transcriere sau altă procedură |
| `ro.civil_status.birth.documents.prepare` | `conditional` | act străin existent și titular român | ro.civil_status.birth.foreign.classify | dosar formalizat |
| `ro.civil_status.birth.transcribe` | `conditional` | dosar complet | ro.civil_status.birth.documents.prepare | act românesc de naștere |

## Canale oficiale

| channel_id | nivel | utilizare | verificare |
|---|---|---|---|
| `ch.local_civil_status` | `national/local` | UAT domiciliu/ultimul domiciliu | Legea 119/1996 |
| `ch.romanian_mission` | `external` | misiunea/oficiul consular competent | Legea 119/1996 |
| `ch.timisoara_civil_status` | `ro.tm.timisoara` | programare pentru domiciliu/ultimul domiciliu Timișoara | portal curent + pagină oficială arhivată |

## Limite deterministe

- Transcrierea presupune un act străin deja înregistrat; lipsa lui declanșează o procedură diferită.
- Regimul formalităților documentului depinde de stat și format; nu se deduce doar din limba documentului.
- Termenul local publicat are o ancoră diferită față de legea consolidată și este expus ca conflict.

## Politica de activare

`effective_from` din `rules.yaml` este data activării acestui ruleset de cercetare (2026-06-25), nu o afirmație despre data intrării în vigoare a fiecărui act normativ. Promovarea din `in_review` cere validare umană și reverificarea surselor cu freshness `critical`.
