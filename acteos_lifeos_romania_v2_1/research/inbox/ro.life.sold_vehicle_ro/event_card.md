# Event Card — ro.life.sold_vehicle_ro (life.vehicle_sold)

**Batch:** R1A-veh2  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Mi-am vândut mașina".

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `contract_date` | date | data contractului de vânzare-cumpărare |
| `has_fiscal_certificate` | boolean | are certificat de atestare fiscală / viză pe contract |
| `sale_completed` | boolean | vânzarea a fost finalizată |

## Reguli cheie

- Înainte de vânzare: contract în **5 exemplare**, vizate de organul fiscal de la domiciliul vânzătorului (viza atestă lipsa datoriilor; ține loc de certificat de atestare fiscală, valabil **30 de zile**).
- După vânzare: vânzătorul depune **declarația de scoatere din evidența fiscală** (ITL016) la organul fiscal local.
- Riscul fiscal rămâne la vânzător cât timp vehiculul nu este scos din evidență.

## Canale (Timișoara)

Direcția Fiscală a Municipiului Timișoara (`https://www.dfmt.ro`).
