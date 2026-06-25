# Event Card — ro.life.criminal_record_certificate (life.criminal_record_certificate)

**Batch:** R1B-3  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Am nevoie de cazier judiciar".

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `applicant_age` | number | vârsta solicitantului |
| `channel_pref` | enum | `online` / `counter` |
| `is_for_third_party` | boolean | depus de împuternicit |
| `citizen_type` | enum | `ro_citizen` / `eu_citizen` / `third_country` |

## Reguli cheie (sursă primară Poliția Română / HUB MAI)

- **Documente**: act de identitate în original, valabil + **cerere-tip** (se poate tipări din sistem la ghișeu). Vârsta minimă **14 ani**.
- **Online** prin `hub.mai.gov.ro` și `ghiseul.ro` (interconectate), gratuit pentru persoane fizice cetățeni români neînregistrați în ROCRIS.
- **Eliberare** (cetățeni români, format fizic): **pe loc sau în cel mult 3 zile lucrătoare**; cetățeni străini ~**30 de zile**.
- **Valabilitate**: **6 luni** de la eliberare.
- **Împuternicit**: procură notarială + actul de identitate al împuternicitului.

## Canale (Timișoara)

- Ghișeu: **IPJ Timiș** — Serviciul Cazier Judiciar; ghișee în județ: Lugoj, Sânnicolau Mare, Jimbolia, Deta.
- Online: `https://hub.mai.gov.ro` / `https://www.ghiseul.ro`.
