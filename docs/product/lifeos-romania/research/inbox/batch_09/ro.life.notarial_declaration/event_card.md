# Event Card — ro.life.notarial_declaration (life.notarial_declaration)

**Titlu:** Vreau să fac o declarație notarială  
**Batch:** B09_NOTARIAL_DECLARATION  
**Status:** `research_inbox` — neaprobat; nu se publică în producție înainte de review independent  
**Pilot jurisdicție:** `ro.tm.timisoara`  
**Accessed_at:** `2026-06-25`

## Declanșator

Utilizatorul trebuie să dea o declarație ori un acord în forma cerută de lege sau de instituția destinatară.

## Fapte cerute (typed facts)

| fact | tip | valori / sens |
|---|---|---|
| `declaration_purpose` | string | scopul exact |
| `recipient_institution` | string | destinatarul |
| `required_form` | enum | authentic/signature_legalisation/unknown |
| `selected_procedure` | enum | authentication/signature_legalisation/other |
| `valid_identity_document_available` | boolean | identificare |
| `personal_appearance_possible` | boolean | prezentare/consimțământ |
| `institution_model_available` | boolean | model destinatar |
| `document_already_signed` | boolean | relevant legalizării |
| `cross_border_use` | boolean | formalități externe |
| `recipient_country` | country code | țara utilizării |
| `jurisdiction_id` | jurisdiction id | locator local |

## Obligații și ramuri

| step_id | condiție | efect determinist | dovezi |
|---|---|---|---|
| `identify_declaration_purpose_and_recipient` | întotdeauna | clarifică textul și forma | `claim.notary.declarations_examples` |
| `book_notary_authentication` | formă autentică | autentifică înscrisul | `claim.notary.form_words_route` |
| `bring_unsigned_copies_to_notary` | legalizare semnătură | prezintă exemplare nesemnate | `claim.notary.signature_unsigned_copies` |
| `find_notary` | pilot Timișoara | localizează notarul | `claim.notary.timisoara_chamber` |

## Canale oficiale

| arie | canal | stare |
|---|---|---|
| național | notar public / căutare UNNPR | `verified` |
| Timiș/Arad/Caraș-Severin | Camera Notarilor Publici Timișoara | `verified_with_local_gap` |

## Note de guvernanță

- Forma autentică și legalizarea semnăturii nu sunt interschimbabile.
- Modelul instituției este input, nu o sursă de adevăr universală.
- Onorariul și actele se confirmă pentru declarația concretă.

===
