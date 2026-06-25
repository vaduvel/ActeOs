---
event_id: ro.life.baptism
title_ro: "Pregătirea botezului"
reference_date: 2026-06-25
timezone: Europe/Bucharest
status: research_candidate_not_production_published
jurisdiction:
  - eu
  - ro
  - ro.tm
  - ro.tm.timisoara
---

# Pregătirea botezului

## Outcome

Utilizatorul clarifică consimțământul și reprezentarea, alege cultul/parohia și obține checklistul local oficial.

## Scope and truth guard

Nu există un dosar civil național pentru botez. Legea protejează libertatea religioasă și pragurile de alegere ale minorului, iar cultul stabilește ritualul și actele locale.

> Acest card este candidat de research. Nicio regulă nu devine activă în producție înainte de captură imutabilă a sursei, review uman și aprobare explicită.

### Note de domeniu

- ActeOS nu decide validitatea sacramentală și nu interpretează dreptul canonic.
- Datele religioase nu se stochează fără consimțământ expres.

## Facts

| id | type | întrebare | motiv | sensibil | obligatoriu |
|---|---|---|---|---:|---:|
| `candidate_kind` | `enum` | Pentru cine pregătești botezul? | Consimțământul și capacitatea de alegere diferă după vârstă. | false | true |
| `candidate_age_years` | `integer` | Ce vârstă are persoana? | Legea stabilește praguri la 14 și 16 ani. | true | true |
| `religion_change_involved` | `boolean` | Demersul implică schimbarea religiei persoanei? | La 14 ani schimbarea religiei necesită consimțământul copilului. | true | false |
| `candidate_consents` | `boolean` | Persoana consimte la botez, dacă poate exprima voința? | Libertatea religioasă exclude constrângerea. | true | true |
| `guardian_authority_confirmed` | `boolean` | Pentru minor, este clar cine exercită autoritatea/tutela? | Aplicația nu poate presupune dreptul de reprezentare. | true | false |
| `guardians_agree` | `boolean` | Reprezentanții legali sunt de acord? | Un conflict parental necesită clarificare juridică/locală, nu decizie automată. | true | false |
| `cult_id` | `enum` | În ce cult vrei botezul? | Ritualul și actele sunt stabilite de cult și parohie. | true | true |
| `locality` | `jurisdiction_ref` | În ce localitate vrei botezul? | Determină unitatea de cult competentă. | false | true |
| `parish_selected` | `boolean` | Ai ales parohia/comunitatea? | Cerințele se confirmă la nivel local. | false | true |
| `local_checklist_confirmed` | `boolean` | Ai primit checklistul oficial al unității de cult? | Nu există o listă națională unică. | false | true |
| `religion_data_storage_consent` | `boolean` | Consimți la stocarea în aplicație a informației religioase? | Este o categorie sensibilă de date. | true | true |
| `contribution_presented_as_mandatory_fee` | `boolean` | Ți s-a prezentat o contribuție ca taxă obligatorie? | Trebuie separată de o taxă publică națională. | false | false |
| `certificate_needed_after` | `boolean` | Ai nevoie de o dovadă/certificat emis de cult după ceremonie? | Forma și disponibilitatea documentului sunt stabilite local. | false | false |

## Gates

| prioritate | id | când | efect | cod | mesaj | claims |
|---:|---|---|---|---|---|---|
| 100 | `gate.no_candidate_consent` | candidate_kind == adult and candidate_consents == false | `block` | `BAPTISM_CONSENT_REQUIRED` | O persoană adultă nu poate fi ghidată spre botez împotriva voinței sale. | `claim.baptism.freedom_no_coercion` |
| 98 | `gate.age_16_choice` | candidate_age_years >= 16 and candidate_consents == false | `block` | `AGE_16_PERSONAL_RELIGIOUS_CHOICE` | De la 16 ani, minorul își alege singur religia; botezul nu poate continua fără voința sa. | `claim.baptism.child_16_choice`, `claim.baptism.freedom_no_coercion` |
| 96 | `gate.age_14_change` | candidate_age_years >= 14 and candidate_age_years < 16 and religion_change_involved == true and candidate_consents == false | `block` | `AGE_14_CONSENT_FOR_CHANGE_REQUIRED` | Schimbarea religiei după 14 ani nu se poate face fără consimțământul copilului. | `claim.baptism.child_14_consent` |
| 90 | `gate.guardian_unclear` | candidate_age_years < 16 and guardian_authority_confirmed == false | `needs_confirmation` | `LEGAL_REPRESENTATION_UNCONFIRMED` | Pentru minor, calitatea și autoritatea reprezentantului trebuie clarificate. | `claim.baptism.parents_religious_education`, `claim.baptism.cult_autonomy` |
| 88 | `gate.guardian_disagreement` | candidate_age_years < 16 and guardians_agree == false | `needs_confirmation` | `GUARDIAN_DISAGREEMENT` | Aplicația nu decide un conflict între reprezentanții legali privind opțiunea religioasă. | `claim.baptism.parents_religious_education`, `claim.baptism.freedom_no_coercion` |
| 85 | `gate.cult_unknown` | cult_id == unknown | `needs_confirmation` | `CULT_AND_PARISH_REQUIRED` | Ritualul și documentele nu pot fi stabilite fără cult și unitate locală. | `claim.baptism.cult_autonomy`, `claim.baptism.official_cult_directory` |
| 80 | `gate.local_checklist_missing` | parish_selected == false or local_checklist_confirmed == false | `needs_confirmation` | `LOCAL_BAPTISM_CHECKLIST_REQUIRED` | Actele, pregătirea, nașii/sponsorii și programarea trebuie confirmate local. | `claim.baptism.cult_autonomy`, `claim.baptism.orthodox_timisoara_channel`, `claim.baptism.catholic_timisoara_channel` |
| 75 | `gate.no_data_consent` | religion_data_storage_consent == false | `warn` | `RELIGION_DATA_NOT_STORED` | ActeOS nu va păstra cultul sau apartenența religioasă fără consimțământ expres. | `claim.baptism.religion_data_consent`, `claim.baptism.religion_disclosure_not_compulsory` |
| 70 | `gate.contribution_as_fee` | contribution_presented_as_mandatory_fee == true | `warn` | `RELIGIOUS_CONTRIBUTION_NOT_PUBLIC_FEE` | Nu trata o contribuție locală drept taxă publică universală obligatorie. | `claim.baptism.contributions_not_compelled`, `claim.baptism.cults_may_set_contributions` |

