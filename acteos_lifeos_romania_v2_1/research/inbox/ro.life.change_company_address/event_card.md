# Event Card — ro.life.change_company_address (life.change_company_address)

**Batch:** B12_CHANGE_COMPANY_ADDRESS  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Vreau să schimb sediul firmei sau PFA-ului.”

## Limita evenimentului

Acoperă mutarea sediului profesional PFA și a sediului social SRL în același județ sau în alt județ. Nu tratează automat mutarea punctelor de lucru, domiciliul fiscal ori avizele spațiului.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `entity_type` | `enum` | pfa sau srl | da |
| `new_address` | `string` | adresa completă a noului sediu | da |
| `county_changes` | `boolean` | se schimbă județul | da |
| `new_seat_use_right_document_available` | `boolean` | există dovada folosinței | da |
| `new_seat_is_dwelling` | `boolean` | noul sediu este locuință | condițional |
| `activity_at_new_seat` | `boolean` | se desfășoară activitate la sediu | condițional |
| `current_seat_use_right_expired` | `boolean` | dreptul actual a expirat | da |
| `decision_date` | `date` | data deciziei SRL | condițional |
| `filing_actor` | `enum` | titular/reprezentant/mandatar/avocat | da |
| `local_commercial_agreement_exists` | `boolean` | există acord local afectat | condițional |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `file_pfa_seat_change` | schimbare sediu PFA | același județ |
| `file_pfa_cross_county_seat_change` | mutare PFA în alt județ | aceeași încheiere |
| `approve_srl_seat_change` | hotărâre SRL | modificare act constitutiv |
| `file_srl_seat_change` | mențiune ONRC | termen și documente |
| `modify_timisoara_agreement_for_seat` | modificare acord local | sediu social schimbat |

## Reguli-cheie verificate

- Schimbarea sediului PFA se înregistrează la ONRC.
- Mutarea PFA în alt județ este dispusă prin aceeași încheiere pentru vechiul și noul sediu.
- Sediul SRL este element al actului constitutiv și impune text actualizat.
- Expirarea dreptului de sediu social poate crea risc de dizolvare.

## Canal pilot Timișoara / Timiș

În Timișoara, sediul social este un caz explicit de modificare a acordului comercial; taxa și documentele sunt dinamice.

## Guvernanță

Adresa și dreptul de folosință sunt gate-uri critice. Motorul nu confundă sediul principal cu punctele de lucru și nu declară automat îndeplinite formalitățile de condominiu când există activitate la adresă.
