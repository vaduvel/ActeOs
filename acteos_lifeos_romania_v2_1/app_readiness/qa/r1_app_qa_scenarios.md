# R1 App QA Scenarios

Scenariile de mai jos sunt generate din toate trigger phrases canonice din catalog. Când YAML-ul nu oferă încă un pas sau document sigur, câmpul rămâne `undetermined_from_yaml` și apare separat în raportul de gaps.

## Scenario ID: QA-R1-001
- Event ID: ro.life.identity_card_expired
- User phrase: îmi expiră cartea de identitate
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: Solicită un nou act de identitate înainte de expirare
- Expected required documents: Trei fotografii 3/4 cm
- Expected warnings/confirmations: Poti solicita noul act cu cel mult 180 de zile inainte de expirare, dar nu mai putin de 15 zile inainte.; Esti mai devreme de 180 de zile fata de expirare; cererea se poate depune incepand cu acel moment.; Termenul de solicitare este depasit sau aproape depasit; prezinta-te urgent la DEP.
- Expected blocker, if any: rule.exp.overdue<-claim.exp.sanction_40_80(conflicting); rule.exp.overdue<-claim.exp.sanction_500_1000(conflicting); rule.exp.sanction_conflict<-claim.exp.sanction_40_80(conflicting)
- Source files used:
  - research/inbox/ro.life.identity_card_expired/source_claims.yaml
  - research/inbox/ro.life.identity_card_expired/rules.yaml
  - research/inbox/ro.life.identity_card_expired/templates.yaml

## Scenario ID: QA-R1-002
- Event ID: ro.life.identity_card_expired
- User phrase: imi expira cartea de identitate
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: Solicită un nou act de identitate înainte de expirare
- Expected required documents: Trei fotografii 3/4 cm
- Expected warnings/confirmations: Poti solicita noul act cu cel mult 180 de zile inainte de expirare, dar nu mai putin de 15 zile inainte.; Esti mai devreme de 180 de zile fata de expirare; cererea se poate depune incepand cu acel moment.; Termenul de solicitare este depasit sau aproape depasit; prezinta-te urgent la DEP.
- Expected blocker, if any: rule.exp.overdue<-claim.exp.sanction_40_80(conflicting); rule.exp.overdue<-claim.exp.sanction_500_1000(conflicting); rule.exp.sanction_conflict<-claim.exp.sanction_40_80(conflicting)
- Source files used:
  - research/inbox/ro.life.identity_card_expired/source_claims.yaml
  - research/inbox/ro.life.identity_card_expired/rules.yaml
  - research/inbox/ro.life.identity_card_expired/templates.yaml

## Scenario ID: QA-R1-003
- Event ID: ro.life.identity_card_lost
- User phrase: mi-am pierdut cartea de identitate
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: Reclamă furtul la poliție
- Expected required documents: Cererea pentru eliberarea actului de identitate (Anexa 11); Certificatele de stare civilă; Dovada adresei de domiciliu sau reședință; Document oficial cu fotografie recentă; Declarația de consimțământ a gazdei
- Expected warnings/confirmations: Pierderea/distrugerea se anunta direct la SPCLEP de la domiciliu/resedinta, fara reclamatie la politie.; Daca imaginea ta nu e in R.N.E.P., adu un document oficial cu fotografie recenta (permis sau pasaport).; Actul declarat pierdut/furat/distrus este nul de drept si nu mai poate fi folosit.
- Expected blocker, if any: rule.lost.sanction_conflict<-claim.lost.sanction_500_1000(conflicting)
- Source files used:
  - research/inbox/ro.life.identity_card_lost/source_claims.yaml
  - research/inbox/ro.life.identity_card_lost/rules.yaml
  - research/inbox/ro.life.identity_card_lost/templates.yaml

## Scenario ID: QA-R1-004
- Event ID: ro.life.identity_card_lost
- User phrase: mi-am pierdut cartea de identitate
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: Reclamă furtul la poliție
- Expected required documents: Cererea pentru eliberarea actului de identitate (Anexa 11); Certificatele de stare civilă; Dovada adresei de domiciliu sau reședință; Document oficial cu fotografie recentă; Declarația de consimțământ a gazdei
- Expected warnings/confirmations: Pierderea/distrugerea se anunta direct la SPCLEP de la domiciliu/resedinta, fara reclamatie la politie.; Daca imaginea ta nu e in R.N.E.P., adu un document oficial cu fotografie recenta (permis sau pasaport).; Actul declarat pierdut/furat/distrus este nul de drept si nu mai poate fi folosit.
- Expected blocker, if any: rule.lost.sanction_conflict<-claim.lost.sanction_500_1000(conflicting)
- Source files used:
  - research/inbox/ro.life.identity_card_lost/source_claims.yaml
  - research/inbox/ro.life.identity_card_lost/rules.yaml
  - research/inbox/ro.life.identity_card_lost/templates.yaml

## Scenario ID: QA-R1-005
- Event ID: ro.life.identity_card_stolen
- User phrase: mi-a fost furată cartea de identitate
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Pierderea/distrugerea se anunta direct la SPCLEP de la domiciliu/resedinta, fara reclamatie la politie.; Daca imaginea ta nu e in R.N.E.P., adu un document oficial cu fotografie recenta (permis sau pasaport).; Actul declarat pierdut/furat/distrus este nul de drept si nu mai poate fi folosit.
- Expected blocker, if any: rule.lost.sanction_conflict<-claim.lost.sanction_500_1000(conflicting)
- Source files used:
  - research/inbox/ro.life.identity_card_stolen/source_claims.yaml
  - research/inbox/ro.life.identity_card_stolen/rules.yaml

## Scenario ID: QA-R1-006
- Event ID: ro.life.identity_card_stolen
- User phrase: mi-a fost furata cartea de identitate
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Pierderea/distrugerea se anunta direct la SPCLEP de la domiciliu/resedinta, fara reclamatie la politie.; Daca imaginea ta nu e in R.N.E.P., adu un document oficial cu fotografie recenta (permis sau pasaport).; Actul declarat pierdut/furat/distrus este nul de drept si nu mai poate fi folosit.
- Expected blocker, if any: rule.lost.sanction_conflict<-claim.lost.sanction_500_1000(conflicting)
- Source files used:
  - research/inbox/ro.life.identity_card_stolen/source_claims.yaml
  - research/inbox/ro.life.identity_card_stolen/rules.yaml

