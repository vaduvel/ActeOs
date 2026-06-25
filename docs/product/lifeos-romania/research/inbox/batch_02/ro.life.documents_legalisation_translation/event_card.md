# Event Card — ro.life.documents_legalisation_translation

- `batch_id`: `B02_DOCUMENTS_LEGALISATION_TRANSLATION`
- `reference_date`: `2026-06-25`
- `pilot_jurisdiction`: `ro.tm.timisoara`
- `research_status`: `in_review`
- `trigger_ro`: Am un document românesc sau străin și trebuie să aflu dacă îi trebuie apostilă, supralegalizare ori traducere pentru utilizarea dorită.

## Fapte de dezambiguizare

| fact | tip | valori / domeniu | obligatoriu | scop |
|---|---|---|---|---|
| `document_direction` | `enum` | `ro_to_foreign` / `foreign_to_ro` | da | stabilește sensul circuitului |
| `issuing_country_group` | `enum` | `eu` / `hague_non_eu` / `non_hague` / `unknown` | da | regimul statului emitent |
| `receiving_country_group` | `enum` | `eu` / `hague_non_eu` / `non_hague` / `unknown` | da | regimul statului primitor |
| `document_subject` | `enum` | `covered_public_matter` / `other_public_document` / `private_document` | da | delimitează simplificarea UE |
| `hague_pair_status` | `enum|boolean` | `true` / `false` / `unknown` | da | confirmă Convenția pentru perechea concretă |
| `receiving_language_status` | `enum` | `accepted` / `not_accepted` / `unknown` | da | decide ramura de traducere |
| `multilingual_form_status` | `enum` | `available` / `unavailable` / `unknown` | da | evită traducerea inutilă |
| `destination_requirements_confirmed` | `boolean` | `true` / `false` | da | gate critic al autorității primitoare |
| `romanian_document_authority_class` | `enum` | `administrative` / `judicial_notarial` / `unknown` | da | alege autoritatea română competentă |
| `preverification_completed` | `boolean` | `true` / `false` | da | ramura rapidă locală |

## Graf de proceduri

| intent_id | obligație | când | depends_on | rezultat |
|---|---|---|---|---|
| `ro.documents.formality.classify` | `mandatory` | mereu | — | regim juridic identificat |
| `ro.documents.eu_public_document.use` | `conditional` | UE→UE și materie acoperită | ro.documents.formality.classify | circulație fără apostilă pentru autenticitate |
| `ro.documents.apostille.obtain` | `conditional` | Convenția Haga confirmată | ro.documents.formality.classify | apostilă de la autoritatea competentă |
| `ro.documents.supralegalisation.confirm` | `conditional` | non-Haga sau necunoscut | ro.documents.formality.classify | lanț confirmat, nu presupus |
| `ro.documents.translation.confirm` | `conditional` | limba nu este acceptată | ro.documents.formality.classify | traducere/formular multilingv potrivit |

## Canale oficiale

| channel_id | nivel | utilizare | verificare |
|---|---|---|---|
| `ch.eu_your_europe_public_documents` | `eu` | regimul UE pentru documente publice | oficial |
| `ch.hcch_apostille_status` | `international` | verificarea perechii de state | oficial |
| `ch.prefectura_timis_apostila` | `ro.tm` | apostilarea actelor administrative românești | oficial; programul se reverifică |

## Limite deterministe

- Motorul nu deduce efectele juridice recunoscute din simpla autenticitate a documentului.
- Lista exactă de acte apostilabile și autoritatea competentă depind de natura emitentului; actele judiciare/notariale nu sunt trimise automat la prefectură.
- Nu este generată o taxă pentru traducere, notar sau supralegalizare fără tarif oficial aplicabil cazului concret.

## Politica de activare

`effective_from` din `rules.yaml` este data activării acestui ruleset de cercetare (2026-06-25), nu o afirmație despre data intrării în vigoare a fiecărui act normativ. Promovarea din `in_review` cere validare umană și reverificarea surselor cu freshness `critical`.
