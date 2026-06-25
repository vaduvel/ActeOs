# Event Card — ro.life.transcribe_foreign_death

- `batch_id`: `B02_TRANSCRIBE_FOREIGN_DEATH`
- `reference_date`: `2026-06-25`
- `pilot_jurisdiction`: `ro.tm.timisoara`
- `research_status`: `in_review`
- `trigger_ro`: Am un certificat de deces emis în străinătate pentru un cetățean român și trebuie să îl transcriu în registrele române.

## Fapte de dezambiguizare

| fact | tip | valori / domeniu | obligatoriu | scop |
|---|---|---|---|---|
| `deceased_romanian_status` | `enum` | `romanian_at_death` / `acquired_or_reacquired` / `not_romanian` / `uncertain` | da | aplicabilitatea procedurii |
| `foreign_event_registered` | `boolean` | `true` / `false` | da | transcriere versus art. 39^2 |
| `applicant_location` | `enum` | `romania` / `abroad` | da | canal local/consular |
| `ever_domiciled_ro` | `boolean` | `true` / `false` | da | competența specială |
| `citizenship_basis` | `enum` | `art10_11` / `other` | da | ruta specială |
| `document_format` | `enum` | `standard` / `multilingual_vienna` / `electronic` / `incomplete` | da | formalități document |
| `issuing_country_group` | `enum` | `eu` / `hague_non_eu` / `non_hague` / `unknown` | da | apostilă/supralegalizare |
| `timisoara_connection` | `enum` | `applicant_domicile` / `deceased_last_domicile` / `none` | da | pilotul local |
| `birth_act_transcribed` | `enum` | `yes` / `no` / `unknown` | da | ordinea naștere înainte de deces |

## Graf de proceduri

| intent_id | obligație | când | depends_on | rezultat |
|---|---|---|---|---|
| `ro.civil_status.death.foreign.classify` | `mandatory` | mereu | — | transcriere sau întocmire art. 39^2 |
| `ro.civil_status.death.birth_precheck` | `mandatory` | transcriere posibilă | ro.civil_status.death.foreign.classify | act naștere verificat/transcris |
| `ro.civil_status.death.documents.prepare` | `conditional` | act străin existent | ro.civil_status.death.birth_precheck | dosar complet |
| `ro.civil_status.death.transcribe` | `conditional` | dosar complet | ro.civil_status.death.documents.prepare | act românesc de deces |

## Canale oficiale

| channel_id | nivel | utilizare | verificare |
|---|---|---|---|
| `ch.local_civil_status` | `national/local` | autoritatea locală competentă | Legea 119/1996 |
| `ch.romanian_mission` | `external` | misiunea/oficiul consular competent | Legea 119/1996 |
| `ch.timisoara_death_transcription` | `ro.tm.timisoara` | programare autentificată pentru transcriere deces | portal curent Primăria Timișoara |

## Limite deterministe

- Un deces neînregistrat în străinătate nu se tratează ca transcriere.
- Dacă nașterea persoanei nu este transcrisă, legea permite/impune rezolvarea ei înaintea actului de deces în situația specială publicată.
- Formula locală a termenului de 6 luni este nealiniată cu ancora din legea consolidată și rămâne conflict explicit.

## Politica de activare

`effective_from` din `rules.yaml` este data activării acestui ruleset de cercetare (2026-06-25), nu o afirmație despre data intrării în vigoare a fiecărui act normativ. Promovarea din `in_review` cere validare umană și reverificarea surselor cu freshness `critical`.
