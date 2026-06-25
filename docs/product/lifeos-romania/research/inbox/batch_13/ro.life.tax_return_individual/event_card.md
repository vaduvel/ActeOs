# Event Card — ro.life.tax_return_individual

**Batch:** B13_TAX_RETURN_INDIVIDUAL  
**Status:** `research_inbox` — neaprobat; nu se promovează automat în producție  
**Pilot teritorial:** România; formular național ANAF  
**Data de referință și acces:** 2026-06-25

## Declanșator

„Vreau să depun sau să corectez declarația unică.”

## Limita evenimentului

Determină ruta D212 pentru anul fiscal 2025, inclusiv precompletare, venituri din străinătate și rectificare. Nu calculează impozit, CAS ori CASS și nu extrapolează formularul la alți ani.

## Fapte de dezambiguizare

| fact | tip | valori admise | de ce schimbă traseul |
|---|---|---|---|
| `fiscal_year` | integer | YYYY | selectează formularul și termenul verificat |
| `has_reportable_income` | boolean | `true`, `false` | separă venitul raportabil de opțiuni/alte motive |
| `income_origin` | enum | `romania`, `foreign`, `both`, `none` | activează secțiunile de venit străin |
| `income_category` | enum | `independent`, `rental`, `investment`, `agriculture_ip`, `withholding_cass`, `other`, `unknown` | alege datele fiscale necesare |
| `filing_state` | enum | `not_filed`, `filed_correct`, `filed_needs_correction` | selectează inițiala sau rectificativa |
| `spv_access` | boolean | `true`, `false` | precompletarea este disponibilă în SPV |
| `prefill_state` | enum | `not_used`, `used_unverified`, `used_verified` | impune verificarea datelor precompletate |

## Graf de proceduri

| intent_id | obligație | depends_on | rezultat urmărit |
|---|---|---|---|
| ro.tax.individual.identify_d212_scope | mandatory | — | anul și sursele de venit clarificate |
| ro.tax.individual.prepare_d212 | conditional | ro.tax.individual.identify_d212_scope | declarație inițială completată |
| ro.tax.individual.rectify_d212 | conditional | ro.tax.individual.identify_d212_scope | declarație rectificativă transmisă |
| ro.tax.individual.archive_receipt | mandatory | ro.tax.individual.prepare_d212 | recipisă și versiune păstrate |

## Canale oficiale

- **ANAF — formular web D212** — https://www.anaf.ro/declaratii/duf
- **ANAF — ghid precompletare D212 2026** — https://www.anaf.ro/declaratii/doc/Ghid_Precompletare_Declaratie_Unica_D212_2026._v1.pdf

## Garanții truth-guard

- `effective_from: 2026-06-25` din `rules.yaml` este pragul de verificare al draftului, nu o afirmație despre data istorică de intrare în vigoare.
- Nicio sumă, taxă, reducere, penalitate sau listă de documente dinamică nu este calculată fără claim oficial aplicabil și fapt de intrare confirmat.
- Claim-urile `needs_confirmation`, `conflicting` ori `expired` nu pot produce singure un efect critic favorabil utilizatorului.
- Pentru alt UAT decât Timișoara, operaționalizarea locală rămâne `verified_with_local_gap`; regulile naționale sunt păstrate separat.

## Observație de integrare

D212 precompletată nu este titlu de creanță și nu înlocuiește transmiterea formularului. Motorul separă datele sugerate de validarea făcută de contribuabil.
