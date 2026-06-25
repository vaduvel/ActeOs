# Event Card — ro.life.power_of_attorney (life.power_of_attorney)

**Titlu:** Vreau să fac o procură  
**Batch:** B09_POWER_OF_ATTORNEY  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Utilizatorul dorește să împuternicească o altă persoană pentru o operațiune sau procedură determinată.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `underlying_act` | string/enum | operațiunea reprezentată |
| `attorney_identity_known` | boolean | identitatea mandatarului |
| `scope_defined` | boolean | puterile concrete |
| `required_form` | enum | authentic/signature_legalisation/unknown |
| `selected_procedure` | enum | authentication/signature_legalisation/other |
| `principal_identity_document_available` | boolean | identificare mandant |
| `principal_personal_appearance_possible` | boolean | prezentare/consimțământ |
| `recipient_model_available` | boolean | model destinatar |
| `cross_border_use` | boolean | folosire externă |
| `recipient_country` | country code | țara utilizării |
| `jurisdiction_id` | jurisdiction id | locator local |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `define_power_of_attorney_scope` | întotdeauna | definește mandatul și mandatarul | `claim.poa.proxies_for_institutions` |
| `book_notary_for_authentic_power_of_attorney` | formă autentică | autentifică procura | `claim.poa.notarial_form_route` |
| `prepare_authentic_succession_power_of_attorney` | reprezentare succesorală | folosește forma autentică | `claim.poa.succession_authentic` |
| `find_notary` | pilot Timișoara | localizează notarul | `claim.poa.timisoara_chamber` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| național | notar public / căutare UNNPR | `verified` |
| Timiș/Arad/Caraș-Severin | Camera Notarilor Publici Timișoara | `verified_with_local_gap` |

## Note de guvernanță

- Procura se construiește pornind de la operațiunea reprezentată, nu dintr-un șablon vag.
- Legalizarea semnăturii nu înlocuiește autentificarea.
- Durata nu este ghicită și trebuie redactată/confirmată pentru mandat.

===
