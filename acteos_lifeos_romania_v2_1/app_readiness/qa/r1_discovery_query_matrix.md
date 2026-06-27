# R1 Discovery Query Matrix

Baza: `data/r1_event_catalog.yaml`, `data/intent_taxonomy.yaml`, `data/intent_event_links.yaml`, `contracts/intent_ranking.yaml` și `contracts/openapi.yaml`.

## Rezumat risc

- `low`: 30 query rows
- `medium`: 0 query rows
- `high`: 28 query rows

| query_ro | normalized_query_if_obvious | expected_event_id | category_id | ambiguity_risk | ambiguity_reason | needs_disambiguation_prompt | suggested_disambiguation_ro |
| --- | --- | --- | --- | --- | --- | --- | --- |
| îmi expiră cartea de identitate | imi expira cartea de identitate | ro.life.identity_card_expired | identity_documents | low | trigger phrase suficient de specifică în catalog | no |  |
| imi expira cartea de identitate | imi expira cartea de identitate | ro.life.identity_card_expired | identity_documents | low | trigger phrase suficient de specifică în catalog | no |  |
| mi-am pierdut cartea de identitate | mi-am pierdut cartea de identitate | ro.life.identity_card_lost | identity_documents | high | confuzie posibilă între pierdut și furat | yes | Este pierdut sau furat? |
| mi-am pierdut cartea de identitate | mi-am pierdut cartea de identitate | ro.life.identity_card_lost | identity_documents | high | confuzie posibilă între pierdut și furat | yes | Este pierdut sau furat? |
| mi-a fost furată cartea de identitate | mi-a fost furata cartea de identitate | ro.life.identity_card_stolen | identity_documents | high | confuzie posibilă între pierdut și furat | yes | Este pierdut sau furat? |
| mi-a fost furata cartea de identitate | mi-a fost furata cartea de identitate | ro.life.identity_card_stolen | identity_documents | high | confuzie posibilă între pierdut și furat | yes | Este pierdut sau furat? |
| îmi schimb domiciliul din actul de identitate | imi schimb domiciliul din actul de identitate | ro.life.identity_card_change_address | identity_documents | high | mutare generală vs schimbarea adresei din act | yes | Vrei doar schimbarea adresei din act sau toate formalitățile după mutare? |
| imi schimb domiciliul din actul de identitate | imi schimb domiciliul din actul de identitate | ro.life.identity_card_change_address | identity_documents | high | mutare generală vs schimbarea adresei din act | yes | Vrei doar schimbarea adresei din act sau toate formalitățile după mutare? |
| mi-am pierdut toate actele | mi-am pierdut toate actele | ro.life.lost_all_documents | identity_documents | high | intent de tip bundle/orchestrator; confuzie posibilă între pierdut și furat | yes | Este pierdut sau furat? |
| mi-am pierdut toate actele | mi-am pierdut toate actele | ro.life.lost_all_documents | identity_documents | high | intent de tip bundle/orchestrator; confuzie posibilă între pierdut și furat | yes | Este pierdut sau furat? |
| m-am mutat | m-am mutat | ro.life.moved_home | home_address_utilities | high | event-ul este legat de mai multe intent-uri publice; intent de tip bundle/orchestrator; mutare generală vs schimbarea adresei din act | yes | Vrei doar schimbarea adresei din act sau toate formalitățile după mutare? |
| m-am mutat | m-am mutat | ro.life.moved_home | home_address_utilities | high | event-ul este legat de mai multe intent-uri publice; intent de tip bundle/orchestrator; mutare generală vs schimbarea adresei din act | yes | Vrei doar schimbarea adresei din act sau toate formalitățile după mutare? |
| m-am mutat în alt oraș sau județ | m-am mutat in alt oras sau judet | ro.life.moved_to_another_city | home_address_utilities | high | event-ul este legat de mai multe intent-uri publice; intent de tip bundle/orchestrator; mutare generală vs schimbarea adresei din act | yes | Vrei doar schimbarea adresei din act sau toate formalitățile după mutare? |
| m-am mutat in alt oras sau judet | m-am mutat in alt oras sau judet | ro.life.moved_to_another_city | home_address_utilities | high | event-ul este legat de mai multe intent-uri publice; intent de tip bundle/orchestrator; mutare generală vs schimbarea adresei din act | yes | Vrei doar schimbarea adresei din act sau toate formalitățile după mutare? |
| am cumpărat o mașină second-hand din românia | am cumparat o masina second-hand din romania | ro.life.bought_used_vehicle_ro | vehicles_mobility | high | intent de tip bundle/orchestrator | yes | Vrei traseul complet sau doar un pas specific? |
| am cumparat o masina second-hand din românia | am cumparat o masina second-hand din romania | ro.life.bought_used_vehicle_ro | vehicles_mobility | high | intent de tip bundle/orchestrator | yes | Vrei traseul complet sau doar un pas specific? |
| am vândut o mașină în românia | am vandut o masina in romania | ro.life.sold_vehicle_ro | vehicles_mobility | high | intent de tip bundle/orchestrator | yes | Vrei traseul complet sau doar un pas specific? |
| am vândut o masina in românia | am vandut o masina in romania | ro.life.sold_vehicle_ro | vehicles_mobility | high | intent de tip bundle/orchestrator | yes | Vrei traseul complet sau doar un pas specific? |
| transcriu dreptul de proprietate al vehiculului | transcriu dreptul de proprietate al vehiculului | ro.life.vehicle_transcription | vehicles_mobility | high | intent de tip bundle/orchestrator; confuzie între declarare, scoatere și transcriere vehicul | yes | Vrei să îl declari, să îl scoți de la taxe sau să transcrii proprietatea? |
| transcriu dreptul de proprietate al vehiculului | transcriu dreptul de proprietate al vehiculului | ro.life.vehicle_transcription | vehicles_mobility | high | intent de tip bundle/orchestrator; confuzie între declarare, scoatere și transcriere vehicul | yes | Vrei să îl declari, să îl scoți de la taxe sau să transcrii proprietatea? |
| mi-am schimbat adresa și am vehicul | mi-am schimbat adresa si am vehicul | ro.life.vehicle_change_address | vehicles_mobility | low | trigger phrase suficient de specifică în catalog | no |  |
| mi-am schimbat adresa si am vehicul | mi-am schimbat adresa si am vehicul | ro.life.vehicle_change_address | vehicles_mobility | low | trigger phrase suficient de specifică în catalog | no |  |
| declar sau scot vehiculul de la taxe locale | declar sau scot vehiculul de la taxe locale | ro.life.vehicle_local_tax_declaration | vehicles_mobility | high | event-ul este legat de mai multe intent-uri publice; confuzie între declarare, scoatere și transcriere vehicul | yes | Vrei să îl declari, să îl scoți de la taxe sau să transcrii proprietatea? |
| declar sau scot vehiculul de la taxe locale | declar sau scot vehiculul de la taxe locale | ro.life.vehicle_local_tax_declaration | vehicles_mobility | high | event-ul este legat de mai multe intent-uri publice; confuzie între declarare, scoatere și transcriere vehicul | yes | Vrei să îl declari, să îl scoți de la taxe sau să transcrii proprietatea? |
| am nevoie de certificat fiscal local | am nevoie de certificat fiscal local | ro.life.local_tax_certificate | tax_money_penalties | low | trigger phrase suficient de specifică în catalog | no |  |
| am nevoie de certificat fiscal local | am nevoie de certificat fiscal local | ro.life.local_tax_certificate | tax_money_penalties | low | trigger phrase suficient de specifică în catalog | no |  |
| declar un vehicul la taxe locale | declar un vehicul la taxe locale | ro.life.declare_vehicle_local_tax | tax_money_penalties | high | confuzie între declarare, scoatere și transcriere vehicul | yes | Vrei să îl declari, să îl scoți de la taxe sau să transcrii proprietatea? |
| declar un vehicul la taxe locale | declar un vehicul la taxe locale | ro.life.declare_vehicle_local_tax | tax_money_penalties | high | confuzie între declarare, scoatere și transcriere vehicul | yes | Vrei să îl declari, să îl scoți de la taxe sau să transcrii proprietatea? |
| scot un vehicul de la taxe locale | scot un vehicul de la taxe locale | ro.life.remove_vehicle_local_tax | tax_money_penalties | high | confuzie între declarare, scoatere și transcriere vehicul | yes | Vrei să îl declari, să îl scoți de la taxe sau să transcrii proprietatea? |
| scot un vehicul de la taxe locale | scot un vehicul de la taxe locale | ro.life.remove_vehicle_local_tax | tax_money_penalties | high | confuzie între declarare, scoatere și transcriere vehicul | yes | Vrei să îl declari, să îl scoți de la taxe sau să transcrii proprietatea? |
| mi-au fost furate actele și cardurile | mi-au fost furate actele si cardurile | ro.life.documents_stolen_bundle | legal_emergency_civic | high | intent de tip bundle/orchestrator; confuzie posibilă între pierdut și furat | yes | Este pierdut sau furat? |
| mi-au fost furate actele si cardurile | mi-au fost furate actele si cardurile | ro.life.documents_stolen_bundle | legal_emergency_civic | high | intent de tip bundle/orchestrator; confuzie posibilă între pierdut și furat | yes | Este pierdut sau furat? |
| îmi fac sau îmi reînnoiesc pașaportul | imi fac sau imi reinnoiesc pasaportul | ro.life.passport_first_or_renew | identity_documents | low | trigger phrase suficient de specifică în catalog | no |  |
| imi fac sau imi reinnoiesc pasaportul | imi fac sau imi reinnoiesc pasaportul | ro.life.passport_first_or_renew | identity_documents | low | trigger phrase suficient de specifică în catalog | no |  |
| fac pașaport unui minor | fac pasaport unui minor | ro.life.minor_passport | identity_documents | low | trigger phrase suficient de specifică în catalog | no |  |
| fac pasaport unui minor | fac pasaport unui minor | ro.life.minor_passport | identity_documents | low | trigger phrase suficient de specifică în catalog | no |  |
| am nevoie de cazier judiciar | am nevoie de cazier judiciar | ro.life.criminal_record_certificate | identity_documents | low | trigger phrase suficient de specifică în catalog | no |  |
| am nevoie de cazier judiciar | am nevoie de cazier judiciar | ro.life.criminal_record_certificate | identity_documents | low | trigger phrase suficient de specifică în catalog | no |  |
| schimb titularul contractului de electricitate | schimb titularul contractului de electricitate | ro.life.change_electricity_holder | home_address_utilities | low | trigger phrase suficient de specifică în catalog | no |  |
| schimb titularul contractului de electricitate | schimb titularul contractului de electricitate | ro.life.change_electricity_holder | home_address_utilities | low | trigger phrase suficient de specifică în catalog | no |  |
| schimb titularul contractului de gaz | schimb titularul contractului de gaz | ro.life.change_gas_holder | home_address_utilities | low | trigger phrase suficient de specifică în catalog | no |  |
| schimb titularul contractului de gaz | schimb titularul contractului de gaz | ro.life.change_gas_holder | home_address_utilities | low | trigger phrase suficient de specifică în catalog | no |  |
| schimb titularul contractului de apă | schimb titularul contractului de apa | ro.life.change_water_holder | home_address_utilities | low | trigger phrase suficient de specifică în catalog | no |  |
| schimb titularul contractului de apa | schimb titularul contractului de apa | ro.life.change_water_holder | home_address_utilities | low | trigger phrase suficient de specifică în catalog | no |  |
| mi s-a născut copilul | mi s-a nascut copilul | ro.life.child_birth | family_civil_status | high | intent de tip bundle/orchestrator | yes | Vrei traseul complet sau doar un pas specific? |
| mi s-a nascut copilul | mi s-a nascut copilul | ro.life.child_birth | family_civil_status | high | intent de tip bundle/orchestrator | yes | Vrei traseul complet sau doar un pas specific? |
| declar nașterea copilului | declar nasterea copilului | ro.life.birth_registration | family_civil_status | low | trigger phrase suficient de specifică în catalog | no |  |
| declar nasterea copilului | declar nasterea copilului | ro.life.birth_registration | family_civil_status | low | trigger phrase suficient de specifică în catalog | no |  |
| solicit alocația copilului | solicit alocatia copilului | ro.life.child_allowance | family_civil_status | low | trigger phrase suficient de specifică în catalog | no |  |
| solicit alocatia copilului | solicit alocatia copilului | ro.life.child_allowance | family_civil_status | low | trigger phrase suficient de specifică în catalog | no |  |
| înscriu copilul la creșă | inscriu copilul la cresa | ro.life.nursery_enrollment | education | low | trigger phrase suficient de specifică în catalog | no |  |
| inscriu copilul la cresa | inscriu copilul la cresa | ro.life.nursery_enrollment | education | low | trigger phrase suficient de specifică în catalog | no |  |
| înscriu copilul la grădiniță | inscriu copilul la gradinita | ro.life.preschool_enrollment | education | low | trigger phrase suficient de specifică în catalog | no |  |
| inscriu copilul la gradinita | inscriu copilul la gradinita | ro.life.preschool_enrollment | education | low | trigger phrase suficient de specifică în catalog | no |  |
| înscriu copilul în clasa pregătitoare | inscriu copilul in clasa pregatitoare | ro.life.preparatory_class_enrollment | education | low | trigger phrase suficient de specifică în catalog | no |  |
| inscriu copilul in clasa pregatitoare | inscriu copilul in clasa pregatitoare | ro.life.preparatory_class_enrollment | education | low | trigger phrase suficient de specifică în catalog | no |  |
| plătesc o amendă | platesc o amenda | ro.life.pay_fine | tax_money_penalties | low | trigger phrase suficient de specifică în catalog | no |  |
| platesc o amenda | platesc o amenda | ro.life.pay_fine | tax_money_penalties | low | trigger phrase suficient de specifică în catalog | no |  |
