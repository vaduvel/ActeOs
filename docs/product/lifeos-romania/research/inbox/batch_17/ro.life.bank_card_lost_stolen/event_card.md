---
event_id: ro.life.bank_card_lost_stolen
title_ro: "Card bancar pierdut sau furat"
reference_date: 2026-06-25
timezone: Europe/Bucharest
status: research_candidate_not_production_published
jurisdiction:
  - eu
  - ro
  - ro.tm
  - ro.tm.timisoara
---

# Card bancar pierdut sau furat

## Outcome

Cardul este blocat, tranzacțiile sunt verificate și, dacă este necesar, este cerut un card nou.

## Scope and truth guard

Eveniment urgent. Motorul prioritizează blocarea și separă contestarea operațiunilor de reemiterea cardului.

> Acest card este candidat de research. Nicio regulă nu devine activă în producție înainte de captură imutabilă a sursei, review uman și aprobare explicită.

## Facts

| id | type | întrebare | motiv | sensibil | obligatoriu |
|---|---|---|---|---:|---:|
| `provider_id` | `enum` | Cine a emis cardul? | Canalul de blocare este specific emitentului. | false | true |
| `incident_type` | `enum` | Cardul este pierdut sau furat? | Contextul ajută la explicație, dar blocarea este urgentă în ambele cazuri. | false | true |
| `can_access_banking_app` | `boolean` | Mai ai acces la aplicația băncii? | Poate fi cel mai rapid canal de blocare. | false | true |
| `unauthorized_transactions_seen` | `boolean` | Vezi tranzacții pe care nu le recunoști? | Activează fluxul separat de contestare a operațiunilor. | false | true |
| `latest_unauthorized_transaction_date` | `date` | Când a fost ultima tranzacție nerecunoscută? | Este necesar pentru verificarea limitei de 13 luni. | true | false |
| `is_abroad` | `boolean` | Ești în străinătate? | Unele bănci au numere diferite pentru apel din străinătate. | false | false |
| `card_already_blocked` | `boolean` | Cardul este deja blocat? | Evită duplicarea pasului și trece la verificarea tranzacțiilor. | false | true |
| `replacement_needed` | `boolean` | Vrei și un card nou? | Blocarea și reemiterea sunt pași distincți. | false | false |

## Gates

| prioritate | id | când | efect | cod | mesaj | claims |
|---:|---|---|---|---|---|---|
| 100 | `gate.card_not_blocked` | card_already_blocked == false | `warn` | `BLOCK_CARD_NOW` | Blochează imediat cardul prin canalul oficial al emitentului. | `claim.bank_card_lost_stolen.notify_without_delay` |
| 90 | `gate.provider_unknown` | provider_id in [other, unknown] | `needs_confirmation` | `ISSUER_CHANNEL_REQUIRED` | Nu folosi un număr găsit într-un mesaj; identifică emitentul și canalul oficial. | `claim.bank_card_lost_stolen.notify_without_delay` |
| 80 | `gate.cec_conflict` | provider_id == cec | `warn` | `CEC_SECONDARY_PHONE_CONFLICT` | Sursele oficiale CEC afișează numere secundare diferite. Numărul comun ambelor pagini este 021 202 69 99. | `claim.bank_card_lost_stolen.cec_faq_numbers`, `claim.bank_card_lost_stolen.cec_contact_numbers` |
| 70 | `gate.transactions` | unauthorized_transactions_seen == true | `warn` | `REPORT_UNAUTHORIZED_TRANSACTIONS` | Raportează separat tranzacțiile neautorizate și păstrează confirmarea. | `claim.bank_card_lost_stolen.unauthorized_13_months`, `claim.bank_card_lost_stolen.refund_next_business_day` |

## Steps

### 1. Blochează cardul

