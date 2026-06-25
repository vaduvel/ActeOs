# Event Card — ro.life.declare_rental_income

**Batch:** B13_DECLARE_RENTAL_INCOME  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** România; administrare fiscală centrală ANAF  
**Data de referință și acces:** 2026-06-25

## Declanșator

„Vreau să declar contractul și venitul din chirie.”

## Limita evenimentului

Coordonează înregistrarea contractului prin C168 și evaluarea declarației fiscale individuale. Nu calculează impozitul, CASS sau termenul C168 fără temei fiscal curent verificat.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `landlord_is_individual` | boolean | `true`, `false` | păstrează evenimentul în sfera persoanei fizice |
| `contract_status` | enum | `new`, `modified`, `terminated`, `none`, `unknown` | alege cererea inițială, modificarea sau încetarea |
| `contract_signed` | boolean | `true`, `false` | previne încărcarea unui draft |
| `contract_attachment_zip_ready` | boolean | `true`, `false` | atașamentul ZIP este obligatoriu tehnic |
| `c168_already_submitted` | boolean | `true`, `false` | separă inițiala de rectificare/actualizare |
| `has_reportable_rental_income` | boolean | `true`, `false` | poate declanșa D212 |
| `tenant_type` | enum | `individual`, `legal_entity`, `unknown` | poate schimba tratamentul fiscal |
| `withholding_at_source` | boolean | `true`, `false` | necesită verificarea obligațiilor rămase |
| `tax_year` | integer | YYYY | selectează versiunea și anul fiscal |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| ro.tax.rental.register_contract | conditional | — | contract înregistrat/actualizat prin C168 |
| ro.tax.rental.assess_income | mandatory | — | obligația fiscală a venitului stabilită |
| ro.tax.rental.file_d212 | conditional | ro.tax.rental.assess_income | venit declarat în D212 când este aplicabil |

## Canale oficiale

- **ANAF — C168** — https://static.anaf.ro/static/10/Anaf/Declaratii_R/168.html
- **ANAF — formular web C168** — https://www.anaf.ro/declaratii/c168
- **ANAF — structura C168 2026** — https://static.anaf.ro/static/10/Anaf/Declaratii_R/AplicatiiDec/structura_C168_2026_260326.pdf

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este pragul de verificare al draftului, nu o afirmație despre data istorică de intrare în vigoare.
- Nicio sumă, taxă, reducere, penalitate sau listă de documente dinamică nu este calculată fără claim oficial aplicabil și fapt de intrare confirmat.
- Claim-urile `needs_confirmation`, `conflicting` ori `expired` nu pot produce singure un efect critic favorabil utilizatorului.
- Pentru alt UAT decât Timișoara, operaționalizarea locală rămâne `verified_with_local_gap`; regulile naționale sunt păstrate separat.

## Observație de integrare

C168 și D212 sunt două proceduri diferite. Un contract înregistrat nu dovedește automat că obligația privind venitul a fost rezolvată.
