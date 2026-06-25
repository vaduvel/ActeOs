# Event Card — ro.life.local_tax_certificate (life.local_tax_certificate)

**Batch:** R1A-6  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Am nevoie de un certificat de atestare fiscală (de la taxele locale)".

> Certificat emis de organul fiscal local (Direcția Fiscală / DITL) care arată obligațiile de plată la bugetul local. Necesar la înstrăinare imobil/vehicul, succesiune sau la cerere.

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `purpose` | enum | `sale_property` / `sale_vehicle` / `succession` / `general` |
| `is_for_third_party` | boolean | solicitat prin împuternicit/notar |
| `is_succession` | boolean | pentru dezbatere succesorală |

## Reguli cheie

- Cerere pe **formular ITL010/2016** + act de identitate (copie+original).
- Pentru succesiune: certificat de deces, adresă notariat, acte care atestă calitatea.
- Pentru împuternicit: împuternicire în original sau copie legalizată + CI împuternicit.
- Emitere locală orientativă **≤ 2 zile lucrătoare**; valabilitate orientativă **30 de zile** pentru persoane fizice (în verificare față de Codul de procedură fiscală, L207/2015).

## Canale (Timișoara)

Direcția Fiscală a Municipiului Timișoara — `https://www.dfmt.ro`, online `https://plata.dfmt.ro`; din 2025 unele certificate se emit **automat**.
