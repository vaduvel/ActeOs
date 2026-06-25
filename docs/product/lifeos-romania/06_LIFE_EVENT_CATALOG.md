# Catalog de evenimente de viață (R1)

Acesta este catalogul executabil pentru R1: evenimentele 🔥 și descompunerea lor în proceduri atomice (`intent_id`) cu dependențe. Toate procedurile sunt `REQUIRES_HUMAN_CURATION` până la legarea de surse oficiale (vezi `19_SOURCE_REGISTRY.json`). ID-urile sunt canonice și stabile.

> Catalogul complet pe domenii (cu ⭐/🏔️ pentru R2/R3) este menținut separat ca taxonomie; aici sunt doar evenimentele R1 și grafurile lor.

## Convenții ID

- Eveniment: `ro.life.<slug>`
- Procedură (intent): `ro.<domain>.<object>.<action>`
- Jurisdicție: `ro`, `ro.tm`, `ro.tm.timisoara`

## E1 — `ro.life.move_residence` (M-am mutat) 🔥

Fapte de dezambiguizare: `move.same_county`, `person.owns_vehicle`, `person.has_minor_children`, `person.is_self_employed`, `housing.is_owner`.

| Procedură (intent_id) | Obligație | depends_on | Aplicabilitate |
|---|---|---|---|
| `ro.identity.id_card.address_change` | mandatory | — | mereu |
| `ro.auto.registration_certificate.address_update` | mandatory | id_card.address_change | owns_vehicle |
| `ro.tax_local.property.declare` | conditional | — | is_owner |
| `ro.utilities.transfer_holder` | conditional | — | mereu (per furnizor) |
| `ro.health.family_doctor.change` | optional | — | dacă schimbă zona |
| `ro.children.school.transfer` | conditional | — | has_minor_children |
| `ro.tax_anaf.residence.update` | conditional | — | is_self_employed |

Notă legală: actualizarea talonului după schimbarea domiciliului se face după emiterea noului act de identitate (de aici dependența). Termenul exact și sursa = de curatoriere.

## E2 — `ro.life.buy_used_car` (Mi-am cumpărat o mașină) 🔥

Fapte: `vehicle.bought_from` (persoană/dealer), `vehicle.category`, `buyer.jurisdiction`.

| Procedură | Obligație | depends_on | Aplicabilitate |
|---|---|---|---|
| `ro.auto.ownership.transfer_contract` | mandatory | — | mereu |
| `ro.tax_local.vehicle.declare` | mandatory | ownership.transfer_contract | mereu |
| `ro.tax_local.fiscal_certificate.vehicle` | mandatory | vehicle.declare | mereu |
| `ro.auto.rca.purchase` | mandatory | ownership.transfer_contract | mereu |
| `ro.auto.itp.perform` | mandatory | — | dacă ITP expirat |
| `ro.auto.registration.transfer` | mandatory | fiscal_certificate.vehicle, rca.purchase | mereu |

Graf tipic: contract → (impozit local → certificat fiscal) + RCA → înmatriculare DRPCIV; ITP în paralel dacă e nevoie.

## E3 — `ro.life.child_born` (Mi s-a născut copilul) 🔥

Fapte: `parents.employed_last_2y`, `birth.location` (RO/străinătate), `parents.marital_status`.

| Procedură | Obligație | depends_on | Aplicabilitate |
|---|---|---|---|
| `ro.civil.birth.register` | mandatory | — | mereu |
| `ro.identity.cnp.obtain` | mandatory | birth.register | mereu |
| `ro.benefits.state_allowance.request` | mandatory | birth.register | mereu |
| `ro.benefits.child_raising_indemnity.request` | conditional | birth.register | parents.employed_last_2y |
| `ro.health.newborn.family_doctor_enroll` | optional | birth.register | mereu |
| `ro.children.nursery.enroll` | optional | — | dacă dorește creșă |

## E4 — `ro.life.lost_documents` (Mi-am pierdut actele) 🔥

Fapte: `lost.items` (set: id_card, passport, driver_license, vehicle_doc, health_card), `lost.context` (furt/pierdere), `lost.abroad`.

| Procedură | Obligație | depends_on | Aplicabilitate |
|---|---|---|---|
| `ro.identity.id_card.reissue_lost` | mandatory | — | id_card ∈ items |
| `ro.identity.passport.reissue_lost` | conditional | — | passport ∈ items |
| `ro.auto.driver_license.reissue_lost` | conditional | id_card.reissue_lost | driver_license ∈ items |
| `ro.auto.registration_certificate.reissue_lost` | conditional | id_card.reissue_lost | vehicle_doc ∈ items |
| `ro.health.health_card.reissue_lost` | conditional | — | health_card ∈ items |

Notă: cele mai multe reemiteri cer un act de identitate valid; de aici dependența de `id_card.reissue_lost` când buletinul este în lista pierdută.

## E5 — `ro.life.id_card_expired` (Îmi expiră buletinul) 🔥

Fapte: `id.choose_electronic` (CEI vs CI simplă), `person.address_changed`.

| Procedură | Obligație | depends_on | Aplicabilitate |
|---|---|---|---|
| `ro.identity.id_card.renew` | mandatory | — | dacă nu alege CEI |
| `ro.identity.electronic_id.issue` | conditional | — | choose_electronic |
| `ro.auto.registration_certificate.address_update` | conditional | — | address_changed && owns_vehicle |

## Alte evenimente 🔥 din R1 (de descompus la curatoriere, același tipar)

`ro.life.sell_car`, `ro.life.buy_home`, `ro.life.rent_apartment`, `ro.life.utilities_transfer`, `ro.life.marriage`, `ro.life.name_change_marriage`, `ro.life.passport_apply`, `ro.life.driver_license_expired`, `ro.life.itp_due`, `ro.life.rca_renew`, `ro.life.enroll_kindergarten`, `ro.life.enroll_school`, `ro.life.state_allowance`, `ro.life.family_doctor_change`, `ro.life.health_card_lost`, `ro.life.local_taxes_pay`, `ro.life.fiscal_certificate`, `ro.life.criminal_record`, `ro.life.spv_enroll`, `ro.life.unemployment`, `ro.life.first_employee`, `ro.life.start_srl`, `ro.life.start_pfa`.

Fiecare primește: fapte de dezambiguizare, listă `ProcedureRef` cu `depends_on`, claim-uri de includere și fixture-uri de plan (pozitive și negative).
