---
event_id: ro.life.bank_card_change
title_ro: "Schimbarea sau reînnoirea cardului bancar"
reference_date: 2026-06-25
timezone: Europe/Bucharest
status: research_candidate_not_production_published
jurisdiction:
  - eu
  - ro
  - ro.tm
  - ro.tm.timisoara
---

# Schimbarea sau reînnoirea cardului bancar

## Outcome

Utilizatorul obține un card nou pentru expirare, deteriorare, schimbarea numelui sau alt motiv non-urgent.

## Scope and truth guard

Traseul este provider-specific și redirecționează pierderea/furtul către fluxul urgent.

> Acest card este candidat de research. Nicio regulă nu devine activă în producție înainte de captură imutabilă a sursei, review uman și aprobare explicită.

## Facts

| id | type | întrebare | motiv | sensibil | obligatoriu |
|---|---|---|---|---:|---:|
| `provider_id` | `enum` | Cine a emis cardul? | Procesul de reînnoire/reemitere este specific băncii. | false | true |
| `change_reason` | `enum` | De ce ai nevoie de alt card? | Motivul selectează traseul corect. | false | true |
| `expiry_month` | `date` | În ce lună expiră cardul? | Determină dacă fereastra de reînnoire este deschisă. | false | false |
| `can_access_banking_app` | `boolean` | Ai acces la aplicația băncii? | Unele fluxuri sunt disponibile în aplicație. | false | true |
| `new_identity_document_ready` | `boolean` | Ai noul act de identitate? | La schimbarea numelui trebuie actualizate datele înaintea cardului. | true | false |
| `delivery_address_current` | `boolean` | Adresa de livrare este actuală? | Cardul poate fi trimis prin curier. | true | false |
| `renewal_option_visible` | `boolean` | Vezi opțiunea de reînnoire? | Poate indica poziția în fereastra operațională. | false | false |

## Gates

| prioritate | id | când | efect | cod | mesaj | claims |
|---:|---|---|---|---|---|---|
| 100 | `gate.lost_redirect` | change_reason == lost_or_stolen | `block` | `USE_LOST_STOLEN_FLOW` | Pentru card pierdut sau furat, folosește fluxul urgent de blocare, nu simpla schimbare. | `claim.bank_card_change.ing_damaged_reissue` |
| 95 | `gate.compromised` | change_reason == compromised | `warn` | `BLOCK_BEFORE_REISSUE` | Dacă datele cardului sunt compromise, blochează-l înainte de reemitere. | `claim.bank_card_change.ing_damaged_reissue` |
| 90 | `gate.name_id` | change_reason == name_change and new_identity_document_ready == false | `block` | `UPDATE_IDENTITY_FIRST` | Pregătește noul act și actualizează datele la bancă înainte de cardul cu numele nou. | `claim.bank_card_change.ing_name_change` |
| 70 | `gate.other_provider` | provider_id in [other, unknown] | `needs_confirmation` | `PROVIDER_REISSUE_RULES_REQUIRED` | Termenul, costul și canalul trebuie confirmate la emitent. | `claim.bank_card_change.ing_valid_until_month_end` |

## Steps

### 1. Stabilește motivul schimbării

- **Ce faci:** Alege expirare, deteriorare, schimbare de nume sau alt motiv.
- **Până când:** `none`
- **Cum știi că e gata:** Motivul este selectat și nu este o situație urgentă de pierdere/furt.
- **Dacă eșuează:** Dacă este pierdut/furat, mută-te în fluxul urgent.
- **Canale:** `channel.ing_cards`, `channel.bcr_cards`, `channel.cec_cards`
- **Claims:** `claim.bank_card_change.ing_damaged_reissue`, `claim.bank_card_change.ing_name_change`, `claim.bank_card_change.bcr_expiry_process`, `claim.bank_card_change.cec_valid_month_end`

### 2. Actualizează datele și adresa

- **Ce faci:** Confirmă numele și adresa de livrare înainte de comandă.
- **Până când:** `none`
- **Cum știi că e gata:** Profilul bancar afișează datele corecte.
- **Dacă eșuează:** Folosește canalul oficial de actualizare date sau unitatea băncii.
- **Canale:** `channel.ing_cards`, `channel.bcr_cards`, `channel.cec_cards`
- **Claims:** `claim.bank_card_change.ing_name_change`, `claim.bank_card_change.bcr_expiry_process`

### 3. Solicită reînnoirea sau reemiterea

