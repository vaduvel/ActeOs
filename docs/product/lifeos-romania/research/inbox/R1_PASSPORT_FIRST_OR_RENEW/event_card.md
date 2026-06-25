# Event Card — ro.life.passport_first_or_renew (life.passport_first_or_renew)

**Batch:** R1B-1  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Vreau să-mi fac / reînnoiesc pașaportul (simplu electronic sau temporar)".

> Pentru minori, vezi evenimentul separat `life.minor_passport` (acordul părinților, valabilități diferite).

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `applicant_age` | number | vârsta solicitantului |
| `passport_type` | enum | `electronic` / `temporary` |
| `has_valid_id` | boolean | CI/CIP/BI valabilă în original |
| `has_previous_passport` | boolean | deține pașaport anterior |

## Reguli cheie (sursă primară DGP)

- **Documente**: CI/CIP/BI valabilă în original (CIP însoțită de certificat de naștere), dovada plății, pașaportul anterior dacă există.
- **Valabilitate pașaport electronic**: 3 ani (<12 ani), 5 ani (12–18 ani), **10 ani (>18 ani)**; temporar = **12 luni**.
- **Taxe**: electronic 258 lei (≥12 ani) / 234 lei (<12 ani); temporar 96 lei (plată CEC Bank sau Ghiseul.ro).
- **Programare doar pe HUB MAI**; cererile se depun **doar personal**.

## Canal (Timișoara)

SPCEEPS Timiș — Iulius Town (Iulius Mall), Etaj 1, Timișoara; tel. 0256.227292; programare `https://hub.mai.gov.ro/epasapoarte/programari/create?judet=TM`.
