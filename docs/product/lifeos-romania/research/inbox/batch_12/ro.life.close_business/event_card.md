# Event Card — ro.life.close_business (life.close_business)

**Batch:** B12_CLOSE_BUSINESS  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Vreau să închid PFA-ul sau firma.”

## Limita evenimentului

Acoperă radierea PFA și alegerea rutei de dizolvare–lichidare–radiere pentru SRL. Nu tratează insolvența, concedierile, declarațiile fiscale finale sau arhivarea contabilă drept rezolvate automat.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `entity_type` | `enum` | pfa sau srl | da |
| `closure_reason` | `enum` | voluntary, death, judicial, other | da pentru PFA |
| `associates_agree_liquidation` | `boolean` | acord asupra lichidării patrimoniului | da pentru SRL |
| `liabilities_settled_or_regularized` | `boolean` | pasiv stins ori regularizat cu creditorii | da pentru ruta simultană |
| `remaining_assets_exist` | `boolean` | există active după plata creditorilor | condițional |
| `assets_distribution_unanimous` | `boolean` | distribuirea activelor este unanimă | condițional |
| `liquidation_income_tax_proof_available` | `boolean` | dovada fiscală pentru lichidare | condițional |
| `decision_date` | `date` | data hotărârii de dizolvare | SRL |
| `dissolution_registered` | `boolean` | mențiunea de dizolvare este operată | condițional |
| `local_commercial_agreement_exists` | `boolean` | există acord comercial local | condițional |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `file_pfa_deregistration` | radiere PFA | motiv și acte doveditoare |
| `approve_simultaneous_dissolution_liquidation` | hotărâre simultană SRL | acord și pasiv regularizat |
| `start_standard_dissolution_liquidation` | procedură etapizată | ruta simultană indisponibilă |
| `file_srl_dissolution_liquidation` | mențiuni ONRC | termen, semnatar, publicare |
| `cancel_timisoara_commercial_agreement` | anulare acord local | existența acordului |

## Reguli-cheie verificate

- PFA poate fi radiată prin voința titularului.
- Dizolvarea SRL deschide, de regulă, lichidarea și oprește operațiunile noi.
- Ruta simultană cere acord asupra patrimoniului și stingerea ori regularizarea pasivului.
- Distribuirea activelor rămase cere unanimitate și dovada fiscală prevăzută de lege.

## Canal pilot Timișoara / Timiș

În Timișoara, acordul comercial se anulează printr-un serviciu separat; radierea ONRC nu este modelată ca anulare locală automată.

## Guvernanță

„Închid firma” este un bundle. Motorul nu declară SRL radiat doar după hotărârea de dizolvare și nu permite ruta simplificată când faptele privind pasivul ori distribuirea activelor lipsesc.
