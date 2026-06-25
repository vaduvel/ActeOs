---
event_id: ro.life.religious_marriage
title_ro: "Pregătirea căsătoriei religioase"
reference_date: 2026-06-25
timezone: Europe/Bucharest
status: research_candidate_not_production_published
jurisdiction:
  - eu
  - ro
  - ro.tm
  - ro.tm.timisoara
---

# Pregătirea căsătoriei religioase

## Outcome

Utilizatorul verifică condiția civilă, identifică cultul/parohia și obține checklistul local oficial.

## Scope and truth guard

Statul impune numai condiția căsătoriei civile și cadrul libertății religioase; actele și pregătirea concretă sunt stabilite autonom de cult.

> Acest card este candidat de research. Nicio regulă nu devine activă în producție înainte de captură imutabilă a sursei, review uman și aprobare explicită.

### Note de domeniu

- ActeOS nu cere utilizatorului să declare religia pentru a afișa ghidul general.
- Apartenența religioasă nu se stochează fără consimțământ expres.

## Facts

| id | type | întrebare | motiv | sensibil | obligatoriu |
|---|---|---|---|---:|---:|
| `civil_marriage_completed` | `boolean` | Căsătoria civilă este deja încheiată? | Este o condiție legală anterioară celebrării religioase. | false | true |
| `civil_certificate_available` | `boolean` | Ai dovada/certificatul căsătoriei civile? | Parohia poate solicita dovada îndeplinirii condiției legale. | false | true |
| `cult_id` | `enum` | În ce cult vrei celebrarea? | Checklistul și pregătirea sunt stabilite de cult și unitatea locală. | true | true |
| `locality` | `jurisdiction_ref` | În ce localitate vrei ceremonia? | Determină eparhia/parohia și canalul local. | false | true |
| `parish_selected` | `boolean` | Ai ales parohia/comunitatea? | Cerințele concrete trebuie confirmate local. | false | true |
| `desired_date_known` | `boolean` | Ai o dată dorită? | Programarea și pregătirea pot varia local. | false | false |
| `both_parties_consent` | `boolean` | Ambele persoane doresc celebrarea religioasă? | Libertatea religioasă exclude constrângerea. | true | true |
| `religion_data_storage_consent` | `boolean` | Consimți ca aplicația să păstreze informația despre cult? | Apartenența religioasă este dată sensibilă și necesită consimțământ expres. | true | true |
| `local_checklist_confirmed` | `boolean` | Ai primit checklistul oficial al parohiei? | Nu există o listă națională unică de acte. | false | true |
| `contribution_presented_as_mandatory_fee` | `boolean` | Ți s-a prezentat o contribuție drept taxă obligatorie? | Trebuie diferențiată contribuția cultului de o taxă publică universală. | false | false |
| `special_canonical_situation` | `boolean` | Există o situație religioasă anterioară care trebuie discutată cu cultul? | Impedimentele și dispensările sunt stabilite canonic, nu de aplicație. | true | false |

## Gates

| prioritate | id | când | efect | cod | mesaj | claims |
|---:|---|---|---|---|---|---|
| 100 | `gate.civil_not_completed` | civil_marriage_completed == false | `block` | `CIVIL_MARRIAGE_REQUIRED_FIRST` | Celebrarea religioasă nu poate avea loc înaintea căsătoriei civile. | `claim.religious_marriage.civil_marriage_first` |
| 95 | `gate.no_mutual_consent` | both_parties_consent == false | `block` | `RELIGIOUS_CONSENT_REQUIRED` | Aplicația nu poate ghida o celebrare religioasă împotriva voinței uneia dintre persoane. | `claim.religious_marriage.religion_disclosure_not_compulsory` |
| 90 | `gate.no_data_consent` | religion_data_storage_consent == false | `warn` | `RELIGION_DATA_NOT_STORED` | ActeOS nu va salva cultul sau apartenența religioasă fără consimțământ expres. | `claim.religious_marriage.religion_data_consent`, `claim.religious_marriage.religion_disclosure_not_compulsory` |
| 85 | `gate.cult_unknown` | cult_id == unknown | `needs_confirmation` | `CULT_AND_PARISH_REQUIRED` | Nu există un checklist național unic; trebuie identificat cultul și unitatea locală. | `claim.religious_marriage.cult_autonomy`, `claim.religious_marriage.official_cult_directory` |
| 80 | `gate.local_checklist_missing` | parish_selected == false or local_checklist_confirmed == false | `needs_confirmation` | `LOCAL_RELIGIOUS_CHECKLIST_REQUIRED` | Actele, pregătirea și programarea trebuie confirmate direct cu parohia/comunitatea. | `claim.religious_marriage.cult_autonomy`, `claim.religious_marriage.orthodox_timisoara_channel`, `claim.religious_marriage.catholic_timisoara_channel` |
| 70 | `gate.contribution_as_fee` | contribution_presented_as_mandatory_fee == true | `warn` | `RELIGIOUS_CONTRIBUTION_NOT_PUBLIC_FEE` | O contribuție a cultului nu trebuie afișată ca taxă publică națională obligatorie. | `claim.religious_marriage.contributions_not_compelled`, `claim.religious_marriage.cults_may_set_contributions` |
| 60 | `gate.canonical_case` | special_canonical_situation == true | `needs_confirmation` | `CANONICAL_REVIEW_REQUIRED` | Aplicația nu decide impedimente sau dispense canonice. | `claim.religious_marriage.cult_autonomy` |

