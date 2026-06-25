# Event Card — ro.life.utility_connection_construction

- `batch_id`: `B16_UTILITY_CONNECTION_CONSTRUCTION`
- `reference_date`: `2026-06-25`
- `pilot_jurisdiction`: `ro.tm.timisoara` / `ro.tm`
- `research_status`: `in_review`
- `trigger_ro`: Am aprobarea și contractul de racordare și vreau să proiectez, execut, recepționez și activez legal branșamentul/racordul.

## Fapte de dezambiguizare

| fact | tip | valori / domeniu | obligatoriu | scop |
|---|---|---|---|---|
| `utility_type` | `enum` | `electricity` / `natural_gas` / `water_sewer` / `district_heat` / `fixed_internet` / `unknown` | da | selectează regulile tehnice |
| `pilot_area` | `enum` | `timisoara` / `timis_other` / `other_uat` / `unknown` | da | delimitează regulile locale |
| `operator_code` | `enum` | `retele_electrice` / `aquatim` / `colterm` / `digi` / `orange` / `gas_operator_confirmed` / `other` / `unknown` | da | previne checklistul operatorului greșit |
| `technical_approval_status` | `enum` | `issued` / `missing` / `changed_or_expired` / `not_applicable` / `unknown` | da | validează ATR/avizul |
| `connection_contract_status` | `enum` | `signed` / `prepared` / `unsigned` / `not_applicable` / `unknown` | da | validează contractul anterior lucrării |
| `design_status` | `enum` | `approved` / `pending` / `missing` / `not_applicable` / `unknown` | da | proiect tehnic |
| `permit_status` | `enum` | `obtained` / `pending` / `missing` / `not_required_confirmed` / `unknown` | da | autorizații și acorduri |
| `executor_authorization_status` | `enum` | `verified` / `unverified` / `not_applicable` / `unknown` | da | atestare/autorizație executant |
| `works_status` | `enum` | `not_started` / `in_progress` / `completed` / `unknown` | da | etapa fizică |
| `reception_status` | `enum` | `pending` / `accepted` / `rejected` / `not_applicable` / `unknown` | da | recepție și remediere |
| `user_installation_file_status` | `enum` | `complete` / `incomplete` / `not_applicable` / `unknown` | da | dosar instalație utilizare electrică |
| `supply_contract_status` | `enum` | `signed` / `unsigned` / `not_applicable` / `unknown` | da | activare după recepție |
| `network_extension_needed` | `enum` | `yes` / `no` / `unknown` | da | extindere vs. branșament simplu |

## Graf de proceduri

| intent_id | obligație | când | depends_on | rezultat |
|---|---|---|---|---|
| `ro.utility.construction.precheck` | `mandatory` | înainte de lucrări | aprobare + contract | precondiții validate |
| `ro.utility.design.execute` | `conditional` | proiect/autorizații/executant valide | precheck | lucrare executată |
| `ro.utility.reception` | `conditional` | lucrare finalizată | execuție | recepție acceptată sau remedieri |
| `ro.utility.supply.activate` | `conditional` | recepție acceptată | dosar/contract furnizare | contor, punere în tensiune sau activare |
| `ro.utility.extension` | `conditional` | extindere rețea | soluție operator | documentație și lucrări suplimentare |

## Canale oficiale

| channel_id | nivel | utilizare | verificare |
|---|---|---|---|
| `ch.aquatim_reception` | `local_operator` | recepție și sigilare apă/canal | Aquatim |
| `ch.colterm_connection` | `local_operator` | condiții tehnice și recepție termoficare | reconfirmare 2026 |
| `ch.anre_gas_licence_registry` | `national` | verificare autorizații gaze | ANRE |
| `ch.retele_electrice_connection` | `operator` | execuție, recepție, certificat, contor | numai operator confirmat |
| `ch.digi_new_service` | `provider` | programare și instalare | DIGI |

## Limite deterministe

- O durată etichetată de operator ca „estimată” rămâne estimată; nu este convertită în termen legal.
- Limita de 90 de zile la electricitate se aplică numai situației publicate în care operatorul gestionează lucrările după avize.
- Aquatim nu este prezentat ca proiectant sau executant.
- Tipul autorizației ANRE pentru gaze se potrivește exact activității; PDIB/EDIB nu sunt substituite automat cu PDSB/EDSB.
- Pentru COLTERM și alți operatori locali, condițiile curente rămân obligatoriu de confirmat.

## Politica de activare

Rulesetul rămâne `in_review`; activarea pentru un caz real cere verificarea documentelor emise pentru adresă și a autorizațiilor executantului la data contractării.