- **Ce faci:** Folosește imediat aplicația sau telefonul oficial al emitentului.
- **Până când:** `none`
- **Cum știi că e gata:** Aplicația sau operatorul confirmă blocarea și ai un număr/referință.
- **Dacă eșuează:** Dacă aplicația nu funcționează, apelează canalul telefonic oficial.
- **Canale:** `channel.ing_card_stop`, `channel.bt_card_stop`, `channel.bcr_card_stop`, `channel.cec_card_stop`
- **Claims:** `claim.bank_card_lost_stolen.notify_without_delay`, `claim.bank_card_lost_stolen.ing_block_channel`, `claim.bank_card_lost_stolen.bt_block_channel`, `claim.bank_card_lost_stolen.bcr_block_channel`, `claim.bank_card_lost_stolen.cec_faq_numbers`, `claim.bank_card_lost_stolen.cec_contact_numbers`

### 2. Verifică tranzacțiile

- **Ce faci:** Controlează lista operațiunilor și marchează ce nu recunoști.
- **Până când:** `none`
- **Cum știi că e gata:** Ai o listă datată a operațiunilor contestate sau ai confirmat că nu există.
- **Dacă eșuează:** Descarcă extrasul sau contactează banca dacă nu ai acces.
- **Canale:** `channel.ing_card_stop`, `channel.bt_card_stop`, `channel.bcr_card_stop`, `channel.cec_card_stop`
- **Claims:** `claim.bank_card_lost_stolen.unauthorized_13_months`

### 3. Raportează operațiunile neautorizate

- **Ce faci:** Transmite băncii reclamația prin canalul indicat și păstrează dovada.
- **Până când:** `relative` — {'max_months': 13, 'anchor': 'debit_date', 'instruction': 'fără întârziere nejustificată'}
- **Cum știi că e gata:** Ai număr de înregistrare sau confirmarea electronică a sesizării.
- **Dacă eșuează:** Dacă banca solicită date suplimentare, răspunde în canalul oficial.; Escaladează conform procedurii de reclamații din contract.
- **Canale:** `channel.ing_card_stop`, `channel.bt_card_stop`, `channel.bcr_card_stop`, `channel.cec_card_stop`
- **Claims:** `claim.bank_card_lost_stolen.unauthorized_13_months`, `claim.bank_card_lost_stolen.refund_next_business_day`, `claim.bank_card_lost_stolen.liability_up_to_30_eur`

### 4. Solicită un card nou

- **Ce faci:** După blocare, urmează fluxul emitentului pentru reemitere și livrare/ridicare.
- **Până când:** `none`
- **Cum știi că e gata:** Ai confirmarea reemiterii și metoda de primire.
- **Dacă eșuează:** Confirmă costul și termenul înainte de comandă; acestea nu sunt universale.
- **Canale:** `channel.ing_card_stop`, `channel.bt_card_stop`, `channel.bcr_card_stop`, `channel.cec_card_stop`
- **Claims:** `claim.bank_card_lost_stolen.bt_block_channel`, `claim.bank_card_lost_stolen.bcr_block_channel`

## Requirements

| id | titlu | obligație | timing | forme | verificări | claims |
|---|---|---|---|---|---|---|
| `req.issuer_identification` | Identificarea emitentului | `mandatory` | `now` | declaration | field_present, user_confirmed | `claim.bank_card_lost_stolen.notify_without_delay` |
| `req.security_identification` | Date pentru identificarea sigură | `mandatory` | `now` | declaration | user_confirmed | `claim.bank_card_lost_stolen.notify_without_delay` |
| `req.transaction_details` | Detaliile tranzacțiilor contestate | `conditional` | `now` | electronic, copy | exists, readable, date_within_window, user_confirmed | `claim.bank_card_lost_stolen.unauthorized_13_months` |

## Official channels

