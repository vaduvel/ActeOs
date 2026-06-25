# Event Card — ro.life.change_heat_holder

- `batch_id`: `B16_CHANGE_HEAT_HOLDER`
- `reference_date`: `2026-06-25`
- `pilot_jurisdiction`: `ro.tm.timisoara`
- `research_status`: `in_review`
- `trigger_ro`: Vreau să trec contractul de termoficare pe alt titular sau să actualizez reprezentantul contractual.

## Fapte de dezambiguizare

| fact | tip | valori / domeniu | obligatoriu | scop |
|---|---|---|---|---|
| `heating_service_type` | `enum` | `district_heating` / `individual_gas` / `electric_heating` / `unknown` | da | evită aplicarea procedurii COLTERM altui serviciu |
| `provider_scope` | `enum` | `colterm_timisoara` / `other_local_operator` / `unknown` | da | selectează operatorul local |
| `contract_arrangement` | `enum` | `direct_individual` / `owners_association` / `company` / `unknown` | da | selectează categoria contractuală |
| `change_reason` | `enum` | `property_transfer` / `tenant_change` / `association_admin_change` / `legal_successor` / `data_correction` / `unknown` | da | separă schimbarea titularului de simpla actualizare |
| `new_holder_role` | `enum` | `owner` / `tenant_user` / `owners_association` / `company` / `legal_successor` / `unknown` | da | determină dovada dreptului și reprezentarea |
| `new_connection_needed` | `enum` | `yes` / `no` / `unknown` | da | separă contractul de racordarea tehnică |
| `ownership_or_use_evidence_status` | `enum` | `available` / `unavailable` / `unknown` | da | verifică dovada proprietății sau folosinței |
| `identity_or_representation_status` | `enum` | `available` / `unavailable` / `unknown` | da | verifică identitatea/reprezentarea |
| `provider_current_checklist_confirmed` | `enum` | `confirmed` / `not_confirmed` / `unknown` | da | blochează folosirea automată a unei pagini vechi |

## Graf de proceduri

| intent_id | obligație | când | depends_on | rezultat |
|---|---|---|---|---|
| `ro.heat.holder.classify` | `mandatory` | mereu | — | serviciu, operator și contract identificate |
| `ro.heat.colterm.individual.update` | `conditional` | contract direct, proprietar | clasificare + dovezi | cerere și documente pregătite |
| `ro.heat.colterm.association.admin` | `conditional` | schimbare administrator | clasificare | notificare către furnizor |
| `ro.heat.colterm.company.update` | `conditional` | societate | clasificare + drept de folosință | dosar societate pregătit |
| `ro.utility.new_connection` | `conditional` | branșament nou | clasificare | rută tehnică separată |

## Canale oficiale

| channel_id | nivel | utilizare | verificare |
|---|---|---|---|
| `ch.colterm_contracts` | `local_operator` | confirmare checklist și depunere Timișoara | COLTERM, obligatoriu înainte de depunere |
| `ch.local_heat_operator` | `local_operator` | alt UAT/operator | `verified_with_local_gap` |

## Limite deterministe

- Nu aplică termoficarea contractelor individuale de gaze sau electricitate.
- Lista COLTERM identificată este datată 2016; documentele sale sunt indicii oficiale, nu un checklist 2026 auto-validat.
- Nu declară taxă, termen, adresă sau program curent fără reconfirmare.
- Branșamentul nou este un eveniment separat de schimbarea titularului.

## Politica de activare

`effective_from` este data activării rulesetului, nu data intrării în vigoare a paginii COLTERM. Promovarea din `in_review` cere confirmarea checklistului live de către operator.
