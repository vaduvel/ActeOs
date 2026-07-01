# Event Card — ro.life.vehicle_local_tax_declaration (life.vehicle_local_tax_declare)

**Batch:** R1A-veh3  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-07-01

## Declanșator

„Declar sau scot vehiculul de la taxe locale".

> Acoperă obligația de declarare la organul fiscal local a vehiculului dobândit (impozit pe mijloacele de transport) și scoaterea din evidență la vânzare/radiere. Este perspectiva dinspre vehicul — ce se întâmplă la DRPCIV/SPCRPCIV și cum fluxul declarării fiscale pornește din înmatriculare.

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `acquisition_date` | date | data dobândirii |
| `acquisition_type` | enum | `bought_ro`, `bought_eu`, `inherited`, `donated` |
| `weight_class` | enum | `under_12t`, `over_12t` |

## Reguli cheie (verificate)

- Declarare la organul fiscal local în **30 de zile** de la dobândire (Cod Fiscal, L227/2015); peste termen = amendă.
- La transcrierea la SPCRPCIV/DRPCIV se cere **dovada declarării fiscale** sau certificatul de atestare fiscală.
- La vânzare/radiere, vehiculul trebuie **scos din evidența fiscală** și obținut certificatul fiscal.
- Impozitul este datorat pentru tot anul fiscal de cine deține vehiculul la **31 decembrie** al anului anterior.

## Documente necesare

- Declarație fiscală (formular ITL — sub 12 t sau peste 12 t)
- Carte de identitate a vehiculului (CIV)
- Actul de dobândire (contract vânzare-cumpărare, factură, certificat de moștenitor etc.)
- Actul de identitate al proprietarului (CI)
- Certificatul fiscal al vânzătorului (la cumpărare de la persoană fizică)
- Dovada radierii de la taxele locale (la achiziționarea unui vehicul de la o persoană fizică)

## Canale (Timișoara)

Direcția Fiscală a Municipiului Timișoara (`https://www.dfmt.ro`).  
SPCRPCIV Timiș pentru înmatriculări (`https://tm.prefectura.mai.gov.ro/permise-auto-si-inmatriculari/`).
