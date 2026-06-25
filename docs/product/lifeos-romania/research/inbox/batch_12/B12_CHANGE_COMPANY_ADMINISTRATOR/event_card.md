# Event Card — ro.life.change_company_administrator (life.change_company_administrator)

**Batch:** B12_CHANGE_COMPANY_ADMINISTRATOR  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Vreau să schimb administratorul firmei.”

## Limita evenimentului

Acoperă numirea, revocarea, înlocuirea, prelungirea mandatului și schimbarea puterilor administratorului unui SRL. Nu acoperă administratorii speciali/judiciari, insolvența, societățile pe acțiuni sau simpla schimbare a datelor de contact.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `entity_type` | `enum` | srl; alte forme cer traseu separat | da |
| `administrator_change_type` | `enum` | appoint, revoke, replace, renew_term, change_powers | da |
| `associates_count` | `integer` | asociat unic sau mai mulți asociați | da |
| `decision_recorded_in_writing` | `boolean` | decizia asociatului unic este scrisă | condițional |
| `decision_valid_under_articles` | `boolean` | majoritatea și procedura sunt valide | condițional |
| `new_admin_identity_data_complete` | `boolean` | date complete ale noului administrator | condițional |
| `mandate_term_defined` | `boolean` | durata mandatului este stabilită | condițional |
| `powers_defined` | `boolean` | puterile sunt stabilite | condițional |
| `representation_mode` | `enum` | jointly sau separately | condițional |
| `constitutive_act_is_modified` | `boolean` | se modifică textul actului constitutiv | da |
| `resulting_admin_count` | `integer` | numărul administratorilor după schimbare | da |
| `decision_date` | `date` | data hotărârii sau deciziei | da |
| `filing_actor` | `enum` | legal_representative, authenticated_proxy, lawyer | da |
| `signer_authority_valid_on_filing_date` | `boolean` | puterea semnatarului este valabilă | condițional |
| `beneficial_owner_identity_or_control_changes` | `boolean` | se schimbă datele beneficiarului real | da |
| `filing_channel` | `enum` | counter, post_courier, online | da |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `approve_administrator_change` | hotărârea/decizia de schimbare | competență și majoritate |
| `prepare_updated_constitutive_act` | act modificator și text actualizat | dacă actul constitutiv este modificat |
| `file_administrator_change_mention` | mențiune ONRC | termen și semnatar valid |
| `update_beneficial_owner_data` | actualizare beneficiar real | numai când datele beneficiarului real se modifică |

## Reguli-cheie verificate

- AGA desemnează și revocă administratorii SRL.
- Asociatul unic consemnează imediat în scris decizia.
- Actul constitutiv stabilește identitatea, durata, puterile și modul de reprezentare al administratorilor.
- Mențiunea se solicită în cel mult 15 zile, iar depunerea online folosește semnătură calificată.
- Societatea nu trebuie lăsată fără organe statutare.

## Canal pilot Timișoara / Timiș

Schimbarea administratorului este o mențiune națională ONRC. Nu a fost identificată o procedură locală distinctă a Municipiului Timișoara pentru simpla schimbare a administratorului; orice autorizație locală afectată se verifică separat, fără a inventa un pas.

## Guvernanță

Motorul verifică separat validitatea hotărârii, conținutul mandatului, puterea semnatarului la data depunerii și efectul real asupra beneficiarului real. Nu presupune că administratorul este automat beneficiar real și nu permite o revocare care lasă societatea fără organ statutar.
