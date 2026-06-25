# Event Card — ro.life.change_internet_holder

- `batch_id`: `B16_CHANGE_INTERNET_HOLDER`
- `reference_date`: `2026-06-25`
- `pilot_jurisdiction`: `ro.tm.timisoara`
- `research_status`: `in_review`
- `trigger_ro`: Vreau să trec contractul de internet fix pe alt titular ori să actualizez beneficiarul.

## Fapte de dezambiguizare

| fact | tip | valori / domeniu | obligatoriu | scop |
|---|---|---|---|---|
| `provider` | `enum` | `orange` / `digi` / `vodafone` / `other` / `unknown` | da | selectează procedura contractuală |
| `customer_type` | `enum` | `individual` / `business` / `unknown` | da | selectează canalul și reprezentarea |
| `service_scope` | `enum` | `fixed_internet` / `fixed_bundle` / `mobile_only` / `unknown` | da | separă instalarea fixă de serviciul mobil |
| `change_reason` | `enum` | `voluntary_transfer` / `property_transfer` / `legal_successor` / `data_correction` / `address_move` / `unknown` | da | selectează cesiune, succesiune, corectare sau relocare |
| `same_service_address` | `enum` | `yes` / `no` / `unknown` | da | detectează instalarea/relocarea |
| `current_holder_participation` | `enum` | `available` / `unavailable` / `deceased` / `unknown` | da | verifică consimțământul ori succesiunea |
| `new_holder_identity_status` | `enum` | `available` / `unavailable` / `unknown` | da | identificarea noului client |
| `representation_mode` | `enum` | `personal` / `power_of_attorney` / `none` / `unknown` | da | validează solicitantul |
| `equipment_inventory_status` | `enum` | `complete` / `incomplete` / `not_applicable` / `unknown` | da | custodie, chirie, returnare, mutare |
| `provider_approval_status` | `enum` | `granted` / `pending` / `denied` / `not_requested` / `not_applicable` / `unknown` | da | efectul cesiunii |

## Graf de proceduri

| intent_id | obligație | când | depends_on | rezultat |
|---|---|---|---|---|
| `ro.internet.holder.classify` | `mandatory` | mereu | — | furnizor și tip schimbare identificate |
| `ro.orange.contract.assignment` | `conditional` | Orange, cesiune | acord operator | contract tip semnat |
| `ro.digi.beneficiary.change` | `conditional` | DIGI, schimbare beneficiar | prezență/procură | formular sau act adițional |
| `ro.internet.legal.successor` | `conditional` | deces/succesiune | dovada succesorului | rută furnizor confirmată |
| `ro.internet.service.relocation` | `conditional` | altă adresă | acoperire și instalare | relocare separată |

## Canale oficiale

| channel_id | nivel | utilizare | verificare |
|---|---|---|---|
| `ch.orange_assignment` | `provider` | acord și contract tip de cesiune | Orange |
| `ch.orange_shop` | `provider` | cesiune persoană fizică | Orange/partener |
| `ch.orange_business` | `provider` | rută persoană juridică | segment de client de confirmat |
| `ch.digi_customer_relations` | `provider` | formular/act adițional și succesiune | DIGI |

## Limite deterministe

- Nu există formular universal între furnizori.
- Pentru Orange, cesiunea nu este finală fără acordul scris al operatorului.
- Pentru DIGI, condițiile curente ancorează modalitatea și data efectului, dar nu publică în extrasul verificat un checklist complet de acte.
- Vodafone și alți furnizori rămân `needs_confirmation` în acest batch.

## Politica de activare

Rulesetul este `in_review`. Orice taxă, sold, perioadă minimă, penalitate, echipament sau excepție contractuală se citește din contractul live și se reconfirmă la furnizor.