- **Ce faci:** Inițiază comanda în aplicație ori prin canalul oficial al emitentului.
- **Până când:** `none`
- **Cum știi că e gata:** Ai confirmarea comenzii și metoda de livrare/ridicare.
- **Dacă eșuează:** Dacă opțiunea nu apare, contactează emitentul; nu deduce automat că s-a comandat.
- **Canale:** `channel.ing_cards`, `channel.bcr_cards`, `channel.cec_cards`
- **Claims:** `claim.bank_card_change.ing_renewal_window`, `claim.bank_card_change.ing_no_automatic_renewal`, `claim.bank_card_change.ing_damaged_reissue`, `claim.bank_card_change.bcr_expiry_process`, `claim.bank_card_change.cec_valid_month_end`

### 4. Primește și activează noul card

- **Ce faci:** Verifică primirea, activează cardul și distruge/reciclează cardul vechi conform indicațiilor emitentului.
- **Până când:** `none`
- **Cum știi că e gata:** Noul card este activ și vechiul card nu mai poate fi folosit.
- **Dacă eșuează:** Dacă livrarea întârzie, verifică adresa și contactează emitentul.
- **Canale:** `channel.ing_cards`, `channel.bcr_cards`, `channel.cec_cards`
- **Claims:** `claim.bank_card_change.ing_valid_until_month_end`, `claim.bank_card_change.bcr_expiry_process`, `claim.bank_card_change.cec_valid_month_end`

## Requirements

| id | titlu | obligație | timing | forme | verificări | claims |
|---|---|---|---|---|---|---|
| `req.current_card_data` | Cardul curent în aplicația oficială | `mandatory` | `now` | electronic | user_confirmed | `claim.bank_card_change.ing_renewal_window` |
| `req.new_identity_document` | Noul act de identitate | `conditional` | `now` | original, electronic | exists, readable, correct_document_type, not_expired, names_consistent | `claim.bank_card_change.ing_name_change` |
| `req.delivery_address_confirmation` | Confirmarea adresei de livrare | `conditional` | `now` | declaration | field_present, address_consistent, user_confirmed | `claim.bank_card_change.ing_renewal_window`, `claim.bank_card_change.bcr_expiry_process` |

## Official channels

| id | tip | etichetă | URL | integrare | teritoriu |
|---|---|---|---|---|---|
| `channel.ing_cards` | `web` | ING — FAQ și Home'Bank pentru carduri | https://ing.ro/persoane-fizice/carduri-si-conturi/faq-carduri | `DEEP_LINK` | ro |
| `channel.bcr_cards` | `web` | BCR — card care expiră | https://www.bcr.ro/ro/persoane-fizice/help-center/carduri-faq-24 | `DEEP_LINK` | ro |
| `channel.cec_cards` | `web` | CEC — card care expiră | https://www.cec.ro/intrebari-raspunsuri/ce-trebuie-sa-fac-daca-imi-expira-cardul-curand | `SOURCE_ONLY` | ro |

## Source claims

| claim_id | afirmație | sursă | confidence | locator |
|---|---|---|---|---|
| `claim.bank_card_change.ing_valid_until_month_end` | Cardurile fizice ING sunt valabile până la sfârșitul lunii înscrise pe ele. | `ing_card_renewal` | `verified` | FAQ «Cardul se reînnoiește automat?» |
| `claim.bank_card_change.ing_renewal_window` | ING afișează opțiunea de reînnoire cu două luni înainte și permite inițierea până la începutul lunii expirării. | `ing_card_renewal` | `verified` | FAQ reînnoire; procesul poate fi inițiat până la începutul lunii expirării |
| `claim.bank_card_change.ing_no_automatic_renewal` | Dacă utilizatorul nu își exprimă opțiunea, cardul fizic ING nu se reînnoiește automat. | `ing_card_renewal` | `verified` | FAQ «Ce se întâmplă dacă nu fac reînnoirea?» |
| `claim.bank_card_change.ing_damaged_reissue` | Pentru un card fizic demagnetizat sau nefuncțional, ING indică emiterea unuia nou din Home'Bank. | `ing_card_renewal` | `verified` | FAQ «Cum procedez dacă nu mai funcționează cardul?» |
| `claim.bank_card_change.ing_name_change` | La schimbarea numelui, ING cere actualizarea datelor cu noul act înaintea emiterii cardului. | `ing_card_renewal` | `verified` | FAQ «Mi-am schimbat numele» |
| `claim.bank_card_change.bcr_expiry_process` | BCR indică notificarea cu aproximativ o lună înainte și expedierea noului card prin curier în luna expirării. | `bcr_card_renewal` | `verified` | FAQ card expirat; livrare prin curier în luna expirării |
| `claim.bank_card_change.cec_valid_month_end` | CEC indică utilizarea cardului până în ultima zi a lunii înscrise ca expirare și reemiterea lui. | `cec_card_renewal` | `verified_with_local_gap` | FAQ card care expiră curând |

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
