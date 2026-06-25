# Event Card — ro.life.foreign_document_recognition

- `batch_id`: `B02_FOREIGN_DOCUMENT_RECOGNITION`
- `reference_date`: `2026-06-25`
- `pilot_jurisdiction`: `ro.tm.timisoara`
- `research_status`: `in_review`
- `trigger_ro`: Am un document emis în străinătate și trebuie să aflu cine îi recunoaște studiile, calificarea, starea civilă sau efectul juridic în România.

## Fapte de dezambiguizare

| fact | tip | valori / domeniu | obligatoriu | scop |
|---|---|---|---|---|
| `document_category` | `enum` | `preuniversity_studies` / `university_studies` / `professional_qualification` / `civil_status` / `court_judgment` / `other` | da | alege autoritatea competentă |
| `intended_use` | `enum` | `continue_studies` / `employment` / `regulated_practice` / `administrative_use` / `other` | da | separă recunoașterea academică de cea profesională |
| `issuing_country_group` | `enum` | `eu_see_ch` / `third_country` | da | ramura automată academică |
| `profession_regulated` | `boolean|enum` | `true` / `false` / `unknown` | da | autoritatea profesională |
| `document_level` | `enum` | `bac_vocational_postsecondary` / `bachelor_master_doctor` / `other` | da | termenul și procedura CNRED |

## Graf de proceduri

| intent_id | obligație | când | depends_on | rezultat |
|---|---|---|---|---|
| `ro.foreign_document.classify` | `mandatory` | mereu | — | categoria și scopul stabilite |
| `ro.education.preuniversity.recognise` | `conditional` | studii preuniversitare | ro.foreign_document.classify | cerere CNRED |
| `ro.education.university.recognise` | `conditional` | studii universitare | ro.foreign_document.classify | cerere CNRED |
| `ro.profession.foreign_qualification.recognise` | `conditional` | profesie reglementată | ro.foreign_document.classify | autoritate profesională identificată |
| `ro.civil_status.foreign_act.route` | `conditional` | stare civilă | ro.foreign_document.classify | transcriere/înregistrare, nu CNRED |

## Canale oficiale

| channel_id | nivel | utilizare | verificare |
|---|---|---|---|
| `ch.cnred_preuniversity` | `national` | recunoaștere studii preuniversitare | oficial CNRED |
| `ch.cnred_university` | `national` | recunoaștere studii universitare | oficial CNRED |
| `ch.cnred_professional_assistance` | `national/eu` | identificare profesie și autoritate competentă | oficial CNRED |

## Limite deterministe

- Apostila dovedește autenticitatea formală, nu produce recunoaștere academică sau drept de practică.
- Motorul nu trimite actele de stare civilă ori hotărârile judecătorești la CNRED.
- Termenul de 30 de zile lucrătoare este aplicat numai categoriilor pentru care pagina CNRED îl publică.

## Politica de activare

`effective_from` din `rules.yaml` este data activării acestui ruleset de cercetare (2026-06-25), nu o afirmație despre data intrării în vigoare a fiecărui act normativ. Promovarea din `in_review` cere validare umană și reverificarea surselor cu freshness `critical`.
