# Event Card — ro.life.bought_used_vehicle_ro (life.vehicle_bought_used)

**Batch:** R1A-veh1  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Am cumpărat o mașină rulată înmatriculată în România".

> Acoperă cumpărătorul unui vehicul **deja înmatriculat în RO** (transcriere). Vehiculele aduse din UE/non-UE (primă înmatriculare) sunt evenimente separate.

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `contract_date` | date | data contractului de vânzare-cumpărare |
| `keeps_old_plates` | boolean | păstrează numerele vechi |
| `has_valid_itp` | boolean | ITP în termen de valabilitate |
| `has_rca` | boolean | RCA valabil pe numele cumpărătorului |

## Reguli cheie

- **Declarare fiscală** la organul fiscal local în **30 de zile** de la dobândire (verificat — Cod Fiscal, L227/2015).
- **Transcriere** la SPCRPCIV în **90 de zile** de la contract (în verificare față de Ordinul MAI 1501/2006).
- Transcrierea cere **CIV valabil + ITP în termen + RCA** pe numele cumpărătorului + dovada declarării fiscale.

## Canale (Timișoara)

Fiscal: Direcția Fiscală a Municipiului Timișoara (`https://www.dfmt.ro`). Înmatriculări: SPCRPCIV Timiș (`https://www.drpciv.ro`).