## Steps

### 1. Încheie căsătoria civilă

- **Ce faci:** Finalizează căsătoria civilă înainte de programarea celebrării religioase.
- **Până când:** `none`
- **Cum știi că e gata:** Căsătoria civilă este încheiată și ai dovada oficială.
- **Dacă eșuează:** Urmează separat traseul de căsătorie civilă.
- **Canale:** `channel.civil_code_source`
- **Claims:** `claim.religious_marriage.civil_marriage_first`

### 2. Alege cultul și parohia/comunitatea

- **Ce faci:** Folosește directorul oficial și canalul eparhial/local, fără a presupune că regulile sunt identice între culte.
- **Până când:** `none`
- **Cum știi că e gata:** Ai identificat unitatea locală și datele ei oficiale de contact.
- **Dacă eșuează:** Contactează structura eparhială/centrală dacă parohia nu are date publice.
- **Canale:** `channel.cult_directory`, `channel.orthodox_timisoara`, `channel.catholic_timisoara`
- **Claims:** `claim.religious_marriage.cult_autonomy`, `claim.religious_marriage.official_cult_directory`, `claim.religious_marriage.orthodox_timisoara_channel`, `claim.religious_marriage.catholic_timisoara_channel`

### 3. Solicită checklistul și pregătirea locală

- **Ce faci:** Cere parohiei lista actuală de documente, eventualele întâlniri/pregătiri, disponibilitatea și modul de programare.
- **Până când:** `none`
- **Cum știi că e gata:** Ai primit un răspuns oficial/local datat și ai confirmat condițiile.
- **Dacă eșuează:** Escaladează la eparhie/structura cultului dacă răspunsul este neclar.
- **Canale:** `channel.orthodox_timisoara`, `channel.catholic_timisoara`
- **Claims:** `claim.religious_marriage.cult_autonomy`

### 4. Pregătește actele confirmate de parohie

- **Ce faci:** Încarcă numai documentele cerute explicit de unitatea locală; nu folosi o listă generică.
- **Până când:** `none`
- **Cum știi că e gata:** Parohia confirmă că dosarul/pregătirea sunt complete.
- **Dacă eșuează:** Corectează doar lipsurile comunicate de unitatea competentă.
- **Canale:** `channel.orthodox_timisoara`, `channel.catholic_timisoara`
- **Claims:** `claim.religious_marriage.cult_autonomy`, `claim.religious_marriage.civil_marriage_first`

### 5. Confirmă data și locul

- **Ce faci:** Obține confirmarea programării și instrucțiunile finale de la unitatea de cult.
- **Până când:** `none`
- **Cum știi că e gata:** Ai confirmare datată privind ceremonia și eventualele etape premergătoare.
- **Dacă eșuează:** Reprogramează direct cu unitatea de cult.
- **Canale:** `channel.orthodox_timisoara`, `channel.catholic_timisoara`
- **Claims:** `claim.religious_marriage.cult_autonomy`

## Requirements