## Scenario ID: QA-R1-007
- Event ID: ro.life.identity_card_change_address
- User phrase: îmi schimb domiciliul din actul de identitate
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: go
- Expected first step: Actualizează actul de identitate la schimbarea domiciliului
- Expected required documents: Dovada adresei de domiciliu/reședință; Declarația de consimțământ a gazdei
- Expected warnings/confirmations: Pentru cartea electronica de identitate, schimbarea adresei nu necesita un nou act fizic (de confirmat).; Ai nevoie de declaratia de primire in spatiu a gazduitorului.; Pentru resedinta se inscrie mentiunea de resedinta, fara schimbarea domiciliului din act.
- Expected blocker, if any: none
- Source files used:
  - research/inbox/ro.life.identity_card_change_address/source_claims.yaml
  - research/inbox/ro.life.identity_card_change_address/rules.yaml
  - research/inbox/ro.life.identity_card_change_address/templates.yaml

## Scenario ID: QA-R1-008
- Event ID: ro.life.identity_card_change_address
- User phrase: imi schimb domiciliul din actul de identitate
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: go
- Expected first step: Actualizează actul de identitate la schimbarea domiciliului
- Expected required documents: Dovada adresei de domiciliu/reședință; Declarația de consimțământ a gazdei
- Expected warnings/confirmations: Pentru cartea electronica de identitate, schimbarea adresei nu necesita un nou act fizic (de confirmat).; Ai nevoie de declaratia de primire in spatiu a gazduitorului.; Pentru resedinta se inscrie mentiunea de resedinta, fara schimbarea domiciliului din act.
- Expected blocker, if any: none
- Source files used:
  - research/inbox/ro.life.identity_card_change_address/source_claims.yaml
  - research/inbox/ro.life.identity_card_change_address/rules.yaml
  - research/inbox/ro.life.identity_card_change_address/templates.yaml

