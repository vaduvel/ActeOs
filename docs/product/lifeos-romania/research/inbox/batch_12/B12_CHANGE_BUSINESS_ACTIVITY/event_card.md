# Event Card — ro.life.change_business_activity (life.change_business_activity)

**Batch:** B12_CHANGE_BUSINESS_ACTIVITY  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Vreau să schimb sau să actualizez activitățile firmei.”

## Limita evenimentului

Separă actualizarea tehnică la CAEN Rev.3 de adăugarea, eliminarea sau schimbarea activității principale. Nu deduce automat codul CAEN și nu înlocuiește avizele sectoriale.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `entity_type` | `enum` | pfa sau srl | da |
| `activity_change_type` | `enum` | caen_rev3_update_only, add_activity, remove_activity, change_main_activity, split_or_aggregate | da |
| `resulting_caen_class_count` | `integer` | numărul final de clase pentru PFA | condițional |
| `involves_caen_rev3_update` | `boolean` | operațiunea include Rev.3 | da |
| `new_activity_already_registered_authorized` | `boolean` | noua activitate este autorizată | condițional |
| `special_permit_required` | `boolean` | există aviz sectorial | condițional |
| `decision_date` | `date` | data hotărârii SRL | condițional |
| `filing_actor` | `enum` | titular/reprezentant/mandatar/avocat | da |
| `local_commercial_agreement_exists` | `boolean` | există acord local | condițional |
| `activity_data_changes` | `boolean` | datele acordului se schimbă | condițional |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `file_simple_caen_rev3_update` | actualizare simplificată CAEN | fără modificare reală |
| `approve_activity_modification` | decizie internă | adăugare/eliminare/principal |
| `file_activity_modification` | mențiune ONRC | acte și termen |
| `modify_timisoara_commercial_agreement` | modificare acord local | CAEN sau activitate schimbată |

## Reguli-cheie verificate

- Actualizarea simplă CAEN Rev.3 are flux distinct și documentație redusă.
- Detalierea sau agregarea claselor este tratată și ca modificare a obiectului.
- PFA rămâne limitată la cinci clase CAEN.
- Un nou certificat se emite gratuit pentru actualizarea CAEN Rev.3.

## Canal pilot Timișoara / Timiș

Timișoara include CAEN Rev.3 între cazurile de modificare a acordului; taxa și documentele apar numai după selectarea situației.

## Guvernanță

Clasificarea între „actualizare” și „modificare” este gate critic. Motorul nu folosește fluxul simplificat dacă există adăugări, eliminări, schimbare de activitate principală sau split/agregare.
