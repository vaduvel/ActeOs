# Event Card — ro.life.company_vehicle_change

**Batch:** B13_COMPANY_VEHICLE_CHANGE  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** România + pilot Timișoara / județul Timiș  
**Data de referință și acces:** 2026-06-25

## Declanșator

„Am cumpărat, vândut sau modificat datele unei mașini a firmei.”

## Limita evenimentului

Coordonează evidența fiscală locală și operațiunea de înmatriculare/transcriere pentru vehiculele persoanei juridice. Nu stabilește impozitul auto și nu inventează lista de documente pentru import ori leasing.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `change_type` | enum | `acquisition_ro_registered`, `sale`, `company_name_change`, `company_address_change`, `end_leasing`, `import_eu`, `import_non_eu`, `unknown` | alege subprocedurile fiscale și de înmatriculare |
| `territory_id` | jurisdiction_id | ex. `RO-TM-TIMISOARA` | aplică pilotul local fără extrapolare |
| `days_since_acquisition` | integer | 0+ | testează termenul de transcriere de 90 zile |
| `tax_record_updated` | boolean | `true`, `false` | contează pentru operațiunea la ghișeu |
| `submission_channel` | enum | `online`, `counter` | schimbă cerința certificatului fiscal în Timiș |
| `fiscal_clearance_available` | boolean | `true`, `false` | blochează ruta online când certificatul lipsește |
| `representative_used` | boolean | `true`, `false` | activează împuternicirea |
| `documents_case_selected` | boolean | `true`, `false` | lista locală depinde de situația selectată |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| ro.vehicle.company.local_tax_update | conditional | — | evidență fiscală locală actualizată |
| ro.vehicle.company.registration_update | conditional | ro.vehicle.company.local_tax_update | transcriere/radiere/modificare certificat rezolvată |
| ro.vehicle.company.fiscal_clearance | conditional | ro.vehicle.company.local_tax_update | certificat fiscal pregătit când canalul îl cere |

## Canale oficiale

- **Primăria Timișoara — declarare vehicul PJ** — https://servicii.primariatm.ro/dfmt-pj-declararea-mijloacelor-de-transport
- **Primăria Timișoara — înstrăinare vehicul** — https://servicii.primariatm.ro/dfmt-pj-declararea-instrainarii-mijloc-transport
- **Prefectura Timiș — înmatriculări** — https://tm.prefectura.mai.gov.ro/permise-auto-si-inmatriculari/
- **Portal Legislativ — OUG nr. 195/2002** — https://legislatie.just.ro/Public/DetaliiDocument/41006

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este pragul de verificare al draftului, nu o afirmație despre data istorică de intrare în vigoare.
- Nicio sumă, taxă, reducere, penalitate sau listă de documente dinamică nu este calculată fără claim oficial aplicabil și fapt de intrare confirmat.
- Claim-urile `needs_confirmation`, `conflicting` ori `expired` nu pot produce singure un efect critic favorabil utilizatorului.
- Pentru alt UAT decât Timișoara, operaționalizarea locală rămâne `verified_with_local_gap`; regulile naționale sunt păstrate separat.

## Observație de integrare

Evenimentul este un `bundle_goal`: motorul păstrează distinctă evidența fiscală locală de evidența națională a înmatriculării și ordonează dependențele.
