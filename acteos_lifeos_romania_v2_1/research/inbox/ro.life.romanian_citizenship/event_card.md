# Event Card — ro.life.romanian_citizenship

- `batch_id`: `B02_ROMANIAN_CITIZENSHIP`
- `reference_date`: `2026-06-25`
- `pilot_jurisdiction`: `ro.tm.timisoara`
- `research_status`: `in_review`
- `trigger_ro`: Vreau să aflu dacă sunt deja cetățean român ori pe ce temei pot dobândi sau redobândi cetățenia română.

## Fapte de dezambiguizare

| fact | tip | valori / domeniu | obligatoriu | scop |
|---|---|---|---|---|
| `basis` | `enum` | `by_birth` / `adoption` / `naturalisation_art8` / `cultural_art8_1` / `sport_art8_2` / `reacquisition_art10` / `restoration_art11` / `unknown` | da | selectează temeiul legal |
| `age` | `number` | ani împliniți | da | majorat și excepția de limbă |
| `former_romanian_citizen` | `boolean` | `true` / `false` | da | art. 10/11 și excepția lingvistică |
| `descendant_degree` | `number` | 0 pentru titular, 1..n pentru descendent | da | limitele art. 10/11 |
| `loss_context` | `enum` | `not_applicable` / `involuntary` / `voluntary_or_unknown` | da | condiția art. 11 |
| `residence_status` | `enum` | `long_term_or_permanent` / `other` / `abroad` | da | art. 8 și canalul de depunere |
| `legal_residence_years` | `number` | ani | da | pragul art. 8 |
| `married_to_romanian_cohabiting` | `boolean` | `true` / `false` | da | ruta de 5 ani |
| `marriage_years` | `number` | ani de la căsătorie | da | pragul de 5 ani |
| `language_proof_status` | `enum` | `available` / `transition_pending` / `exempt` / `missing` | da | dovada limbii art. 10/11 |
| `annual_absence_over_6m` | `boolean` | `true` / `false` | da | calculul rezidenței art. 8 |
| `reduction_case_claimed` | `boolean` | `true` / `false` | da | reducerea posibilă cu până la 3 ani |

## Graf de proceduri

| intent_id | obligație | când | depends_on | rezultat |
|---|---|---|---|---|
| `ro.citizenship.basis.classify` | `mandatory` | mereu | — | temei legal selectat |
| `ro.citizenship.eligibility.evaluate` | `mandatory` | acordare/redobândire la cerere | ro.citizenship.basis.classify | eligibilitate preliminară |
| `ro.citizenship.file.prepare` | `conditional` | rută eligibilă | ro.citizenship.eligibility.evaluate | dosar pregătit |
| `ro.citizenship.application.file` | `conditional` | dosar complet | ro.citizenship.file.prepare | cerere ANC/consulară depusă |
| `ro.citizenship.oath.complete` | `conditional` | cerere aprobată | ro.citizenship.application.file | cetățenie dobândită/redobândită |

## Canale oficiale

| channel_id | nivel | utilizare | verificare |
|---|---|---|---|
| `ch.anc` | `national` | depunere personală și soluționare | Legea 21/1991 |
| `ch.romanian_mission` | `external` | depunere art. 8^1, 10, 11 în statul de domiciliu/reședință legală | Legea 21/1991, art. 13 |

## Limite deterministe

- Motorul separă dovada cetățeniei prin naștere de acordarea sau redobândirea la cerere.
- Evaluarea este preliminară; ANC decide pe baza probelor și a verificărilor legale.
- Nu se inventează cuantumul contravalorii cardului, programări sau liste operaționale care nu sunt ancorate într-o pagină oficială curentă.

## Politica de activare

`effective_from` din `rules.yaml` este data activării acestui ruleset de cercetare (2026-06-25), nu o afirmație despre data intrării în vigoare a fiecărui act normativ. Promovarea din `in_review` cere validare umană și reverificarea surselor cu freshness `critical`.