| id | tip | etichetă | URL | integrare | teritoriu |
|---|---|---|---|---|---|
| `channel.ing_card_stop` | `phone` | ING Card Stop — 021 402 85 99 | tel:+40214028599 | `DEEP_LINK` | ro |
| `channel.bt_card_stop` | `phone` | BT Call Center — 0264 308 028 | tel:+40264308028 | `DEEP_LINK` | ro |
| `channel.bcr_card_stop` | `phone` | BCR Asistența — *2227 / +4021 407 42 00 | tel:+40214074200 | `DEEP_LINK` | ro |
| `channel.cec_card_stop` | `phone` | CEC — numărul comun surselor: 021 202 69 99 | tel:+40212026999 | `DEEP_LINK` | ro |

## Source claims

| claim_id | afirmație | sursă | confidence | locator |
|---|---|---|---|---|
| `claim.bank_card_lost_stolen.notify_without_delay` | Utilizatorul trebuie să notifice fără întârziere pierderea, furtul sau folosirea neautorizată a instrumentului de plată. | `law_209_2019` | `verified` | Art. 166 alin. (1) lit. b) |
| `claim.bank_card_lost_stolen.unauthorized_13_months` | Semnalarea operațiunii neautorizate sau executate incorect nu poate fi făcută mai târziu de 13 luni de la debitare. | `law_209_2019` | `verified` | Art. 169 alin. (1) |
| `claim.bank_card_lost_stolen.refund_next_business_day` | În cazul unei operațiuni neautorizate, rambursarea se face imediat sau până la sfârșitul următoarei zile lucrătoare, cu excepția suspiciunii rezonabile de fraudă. | `law_209_2019` | `verified` | Art. 173 lit. a); include excepția suspiciunii rezonabile de fraudă |
| `claim.bank_card_lost_stolen.liability_up_to_30_eur` | În anumite situații fără fraudă sau încălcare intenționată, răspunderea plătitorului poate fi de cel mult 30 euro. | `law_209_2019` | `verified` | Art. 177 alin. (1); se aplică doar în condițiile articolului |
| `claim.bank_card_lost_stolen.ing_block_channel` | ING indică blocarea cardului în Home'Bank sau prin Card Stop, disponibil 24/7. | `ing_lost_card` | `verified` | Secțiunea de contact pentru card pierdut/furat |
| `claim.bank_card_lost_stolen.bt_block_channel` | BT indică blocarea urgentă și solicitarea unui card nou din BT Pay sau la 0264 308 028, 24/7. | `bt_lost_card` | `verified` | Răspuns ÎntrebBT, actualizat 25.06.2026 |
| `claim.bank_card_lost_stolen.bcr_block_channel` | BCR indică blocarea din George ori contactarea BCR Asistența 24/7. | `bcr_lost_card` | `verified` | FAQ card pierdut/furat; *2227 / +4021.407.42.00 |
| `claim.bank_card_lost_stolen.cec_faq_numbers` | CEC publică pentru blocarea cardului numerele 021.202.69.99 și 021.315.71.00. | `cec_lost_card_faq` | `conflicting` | FAQ card pierdut/furat |
| `claim.bank_card_lost_stolen.cec_contact_numbers` | Pagina de contact CEC publică 021 202 69 99 și un al doilea număr diferit, 021 351 71 00. | `cec_contact` | `conflicting` | Pagina Contact — asistență carduri |

## Conflicts

| id | claim A | claim B | status | handling |
|---|---|---|---|---|
| `conflict.cec.secondary_phone` | `claim.bank_card_lost_stolen.cec_faq_numbers` | `claim.bank_card_lost_stolen.cec_contact_numbers` | `unresolved` | Nu se alege numărul secundar; se afișează doar 021 202 69 99, comun ambelor surse, până la clarificare. |

## Freshness

critical:
  review_due_at: '2026-07-25'
  hard_expiry_at: '2026-09-23'
  on_expiry: needs_confirmation
operational:
  review_due_at: '2026-08-24'
  hard_expiry_at: '2026-12-22'
  on_expiry: warn
normative:
  review_due_at: '2026-12-22'
  hard_expiry_at: '2027-06-25'
  on_expiry: needs_confirmation
