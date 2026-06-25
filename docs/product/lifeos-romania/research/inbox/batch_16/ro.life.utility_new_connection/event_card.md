# Event Card — ro.life.utility_new_connection

- `batch_id`: `B16_UTILITY_NEW_CONNECTION`
- `reference_date`: `2026-06-25`
- `pilot_jurisdiction`: `ro.tm.timisoara` / `ro.tm`
- `research_status`: `in_review`
- `trigger_ro`: Vreau să racordez pentru prima dată imobilul la o utilitate și să obțin aprobările și contractele necesare înainte de lucrări.

## Fapte de dezambiguizare

| fact | tip | valori / domeniu | obligatoriu | scop |
|---|---|---|---|---|
| `utility_type` | `enum` | `electricity` / `natural_gas` / `water_sewer` / `district_heat` / `fixed_internet` / `unknown` | da | selectează fluxul |
| `pilot_area` | `enum` | `timisoara` / `timis_other` / `other_uat` / `unknown` | da | delimitează verificarea locală |
| `existing_connection_status` | `enum` | `none` / `existing_inactive` / `existing_active` / `unknown` | da | evită racordul duplicat |
| `applicant_role` | `enum` | `owner` / `tenant_user` / `company` / `association` / `developer` / `unknown` | da | selectează dreptul și reprezentarea |
| `title_or_use_document_status` | `enum` | `available` / `unavailable` / `unknown` | da | dovada asupra imobilului |
| `owner_consent_status` | `enum` | `available` / `unavailable` / `not_applicable` / `unknown` | da | cazul chiriașului/utilizatorului |
| `operator_code` | `enum` | `retele_electrice` / `aquatim` / `colterm` / `digi` / `orange` / `gas_operator_confirmed` / `other` / `unknown` | da | aplică numai sursa operatorului corect |
| `technical_approval_status` | `enum` | `not_requested` / `requested` / `issued` / `rejected` / `not_applicable` / `unknown` | da | ATR/aviz/răspuns tehnic |
| `network_extension_needed` | `enum` | `yes` / `no` / `unknown` | da | separă branșamentul de extindere |
| `operator_contract_status` | `enum` | `not_started` / `pending` / `prepared` / `signed` / `rejected` / `not_applicable` / `unknown` | da | contract de racordare/servicii specific utilității |

## Graf de proceduri

| intent_id | obligație | când | depends_on | rezultat |
|---|---|---|---|---|
| `ro.utility.connection.classify` | `mandatory` | mereu | — | utilitate și operator identificați |
| `ro.utility.technical.approval` | `conditional` | electricitate/gaze/apă/termoficare | clasificare + titlu | ATR/aviz emis |
| `ro.utility.operator.contract` | `conditional` | după aprobarea tehnică | aprobare | contract specific semnat/pregătit |
| `ro.utility.network.extension` | `conditional` | extindere necesară | soluție operator | documentație suplimentară |
| `ro.utility.connection.construction` | `conditional` | aprobare + contract | etapele anterioare | handoff la proiectare/execuție/recepție |

## Canale oficiale

| channel_id | nivel | utilizare | verificare |
|---|---|---|---|
| `ch.retele_electrice_connection` | `operator` | cerere/ATR și contract | numai dacă operatorul adresei este Rețele Electrice |
| `ch.aquatim_technical_approval` | `local_operator` | aviz apă/canal | Aquatim, Timiș |
| `ch.aquatim_contract` | `local_operator` | contract servicii | Aquatim |
| `ch.anre_gas_licence_registry` | `national` | identificare operator gaze | registru ANRE |
| `ch.colterm_connection` | `local_operator` | branșare/răspuns tehnic | checklist curent de reconfirmat |
| `ch.digi_new_service` | `provider` | contract și instalare internet fix | DIGI |

## Limite deterministe

- Evenimentul se oprește înainte de lucrări; execuția și recepția sunt în `ro.life.utility_connection_construction`.
- Termenele Rețele Electrice nu sunt extrapolate altui distribuitor.
- Taxa Aquatim de 84,70 lei este snapshot 2026-06-25 și se verifică pe factura curentă.
- Operatorul de gaze se identifică pentru adresă în registrul ANRE; nu este hardcodat pentru județul Timiș.
- Pagina COLTERM este veche și produce obligatoriu reconfirmare.

## Politica de activare

Rulesetul rămâne `in_review` până la verificarea umană a perechii adresă–operator și a documentelor generate de formularul live al operatorului.
