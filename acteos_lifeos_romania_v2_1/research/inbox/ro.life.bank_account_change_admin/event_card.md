# Event Card — ro.life.bank_account_change_admin (life.bank_account_change_admin)

**Batch:** BATCH_11_PENSIONS_HEALTH_ADMIN  
**Status:** research_inbox — neaprobat pentru producție  
**Pilot jurisdicție locală:** `ro.tm.timisoara`  
**Data de referință:** 2026-06-25  
**Accessed_at surse:** 2026-06-25

## Declanșator

„Vreau să schimb contul în care primesc o plată publică”.

## Limită de domeniu

Evenimentul este un router administrativ. Procedura verificată în acest batch este schimbarea modalității de plată pentru pensii/indemnizații/pensii de serviciu gestionate de CNPP; pentru alte instituții se cere identificarea și cercetarea procedurii proprii.

## Fapte cerute (typed facts)

| fact | tip | valori / sens | obligatoriu |
|---|---|---|---|
| `paying_authority` | enum/string | instituția care efectuează plata | da |
| `payment_type` | enum/string | pensie / indemnizație / altă plată | da |
| `old_payment_method` | enum | post / current_account / card_account | da |
| `new_payment_method` | enum | post / current_account / card_account | da |
| `old_iban` | string\|null | contul vechi | condiționat |
| `new_iban` | string\|null | contul nou | condiționat |
| `account_holder_is_beneficiary` | boolean | titularul contului este beneficiarul | da |
| `account_country` | enum | romania / foreign | da |
| `also_changes_identity_or_contact_data` | boolean | necesită formular separat | da |
| `jurisdiction_id` | jurisdiction_id | casa teritorială competentă | da |

## Traseu determinist

1. **identify_paying_authority** — identifică instituția plătitoare — `verified`.
2. **select_institution_specific_procedure** — alege procedura instituției — `verified_with_local_gap`.
3. **prepare_cnpp_payment_change_request** — pentru CNPP, completează formularul oficial — `verified`.
4. **confirm_attachments_and_effective_month** — confirmă dovada contului și data aplicării — `verified_with_local_gap`.
5. **submit_to_competent_authority** — depune prin canalul oficial confirmat — `verified_with_local_gap`.

## Canale oficiale

- `ch.cnpp.online_forms` — formularele și serviciile electronice CNPP
- `ch.cjp_timisoara.contact` — CJP Timiș pentru procedura locală CNPP

## Excluderi și hand-off

- Nu folosește formularul CNPP pentru plăți AJPIS, ANAF, UAT sau alte instituții.
- Nu validează un IBAN și nu confirmă titularitatea fără document oficial.
- Nu promite luna de aplicare a schimbării fără confirmarea casei competente.

## Note de guvernanță

- Numele evenimentului este generic, dar regulile de execuție sunt obligatoriu instituție-specifice.
- Schimbarea contului și schimbarea datelor personale sunt formulate separat de CNPP.
- Pentru conturi externe se declanșează un traseu internațional distinct.
