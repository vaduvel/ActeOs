# Event Card — ro.life.minor_passport (life.minor_passport)

**Batch:** R1B-2  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Vreau să fac pașaport pentru copilul meu".

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `minor_age` | number | vârsta minorului |
| `passport_type` | enum | `electronic` / `temporary` |
| `both_parents_consent` | boolean | ambii părinți prezenți/consimt |
| `has_single_parent_doc` | boolean | procură/acord scris/hotărâre încredințare/act deces |
| `minor_present` | boolean | minorul este prezent la depunere |

## Reguli cheie (sursă primară DGP)

- **Documente**: certificatul de naștere al minorului în original, actele de identitate ale părinților valabile, dovada plății, pașaportul anterior al minorului dacă există.
- **Sub 14 ani**: cererea de **ambii părinți** (sau un părinte cu procură specială/acord scris al celuilalt; reprezentant legal).
- **Prezența minorului și a părinților obligatorie**; dacă minorul nu e prezent (temporar) → **2 fotografii 3,5 × 4,5 cm**.
- **Peste 14 ani**: minorul își ridică pașaportul **personal**, însoțit de un părinte, cu CI valabilă.
- **Valabilitate**: 3 ani (<12 ani), 5 ani (12–18 ani). **Taxe**: 234 lei (<12) / 258 lei (≥12) electronic; 96 lei temporar.

## Canal (Timișoara)

SPCEEPS Timiș — Iulius Town, Etaj 1; programare `https://hub.mai.gov.ro/epasapoarte/programari/create?judet=TM`.
