# Event Card — ro.life.pay_local_taxes

**Batch:** B13_PAY_LOCAL_TAXES  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** Municipiul Timișoara; pentru alt UAT există numai gap local explicit  
**Data de referință și acces:** 2026-06-25

## Declanșator

„Vreau să plătesc taxele și impozitele locale.”

## Limita evenimentului

Acoperă scadențele publicate pentru clădiri, terenuri și vehicule în Timișoara. Nu afișează cuantumuri, IBAN-uri sau bonificația 2026 fără sursa locală curentă validată.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `territory_id` | jurisdiction id | ex. `RO-TM-TIMISOARA` | selectează UAT competent |
| `tax_year` | integer | YYYY | previne reutilizarea bonificațiilor istorice |
| `tax_type` | enum | `building`, `land`, `vehicle`, `multiple`, `other` | selectează termenele publicate |
| `payment_stage` | enum | `before_march_31`, `between_installments`, `on_september_30`, `after_september_30` | arată care scadență este relevantă |
| `amount_verified_in_current_assessment` | boolean | `true`, `false` | blochează plata unei sume istorice |
| `payment_channel` | enum | `online`, `bank`, `cash` | cere validarea metodei și contului |
| `claims_early_payment_bonus` | boolean | `true`, `false` | detectează sursa expirată din 2021 |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| ro.local_tax.verify_roll | mandatory | — | sold și obiecte fiscale verificate |
| ro.local_tax.verify_deadline | mandatory | ro.local_tax.verify_roll | rata scadentă identificată |
| ro.local_tax.verify_channel | mandatory | ro.local_tax.verify_roll | cont și beneficiar validați |
| ro.local_tax.pay | mandatory | ro.local_tax.verify_channel | plată și dovadă păstrată |

## Canale oficiale

- **DFMT Timișoara — termene de plată** — https://www.dfmt.ro/taxe-si-impozite/termene-de-plata
- **DFMT Timișoara — modalități de plată** — https://www.dfmt.ro/taxe-si-impozite/modalitati-de-plata
- **DFMT — taxe locale 2026** — https://www.dfmt.ro/taxe-si-impozite/impozite-si-taxe-locale-aferente-anului-fiscal-2026

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este pragul de verificare al draftului, nu o afirmație despre data istorică de intrare în vigoare.
- Nicio sumă, taxă, reducere, penalitate sau listă de documente dinamică nu este calculată fără claim oficial aplicabil și fapt de intrare confirmat.
- Claim-urile `needs_confirmation`, `conflicting` ori `expired` nu pot produce singure un efect critic favorabil utilizatorului.
- Pentru alt UAT decât Timișoara, operaționalizarea locală rămâne `verified_with_local_gap`; regulile naționale sunt păstrate separat.

## Observație de integrare

Pagina oficială a termenelor amestecă scadențe recurente cu referințe explicite la 2021. Motorul acceptă scadențele, dar blochează bonificația și pragul de 50 lei pentru 2026.
