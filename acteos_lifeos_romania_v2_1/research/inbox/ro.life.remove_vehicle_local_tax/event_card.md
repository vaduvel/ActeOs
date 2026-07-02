# Event Card — ro.life.remove_vehicle_local_tax (life.vehicle_local_tax_remove)

**Batch:** R1A-tax7
**Status:** research_inbox (neaprobat)
**Pilot:** `ro.tm.timisoara`
**Accessed_at:** 2026-07-01

## Declanșator

„Scot vehiculul de la taxele locale (l-am vândut, l-am donat, s-a dezmembrat sau a fost furat)".

> Acoperă obligația de scoatere din evidența fiscală locală a unui mijloc de transport, în special când vehiculul este înstrăinat sau radiat. Include eliberarea certificatului de atestare fiscală necesar pentru transcrierea/radierea la SPCRPCIV.

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `removal_reason` | enum | `sold`, `donated`, `deregistered`, `scrap`, `stolen_lost_total`, `transferred_abroad` |
| `removal_date` | date | data înstrăinării / pierderii |
| `had_fiscal_arrears` | enum | `yes`, `no`, `unknown` |
| `tax_certificate_needed` | enum | `for_transcription`, `for_radiation`, `for_archive`, `no` |

## Reguli cheie (verificate)

- **Termen de scoatere:** în **30 de zile** de la data înstrăinării/pierderii (Cod Fiscal, L227/2015 — corespunzător declarării).
- **Documente la scoatere:** declarație fiscală de scoatere (ITL), act de înstrăinare (contract vânzare-cumpărare, proces-verbal de dezmembrare, certificat de moștenitor, hotărâre judecătorească etc.), BI/CI al proprietarului, cartea de identitate a vehiculului (CIV) în original sau dovada radierii.
- **Certificat de atestare fiscală:** se eliberează la cerere de organul fiscal local; este document necesar pentru transcrierea vehiculului la SPCRPCIV la cumpărare de la PF.
- **Impozitul rămâne datorat** de cel care deținea vehiculul la **31 decembrie** al anului anterior, chiar dacă vânzarea/radierea survine în cursul anului fiscal.

## Documente necesare

- Declarație fiscală pentru scoaterea din evidență (ITL specifică).
- Act de înstrăinare/dovada radierii (act autentic).
- Actul de identitate al proprietarului.
- Certificat de atestare fiscală (dacă e cerut de SPCRPCIV sau de cumpărător).

## Canale (Timișoara)

Direcția Fiscală a Municipiului Timișoara (`https://www.dfmt.ro`).
SPCRPCIV Timiș pentru transcriere / radiere (`https://tm.prefectura.mai.gov.ro/permise-auto-si-inmatriculari/`).