| id | titlu | obligație | timing | forme | verificări | claims |
|---|---|---|---|---|---|---|
| `req.civil_marriage_proof` | Dovada căsătoriei civile | `mandatory` | `now` | original, copy, electronic, certified_copy | exists, readable, correct_document_type, names_consistent, date_within_window | `claim.religious_marriage.civil_marriage_first` |
| `req.local_checklist_confirmation` | Checklist local confirmat | `mandatory` | `now` | electronic, copy, declaration | exists, readable, date_within_window, user_confirmed | `claim.religious_marriage.cult_autonomy` |
| `req.religion_data_consent` | Consimțământ pentru stocarea datelor religioase | `conditional` | `now` | electronic, declaration | user_confirmed | `claim.religious_marriage.religion_data_consent`, `claim.religious_marriage.religion_disclosure_not_compulsory` |

## Official channels

| id | tip | etichetă | URL | integrare | teritoriu |
|---|---|---|---|---|---|
| `channel.civil_code_source` | `web` | Portal Legislativ — condiția căsătoriei civile | https://legislatie.just.ro/Public/DetaliiDocumentAfis/130143 | `SOURCE_ONLY` | ro |
| `channel.cult_directory` | `web` | Secretariatul de Stat pentru Culte — director | https://culte.gov.ro/culte-religioase/ | `DEEP_LINK` | ro |
| `channel.orthodox_timisoara` | `web` | Arhiepiscopia Timișoarei — parohii/contact | https://www.arhiepiscopiatimisoarei.ro/ | `DEEP_LINK` | ro.tm, ro.tm.timisoara |
| `channel.catholic_timisoara` | `web` | Episcopia Romano-Catolică de Timișoara — parohii/contact | https://gerhardus.ro/ | `DEEP_LINK` | ro.tm, ro.tm.timisoara |

## Source claims

| claim_id | afirmație | sursă | confidence | locator |
|---|---|---|---|---|
| `claim.religious_marriage.civil_marriage_first` | Celebrarea religioasă a căsătoriei poate avea loc numai după încheierea căsătoriei civile. | `civil_code` | `verified` | Codul civil, art. 259 alin. (3) |
| `claim.religious_marriage.cult_autonomy` | Cultele recunoscute se organizează autonom potrivit propriilor statute sau coduri canonice. | `law_489_2006` | `verified` | Art. 8 alin. (1)-(3); forma consolidată accesată la 25.06.2026 |
| `claim.religious_marriage.religion_data_consent` | Datele privind convingerile religioase sau apartenența la cult pot fi prelucrate numai cu consimțământ expres, în afara excepțiilor legale. | `law_489_2006` | `verified` | Art. 5 alin. (5); forma consolidată accesată la 25.06.2026 |
| `claim.religious_marriage.religion_disclosure_not_compulsory` | Persoanele nu pot fi obligate să își menționeze religia în relația cu autorități sau persoane juridice private. | `law_489_2006` | `verified` | Art. 5 alin. (6); forma consolidată accesată la 25.06.2026 |
| `claim.religious_marriage.contributions_not_compelled` | Nimeni nu poate fi constrâns prin acte administrative sau alte metode să contribuie la cheltuielile unui cult. | `law_489_2006` | `verified` | Art. 10 alin. (5); forma consolidată accesată la 25.06.2026 |
| `claim.religious_marriage.cults_may_set_contributions` | Cultele pot stabili contribuții ale credincioșilor pentru susținerea activităților lor. | `law_489_2006` | `verified` | Art. 10 alin. (2); forma consolidată accesată la 25.06.2026 |
| `claim.religious_marriage.official_cult_directory` | Secretariatul de Stat pentru Culte publică directorul cultelor religioase recunoscute. | `cultes_list` | `verified_with_local_gap` | Titlul paginii/directorului oficial |
| `claim.religious_marriage.orthodox_timisoara_channel` | Site-ul eparhial identifică Arhiepiscopia Timișoarei și publică harta parohiilor/contactele locale. | `archdiocese_timisoara` | `verified_with_local_gap` | Pagina principală, meniu «Protopopiate» |
| `claim.religious_marriage.catholic_timisoara_channel` | Site-ul diecezan publică structura și parohiile Episcopiei Romano-Catolice de Timișoara. | `diocese_timisoara` | `verified_with_local_gap` | Pagina principală, meniu «Episcopie» |

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
