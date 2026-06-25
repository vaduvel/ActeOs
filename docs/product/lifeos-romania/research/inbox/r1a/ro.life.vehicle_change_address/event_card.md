# Event Card — ro.life.vehicle_change_address (life.vehicle_change_address)

**Batch:** R1A-veh5  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Mi-am schimbat domiciliul și trebuie să actualizez adresa din talon (certificatul de înmatriculare)".

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `move_date` | date | data schimbării domiciliului |
| `domicile_changed` | boolean | s-a schimbat domiciliul din CI |
| `has_rca` | boolean | RCA valabil |

## Reguli cheie

- La schimbarea domiciliului se eliberează un **nou certificat de înmatriculare** cu adresa actualizată, orientativ în **30 de zile** (în verificare față de Ordinul 1501/2006).
- Documente: cerere, CI cu adresa nouă, certificatul de înmatriculare vechi, CIV, RCA valabil, dovada plății.
- Procedura confirmată de DGPCI: eliberarea unui nou certificat când se modifică date.

## Canale (Timișoara)

SPCRPCIV Timiș (`https://www.drpciv.ro`).