## Steps

### 1. Confirmă voința și reprezentarea

- **Ce faci:** Verifică consimțământul persoanei conform vârstei și, pentru minor, situația reprezentanților legali.
- **Până când:** `none`
- **Cum știi că e gata:** Consimțământul necesar și autoritatea de reprezentare sunt clarificate.
- **Dacă eșuează:** Oprește traseul dacă există constrângere sau conflict nerezolvat.
- **Canale:** `channel.cult_directory`
- **Claims:** `claim.baptism.freedom_no_coercion`, `claim.baptism.parents_religious_education`, `claim.baptism.child_14_consent`, `claim.baptism.child_16_choice`

### 2. Alege cultul și unitatea locală

- **Ce faci:** Folosește directorul oficial și canalele eparhiale/parohiale pentru localitatea aleasă.
- **Până când:** `none`
- **Cum știi că e gata:** Ai identificat unitatea locală și contactul oficial.
- **Dacă eșuează:** Contactează structura centrală/eparhială dacă parohia nu este publicată.
- **Canale:** `channel.cult_directory`, `channel.orthodox_timisoara`, `channel.catholic_timisoara`
- **Claims:** `claim.baptism.cult_autonomy`, `claim.baptism.official_cult_directory`, `claim.baptism.orthodox_timisoara_channel`, `claim.baptism.catholic_timisoara_channel`

### 3. Solicită checklistul local

- **Ce faci:** Cere în scris actele, condițiile pentru candidat și nași/sponsori, pregătirea/cateheza, programarea și contribuțiile, dacă există.
- **Până când:** `none`
- **Cum știi că e gata:** Ai checklistul local actual și răspunsul la situația concretă.
- **Dacă eșuează:** Cere clarificări eparhiei/structurii competente.
- **Canale:** `channel.orthodox_timisoara`, `channel.catholic_timisoara`
- **Claims:** `claim.baptism.cult_autonomy`, `claim.baptism.contributions_not_compelled`, `claim.baptism.cults_may_set_contributions`

### 4. Pregătește numai cerințele confirmate

- **Ce faci:** Adună documentele și finalizează pregătirea indicată de unitatea de cult; nu folosi checklisturi generice de pe bloguri.
- **Până când:** `none`
- **Cum știi că e gata:** Unitatea de cult confirmă că pregătirea este completă.
- **Dacă eșuează:** Corectează lipsurile comunicate de unitatea competentă.
- **Canale:** `channel.orthodox_timisoara`, `channel.catholic_timisoara`
- **Claims:** `claim.baptism.cult_autonomy`

### 5. Confirmă ceremonia și dovada ulterioară

- **Ce faci:** Obține confirmarea datei și întreabă dacă/în ce formă se eliberează un certificat sau extras după botez.
- **Până când:** `none`
- **Cum știi că e gata:** Ai confirmarea programării și știi cum se obține dovada, dacă este necesară.
- **Dacă eșuează:** Reprogramează sau solicită duplicatul direct unității de cult.
- **Canale:** `channel.orthodox_timisoara`, `channel.catholic_timisoara`
- **Claims:** `claim.baptism.cult_autonomy`

## Requirements

