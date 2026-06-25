# Event Card — ro.life.vehicle_local_tax_declaration (life.vehicle_local_tax_declare)

**Batch:** R1A-veh3  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Trebuie să declar mașina la taxele locale".

> Acoperă declararea dobândirii unui mijloc de transport la organul fiscal local (impozit pe mijloacele de transport).

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `acquisition_date` | date | data dobândirii |
| `acquisition_type` | enum | `bought_ro`, `bought_eu`, `inherited`, `donated` |
| `weight_class` | enum | `under_12t`, `over_12t` |

## Reguli cheie (verificate)

- Declarare în **30 de zile** de la dobândire (Cod Fiscal, L227/2015); peste termen = amendă.
- Impozitul este datorat pentru tot anul fiscal de cine deține vehiculul la **31 decembrie** al anului anterior.
- Documente: declarație fiscală (ITL pentru sub/peste 12 t), CIV, act de dobândire, CI, certificat fiscal vânzător (în cazul facturii).

## Canale (Timișoara)

Direcția Fiscală a Municipiului Timișoara (`https://www.dfmt.ro`).