## Scenario ID: QA-R1-009
- Event ID: ro.life.lost_all_documents
- User phrase: mi-am pierdut toate actele
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Reface intai cartea de identitate; restul documentelor necesita un act de identitate valid.; Pierdere (nu furt): de regula nu este necesara sesizarea la politie.; Confirma formularea oficiala SPCLEP privind pierderea vs furtul.
- Expected blocker, if any: rule.lad.loss_not_theft<-claim.lad.loss_no_police_required(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.lost_all_documents/source_claims.yaml
  - research/inbox/ro.life.lost_all_documents/rules.yaml

## Scenario ID: QA-R1-010
- Event ID: ro.life.lost_all_documents
- User phrase: mi-am pierdut toate actele
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Reface intai cartea de identitate; restul documentelor necesita un act de identitate valid.; Pierdere (nu furt): de regula nu este necesara sesizarea la politie.; Confirma formularea oficiala SPCLEP privind pierderea vs furtul.
- Expected blocker, if any: rule.lad.loss_not_theft<-claim.lad.loss_no_police_required(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.lost_all_documents/source_claims.yaml
  - research/inbox/ro.life.lost_all_documents/rules.yaml

## Scenario ID: QA-R1-011
- Event ID: ro.life.moved_home
- User phrase: m-am mutat
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: no_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Ai 15 zile de la mutare sa soliciti noul act de identitate. Nerespectarea se sanctioneaza contraventional (40-80 lei).; La cartea electronica de identitate (CEI) schimbarea adresei se poate face fara un act nou. Confirma procedura curenta la DEP inainte de a renunta la actualizare.; Daca detii vehicul, certificatul de inmatriculare trebuie actualizat la noua adresa la DRPCIV. Termenul legal exact este in curs de confirmare din sursa oficiala.
- Expected blocker, if any: rule.moved.vehicle_address_update<-claim.veh.address_update_exists(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.moved_home/source_claims.yaml
  - research/inbox/ro.life.moved_home/rules.yaml

## Scenario ID: QA-R1-012
- Event ID: ro.life.moved_home
- User phrase: m-am mutat
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: no_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Ai 15 zile de la mutare sa soliciti noul act de identitate. Nerespectarea se sanctioneaza contraventional (40-80 lei).; La cartea electronica de identitate (CEI) schimbarea adresei se poate face fara un act nou. Confirma procedura curenta la DEP inainte de a renunta la actualizare.; Daca detii vehicul, certificatul de inmatriculare trebuie actualizat la noua adresa la DRPCIV. Termenul legal exact este in curs de confirmare din sursa oficiala.
- Expected blocker, if any: rule.moved.vehicle_address_update<-claim.veh.address_update_exists(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.moved_home/source_claims.yaml
  - research/inbox/ro.life.moved_home/rules.yaml

## Scenario ID: QA-R1-013
- Event ID: ro.life.moved_to_another_city
- User phrase: m-am mutat în alt oraș sau județ
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: La schimbarea localitatii, impozitul auto trece la noua UAT; declara vehiculul la noul organ fiscal local.; Pentru copii, initiaza transferul/inscrierea la unitatea de invatamant de la noua adresa.; Procedura exacta de transfer fiscal intre UAT se confirma din Codul fiscal.
- Expected blocker, if any: rule.mac.trigger_vehicle_tax_new_uat<-claim.mac.vehicle_tax_at_new_domicile(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.moved_to_another_city/source_claims.yaml
  - research/inbox/ro.life.moved_to_another_city/rules.yaml

## Scenario ID: QA-R1-014
- Event ID: ro.life.moved_to_another_city
- User phrase: m-am mutat in alt oras sau judet
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: La schimbarea localitatii, impozitul auto trece la noua UAT; declara vehiculul la noul organ fiscal local.; Pentru copii, initiaza transferul/inscrierea la unitatea de invatamant de la noua adresa.; Procedura exacta de transfer fiscal intre UAT se confirma din Codul fiscal.
- Expected blocker, if any: rule.mac.trigger_vehicle_tax_new_uat<-claim.mac.vehicle_tax_at_new_domicile(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.moved_to_another_city/source_claims.yaml
  - research/inbox/ro.life.moved_to_another_city/rules.yaml

## Scenario ID: QA-R1-015
- Event ID: ro.life.bought_used_vehicle_ro
- User phrase: am cumpărat o mașină second-hand din românia
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: no_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Ai nevoie de RCA valabil pe numele tau inainte de transcriere.; Daca nu pastrezi numerele vechi, platesti pentru placute noi.; Termenul de 90 de zile pentru transcriere se confirma din Ordinul MAI 1501/2006 inainte de afisare ferma.
- Expected blocker, if any: rule.veh.transcription_90d<-claim.veh.transcription_90d(needs_confirmation); rule.veh.new_plates<-claim.veh.transcription_fee_37(needs_confirmation); rule.veh.tm_fiscal_channel<-claim.veh.tm_fiscal_channel(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.bought_used_vehicle_ro/source_claims.yaml
  - research/inbox/ro.life.bought_used_vehicle_ro/rules.yaml

## Scenario ID: QA-R1-016
- Event ID: ro.life.bought_used_vehicle_ro
- User phrase: am cumparat o masina second-hand din românia
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: no_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Ai nevoie de RCA valabil pe numele tau inainte de transcriere.; Daca nu pastrezi numerele vechi, platesti pentru placute noi.; Termenul de 90 de zile pentru transcriere se confirma din Ordinul MAI 1501/2006 inainte de afisare ferma.
- Expected blocker, if any: rule.veh.transcription_90d<-claim.veh.transcription_90d(needs_confirmation); rule.veh.new_plates<-claim.veh.transcription_fee_37(needs_confirmation); rule.veh.tm_fiscal_channel<-claim.veh.tm_fiscal_channel(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.bought_used_vehicle_ro/source_claims.yaml
  - research/inbox/ro.life.bought_used_vehicle_ro/rules.yaml

## Scenario ID: QA-R1-017
- Event ID: ro.life.sold_vehicle_ro
- User phrase: am vândut o mașină în românia
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: no_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Inainte de vanzare ai nevoie de certificatul de atestare fiscala / viza pe contract (valabil 30 de zile).; Pana cand vehiculul nu este scos din evidenta fiscala, impozitul ramane pe numele tau.; Recomandare: nu lasa mai mult de ~48 de ore intre viza fiscala si semnarea contractului.
- Expected blocker, if any: rule.sold.removal_from_evidence<-claim.sold.removal_deadline_30d(needs_confirmation); rule.sold.visa_48h_advice<-claim.sold.contract_visa_48h(needs_confirmation); rule.sold.tm_fiscal_channel<-claim.sold.tm_fiscal_channel(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.sold_vehicle_ro/source_claims.yaml
  - research/inbox/ro.life.sold_vehicle_ro/rules.yaml

## Scenario ID: QA-R1-018
- Event ID: ro.life.sold_vehicle_ro
- User phrase: am vândut o masina in românia
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: no_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Inainte de vanzare ai nevoie de certificatul de atestare fiscala / viza pe contract (valabil 30 de zile).; Pana cand vehiculul nu este scos din evidenta fiscala, impozitul ramane pe numele tau.; Recomandare: nu lasa mai mult de ~48 de ore intre viza fiscala si semnarea contractului.
- Expected blocker, if any: rule.sold.removal_from_evidence<-claim.sold.removal_deadline_30d(needs_confirmation); rule.sold.visa_48h_advice<-claim.sold.contract_visa_48h(needs_confirmation); rule.sold.tm_fiscal_channel<-claim.sold.tm_fiscal_channel(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.sold_vehicle_ro/source_claims.yaml
  - research/inbox/ro.life.sold_vehicle_ro/rules.yaml

## Scenario ID: QA-R1-019
- Event ID: ro.life.vehicle_transcription
- User phrase: transcriu dreptul de proprietate al vehiculului
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: no_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Cererea se solutioneaza in pana la 20 de zile lucratoare (de confirmat).; Termenul de 90 de zile se confirma din articolul exact al Ordinului 1501/2006 inainte de afisare ferma.
- Expected blocker, if any: rule.trans.90d<-claim.trans.90d(needs_confirmation); rule.trans.solve_time_info<-claim.trans.solve_20_working_days(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.vehicle_transcription/source_claims.yaml
  - research/inbox/ro.life.vehicle_transcription/rules.yaml

## Scenario ID: QA-R1-020
- Event ID: ro.life.vehicle_transcription
- User phrase: transcriu dreptul de proprietate al vehiculului
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: no_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Cererea se solutioneaza in pana la 20 de zile lucratoare (de confirmat).; Termenul de 90 de zile se confirma din articolul exact al Ordinului 1501/2006 inainte de afisare ferma.
- Expected blocker, if any: rule.trans.90d<-claim.trans.90d(needs_confirmation); rule.trans.solve_time_info<-claim.trans.solve_20_working_days(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.vehicle_transcription/source_claims.yaml
  - research/inbox/ro.life.vehicle_transcription/rules.yaml

## Scenario ID: QA-R1-021
- Event ID: ro.life.vehicle_change_address
- User phrase: mi-am schimbat adresa și am vehicul
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: no_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Ai nevoie de RCA valabil pentru eliberarea noului certificat.; Daca domiciliul din CI nu s-a schimbat, talonul nu trebuie actualizat pentru adresa.; Termenul de 30 de zile pentru actualizarea talonului se confirma din Ordinul 1501/2006 / OUG 195/2002.
- Expected blocker, if any: rule.vaddr.update_30d<-claim.vaddr.update_30d(needs_confirmation); rule.vaddr.update_30d<-claim.vaddr.docs(needs_confirmation); rule.vaddr.require_rca<-claim.vaddr.docs(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.vehicle_change_address/source_claims.yaml
  - research/inbox/ro.life.vehicle_change_address/rules.yaml

## Scenario ID: QA-R1-022
- Event ID: ro.life.vehicle_change_address
- User phrase: mi-am schimbat adresa si am vehicul
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: no_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Ai nevoie de RCA valabil pentru eliberarea noului certificat.; Daca domiciliul din CI nu s-a schimbat, talonul nu trebuie actualizat pentru adresa.; Termenul de 30 de zile pentru actualizarea talonului se confirma din Ordinul 1501/2006 / OUG 195/2002.
- Expected blocker, if any: rule.vaddr.update_30d<-claim.vaddr.update_30d(needs_confirmation); rule.vaddr.update_30d<-claim.vaddr.docs(needs_confirmation); rule.vaddr.require_rca<-claim.vaddr.docs(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.vehicle_change_address/source_claims.yaml
  - research/inbox/ro.life.vehicle_change_address/rules.yaml

## Scenario ID: QA-R1-023
- Event ID: ro.life.vehicle_local_tax_declaration
- User phrase: declar sau scot vehiculul de la taxe locale
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: not_checked
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: none
- Expected blocker, if any: none
- Source files used:

## Scenario ID: QA-R1-024
- Event ID: ro.life.vehicle_local_tax_declaration
- User phrase: declar sau scot vehiculul de la taxe locale
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: not_checked
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: none
- Expected blocker, if any: none
- Source files used:

## Scenario ID: QA-R1-025
- Event ID: ro.life.local_tax_certificate
- User phrase: am nevoie de certificat fiscal local
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: no_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Certificatul se elibereaza orientativ in cel mult 2 zile lucratoare (de confirmat).; La Timisoara poti solicita online prin plata.dfmt.ro; unele certificate se emit automat.; Se poate percepe o taxa de timbru (variaza pe UAT); confirma tariful pentru Timisoara.
- Expected blocker, if any: rule.fc.issue_term<-claim.fc.issue_2_working_days(needs_confirmation); rule.fc.validity<-claim.fc.validity_30d_pf(needs_confirmation); rule.fc.fee_info<-claim.fc.fee(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.local_tax_certificate/source_claims.yaml
  - research/inbox/ro.life.local_tax_certificate/rules.yaml

## Scenario ID: QA-R1-026
- Event ID: ro.life.local_tax_certificate
- User phrase: am nevoie de certificat fiscal local
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: no_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Certificatul se elibereaza orientativ in cel mult 2 zile lucratoare (de confirmat).; La Timisoara poti solicita online prin plata.dfmt.ro; unele certificate se emit automat.; Se poate percepe o taxa de timbru (variaza pe UAT); confirma tariful pentru Timisoara.
- Expected blocker, if any: rule.fc.issue_term<-claim.fc.issue_2_working_days(needs_confirmation); rule.fc.validity<-claim.fc.validity_30d_pf(needs_confirmation); rule.fc.fee_info<-claim.fc.fee(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.local_tax_certificate/source_claims.yaml
  - research/inbox/ro.life.local_tax_certificate/rules.yaml

## Scenario ID: QA-R1-027
- Event ID: ro.life.declare_vehicle_local_tax
- User phrase: declar un vehicul la taxe locale
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: Depune declarația fiscală pentru mijlocul de transport
- Expected required documents: Declarația fiscală pentru mijlocul de transport; Formularul distinct pentru peste 12 tone; Certificatul fiscal al vânzătorului; Dovada contractului cu operatorul de salubritate
- Expected warnings/confirmations: Pentru vehicule peste 12 tone se foloseste formularul de declaratie distinct.; Impozitul se datoreaza pentru tot anul de cine detine vehiculul la 31 decembrie al anului anterior.
- Expected blocker, if any: rule.vtax.salubritate_not_tm<-claim.vtax.salubritate_local(needs_confirmation); rule.vtax.tm_channel<-claim.vtax.tm_channel(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.declare_vehicle_local_tax/source_claims.yaml
  - research/inbox/ro.life.declare_vehicle_local_tax/rules.yaml
  - research/inbox/ro.life.declare_vehicle_local_tax/templates.yaml

## Scenario ID: QA-R1-028
- Event ID: ro.life.declare_vehicle_local_tax
- User phrase: declar un vehicul la taxe locale
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: Depune declarația fiscală pentru mijlocul de transport
- Expected required documents: Declarația fiscală pentru mijlocul de transport; Formularul distinct pentru peste 12 tone; Certificatul fiscal al vânzătorului; Dovada contractului cu operatorul de salubritate
- Expected warnings/confirmations: Pentru vehicule peste 12 tone se foloseste formularul de declaratie distinct.; Impozitul se datoreaza pentru tot anul de cine detine vehiculul la 31 decembrie al anului anterior.
- Expected blocker, if any: rule.vtax.salubritate_not_tm<-claim.vtax.salubritate_local(needs_confirmation); rule.vtax.tm_channel<-claim.vtax.tm_channel(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.declare_vehicle_local_tax/source_claims.yaml
  - research/inbox/ro.life.declare_vehicle_local_tax/rules.yaml
  - research/inbox/ro.life.declare_vehicle_local_tax/templates.yaml

## Scenario ID: QA-R1-029
- Event ID: ro.life.remove_vehicle_local_tax
- User phrase: scot un vehicul de la taxe locale
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: not_checked
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: none
- Expected blocker, if any: none
- Source files used:

## Scenario ID: QA-R1-030
- Event ID: ro.life.remove_vehicle_local_tax
- User phrase: scot un vehicul de la taxe locale
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: not_checked
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: none
- Expected blocker, if any: none
- Source files used:

## Scenario ID: QA-R1-031
- Event ID: ro.life.documents_stolen_bundle
- User phrase: mi-au fost furate actele și cardurile
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: O singura sesizare la politie acopera tot pachetul furat; pastreaza dovada pentru toate inlocuirile.; Inlocuirea permisului de conducere este un eveniment separat (R1B/ulterior).; Duplicat certificat de inmatriculare se elibereaza de SPCRPCIV (Ordinul 1501/2006).
- Expected blocker, if any: rule.dsb.single_police_report<-claim.dsb.single_police_report(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.documents_stolen_bundle/source_claims.yaml
  - research/inbox/ro.life.documents_stolen_bundle/rules.yaml

## Scenario ID: QA-R1-032
- Event ID: ro.life.documents_stolen_bundle
- User phrase: mi-au fost furate actele si cardurile
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: O singura sesizare la politie acopera tot pachetul furat; pastreaza dovada pentru toate inlocuirile.; Inlocuirea permisului de conducere este un eveniment separat (R1B/ulterior).; Duplicat certificat de inmatriculare se elibereaza de SPCRPCIV (Ordinul 1501/2006).
- Expected blocker, if any: rule.dsb.single_police_report<-claim.dsb.single_police_report(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.documents_stolen_bundle/source_claims.yaml
  - research/inbox/ro.life.documents_stolen_bundle/rules.yaml

## Scenario ID: QA-R1-033
- Event ID: ro.life.passport_first_or_renew
- User phrase: îmi fac sau îmi reînnoiesc pașaportul
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: go
- Expected first step: Depune cererea de pașaport
- Expected required documents: Act de identitate valabil în original; Dovada plății taxei de pașaport; Pașaportul anterior
- Expected warnings/confirmations: Valabilitate pasaport electronic: 3 ani (sub 12 ani).; Valabilitate pasaport electronic: 5 ani (12-18 ani).; Valabilitate pasaport electronic: 10 ani (peste 18 ani).
- Expected blocker, if any: none
- Source files used:
  - research/inbox/ro.life.passport_first_or_renew/source_claims.yaml
  - research/inbox/ro.life.passport_first_or_renew/rules.yaml
  - research/inbox/ro.life.passport_first_or_renew/templates.yaml

## Scenario ID: QA-R1-034
- Event ID: ro.life.passport_first_or_renew
- User phrase: imi fac sau imi reinnoiesc pasaportul
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: go
- Expected first step: Depune cererea de pașaport
- Expected required documents: Act de identitate valabil în original; Dovada plății taxei de pașaport; Pașaportul anterior
- Expected warnings/confirmations: Valabilitate pasaport electronic: 3 ani (sub 12 ani).; Valabilitate pasaport electronic: 5 ani (12-18 ani).; Valabilitate pasaport electronic: 10 ani (peste 18 ani).
- Expected blocker, if any: none
- Source files used:
  - research/inbox/ro.life.passport_first_or_renew/source_claims.yaml
  - research/inbox/ro.life.passport_first_or_renew/rules.yaml
  - research/inbox/ro.life.passport_first_or_renew/templates.yaml

## Scenario ID: QA-R1-035
- Event ID: ro.life.minor_passport
- User phrase: fac pașaport unui minor
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: go
- Expected first step: Depune cererea de pașaport pentru minor
- Expected required documents: Certificatul de naștere al minorului; Actele de identitate ale părinților; Dovada plății taxei de pașaport; Document pentru depunerea fără ambii părinți; Două fotografii ale minorului (3,5 × 4,5 cm); Cartea de identitate a minorului (peste 14 ani)
- Expected warnings/confirmations: Prezenta minorului si a parintilor este obligatorie la depunere.; Daca minorul nu este prezent, sunt necesare 2 fotografii 3,5x4,5 cm.; Minorul peste 14 ani isi ridica pasaportul personal, insotit de un parinte, cu CI valabila.
- Expected blocker, if any: none
- Source files used:
  - research/inbox/ro.life.minor_passport/source_claims.yaml
  - research/inbox/ro.life.minor_passport/rules.yaml
  - research/inbox/ro.life.minor_passport/templates.yaml

## Scenario ID: QA-R1-036
- Event ID: ro.life.minor_passport
- User phrase: fac pasaport unui minor
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: go
- Expected first step: Depune cererea de pașaport pentru minor
- Expected required documents: Certificatul de naștere al minorului; Actele de identitate ale părinților; Dovada plății taxei de pașaport; Document pentru depunerea fără ambii părinți; Două fotografii ale minorului (3,5 × 4,5 cm); Cartea de identitate a minorului (peste 14 ani)
- Expected warnings/confirmations: Prezenta minorului si a parintilor este obligatorie la depunere.; Daca minorul nu este prezent, sunt necesare 2 fotografii 3,5x4,5 cm.; Minorul peste 14 ani isi ridica pasaportul personal, insotit de un parinte, cu CI valabila.
- Expected blocker, if any: none
- Source files used:
  - research/inbox/ro.life.minor_passport/source_claims.yaml
  - research/inbox/ro.life.minor_passport/rules.yaml
  - research/inbox/ro.life.minor_passport/templates.yaml

## Scenario ID: QA-R1-037
- Event ID: ro.life.criminal_record_certificate
- User phrase: am nevoie de cazier judiciar
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: Depune cererea de certificat de cazier judiciar
- Expected required documents: Act de identitate valabil; Cerere-tip pentru cazier judiciar; Documente pentru reprezentantul legal; Împuternicire pentru depunerea prin mandat; Act de identitate al imputernicitului
- Expected warnings/confirmations: Sub 14 ani cererea se depune prin reprezentant legal (parinte/tutore).; Pentru cetateni romani: eliberare pe loc sau in cel mult 3 zile lucratoare.; Pentru cetateni straini: eliberare in aproximativ 30 de zile (se ataseaza extrase din alte state).
- Expected blocker, if any: rule.cj.validity_6m<-claim.cj.validity_6m(needs_confirmation); rule.cj.fee_conflict<-claim.cj.fee_conflict(conflicting); rule.cj.power_of_attorney<-claim.cj.power_of_attorney(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.criminal_record_certificate/source_claims.yaml
  - research/inbox/ro.life.criminal_record_certificate/rules.yaml
  - research/inbox/ro.life.criminal_record_certificate/templates.yaml

## Scenario ID: QA-R1-038
- Event ID: ro.life.criminal_record_certificate
- User phrase: am nevoie de cazier judiciar
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: Depune cererea de certificat de cazier judiciar
- Expected required documents: Act de identitate valabil; Cerere-tip pentru cazier judiciar; Documente pentru reprezentantul legal; Împuternicire pentru depunerea prin mandat; Act de identitate al imputernicitului
- Expected warnings/confirmations: Sub 14 ani cererea se depune prin reprezentant legal (parinte/tutore).; Pentru cetateni romani: eliberare pe loc sau in cel mult 3 zile lucratoare.; Pentru cetateni straini: eliberare in aproximativ 30 de zile (se ataseaza extrase din alte state).
- Expected blocker, if any: rule.cj.validity_6m<-claim.cj.validity_6m(needs_confirmation); rule.cj.fee_conflict<-claim.cj.fee_conflict(conflicting); rule.cj.power_of_attorney<-claim.cj.power_of_attorney(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.criminal_record_certificate/source_claims.yaml
  - research/inbox/ro.life.criminal_record_certificate/rules.yaml
  - research/inbox/ro.life.criminal_record_certificate/templates.yaml

## Scenario ID: QA-R1-039
- Event ID: ro.life.change_electricity_holder
- User phrase: schimb titularul contractului de electricitate
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: Solicită schimbarea titularului contractului de energie electrică
- Expected required documents: Act de identitate valabil; Act care atestă dreptul locativ; Indexul contorului la zi; Certificatul de deces al titularului
- Expected warnings/confirmations: La deces contractul inceteaza; se depune copie act identitate solicitant + copie certificat de deces al titularului.; Schimbarea furnizorului este gratuita (ANRE); nu se percep taxe pentru proces.; Noul contract intra in vigoare in ~21 zile de la cerere (de confirmat pentru titular).
- Expected blocker, if any: rule.elec.activation_term<-claim.elec.21d(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.change_electricity_holder/source_claims.yaml
  - research/inbox/ro.life.change_electricity_holder/rules.yaml
  - research/inbox/ro.life.change_electricity_holder/templates.yaml

## Scenario ID: QA-R1-040
- Event ID: ro.life.change_electricity_holder
- User phrase: schimb titularul contractului de electricitate
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: Solicită schimbarea titularului contractului de energie electrică
- Expected required documents: Act de identitate valabil; Act care atestă dreptul locativ; Indexul contorului la zi; Certificatul de deces al titularului
- Expected warnings/confirmations: La deces contractul inceteaza; se depune copie act identitate solicitant + copie certificat de deces al titularului.; Schimbarea furnizorului este gratuita (ANRE); nu se percep taxe pentru proces.; Noul contract intra in vigoare in ~21 zile de la cerere (de confirmat pentru titular).
- Expected blocker, if any: rule.elec.activation_term<-claim.elec.21d(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.change_electricity_holder/source_claims.yaml
  - research/inbox/ro.life.change_electricity_holder/rules.yaml
  - research/inbox/ro.life.change_electricity_holder/templates.yaml

## Scenario ID: QA-R1-041
- Event ID: ro.life.change_gas_holder
- User phrase: schimb titularul contractului de gaz
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: go
- Expected first step: Solicită schimbarea titularului contractului de gaze
- Expected required documents: Copie a actului de identitate; Declarație privind calitatea folosirii imobilului; Poză a contorului de gaz; Codul locului de consum; Certificatul de deces al titularului
- Expected warnings/confirmations: Ca proprietar, poti folosi actul de proprietate in locul declaratiei pe propria raspundere.; La deces contractul de gaze inceteaza; se incheie contract nou cu copie certificat de deces al titularului.; Furnizorul se alege liber; identifica operatorul de distributie gaz din zona ta (de confirmat pentru Timis).
- Expected blocker, if any: none
- Source files used:
  - research/inbox/ro.life.change_gas_holder/source_claims.yaml
  - research/inbox/ro.life.change_gas_holder/rules.yaml
  - research/inbox/ro.life.change_gas_holder/templates.yaml

## Scenario ID: QA-R1-042
- Event ID: ro.life.change_gas_holder
- User phrase: schimb titularul contractului de gaz
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: go
- Expected first step: Solicită schimbarea titularului contractului de gaze
- Expected required documents: Copie a actului de identitate; Declarație privind calitatea folosirii imobilului; Poză a contorului de gaz; Codul locului de consum; Certificatul de deces al titularului
- Expected warnings/confirmations: Ca proprietar, poti folosi actul de proprietate in locul declaratiei pe propria raspundere.; La deces contractul de gaze inceteaza; se incheie contract nou cu copie certificat de deces al titularului.; Furnizorul se alege liber; identifica operatorul de distributie gaz din zona ta (de confirmat pentru Timis).
- Expected blocker, if any: none
- Source files used:
  - research/inbox/ro.life.change_gas_holder/source_claims.yaml
  - research/inbox/ro.life.change_gas_holder/rules.yaml
  - research/inbox/ro.life.change_gas_holder/templates.yaml

## Scenario ID: QA-R1-043
- Event ID: ro.life.change_water_holder
- User phrase: schimb titularul contractului de apă
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: Depune documentația pentru contractul Aquatim
- Expected required documents: Act de identitate valabil; Dovada folosirii spațiului; Certificatul de deces al titularului
- Expected warnings/confirmations: La Timisoara operatorul unic este Aquatim; contractul se incheie cu formularul F-01.00.06-3.; Exista deja bransament/racord: depui documentele si Aquatim te contacteaza pentru semnare.; Fara bransament/racord existent este nevoie intai de aviz tehnic de bransare/racordare (alt proces).
- Expected blocker, if any: rule.water.death_path<-claim.water.death_terminates(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.change_water_holder/source_claims.yaml
  - research/inbox/ro.life.change_water_holder/rules.yaml
  - research/inbox/ro.life.change_water_holder/templates.yaml

## Scenario ID: QA-R1-044
- Event ID: ro.life.change_water_holder
- User phrase: schimb titularul contractului de apa
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: Depune documentația pentru contractul Aquatim
- Expected required documents: Act de identitate valabil; Dovada folosirii spațiului; Certificatul de deces al titularului
- Expected warnings/confirmations: La Timisoara operatorul unic este Aquatim; contractul se incheie cu formularul F-01.00.06-3.; Exista deja bransament/racord: depui documentele si Aquatim te contacteaza pentru semnare.; Fara bransament/racord existent este nevoie intai de aviz tehnic de bransare/racordare (alt proces).
- Expected blocker, if any: rule.water.death_path<-claim.water.death_terminates(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.change_water_holder/source_claims.yaml
  - research/inbox/ro.life.change_water_holder/rules.yaml
  - research/inbox/ro.life.change_water_holder/templates.yaml

## Scenario ID: QA-R1-045
- Event ID: ro.life.child_birth
- User phrase: mi s-a născut copilul
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Declară nașterea în 30 de zile de la data nașterii.; Pentru copilul născut mort, declararea are termen de 3 zile.; Declararea nașterii se face în 24 de ore de la deces.
- Expected blocker, if any: none
- Source files used:
  - research/inbox/ro.life.child_birth/source_claims.yaml
  - research/inbox/ro.life.child_birth/rules.yaml

## Scenario ID: QA-R1-046
- Event ID: ro.life.child_birth
- User phrase: mi s-a nascut copilul
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Declară nașterea în 30 de zile de la data nașterii.; Pentru copilul născut mort, declararea are termen de 3 zile.; Declararea nașterii se face în 24 de ore de la deces.
- Expected blocker, if any: none
- Source files used:
  - research/inbox/ro.life.child_birth/source_claims.yaml
  - research/inbox/ro.life.child_birth/rules.yaml

## Scenario ID: QA-R1-047
- Event ID: ro.life.birth_registration
- User phrase: declar nașterea copilului
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: go
- Expected first step: Înregistrează nașterea copilului
- Expected required documents: Certificat medical constatator al nașterii; Act de identitate al mamei; Act de identitate al declarantului; Certificat de căsătorie al părinților; Declarație privind numele copilului; Declarație de recunoaștere paternitate; Consimțământ privind numele copilului; Aviz de conformitate județean
- Expected warnings/confirmations: Declară nașterea în 30 de zile de la data nașterii.; Declară nașterea copilului născut mort în 3 zile.; Declară nașterea în 24 de ore de la deces.
- Expected blocker, if any: none
- Source files used:
  - research/inbox/ro.life.birth_registration/source_claims.yaml
  - research/inbox/ro.life.birth_registration/rules.yaml
  - research/inbox/ro.life.birth_registration/templates.yaml

## Scenario ID: QA-R1-048
- Event ID: ro.life.birth_registration
- User phrase: declar nasterea copilului
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: go
- Expected first step: Înregistrează nașterea copilului
- Expected required documents: Certificat medical constatator al nașterii; Act de identitate al mamei; Act de identitate al declarantului; Certificat de căsătorie al părinților; Declarație privind numele copilului; Declarație de recunoaștere paternitate; Consimțământ privind numele copilului; Aviz de conformitate județean
- Expected warnings/confirmations: Declară nașterea în 30 de zile de la data nașterii.; Declară nașterea copilului născut mort în 3 zile.; Declară nașterea în 24 de ore de la deces.
- Expected blocker, if any: none
- Source files used:
  - research/inbox/ro.life.birth_registration/source_claims.yaml
  - research/inbox/ro.life.birth_registration/rules.yaml
  - research/inbox/ro.life.birth_registration/templates.yaml

## Scenario ID: QA-R1-049
- Event ID: ro.life.child_allowance
- User phrase: solicit alocația copilului
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: Depune cerere de alocație pentru copil
- Expected required documents: Cerere pentru alocația de stat; Certificat de naștere al copilului; Act de identitate al solicitantului; Adeverință de înscriere la școală; Certificat de handicap; Certificat medical de motiv medical de repetare; Documente de rezidență pentru copil străin/apatrid; Acordul părinților sau hotărârea aplicabilă; Consimțământ reprezentant legal (plată directă copil)
- Expected warnings/confirmations: Dreptul începe din luna următoare nașterii; plata urmează cererii, cu retroactivitate de cel mult 12 luni.; Comunică modificarea în cel mult 15 zile.; Cuantumul numeric 2026 trebuie preluat dintr-o sursă oficială care publică valorile curente; nu se deduce manual din textul consolidat.
- Expected blocker, if any: rule.allowance.amount_2026_confirmation<-claim.allowance.amount_2026_freeze(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.child_allowance/source_claims.yaml
  - research/inbox/ro.life.child_allowance/rules.yaml
  - research/inbox/ro.life.child_allowance/templates.yaml

## Scenario ID: QA-R1-050
- Event ID: ro.life.child_allowance
- User phrase: solicit alocatia copilului
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: conditional_go
- Expected first step: Depune cerere de alocație pentru copil
- Expected required documents: Cerere pentru alocația de stat; Certificat de naștere al copilului; Act de identitate al solicitantului; Adeverință de înscriere la școală; Certificat de handicap; Certificat medical de motiv medical de repetare; Documente de rezidență pentru copil străin/apatrid; Acordul părinților sau hotărârea aplicabilă; Consimțământ reprezentant legal (plată directă copil)
- Expected warnings/confirmations: Dreptul începe din luna următoare nașterii; plata urmează cererii, cu retroactivitate de cel mult 12 luni.; Comunică modificarea în cel mult 15 zile.; Cuantumul numeric 2026 trebuie preluat dintr-o sursă oficială care publică valorile curente; nu se deduce manual din textul consolidat.
- Expected blocker, if any: rule.allowance.amount_2026_confirmation<-claim.allowance.amount_2026_freeze(needs_confirmation)
- Source files used:
  - research/inbox/ro.life.child_allowance/source_claims.yaml
  - research/inbox/ro.life.child_allowance/rules.yaml
  - research/inbox/ro.life.child_allowance/templates.yaml

## Scenario ID: QA-R1-051
- Event ID: ro.life.nursery_enrollment
- User phrase: înscriu copilul la creșă
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: no_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Fereastra standard de reînscriere a fost 18-22 mai 2026.; Etapa a II-a folosește o nouă cerere cu trei opțiuni, pe locurile rămase.; Numărul de înregistrare nu acordă prioritate; se aplică criteriile oficiale.
- Expected blocker, if any: rule.nursery.local_gap<-claim.nursery.timis.local_dataset(expired)
- Source files used:
  - research/inbox/ro.life.nursery_enrollment/source_claims.yaml
  - research/inbox/ro.life.nursery_enrollment/rules.yaml

## Scenario ID: QA-R1-052
- Event ID: ro.life.nursery_enrollment
- User phrase: inscriu copilul la cresa
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: no_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Fereastra standard de reînscriere a fost 18-22 mai 2026.; Etapa a II-a folosește o nouă cerere cu trei opțiuni, pe locurile rămase.; Numărul de înregistrare nu acordă prioritate; se aplică criteriile oficiale.
- Expected blocker, if any: rule.nursery.local_gap<-claim.nursery.timis.local_dataset(expired)
- Source files used:
  - research/inbox/ro.life.nursery_enrollment/source_claims.yaml
  - research/inbox/ro.life.nursery_enrollment/rules.yaml

## Scenario ID: QA-R1-053
- Event ID: ro.life.preschool_enrollment
- User phrase: înscriu copilul la grădiniță
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: no_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Fereastra standard de reînscriere a fost 18-22 mai 2026.; Etapa a II-a folosește o nouă cerere cu trei opțiuni, pe locurile rămase.; Numărul de înregistrare nu acordă prioritate; se aplică criteriile oficiale.
- Expected blocker, if any: rule.preschool.local_gap<-claim.preschool.timis.local_dataset(expired)
- Source files used:
  - research/inbox/ro.life.preschool_enrollment/source_claims.yaml
  - research/inbox/ro.life.preschool_enrollment/rules.yaml

## Scenario ID: QA-R1-054
- Event ID: ro.life.preschool_enrollment
- User phrase: inscriu copilul la gradinita
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: no_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: Fereastra standard de reînscriere a fost 18-22 mai 2026.; Etapa a II-a folosește o nouă cerere cu trei opțiuni, pe locurile rămase.; Numărul de înregistrare nu acordă prioritate; se aplică criteriile oficiale.
- Expected blocker, if any: rule.preschool.local_gap<-claim.preschool.timis.local_dataset(expired)
- Source files used:
  - research/inbox/ro.life.preschool_enrollment/source_claims.yaml
  - research/inbox/ro.life.preschool_enrollment/rules.yaml

## Scenario ID: QA-R1-055
- Event ID: ro.life.preparatory_class_enrollment
- User phrase: înscriu copilul în clasa pregătitoare
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: no_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: La școala de circumscripție, înscrierea este asigurată după validarea cererii.; O altă școală poate admite numai în limita locurilor și după criteriile aplicabile.; Completarea online nu finalizează dosarul; cererea trebuie validată.
- Expected blocker, if any: rule.prep.local_gap<-claim.prep.timis.catchments(verified_with_local_gap)
- Source files used:
  - research/inbox/ro.life.preparatory_class_enrollment/source_claims.yaml
  - research/inbox/ro.life.preparatory_class_enrollment/rules.yaml

## Scenario ID: QA-R1-056
- Event ID: ro.life.preparatory_class_enrollment
- User phrase: inscriu copilul in clasa pregatitoare
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: no_go
- Expected first step: undetermined_from_yaml
- Expected required documents: undetermined_from_yaml
- Expected warnings/confirmations: La școala de circumscripție, înscrierea este asigurată după validarea cererii.; O altă școală poate admite numai în limita locurilor și după criteriile aplicabile.; Completarea online nu finalizează dosarul; cererea trebuie validată.
- Expected blocker, if any: rule.prep.local_gap<-claim.prep.timis.catchments(verified_with_local_gap)
- Source files used:
  - research/inbox/ro.life.preparatory_class_enrollment/source_claims.yaml
  - research/inbox/ro.life.preparatory_class_enrollment/rules.yaml

## Scenario ID: QA-R1-057
- Event ID: ro.life.pay_fine
- User phrase: plătesc o amendă
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: go
- Expected first step: Plătește în 15 zile jumătate din minimul legal
- Expected required documents: Minimul legal al amenzii și datele de plată; Actul sancționator și minimul legal; Cuantumul amenzii aplicate și datele de plată
- Expected warnings/confirmations: Baza este minimul din actul normativ, nu neapărat amenda aplicată în procesul-verbal.; Fereastra generală de 15 zile pentru plata redusă a trecut.; Pentru această regulă specială, baza este amenda aplicată.
- Expected blocker, if any: none
- Source files used:
  - research/inbox/ro.life.pay_fine/source_claims.yaml
  - research/inbox/ro.life.pay_fine/rules.yaml
  - research/inbox/ro.life.pay_fine/templates.yaml

## Scenario ID: QA-R1-058
- Event ID: ro.life.pay_fine
- User phrase: platesc o amenda
- Given facts: reference_date=2026-06-27; timezone=Europe/Bucharest; jurisdiction_path=[ro, ro.tm.timisoara]; facts=undetermined_from_yaml
- Expected app route status: go
- Expected first step: Plătește în 15 zile jumătate din minimul legal
- Expected required documents: Minimul legal al amenzii și datele de plată; Actul sancționator și minimul legal; Cuantumul amenzii aplicate și datele de plată
- Expected warnings/confirmations: Baza este minimul din actul normativ, nu neapărat amenda aplicată în procesul-verbal.; Fereastra generală de 15 zile pentru plata redusă a trecut.; Pentru această regulă specială, baza este amenda aplicată.
- Expected blocker, if any: none
- Source files used:
  - research/inbox/ro.life.pay_fine/source_claims.yaml
  - research/inbox/ro.life.pay_fine/rules.yaml
  - research/inbox/ro.life.pay_fine/templates.yaml