| id | titlu | obligație | timing | forme | verificări | claims |
|---|---|---|---|---|---|---|
| `req.consent_confirmation` | Confirmarea consimțământului | `mandatory` | `now` | declaration, electronic, original | user_confirmed | `claim.baptism.freedom_no_coercion`, `claim.baptism.child_14_consent`, `claim.baptism.child_16_choice` |
| `req.guardian_authority_confirmation` | Confirmarea reprezentării minorului | `conditional` | `now` | original, copy, electronic, certified_copy, declaration | exists, readable, names_consistent, user_confirmed | `claim.baptism.parents_religious_education` |
| `req.local_checklist_confirmation` | Checklistul oficial al parohiei/comunității | `mandatory` | `now` | electronic, copy, declaration | exists, readable, date_within_window, user_confirmed | `claim.baptism.cult_autonomy` |
| `req.religion_data_consent` | Consimțământ pentru stocarea datelor religioase | `conditional` | `now` | electronic, declaration | user_confirmed | `claim.baptism.religion_data_consent`, `claim.baptism.religion_disclosure_not_compulsory` |

## Official channels

| id | tip | etichetă | URL | integrare | teritoriu |
|---|---|---|---|---|---|
| `channel.cult_directory` | `web` | Secretariatul de Stat pentru Culte — director | https://culte.gov.ro/culte-religioase/ | `DEEP_LINK` | ro |
| `channel.orthodox_timisoara` | `web` | Arhiepiscopia Timișoarei — parohii/contact | https://www.arhiepiscopiatimisoarei.ro/ | `DEEP_LINK` | ro.tm, ro.tm.timisoara |
| `channel.catholic_timisoara` | `web` | Episcopia Romano-Catolică de Timișoara — parohii/contact | https://gerhardus.ro/ | `DEEP_LINK` | ro.tm, ro.tm.timisoara |

## Source claims

| claim_id | afirmație | sursă | confidence | locator |
|---|---|---|---|---|
| `claim.baptism.freedom_no_coercion` | Nicio persoană nu poate fi constrânsă să adere la o credință religioasă contrară convingerilor sale. | `law_489_2006` | `verified` | Art. 1 alin. (2); forma consolidată accesată la 25.06.2026 |
| `claim.baptism.parents_religious_education` | Părinții sau tutorii au dreptul exclusiv de a opta pentru educația religioasă a copiilor minori, potrivit propriilor convingeri. | `law_489_2006` | `verified` | Art. 3 alin. (1); forma consolidată accesată la 25.06.2026 |
| `claim.baptism.child_14_consent` | Religia copilului care a împlinit 14 ani nu poate fi schimbată fără consimțământul său. | `law_489_2006` | `verified` | Art. 3 alin. (2), prima teză; forma consolidată accesată la 25.06.2026 |
| `claim.baptism.child_16_choice` | Copilul care a împlinit 16 ani are dreptul să își aleagă singur religia. | `law_489_2006` | `verified` | Art. 3 alin. (2), teza finală; forma consolidată accesată la 25.06.2026 |
| `claim.baptism.cult_autonomy` | Ritualul, pregătirea și cerințele cultului sunt reglementate autonom prin statute și coduri canonice. | `law_489_2006` | `verified` | Art. 8 alin. (3); forma consolidată accesată la 25.06.2026 |
| `claim.baptism.religion_data_consent` | Prelucrarea apartenenței sau convingerilor religioase necesită consimțământ expres, în afara excepțiilor legale. | `law_489_2006` | `verified` | Art. 5 alin. (5); forma consolidată accesată la 25.06.2026 |
| `claim.baptism.religion_disclosure_not_compulsory` | Persoana nu poate fi obligată să își menționeze religia în relația cu autorități sau persoane juridice private. | `law_489_2006` | `verified` | Art. 5 alin. (6); forma consolidată accesată la 25.06.2026 |
| `claim.baptism.contributions_not_compelled` | Nimeni nu poate fi constrâns să contribuie la cheltuielile unui cult prin acte administrative sau alte metode. | `law_489_2006` | `verified` | Art. 10 alin. (5); forma consolidată accesată la 25.06.2026 |
| `claim.baptism.cults_may_set_contributions` | Cultele pot stabili contribuții din partea credincioșilor pentru activitățile lor. | `law_489_2006` | `verified` | Art. 10 alin. (2); forma consolidată accesată la 25.06.2026 |
| `claim.baptism.official_cult_directory` | Secretariatul de Stat pentru Culte publică directorul cultelor religioase recunoscute. | `cultes_list` | `verified_with_local_gap` | Titlul paginii/directorului oficial |
| `claim.baptism.orthodox_timisoara_channel` | Arhiepiscopia Timișoarei publică harta parohiilor și contacte eparhiale pentru Timișoara. | `archdiocese_timisoara` | `verified_with_local_gap` | Pagina principală, meniu «Protopopiate» |
| `claim.baptism.catholic_timisoara_channel` | Episcopia Romano-Catolică de Timișoara publică structura diecezei și lista parohiilor. | `diocese_timisoara` | `verified_with_local_gap` | Pagina principală, meniu «Episcopie» |

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
