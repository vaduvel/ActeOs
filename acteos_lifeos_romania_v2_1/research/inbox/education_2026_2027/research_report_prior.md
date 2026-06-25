# DEEP RESEARCH EXECUTAT — Waze pentru birocrație, R1 Educație

**Domeniu:** România + județul Timiș + municipiul Timișoara  
**An școlar:** 2026-2027  
**Data accesării surselor:** 2026-06-25  
**Timezone:** Europe/Bucharest  
**Stare livrabil:** research corpus verificabil; regulile sunt `in_review`, nu `published`.

## Rezumat executiv

Au fost confirmate baza normativă și calendarele pentru cele trei trasee: Ordinul nr. 3.707/2026 pentru antepreșcolar/preșcolar, Ordinul nr. 3.334/2026 pentru învățământ primar și Ordinul nr. 6.060/2025 cu anexele pentru admiterea la liceu. Codurile SIRUTA confirmate sunt **350 pentru județul Timiș** și **155243 pentru municipiul Timișoara**.

La data cercetării, traseul preșcolar se afla în colectarea cererilor din etapa a II-a, 22-26 iunie 2026. Etapele standard ale clasei pregătitoare se încheiaseră la 16 iunie, cu fereastră pentru situații rămase între 1 și 4 septembrie. Pentru liceu, completarea opțiunilor este programată în intervalul 13-20 iulie, repartizarea la 22 iulie și depunerea dosarelor în intervalul 23-28 iulie.

Stratul național este suficient de clar pentru reguli deterministe. Stratul local nu este încă gata de producție: sursele oficiale ale ISJ Timiș pentru circumscripții, locuri și broșura liceelor există, dar accesul automat este afectat de protecție anti-bot, iar criteriile fiecărei unități trebuie colectate individual. Din acest motiv, resolverul exact stradă→școală, compatibilitatea cu criteriile unei grădinițe și validarea codurilor de liceu rămân blocate până la importul verificat.

A fost identificată o ambiguitate operațională relevantă: metodologia primară permite validarea electronică „după caz”, în timp ce FAQ-ul ministerului indică prezentarea la școală după completarea online. Produsul nu alege arbitrar; cere confirmarea școlii și folosește prezentarea fizică drept ruta sigură implicită.

### Acoperire

| Traseu | Bază națională | Calendar | Acte | Local Timiș/Timișoara | Stare producție |
|---|---|---|---|---|---|
| A. Antepreșcolar/preșcolar | confirmată | complet | confirmate național | surse identificate; unități/criterii/locuri curente incomplete | BLOCK local |
| B. Clasa pregătitoare | confirmată | complet | confirmate național | PDF circumscripții/locuri identificat; rânduri neimportate | BLOCK resolver |
| C. Admitere liceu | confirmată | calendar principal + special | dosar standard confirmat | ghid/broșură identificate; coduri neimportate | BLOCK code validator |

### Convenție de dovezi

Pentru a evita duplicarea citatelor, fiecare claim indică unul sau mai multe `evidence_fragment_ids`. Textul exact al fragmentului este stocat o singură dată în `registries/source_registry.json`, împreună cu locatorul și URL-ul canonic. Nicio afirmație critică din regulile candidate nu există fără claim.


## A. Înscriere/reînscriere antepreșcolar și preșcolar

### 1. Jurisdicție

| Nivel | ID intern | Cod verificat | Stare |
|---|---|---|---|
| UE | eu | — | cadru superior |
| România | ro | RO | confirmat |
| Județ Timiș | ro.tm | SIRUTA 350 | confirmat |
| Municipiul Timișoara | ro.tm.timisoara | SIRUTA 155243 | confirmat |
| Instituție | target.unit_id | depinde de traseu | parțial / necesită registru local |

Regula națională și suplimentul local sunt separate. Un override local este aplicabil numai dacă autoritatea are competență și nu contrazice norma superioară.

### 2. Temporal / calendar

| event_id | Etapă | kind | start | end | claim-uri |
|---|---|---|---|---|---|
| ps.reenrollment | Reînscrieri | fixed_window | 2026-05-18T00:00:00+03:00 | 2026-05-22T23:59:59+03:00 | claim.ps.calendar.reenrollment |
| ps.reenrollment_results | Rezultat reînscrieri și locuri libere | fixed_instant | 2026-05-22T00:00:00+03:00 | 2026-05-22T23:59:59+03:00 | claim.ps.calendar.reenrollment |
| ps.stage1.collect | Etapa I — colectare cereri | fixed_window | 2026-05-25T00:00:00+03:00 | 2026-05-29T23:59:59+03:00 | claim.ps.calendar.stage1 |
| ps.stage1.phase1 | Etapa I — procesare opțiunea 1 | fixed_window | 2026-06-02T00:00:00+03:00 | 2026-06-08T23:59:59+03:00 | claim.ps.calendar.stage1 |
| ps.stage1.phase2 | Etapa I — procesare opțiunea 2 | fixed_window | 2026-06-09T00:00:00+03:00 | 2026-06-12T23:59:59+03:00 | claim.ps.calendar.stage1 |
| ps.stage1.phase3 | Etapa I — procesare opțiunea 3 | fixed_window | 2026-06-15T00:00:00+03:00 | 2026-06-17T23:59:59+03:00 | claim.ps.calendar.stage1 |
| ps.stage1.results | Rezultate etapa I | fixed_instant | 2026-06-18T00:00:00+03:00 | 2026-06-18T23:59:59+03:00 | claim.ps.calendar.stage1 |
| ps.stage2.collect | Etapa II — colectare cereri | fixed_window | 2026-06-22T00:00:00+03:00 | 2026-06-26T23:59:59+03:00 | claim.ps.calendar.stage2 |
| ps.stage2.phase1 | Etapa II — procesare opțiunea 1 | fixed_window | 2026-06-29T00:00:00+03:00 | 2026-07-01T23:59:59+03:00 | claim.ps.calendar.stage2 |
| ps.stage2.phase2 | Etapa II — procesare opțiunea 2 | fixed_window | 2026-07-02T00:00:00+03:00 | 2026-07-06T23:59:59+03:00 | claim.ps.calendar.stage2 |
| ps.stage2.phase3 | Etapa II — procesare opțiunea 3 | fixed_window | 2026-07-07T00:00:00+03:00 | 2026-07-08T23:59:59+03:00 | claim.ps.calendar.stage2 |
| ps.stage2.results | Rezultate etapa II | fixed_instant | 2026-07-09T00:00:00+03:00 | 2026-07-09T23:59:59+03:00 | claim.ps.calendar.stage2 |
| ps.adjustments | Etapa de ajustări | fixed_window | 2026-08-17T00:00:00+03:00 | 2026-08-27T23:59:59+03:00 | claim.ps.calendar.adjustments |
| ps.adjustments.results | Rezultate ajustări | fixed_instant | 2026-08-28T00:00:00+03:00 | 2026-08-28T23:59:59+03:00 | claim.ps.calendar.adjustment_result |
| ps.siiir | Introducere copii în SIIIR | fixed_instant | 2026-09-04T00:00:00+03:00 | 2026-09-04T23:59:59+03:00 | claim.ps.calendar.siiir |
| ps.during_year | Înscriere excepțională pe parcursul anului | none | — | — | claim.ps.calendar.adjustments |

### 3. Facts — întrebări către utilizator

| id | type | Întrebare | De ce | sensibil | obligatoriu |
|---|---|---|---|---|---|
| child.birth_date | date | Care este data nașterii copilului? | Stabilește nivelul, grupa și criteriile de vârstă aplicabile. | True | True |
| journey.evaluated_date | date | La ce dată verificăm traseul? | Selectează etapa activă și evită afișarea unui termen expirat. | False | True |
| enrollment.mode | enum | Este reînscriere în aceeași unitate sau înscriere nouă? | Reînscrierea are fereastră și logică diferite. | False | True |
| education.level | enum | Ce nivel urmărești? | Separă antepreșcolarul de preșcolar. | False | True |
| program.type | enum | Ce program dorești? | Programul prelungit schimbă documentele necesare. | False | True |
| submission.channel | enum | Cum vei transmite cererea? | E-mailul/poșta implică declarația de veridicitate; validarea rămâne la unitate. | False | True |
| family.parents_divorced | boolean | Părinții sunt divorțați? | Poate fi necesară dovada autorității părintești și a locuinței minorului. | True | True |
| criteria.invoked | boolean | Invoci criterii generale sau specifice? | Fiecare criteriu invocat trebuie dovedit cu documentul indicat. | True | True |
| application.stage | enum | În ce etapă te afli? | Determină fereastra și cererea aplicabilă. | False | True |
| child.start_date | date | Care este prima zi estimată de frecventare? | Stabilește momentul corect pentru avizul epidemiologic. | True | False |
| target.unit_id | string | Ce unitate din Timișoara alegi? | Criteriile, programul și locurile sunt stabilite la nivel de unitate. | False | True |
| local.unit_dataset_verified | boolean | Datele unității sunt verificate de curator? | Împiedică folosirea unei liste incomplete sau expirate. | False | True |
| local.places_snapshot_current | boolean | Snapshot-ul locurilor este curent pentru etapa activă? | Locurile se modifică după fiecare fază și etapă. | False | True |
| local.criteria_verified | boolean | Criteriile specifice și documentele lor sunt verificate? | Compatibilitatea nu poate fi calculată fără dovezi la nivelul unității. | False | True |

### 4. Gates — eligibilitate și blocaje

| id | priority | when | effect | code | mesaj | claim-uri |
|---|---|---|---|---|---|---|
| gate.ps.reenrollment.window | 10 | (enrollment.mode equals reenrollment) AND (journey.evaluated_date date_after 2026-05-22) | needs_confirmation | ps.reenrollment.window_closed | Fereastra standard de reînscriere s-a încheiat; unitatea trebuie să confirme ruta disponibilă. | claim.ps.calendar.reenrollment |
| gate.ps.stage1.closed | 20 | (application.stage equals stage1) AND (journey.evaluated_date date_after 2026-06-18) | needs_confirmation | ps.stage1.closed | Etapa I este închisă; recalculează către etapa a II-a sau ajustări. | claim.ps.calendar.stage1 |
| gate.ps.stage2.closed | 30 | (application.stage equals stage2) AND (journey.evaluated_date date_after 2026-07-09) | needs_confirmation | ps.stage2.closed | Etapa a II-a este închisă; următoarea rută standard este ajustarea. | claim.ps.calendar.stage2, claim.ps.calendar.adjustments |
| gate.ps.extended.employment | 40 | (program.type equals extended) OR (education.level equals antepreschool) | warn | ps.employment_documents_required | Pentru program prelungit sau antepreșcolar, pregătește documentele privind angajarea/concediul de creștere pentru fiecare părinte/reprezentant. | claim.ps.req.employment_extended |
| gate.ps.local.units | 1 | local.unit_dataset_verified is_false | needs_confirmation | ps.local.unit_data_missing | Lista și contactele unității nu sunt încă verificate complet; nu afișa recomandări ferme. | claim.ps.isj_publish_units_places |
| gate.ps.local.places | 2 | local.places_snapshot_current is_false | needs_confirmation | ps.local.places_stale | Locurile disponibile nu sunt confirmate pentru etapa curentă. | claim.ps.local.snapshot.2026_05_22, claim.ps.calendar.stage2 |
| gate.ps.local.criteria | 3 | local.criteria_verified is_false | needs_confirmation | ps.local.criteria_missing | Criteriile specifice ale unității nu sunt verificate; compatibilitatea nu poate fi calculată. | claim.ps.criteria_specific_locked |

### 5. Pași cap-coadă

| ordine | step_id | titlu | instrucțiune | deadline | dovada finalizării | recovery |
|---|---|---|---|---|---|---|
| 10 | step.ps.identify_stage | Identifică etapa activă | Folosește data curentă și istoricul cererii pentru a selecta reînscrierea, etapa I, etapa II sau ajustările. | institution_schedule | Etapa selectată corespunde calendarului și situației copilului. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 15 | step.ps.local.verify_unit | Verifică unitatea, locurile și criteriile | Confirmă pentru unitatea aleasă: programul, locurile pentru etapa curentă, criteriile specifice, documentele doveditoare și canalul de programare. | none | Fiecare câmp local are URL, dată de verificare și stare de încredere. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 20 | step.ps.choose_options | Alege trei opțiuni | Pentru înscriere nouă, ordonează trei unități după preferință și verifică programul și criteriile fiecăreia. | none | Cererea conține trei opțiuni confirmate; ordinea nu este confundată cu prioritatea depunerii. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 30 | step.ps.prepare_dossier | Pregătește dosarul personalizat | Adună documentele obligatorii și numai documentele condiționale aplicabile situației tale. | none | Toate cerințele aplicabile sunt prezente și marcate gata; cele neaplicabile sunt justificate. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 40 | step.ps.submit | Depune sau transmite cererea | Depune/transmite cererea și dosarul în fereastra etapei selectate, la unitatea corespunzătoare primei opțiuni sau conform procedurii etapei. | institution_schedule | Ai dovadă de depunere/transmitere și data acesteia. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 50 | step.ps.validate | Validează dosarul la unitate | Prezintă originalele și semnează validarea la unitatea solicitată, indiferent de canalul inițial de transmitere. | none | Ai cererea validată/semnată și o confirmare sau un număr de înregistrare. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 60 | step.ps.medical | Pregătește documentele medicale la momentul corect | Nu obține avizul epidemiologic prea devreme; programează documentele medicale pentru începutul frecventării. | none | Documentele medicale sunt valabile la prima zi de frecventare. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |

### 6. Cerințe / acte

| id | act/cerință | obligație | moment | forme | readiness checks | claim-uri |
|---|---|---|---|---|---|---|
| req.ps.three_options | Trei opțiuni în cerere | mandatory | now | original, electronic | exists, user_confirmed | claim.ps.three_options |
| req.ps.application | Cerere-tip | mandatory | now | original, electronic | exists, readable, has_signature | claim.ps.req.application |
| req.ps.birth_certificate | Copie certificat de naștere copil | mandatory | now | copy | exists, readable, correct_document_type, names_consistent | claim.ps.req.birth_certificate |
| req.ps.parent_ids | Copii acte de identitate părinți/reprezentant | mandatory | now | copy | exists, readable, correct_document_type, not_expired, names_consistent | claim.ps.req.parent_ids |
| req.ps.employment | Adeverințe de angajat / document concediu creștere | conditional | now | original, electronic, copy | exists, readable, has_signature, date_within_window | claim.ps.req.employment_extended |
| req.ps.criteria | Documente doveditoare pentru criterii | conditional | now | original, copy, electronic, certified_copy | exists, readable, correct_document_type, user_confirmed | claim.ps.req.criteria_documents |
| req.ps.remote_declaration | Declarație privind veridicitatea datelor | conditional | now | declaration, electronic, original | exists, readable, has_signature | claim.ps.req.remote_declaration |
| req.ps.parental_authority | Dovada autorității părintești și a locuinței minorului | conditional | now | copy, certified_copy, electronic | exists, readable, names_consistent, user_confirmed | claim.ps.req.parental_authority |
| req.ps.validation.originals | Originale pentru certificarea copiilor | mandatory | now | original | exists, not_expired, names_consistent | claim.ps.validation.in_person |
| req.ps.medical.clinical | Adeverință clinică de la medicul de familie | mandatory | later | original | exists, readable, has_signature, has_stamp | claim.ps.medical.family_doctor |
| req.ps.medical.epidemiological | Aviz epidemiologic / dovada vaccinării | mandatory | later | original | exists, readable, date_within_window, has_signature | claim.ps.medical.epidemiological |

### 7. Canale oficiale

| id | tip | etichetă | URL | status | domeniu |
|---|---|---|---|---|---|
| channel.ps.edu.faq | web | Ministerul Educației — ghid oficial 2026-2027 | https://www.edu.ro/inscriere_invatamant_prescolar_anteprescolar_faq | DEEP_LINK | edu.ro |
| channel.ps.legislation | web | Portal Legislativ — calendar și metodologie | https://legislatie.just.ro/Public/DetaliiDocument/309970 | SOURCE_ONLY | legislatie.just.ro |
| channel.ps.isjtm.page | web | ISJ Timiș — pagina locală de înscrieri | https://www.isj.tm.edu.ro/inscrieri/inscrierea-in-unitati-de-invatamant-preuniversitar-anul-2025-2026 | SOURCE_ONLY | isj.tm.edu.ro |
| channel.ps.local.isj | web | ISJ Timiș — înscrieri educație timpurie | https://www.isj.tm.edu.ro/inscrieri/inscrierea-in-unitati-de-invatamant-preuniversitar-anul-2025-2026 | SOURCE_ONLY | isj.tm.edu.ro |
| channel.isjtm.email | email | Registratura ISJ Timiș | mailto:registratura@isjtm.ro | DEEP_LINK | isj.tm.edu.ro |
| channel.isjtm.phone | phone | ISJ Timiș — 0256 305 799 | tel:+40256305799 | DEEP_LINK | isj.tm.edu.ro |

### 8. Source claims

| claim_id | afirmație atomică | source_id | locator | quote_ref | confidence |
|---|---|---|---|---|---|
| claim.jurisdiction.timis.siruta | Codul SIRUTA verificat pentru județul Timiș este 350. | src.ro.siruta.nomenclator | NRSIRUTA, p. 39 | ev.siruta.timis | verified |
| claim.jurisdiction.timisoara.siruta | Codul SIRUTA verificat pentru municipiul Timișoara este 155243. | src.ro.siruta.nomenclator | NRSIRUTA, p. 39 | ev.siruta.timisoara | verified |
| claim.ps.calendar.reenrollment | Reînscrierile sunt programate în intervalul 18-22 mai 2026. | src.preschool.order.3707.2026 | Anexă, etapa de reînscrieri | ev.ps.cal.reenrollment | verified |
| claim.ps.calendar.stage1 | Etapa I se desfășoară între 25 mai și 18 iunie 2026. | src.preschool.order.3707.2026 | Anexă, etapa I | ev.ps.cal.stage1 | verified |
| claim.ps.calendar.stage2 | Etapa a II-a se desfășoară între 22 iunie și 9 iulie 2026. | src.preschool.order.3707.2026 | Anexă, etapa a II-a | ev.ps.cal.stage2 | verified |
| claim.ps.calendar.adjustments | Etapa de ajustări se desfășoară între 17 și 27 august 2026. | src.preschool.order.3707.2026 | Anexă, etapa de ajustări | ev.ps.cal.adjustments | verified |
| claim.ps.calendar.adjustment_result | Rezultatele ajustărilor și locurile rămase se afișează la 28 august 2026. | src.preschool.order.3707.2026 | Anexă, rezultat ajustări | ev.ps.cal.adjustment_result | verified |
| claim.ps.calendar.siiir | Termenul de introducere a copiilor înscriși în SIIIR este 4 septembrie 2026. | src.preschool.order.3707.2026 | Anexă, introducerea în SIIIR | ev.ps.cal.siiir | verified |
| claim.ps.three_options | Cererea de înscriere conține trei opțiuni de unități, în ordinea preferinței. | src.preschool.faq.2026 | Secțiunea documentele dosarului | ev.ps.faq.three_options | verified |
| claim.ps.not_first_come | Ordinea depunerii sau numărul de înregistrare nu constituie criteriu de admitere. | src.preschool.faq.2026 | Secțiunea criterii de departajare | ev.ps.faq.not_first | verified |
| claim.ps.criteria_specific_locked | Criteriile specifice devin publice la data din calendar și nu mai pot fi modificate ori completate după publicare. | src.preschool.methodology.4018.2024 | Art. 12 alin. (2) | ev.ps.method.criteria_locked | verified |
| claim.ps.isj_publish_units_places | Inspectoratul trebuie să publice unitățile, adresele, numărul de grupe/locuri și site-urile unităților. | src.preschool.methodology.4018.2024 | Art. 13 alin. (1)-(2) | ev.ps.method.publish | verified |
| claim.ps.isj_telverde | Inspectoratul trebuie să instituie o linie Telverde pe perioada înscrierilor. | src.preschool.methodology.4018.2024 | Art. 13 alin. (1) lit. a) | ev.ps.method.telverde | verified |
| claim.ps.req.application | Cererea-tip este document obligatoriu al dosarului. | src.preschool.faq.2026 | Secțiunea documentele dosarului | ev.ps.faq.three_options | verified |
| claim.ps.req.birth_certificate | Dosarul include copia certificatului de naștere al copilului. | src.preschool.faq.2026 | Secțiunea documentele dosarului, pct. certificat | ev.ps.faq.three_options | verified |
| claim.ps.req.parent_ids | Dosarul include copii ale actelor de identitate ale părinților/reprezentantului legal. | src.preschool.faq.2026 | Secțiunea documentele dosarului, pct. acte identitate | ev.ps.faq.validation | verified |
| claim.ps.req.employment_extended | Pentru program prelungit și pentru antepreșcolar se solicită adeverințe de angajat pentru fiecare părinte/reprezentant sau documentul privind concediul de creștere. | src.preschool.faq.2026 | Secțiunea documentele dosarului | ev.ps.faq.employment | verified |
| claim.ps.req.criteria_documents | Documentele care dovedesc criteriile generale ori specifice se adaugă numai când criteriul este invocat. | src.preschool.faq.2026 | Secțiunea documentele dosarului | ev.ps.faq.three_options | verified |
| claim.ps.req.remote_declaration | Transmiterea cererii prin e-mail sau poștă necesită declarație pe propria răspundere privind veridicitatea datelor. | src.preschool.faq.2026 | Secțiunea documentele dosarului | ev.ps.faq.validation | verified |
| claim.ps.req.parental_authority | Părinții divorțați trebuie să dovedească exercitarea autorității părintești și locuința minorului. | src.preschool.faq.2026 | Secțiunea documentele dosarului | ev.ps.faq.validation | verified |
| claim.ps.validation.in_person | Validarea dosarului se face la unitatea solicitată, în prezența părintelui/reprezentantului, cu originale pentru certificarea copiilor. | src.preschool.faq.2026 | Secțiunea validarea dosarului | ev.ps.faq.validation | verified |
| claim.ps.medical.family_doctor | Adeverința clinică se adaugă la începutul anului și este necesară în prima zi de prezentare. | src.preschool.faq.2026 | Secțiunea documente medicale | ev.ps.faq.five_days | verified |
| claim.ps.medical.epidemiological | Avizul epidemiologic/dovada de vaccinare se emite cu maximum cinci zile înainte de începerea frecventării. | src.preschool.faq.2026 | Secțiunea documente medicale | ev.ps.faq.five_days | verified |
| claim.ps.local.snapshot.2026_05_22 | ISJ Timiș a publicat un snapshot al locurilor la 22 mai 2026; acesta este istoric și nu poate fi folosit ca disponibilitate curentă după etapele ulterioare. | src.isjtm.preschool.places.2026_05_22 | Antet/subsol raport | ev.isjtm.ps.snapshot | expired |
| claim.isjtm.contact.registry | Registratura ISJ Timiș primește documente electronic la adresa publicată și are program fizic luni-joi, 13:00-15:00. | src.isjtm.contact | Programul registraturii | ev.isjtm.contact.email, ev.isjtm.contact.hours | verified |
| claim.isjtm.contact.phone | Numărul publicat pentru programări/audiențe ISJ Timiș este 0256 305 799. | src.isjtm.contact | Program audiențe | ev.isjtm.contact.phone | verified |

### 9. Freshness și gap-uri locale

Bază națională: `critical`, verificată la `2026-06-25T19:00:00+03:00`, hard expiry `2026-07-10T00:00:00+03:00`, acțiune `block`.

Supliment local: `critical`, verificat la `2026-06-25T19:00:00+03:00`, hard expiry `2026-06-27T00:00:00+03:00`, acțiune `block`.

| gap_id | prioritate | ce lipsește | de ce | on_gap |
|---|---|---|---|---|
| gap.ps.timisoara.unit_inventory | P0 | Lista normalizată completă a unităților publice/particulare relevante, cu SIIIR, adresă, program și contacte 2026-2027. | Directorul oficial este protejat anti-bot și nu a furnizat rândurile în mod stabil. | block_unit_specific_recommendation |
| gap.ps.timisoara.current_places | P0 | Locuri curente după rezultatul etapei active, pe unitate/nivel/program/limbă. | Snapshot-ul din 22.05.2026 este expirat pentru disponibilitatea curentă. | needs_confirmation |
| gap.ps.timisoara.criteria | P0 | Criteriile specifice și documentele doveditoare pentru fiecare unitate. | Necesită parcurgerea site-urilor fiecărei unități și snapshot al documentelor publicate. | block_compatibility_scoring |
| gap.ps.timisoara.telverde | P1 | Numărul și programul Telverde 2026 pentru educație timpurie. | Nu a fost confirmat oficial în materialele accesibile. | hide_channel |
| gap.all.source_snapshots | P0 | Snapshot-uri locale cu SHA-256 pentru documentele care vor alimenta producția. | URL-ul singur nu garantează reproducerea conținutului dacă fișierul este înlocuit. | block_promotion_to_production |



## B. Înscriere în clasa pregătitoare / învățământ primar

### 1. Jurisdicție

| Nivel | ID intern | Cod verificat | Stare |
|---|---|---|---|
| UE | eu | — | cadru superior |
| România | ro | RO | confirmat |
| Județ Timiș | ro.tm | SIRUTA 350 | confirmat |
| Municipiul Timișoara | ro.tm.timisoara | SIRUTA 155243 | confirmat |
| Instituție | target.unit_id | depinde de traseu | parțial / necesită registru local |

Regula națională și suplimentul local sunt separate. Un override local este aplicabil numai dacă autoritatea are competență și nu contrazice norma superioară.

### 2. Temporal / calendar

| event_id | Etapă | kind | start | end | claim-uri |
|---|---|---|---|---|---|
| pr.circumscriptions | Afișare circumscripții și plan | fixed_instant | 2026-03-12T00:00:00+02:00 | 2026-03-12T23:59:59+02:00 | claim.pr.calendar.circumscriptions |
| pr.recommendations | Recomandări/evaluări și amânări | fixed_window | 2026-03-16T00:00:00+02:00 | 2026-03-30T23:59:59+03:00 | claim.pr.calendar.recommendation |
| pr.application | Cereri, documente și validare etapa I | fixed_window | 2026-03-31T00:00:00+03:00 | 2026-05-06T23:59:59+03:00 | claim.pr.calendar.application |
| pr.stage1.circ | Procesare școli de circumscripție | fixed_window | 2026-05-06T00:00:00+03:00 | 2026-05-11T23:59:59+03:00 | claim.pr.calendar.application |
| pr.stage1.other | Procesare alte școli | fixed_window | 2026-05-13T00:00:00+03:00 | 2026-05-20T23:59:59+03:00 | claim.pr.calendar.application |
| pr.stage1.results | Rezultate etapa I și locuri libere | fixed_instant | 2026-05-21T00:00:00+03:00 | 2026-05-21T23:59:59+03:00 | claim.pr.calendar.application |
| pr.stage2.procedure | Publicare procedură etapa II | fixed_instant | 2026-05-22T00:00:00+03:00 | 2026-05-22T23:59:59+03:00 | claim.pr.calendar.stage2_application |
| pr.stage2.application | Cereri etapa II | fixed_window | 2026-05-25T00:00:00+03:00 | 2026-05-29T23:59:59+03:00 | claim.pr.calendar.stage2_application |
| pr.stage2.validation | Validare cereri etapa II | fixed_window | 2026-06-02T00:00:00+03:00 | 2026-06-08T23:59:59+03:00 | claim.pr.calendar.stage2_application |
| pr.stage2.processing | Procesare cereri etapa II | fixed_window | 2026-06-09T00:00:00+03:00 | 2026-06-15T23:59:59+03:00 | claim.pr.calendar.stage2_application |
| pr.final | Liste finale | fixed_instant | 2026-06-16T00:00:00+03:00 | 2026-06-16T23:59:59+03:00 | claim.pr.calendar.final |
| pr.unresolved | Soluționarea cazurilor neînscrise | fixed_window | 2026-09-01T00:00:00+03:00 | 2026-09-04T23:59:59+03:00 | claim.pr.calendar.unresolved |

### 3. Facts — întrebări către utilizator

| id | type | Întrebare | De ce | sensibil | obligatoriu |
|---|---|---|---|---|---|
| child.birth_date | date | Care este data nașterii copilului? | Stabilește fereastra de vârstă și necesitatea recomandării/evaluării. | True | True |
| journey.evaluated_date | date | La ce dată verificăm traseul? | Etapele standard sunt temporale. | False | True |
| child.attended_kindergarten | boolean | Copilul a frecventat grădinița? | Determină dacă recomandarea vine de la grădiniță sau dacă este necesară evaluarea CJRAE. | True | True |
| child.returned_from_abroad | boolean | Copilul s-a întors din străinătate? | Poate activa ruta de evaluare CJRAE. | True | True |
| child.ces | boolean | Copilul are CES/certificat de orientare? | Există reguli speciale de vârstă și documente. | True | True |
| school.choice | enum | Alegi școala de circumscripție sau altă școală? | Garanția locului și criteriile diferă. | False | True |
| school.reserve_circumscription | boolean | Păstrezi locul la școala de circumscripție? | Protejează ruta de rezervă dacă nu ești admis la altă școală. | False | False |
| family.parents_divorced | boolean | Părinții sunt divorțați? | Poate fi necesară dovada autorității părintești. | True | True |
| criteria.invoked | boolean | Invoci criterii pentru o școală din afara circumscripției? | Documentele doveditoare devin obligatorii. | True | True |
| submission.channel | enum | Completezi cererea online sau la școală? | Canalul de completare nu este identic cu validarea. | False | True |
| child.address | string | Care este adresa exactă a copilului? | Circumscripția poate depinde de stradă, interval și paritatea numărului. | True | True |
| local.circumscriptions_verified | boolean | Maparea locală a circumscripțiilor este verificată? | Împiedică atribuirea unei școli greșite. | False | True |
| local.school_criteria_verified | boolean | Criteriile școlii sunt verificate? | Sunt necesare pentru o școală din afara circumscripției. | False | True |
| local.validation_channel_confirmed | boolean | Canalul de validare al școlii este confirmat? | Separă posibilitatea juridică de canalul operațional efectiv. | False | True |

### 4. Gates — eligibilitate și blocaje

| id | priority | when | effect | code | mesaj | claim-uri |
|---|---|---|---|---|---|---|
| gate.pr.too_young | 10 | (child.birth_date date_after 2020-12-31) AND (child.ces is_false) | block | pr.age.standard_not_met | Copilul nu intră în fereastra standard de vârstă pentru 2026-2027. | claim.pr.age.mandatory_august, claim.pr.age.september_december |
| gate.pr.sep_dec.recommendation | 20 | (child.birth_date between 2020-09-01…2020-12-31) AND (child.attended_kindergarten is_true) AND (child.returned_from_abroad is_false) | warn | pr.recommendation.kindergarten_required | Este necesară recomandarea emisă de grădiniță. | claim.pr.recommendation.kindergarten, claim.pr.calendar.recommendation |
| gate.pr.sep_dec.cjrae | 21 | (child.birth_date between 2020-09-01…2020-12-31) AND ((child.attended_kindergarten is_false) OR (child.returned_from_abroad is_true)) | warn | pr.cjrae.evaluation_required | Este necesară ruta CJRAE pentru evaluare/recomandare. | claim.pr.recommendation.cjrae, claim.pr.calendar.recommendation |
| gate.pr.other_without_reserve | 30 | (school.choice equals other) AND (school.reserve_circumscription is_false) | warn | pr.reserve.not_selected | Ai ales altă școală fără să păstrezi explicit locul de circumscripție. | claim.pr.reserve.circumscription |
| gate.pr.standard_closed | 40 | journey.evaluated_date date_after 2026-06-16 | needs_confirmation | pr.standard_stages_closed | Etapele standard s-au încheiat; cazul trebuie rutat către soluționarea ISJ sau o procedură locală actuală. | claim.pr.calendar.final, claim.pr.calendar.unresolved |
| gate.pr.local.circ | 1 | local.circumscriptions_verified is_false | needs_confirmation | pr.local.circumscriptions_missing | Nu putem atribui exact școala de circumscripție fără importul verificat al tuturor rândurilor stradă/număr. | claim.pr.local.circumscriptions_source_exists |
| gate.pr.local.criteria | 2 | local.school_criteria_verified is_false | needs_confirmation | pr.local.criteria_missing | Criteriile specifice ale școlii nu sunt verificate; nu calcula o probabilitate sau o ierarhie. | claim.pr.req.criteria_documents |
| gate.pr.local.validation | 3 | local.validation_channel_confirmed is_false | warn | pr.local.validation_unconfirmed | Canalul electronic de validare nu este confirmat; ruta sigură rămâne prezentarea la școală. | claim.pr.validation.electronic_possible, claim.pr.validation.faq_in_person |

### 5. Pași cap-coadă

| ordine | step_id | titlu | instrucțiune | deadline | dovada finalizării | recovery |
|---|---|---|---|---|---|---|
| 10 | step.pr.check_age | Verifică ruta de vârstă | Încadrează copilul în fereastra până la 31 august, fereastra 1 septembrie-31 decembrie sau ruta CES. | none | Ruta de vârstă este determinată și motivată prin claim-uri oficiale. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 20 | step.pr.obtain_recommendation | Obține recomandarea sau evaluarea | Pentru fereastra septembrie-decembrie, obține recomandarea de la grădiniță ori prin CJRAE, după situație. | fixed_window | Recomandarea/evaluarea aplicabilă este emisă și atașabilă. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 25 | step.pr.local.resolve_address | Rezolvă adresa în circumscripția oficială | Normalizează strada, numărul și paritatea și returnează școala numai dacă rândul sursă este importat și verificat. | none | Rezultatul păstrează rândul sursă, pagina și hash-ul snapshot-ului. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 30 | step.pr.resolve_school | Determină școala și ruta de rezervă | Identifică școala de circumscripție pe baza adresei sau alege altă școală și decide dacă păstrezi locul de circumscripție. | none | Școala de circumscripție și opțiunea de rezervă sunt confirmate. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 35 | step.pr.local.verify_school | Verifică școala, locurile, criteriile și canalul | Pentru școala aleasă, confirmă locurile publicate, criteriile specifice, documentele și modalitatea de validare. | none | Fiecare informație locală are sursă, dată și stare de încredere. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 40 | step.pr.prepare_dossier | Pregătește dosarul | Adună cererea, actele de identitate, certificatul copilului și documentele condiționale. | none | Dosarul este complet pentru situația personală și alegerea școlii. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 50 | step.pr.submit_validate | Completează, depune și validează cererea | Completează online sau la școală, depune/transmite documentele și finalizează validarea prin canalul confirmat de unitate. | fixed_window | Ai fișa validată și dovada/confirmarea unității. | Dacă școala nu confirmă validarea electronică, folosește ruta fizică indicată de FAQ. |
| 60 | step.pr.stage2 | Continuă în etapa a II-a dacă este necesar | Dacă nu ai fost cuprins în etapa I, completează trei opțiuni și depune cererea la unitatea aflată pe prima poziție. | fixed_window | Cererea etapei a II-a este validată și urmărită până la rezultatul final. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 70 | step.pr.unresolved | Soluționează cazul rămas neînscris | Pentru situațiile nerezolvate după etapele standard, depune solicitarea la ISJ în fereastra oficială sau urmează instrucțiunea actuală a comisiei județene. | fixed_window | ISJ a înregistrat și soluționat cererea sau a comunicat pașii următori. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |

### 6. Cerințe / acte

| id | act/cerință | obligație | moment | forme | readiness checks | claim-uri |
|---|---|---|---|---|---|---|
| req.pr.recommendation | Recomandare pentru clasa pregătitoare | conditional | now | original, copy, electronic | exists, readable, correct_document_type, has_signature | claim.pr.recommendation.kindergarten, claim.pr.recommendation.cjrae |
| req.pr.reserve | Bifarea rezervării locului de circumscripție | optional | now | declaration, electronic, original | user_confirmed | claim.pr.reserve.circumscription |
| req.pr.parent_id | Act identitate părinte/reprezentant | mandatory | now | original, copy | exists, readable, correct_document_type, not_expired, names_consistent | claim.pr.req.parent_id |
| req.pr.birth_certificate | Certificat de naștere copil | mandatory | now | original, copy | exists, readable, correct_document_type, names_consistent | claim.pr.req.birth_certificate |
| req.pr.parental_authority | Dovada autorității părintești și a locuinței | conditional | now | original, copy, certified_copy, electronic | exists, readable, names_consistent | claim.pr.req.parental_authority |
| req.pr.criteria | Documente pentru criteriile de departajare | conditional | now | copy, electronic, certified_copy | exists, readable, correct_document_type, user_confirmed | claim.pr.req.criteria_documents |

### 7. Canale oficiale

| id | tip | etichetă | URL | status | domeniu |
|---|---|---|---|---|---|
| channel.pr.edu.faq | web | Ministerul Educației — FAQ clasa pregătitoare | https://www.edu.ro/intrebari_raspunsuri_inscriere_invatamant_primar | DEEP_LINK | edu.ro |
| channel.pr.portal | deep_link | Portalul oficial de completare cereri | https://inscriere.edu.ro/ | DEEP_LINK | inscriere.edu.ro |
| channel.pr.isjtm | web | ISJ Timiș — înscriere în învățământul primar | https://www.isj.tm.edu.ro/inscrieri/inscrierea-in-invatamantul-primar/anul-2026-2027 | SOURCE_ONLY | isj.tm.edu.ro |
| channel.isjtm.email | email | Registratura ISJ Timiș | mailto:registratura@isjtm.ro | DEEP_LINK | isj.tm.edu.ro |
| channel.isjtm.phone | phone | ISJ Timiș — 0256 305 799 | tel:+40256305799 | DEEP_LINK | isj.tm.edu.ro |
| channel.pr.local.isj | web | ISJ Timiș — primar 2026-2027 | https://www.isj.tm.edu.ro/inscrieri/inscrierea-in-invatamantul-primar/anul-2026-2027 | SOURCE_ONLY | isj.tm.edu.ro |
| channel.isjtm.email | email | Registratura ISJ Timiș | mailto:registratura@isjtm.ro | DEEP_LINK | isj.tm.edu.ro |
| channel.isjtm.phone | phone | ISJ Timiș — 0256 305 799 | tel:+40256305799 | DEEP_LINK | isj.tm.edu.ro |

### 8. Source claims

| claim_id | afirmație atomică | source_id | locator | quote_ref | confidence |
|---|---|---|---|---|---|
| claim.jurisdiction.timis.siruta | Codul SIRUTA verificat pentru județul Timiș este 350. | src.ro.siruta.nomenclator | NRSIRUTA, p. 39 | ev.siruta.timis | verified |
| claim.jurisdiction.timisoara.siruta | Codul SIRUTA verificat pentru municipiul Timișoara este 155243. | src.ro.siruta.nomenclator | NRSIRUTA, p. 39 | ev.siruta.timisoara | verified |
| claim.pr.calendar.circumscriptions | Circumscripțiile și planul propus trebuiau afișate la 12 martie 2026. | src.primary.order.3334.2026 | Anexă, pregătirea înscrierii | ev.pr.cal.circ | verified |
| claim.pr.calendar.recommendation | Recomandările/evaluările și cererile de amânare se derulează în intervalul 16-30 martie 2026. | src.primary.order.3334.2026 | Anexă, recomandare/evaluare | ev.pr.cal.recommendation | verified |
| claim.pr.calendar.application | Completarea, depunerea/transmiterea și validarea cererilor din etapa I se fac între 31 martie și 6 mai 2026. | src.primary.order.3334.2026 | Anexă, cereri și validare | ev.pr.cal.application | verified |
| claim.pr.calendar.stage2_application | Cererile pentru etapa a II-a se depun/transmit în perioada 25-29 mai 2026. | src.primary.order.3334.2026 | Anexă, etapa a II-a | ev.pr.cal.stage2 | verified |
| claim.pr.calendar.final | Listele finale ale copiilor înscriși în clasa pregătitoare se afișează la 16 iunie 2026. | src.primary.order.3334.2026 | Anexă, etapa a II-a | ev.pr.cal.final | verified |
| claim.pr.calendar.unresolved | Situațiile copiilor încă neînscriși se centralizează și soluționează în intervalul 1-4 septembrie 2026. | src.primary.order.3334.2026 | Anexă, situații rămase | ev.pr.cal.unresolved | verified |
| claim.pr.age.mandatory_august | Copiii care au frecventat preșcolarul și împlinesc șase ani până la 31 august inclusiv trebuie înscriși în clasa pregătitoare. | src.primary.methodology.4019.2024 | Art. 5 alin. (1) | ev.pr.method.age_aug | verified |
| claim.pr.age.september_december | Copiii care împlinesc șase ani între 1 septembrie și 31 decembrie pot fi înscriși dacă nivelul de dezvoltare este corespunzător. | src.primary.methodology.4019.2024 | Art. 6 alin. (1) | ev.pr.method.age_dec | verified |
| claim.pr.recommendation.kindergarten | Pentru copilul din fereastra septembrie-decembrie care a frecventat grădinița este necesară recomandarea unității preșcolare. | src.primary.methodology.4019.2024 | Art. 6 alin. (2) | ev.pr.method.age_dec | verified |
| claim.pr.recommendation.cjrae | Evaluarea/recomandarea CJRAE se aplică, în această rută, copiilor care nu au frecventat grădinița sau s-au întors din străinătate. | src.primary.methodology.4019.2024 | Art. 7 alin. (1) | ev.pr.method.age_dec | verified |
| claim.pr.defer.one_year | În cazuri justificate, înscrierea copilului care împlinește șase ani până la 31 august poate fi amânată cu maximum un an. | src.primary.faq.2026 | Nota privind amânarea | ev.pr.faq.defer | verified |
| claim.pr.circumscription.guaranteed | Copilul pentru care se solicită școala de circumscripție este înmatriculat acolo după validarea cererii. | src.primary.methodology.4019.2024 | Art. 9 alin. (1) | ev.pr.method.circ | verified |
| claim.pr.other_school.free_places | Înscrierea la altă școală decât cea de circumscripție depinde de locurile libere și criteriile de departajare. | src.primary.methodology.4019.2024 | Art. 9-10 | ev.pr.method.circ | verified |
| claim.pr.reserve.circumscription | Părintele poate bifa păstrarea locului la școala de circumscripție dacă solicită o altă școală. | src.primary.faq.2026 | Secțiunea alegerea unității | ev.pr.faq.reserve | verified |
| claim.pr.req.parent_id | Dosarul include copie și original după actul de identitate al părintelui/reprezentantului. | src.primary.faq.2026 | Secțiunea actele necesare | ev.pr.faq.original | verified |
| claim.pr.req.birth_certificate | Dosarul include copie și original după certificatul de naștere al copilului. | src.primary.faq.2026 | Secțiunea actele necesare | ev.pr.faq.original | verified |
| claim.pr.req.parental_authority | Părinții divorțați depun dovada modului de exercitare a autorității părintești și a locuinței minorului. | src.primary.faq.2026 | Secțiunea actele necesare | ev.pr.faq.original | verified |
| claim.pr.req.criteria_documents | Pentru o școală din afara circumscripției se depun documentele care dovedesc criteriile generale și specifice invocate. | src.primary.methodology.4019.2024 | Art. 10 și art. 14 alin. (6) | ev.pr.method.circ | verified |
| claim.pr.validation.electronic_possible | Metodologia permite, după caz, validarea prin semnătură la sediu sau prin mijloace electronice. | src.primary.methodology.4019.2024 | Art. 15 alin. (4) | ev.pr.method.electronic | verified_with_local_gap |
| claim.pr.validation.faq_in_person | Ghidul operațional indică prezentarea la unitate pentru validarea cererii completate online. | src.primary.faq.2026 | Secțiunea unde au loc înscrierile | ev.pr.faq.in_person | verified_with_local_gap |
| claim.pr.local.circumscriptions_source_exists | ISJ Timiș a publicat documentul oficial de circumscripții Timișoara 2026-2027. | src.isjtm.primary.circumscriptions.timisoara.2026 | Antetul documentului indexat | ev.isjtm.pr.circ.docno | verified_with_local_gap |
| claim.pr.local.places_source_exists | ISJ Timiș a publicat documentul oficial privind locurile pentru clasa pregătitoare în Timișoara. | src.isjtm.primary.places.timisoara.2026 | Titlul raportului indexat | ev.isjtm.pr.places | verified_with_local_gap |
| claim.isjtm.contact.registry | Registratura ISJ Timiș primește documente electronic la adresa publicată și are program fizic luni-joi, 13:00-15:00. | src.isjtm.contact | Programul registraturii | ev.isjtm.contact.email, ev.isjtm.contact.hours | verified |
| claim.isjtm.contact.phone | Numărul publicat pentru programări/audiențe ISJ Timiș este 0256 305 799. | src.isjtm.contact | Program audiențe | ev.isjtm.contact.phone | verified |

### 9. Freshness și gap-uri locale

Bază națională: `critical`, verificată la `2026-06-25T19:00:00+03:00`, hard expiry `2026-09-05T00:00:00+03:00`, acțiune `block`.

Supliment local: `critical`, verificat la `2026-06-25T19:00:00+03:00`, hard expiry `2026-09-05T00:00:00+03:00`, acțiune `block`.

| gap_id | prioritate | ce lipsește | de ce | on_gap |
|---|---|---|---|---|
| gap.pr.timisoara.circumscriptions_rows | P0 | Maparea exactă stradă + interval/paritate numere → școală, pentru toate rândurile. | PDF-ul oficial există, dar accesul automat stabil este blocat; nu se acceptă extragere incompletă din snippeturi. | block_exact_circumscription_resolution |
| gap.pr.timisoara.places_rows | P0 | Planul complet de școlarizare și locurile/clasele per unitate. | PDF-ul oficial nu a putut fi normalizat rând cu rând. | needs_confirmation |
| gap.pr.timisoara.criteria | P0 | Criteriile specifice și documentele doveditoare pentru fiecare școală. | Sunt publicate la nivelul unității; nu există încă un registru normalizat verificat. | block_out_of_circumscription_ranking |
| gap.pr.timisoara.validation_channel | P1 | Confirmarea pe școală a validării fizice versus electronice active. | Metodologia și FAQ-ul lasă o diferență între posibilitatea juridică și practica operațională. | default_to_in_person_and_warn |
| gap.all.source_snapshots | P0 | Snapshot-uri locale cu SHA-256 pentru documentele care vor alimenta producția. | URL-ul singur nu garantează reproducerea conținutului dacă fișierul este înlocuit. | block_promotion_to_production |



## C. Admitere liceu 2026-2027

### 1. Jurisdicție

| Nivel | ID intern | Cod verificat | Stare |
|---|---|---|---|
| UE | eu | — | cadru superior |
| România | ro | RO | confirmat |
| Județ Timiș | ro.tm | SIRUTA 350 | confirmat |
| Municipiul Timișoara | ro.tm.timisoara | SIRUTA 155243 | confirmat |
| Instituție | target.unit_id | depinde de traseu | parțial / necesită registru local |

Regula națională și suplimentul local sunt separate. Un override local este aplicabil numai dacă autoritatea are competență și nu contrazice norma superioară.

### 2. Temporal / calendar

| event_id | Etapă | kind | start | end | claim-uri |
|---|---|---|---|---|---|
| hs.aptitude.registration | Înscriere probe aptitudini/limbă | fixed_window | 2026-05-13T00:00:00+03:00 | 2026-05-15T23:59:59+03:00 | claim.hs.order.scope |
| hs.aptitude.tests | Probe aptitudini/limbă | fixed_window | 2026-05-18T00:00:00+03:00 | 2026-05-22T23:59:59+03:00 | claim.hs.order.scope |
| hs.roma.recommendation | Eliberare recomandări apartenență etnică | fixed_instant | 2026-06-12T00:00:00+03:00 | 2026-06-12T23:59:59+03:00 | claim.hs.order.scope |
| hs.ces.documents | Depunere documente pentru locuri distincte CES | fixed_window | 2026-06-08T00:00:00+03:00 | 2026-06-15T23:59:59+03:00 | claim.hs.order.scope |
| hs.options | Completare și verificare opțiuni | fixed_window | 2026-07-13T00:00:00+03:00 | 2026-07-20T23:59:59+03:00 | claim.hs.calendar.options, claim.hs.options.risk |
| hs.allocation | Repartizare computerizată | fixed_instant | 2026-07-22T00:00:00+03:00 | 2026-07-22T23:59:59+03:00 | claim.hs.calendar.allocation |
| hs.dossier | Depunere dosar la liceul repartizat | fixed_window | 2026-07-23T00:00:00+03:00 | 2026-07-28T23:59:59+03:00 | claim.hs.calendar.dossier |
| hs.special_cases | Soluționare situații speciale | fixed_window | 2026-07-29T00:00:00+03:00 | 2026-07-31T23:59:59+03:00 | claim.hs.calendar.dossier |
| hs.stage2.announce | Afișare centru și locuri etapa II | fixed_instant | 2026-07-31T00:00:00+03:00 | 2026-07-31T23:59:59+03:00 | claim.hs.calendar.dossier |
| hs.stage2.applications | Cereri etapa II | fixed_window | 2026-08-10T00:00:00+03:00 | 2026-08-12T23:59:59+03:00 | claim.hs.calendar.dossier |
| hs.stage2.allocation | Repartizare etapa II | fixed_window | 2026-08-17T00:00:00+03:00 | 2026-08-18T23:59:59+03:00 | claim.hs.calendar.dossier |

### 3. Facts — întrebări către utilizator

| id | type | Întrebare | De ce | sensibil | obligatoriu |
|---|---|---|---|---|---|
| candidate.took_national_assessment | boolean | Candidatul a susținut Evaluarea Națională? | Determină accesul la repartizarea computerizată principală. | True | True |
| candidate.admission_average | decimal | Care este media de admitere? | Permite verificarea listei, fără a promite admiterea. | True | True |
| candidate.series | enum | Candidatul este din seria curentă sau anterioară? | Vârsta și seria pot schimba ruta spre zi/seral/frecvență redusă. | False | True |
| candidate.age_at_school_start | integer | Ce vârstă are candidatul la începerea cursurilor? | Separă ruta standard de seral, în cazurile prevăzute. | True | True |
| candidate.vocational_route | boolean | Alege un profil cu probe de aptitudini? | Activează calendarul și formula specială. | False | True |
| candidate.ces_route | boolean | Candidează pe loc distinct CES? | Există documente și calendar separat. | True | True |
| candidate.roma_route | boolean | Candidează pe loc special pentru rromi? | Există recomandare și calendar separat. | True | True |
| options.count | integer | Câte opțiuni ai completat? | Prea puține opțiuni cresc riscul de nerepartizare. | False | True |
| allocation.completed | boolean | Candidatul a fost repartizat? | Activează depunerea dosarului la liceu. | True | True |
| local.brochure_verified | boolean | Broșura Timiș a fost importată și verificată integral? | Codurile și locurile trebuie să provină din oferta oficială curentă. | False | True |
| option.code | string | Ce cod de opțiune verifici? | Fiecare cod trebuie rezolvat exact la liceu/profil/specializare/limbă. | False | False |

### 4. Gates — eligibilitate și blocaje

| id | priority | when | effect | code | mesaj | claim-uri |
|---|---|---|---|---|---|---|
| gate.hs.no_en | 10 | candidate.took_national_assessment is_false | needs_confirmation | hs.main_allocation_not_available | Ruta principală de repartizare computerizată nu este disponibilă în forma standard; selectează etapa/ruta alternativă aplicabilă. | claim.hs.average.national_assessment |
| gate.hs.low_options | 20 | options.count lt 10 | warn | hs.options.low_count | Lista are puține opțiuni. Nu există un prag oficial universal, dar ordinul avertizează că prea puține opțiuni pot duce la nerepartizare. | claim.hs.options.risk |
| gate.hs.dossier | 30 | allocation.completed is_true | warn | hs.dossier.deadline | Repartizarea nu finalizează înscrierea; dosarul trebuie depus la liceul repartizat în termen. | claim.hs.calendar.dossier, claim.hs.no_dossier_loses_place |
| gate.hs.local.brochure | 1 | local.brochure_verified is_false | needs_confirmation | hs.local.brochure_not_verified | Nu valida și nu recomanda coduri până când broșura Timiș nu este importată integral și verificată. | claim.hs.local.guide_published |

### 5. Pași cap-coadă

| ordine | step_id | titlu | instrucțiune | deadline | dovada finalizării | recovery |
|---|---|---|---|---|---|---|
| 10 | step.hs.determine_route | Determină ruta de admitere | Confirmă seria, Evaluarea Națională, vârsta și eventualele rute vocaționale/CES/rromi. | none | Ruta principală sau specială este selectată și explicată. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 15 | step.hs.local.import_offer | Importă și validează oferta județeană | Normalizează toate rândurile broșurii: cod, unitate, profil, specializare, limbă, locuri și indicatori istorici, păstrând pagina și snapshot-ul. | none | Importul trece validarea de unicitate a codurilor și verificarea cu două persoane. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 20 | step.hs.load_offer | Încarcă oferta și codurile oficiale | Folosește numai broșura județeană curentă pentru licee, profiluri, specializări, locuri și coduri. | none | Fiecare cod din listă se rezolvă la o ofertă oficială din anul 2026-2027. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 25 | step.hs.local.verify_code | Verifică fiecare cod din listă | Blochează salvarea dacă un cod nu există, este duplicat sau nu corespunde textului afișat utilizatorului. | none | Codul și eticheta utilizatorului sunt identice cu rândul oficial. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 30 | step.hs.build_options | Construiește și verifică lista de opțiuni | Ordonează opțiunile strict după preferință, verifică fiecare cod și adaugă alternative reale pentru a reduce riscul de nerepartizare. | fixed_window | Lista tipărită/confirmată corespunde codurilor și ordinii dorite. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 40 | step.hs.check_allocation | Verifică repartizarea | Consultă rezultatul din 22 iulie și păstrează liceul/profilul/codul rezultat. | fixed_instant | Rezultatul repartizării este salvat și verificat. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 50 | step.hs.prepare_dossier | Pregătește dosarul de liceu | După repartizare, pregătește cererea, actele de identitate/certificatul și fișa medicală. | none | Dosarul este complet în forma solicitată de liceu. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |
| 60 | step.hs.submit_dossier | Depune dosarul la liceul repartizat | Depune dosarul în termen; altfel locul repartizat poate fi pierdut. | fixed_window | Ai dovada depunerii și confirmarea liceului. | Deschide sursa oficială și cere confirmarea instituției dacă informația locală lipsește. |

### 6. Cerințe / acte

| id | act/cerință | obligație | moment | forme | readiness checks | claim-uri |
|---|---|---|---|---|---|---|
| req.hs.options_form | Fișa de opțiuni verificată | mandatory | now | original, electronic | exists, readable, user_confirmed | claim.hs.calendar.options, claim.hs.options.risk |
| req.hs.application | Cerere de înscriere | mandatory | now | original | exists, readable, has_signature | claim.hs.req.enrollment_application |
| req.hs.identity_birth | Act de identitate, dacă este cazul, și certificat de naștere | mandatory | now | original, copy, certified_copy | exists, readable, correct_document_type, names_consistent | claim.hs.req.identity_birth |
| req.hs.medical | Fișă medicală | mandatory | now | original | exists, readable, has_signature, has_stamp | claim.hs.req.medical |

### 7. Canale oficiale

| id | tip | etichetă | URL | status | domeniu |
|---|---|---|---|---|---|
| channel.hs.edu | web | Ministerul Educației — admitere liceu | https://www.edu.ro/admitere-liceu-si-inv-profesional | DEEP_LINK | edu.ro |
| channel.hs.legislation | web | Portal Legislativ — calendar 2026-2027 | https://legislatie.just.ro/Public/DetaliiDocumentAfis/302010 | SOURCE_ONLY | legislatie.just.ro |
| channel.hs.isjtm | web | ISJ Timiș — Ghidul candidatului 2026-2027 | https://www.isj.tm.edu.ro/examene-nationale/admitere/ghidul-candidatului-2026-2027 | DEEP_LINK | isj.tm.edu.ro |
| channel.hs.local.guide | web | ISJ Timiș — Ghid și broșură admitere | https://www.isj.tm.edu.ro/examene-nationale/admitere/ghidul-candidatului-2026-2027 | DEEP_LINK | isj.tm.edu.ro |
| channel.isjtm.email | email | Registratura ISJ Timiș | mailto:registratura@isjtm.ro | DEEP_LINK | isj.tm.edu.ro |

### 8. Source claims

| claim_id | afirmație atomică | source_id | locator | quote_ref | confidence |
|---|---|---|---|---|---|
| claim.jurisdiction.timis.siruta | Codul SIRUTA verificat pentru județul Timiș este 350. | src.ro.siruta.nomenclator | NRSIRUTA, p. 39 | ev.siruta.timis | verified |
| claim.jurisdiction.timisoara.siruta | Codul SIRUTA verificat pentru municipiul Timișoara este 155243. | src.ro.siruta.nomenclator | NRSIRUTA, p. 39 | ev.siruta.timisoara | verified |
| claim.hs.order.scope | Ordinul nr. 6.060/2025 reglementează admiterea pentru anul școlar 2026-2027. | src.highschool.order.6060.2025 | Titlul ordinului | ev.hs.order.identity | verified |
| claim.hs.calendar.options | Completarea și verificarea opțiunilor pentru repartizarea principală se desfășoară între 13 și 20 iulie 2026. | src.highschool.calendar.annex.2026_2027 | Secțiunea G | ev.hs.cal.options | verified |
| claim.hs.calendar.allocation | Repartizarea computerizată și comunicarea rezultatelor sunt programate pentru 22 iulie 2026. | src.highschool.calendar.annex.2026_2027 | Secțiunea G | ev.hs.cal.allocation | verified |
| claim.hs.calendar.dossier | Dosarele se depun la liceul unde candidatul a fost repartizat în perioada 23-28 iulie 2026. | src.highschool.calendar.annex.2026_2027 | Secțiunea G | ev.hs.cal.dossier | verified |
| claim.hs.options.risk | Un număr prea mic de opțiuni poate conduce la nerepartizarea candidatului. | src.highschool.calendar.annex.2026_2027 | Nota din secțiunea G | ev.hs.cal.warning | verified |
| claim.hs.average.national_assessment | Pentru ruta standard, media de admitere este media generală la Evaluarea Națională, calculată cu două zecimale fără rotunjire. | src.highschool.calendar.annex.2026_2027 | Anexa nr. 2, secțiunea I | ev.hs.cal.allocation | verified |
| claim.hs.req.enrollment_application | Dosarul de înscriere la liceul repartizat include cererea de înscriere. | src.highschool.procedure.2026_2027 | Secțiunea dosarul de înscriere | ev.hs.docs.application | verified |
| claim.hs.req.identity_birth | Dosarul include actul de identitate, dacă este cazul, și certificatul de naștere în forma indicată de procedură. | src.highschool.procedure.2026_2027 | Secțiunea dosarul de înscriere | ev.hs.docs.birth | verified |
| claim.hs.req.medical | Dosarul include fișa medicală. | src.highschool.procedure.2026_2027 | Secțiunea dosarul de înscriere | ev.hs.docs.medical | verified |
| claim.hs.no_dossier_loses_place | Candidatul care nu depune dosarul în termen pierde locul repartizat și intră pe ruta ulterioară aplicabilă. | src.highschool.procedure.2026_2027 | Secțiunea neprezentarea dosarului | ev.hs.docs.lose | verified |
| claim.hs.local.guide_published | ISJ Timiș a publicat Ghidul candidatului 2026-2027 la 20 mai 2026. | src.isjtm.highschool.guide.page.2026_2027 | Titlul și data paginii | ev.isjtm.hs.guide, ev.isjtm.hs.date | verified |
| claim.isjtm.contact.registry | Registratura ISJ Timiș primește documente electronic la adresa publicată și are program fizic luni-joi, 13:00-15:00. | src.isjtm.contact | Programul registraturii | ev.isjtm.contact.email, ev.isjtm.contact.hours | verified |
| claim.isjtm.contact.phone | Numărul publicat pentru programări/audiențe ISJ Timiș este 0256 305 799. | src.isjtm.contact | Program audiențe | ev.isjtm.contact.phone | verified |
| claim.isjtm.highschools.directory | Registrul oficial ISJ Timiș permite filtrarea liceelor după localitatea Timișoara. | src.isjtm.institutions.highschools | Filtrul localitate | ev.isjtm.institutions.locality | verified_with_local_gap |

### 9. Freshness și gap-uri locale

Bază națională: `critical`, verificată la `2026-06-25T19:00:00+03:00`, hard expiry `2026-08-19T00:00:00+03:00`, acțiune `block`.

Supliment local: `critical`, verificat la `2026-06-25T19:00:00+03:00`, hard expiry `2026-08-19T00:00:00+03:00`, acțiune `block`.

| gap_id | prioritate | ce lipsește | de ce | on_gap |
|---|---|---|---|---|
| gap.hs.timis.offer_codes | P0 | Codurile oficiale, unitățile, profilurile, specializările, limbile, locurile și ultimele medii din broșura județeană. | Broșura oficială a fost identificată, dar conținutul nu a putut fi normalizat din cauza accesului anti-bot. | block_code_validation_and_option_builder |
| gap.hs.timis.special_routes | P1 | Centrele, adresele și programele locale pentru probe, rromi, CES, etapa a II-a și situații speciale. | Necesită importul integral al ghidului/broșurii și al eventualelor proceduri județene ulterioare. | needs_confirmation |
| gap.all.source_snapshots | P0 | Snapshot-uri locale cu SHA-256 pentru documentele care vor alimenta producția. | URL-ul singur nu garantează reproducerea conținutului dacă fișierul este înlocuit. | block_promotion_to_production |


## Registru de surse

| source_id | titlu | publisher | autoritate | tier | publicat | acces | ingestie | URL |
|---|---|---|---|---|---|---|---|---|
| src.ro.siruta.nomenclator | Nomenclatorul redus al localităților — SIRUTA | Institutul Național de Statistică / Recensământul Populației și Locuințelor | national_operational | 3 | — | accessible | normalized | https://www.recensamantromania.ro/wp-content/uploads/2021/11/SIRUTA.pdf |
| src.preschool.order.3707.2026 | Ordinul nr. 3.707/2026 — Calendar înscriere antepreșcolar și preșcolar 2026-2027 | Ministerul Educației și Cercetării / Portal Legislativ | national_normative | 1 | 2026-04-28 | accessible | normalized | https://legislatie.just.ro/Public/DetaliiDocument/309970 |
| src.preschool.methodology.4018.2024 | Metodologia-cadru aprobată prin Ordinul nr. 4.018/2024, forma consolidată la 28.04.2026 | Ministerul Educației / Portal Legislativ | national_normative | 1 | 2024-03-25 | accessible | normalized | https://legislatie.just.ro/Public/DetaliiDocumentAfis/309263 |
| src.preschool.faq.2026 | Ghid întrebări și răspunsuri — înscriere/reînscriere antepreșcolar și preșcolar 2026-2027 | Ministerul Educației și Cercetării | national_operational | 2 | 2026-05-10 | accessible | normalized | https://www.edu.ro/inscriere_invatamant_prescolar_anteprescolar_faq |
| src.primary.order.3334.2026 | Ordinul nr. 3.334/2026 — Calendar înscriere în învățământul primar 2026-2027 | Ministerul Educației și Cercetării / Portal Legislativ | national_normative | 1 | 2026-02-27 | accessible | normalized | https://legislatie.just.ro/Public/DetaliiDocument/307906 |
| src.primary.methodology.4019.2024 | Metodologia de înscriere în învățământul primar aprobată prin Ordinul nr. 4.019/2024 | Ministerul Educației / Portal Legislativ | national_normative | 1 | 2024-03-22 | accessible | normalized | https://legislatie.just.ro/Public/DetaliiDocumentAfis/280424 |
| src.primary.faq.2026 | Înscrierea în învățământul primar 2026-2027 — FAQ | Ministerul Educației și Cercetării | national_operational | 2 | 2026-02-26 | accessible | normalized | https://www.edu.ro/intrebari_raspunsuri_inscriere_invatamant_primar |
| src.highschool.order.6060.2025 | Ordinul nr. 6.060/2025 privind organizarea și desfășurarea admiterii în liceu 2026-2027 | Ministerul Educației și Cercetării / Portal Legislativ | national_normative | 1 | 2025-09-08 | accessible | normalized | https://legislatie.just.ro/Public/DetaliiDocument/301910 |
| src.highschool.calendar.annex.2026_2027 | Anexa la Ordinul nr. 6.060/2025 — calendarul admiterii în liceu 2026-2027 | Ministerul Educației și Cercetării / Portal Legislativ | national_normative | 1 | 2025-09-08 | accessible | normalized | https://legislatie.just.ro/Public/DetaliiDocumentAfis/302010 |
| src.highschool.procedure.2026_2027 | Procedura/admiterea în învățământul liceal de stat 2026-2027 | Ministerul Educației și Cercetării | national_normative | 1 | — | accessible | normalized | https://www.edu.ro/sites/default/files/PO_AdLic_stat_2026_2027.pdf |
| src.isjtm.contact | Program de audiențe și lucru cu publicul — ISJ Timiș | Inspectoratul Școlar Județean Timiș | county | 2 | — | accessible | normalized | https://www.isj.tm.edu.ro/program-de-audiente-si-lucru-cu-publicul |
| src.isjtm.preschool.page.2026_2027 | Pagina ISJ Timiș pentru înscriere antepreșcolar/preșcolar 2026-2027 | Inspectoratul Școlar Județean Timiș | county | 2 | — | blocked_by_antibot | discovered_not_normalized | https://www.isj.tm.edu.ro/inscrieri/inscrierea-in-unitati-de-invatamant-preuniversitar-anul-2025-2026 |
| src.isjtm.preschool.places.2026_05_22 | Raport dinamic al locurilor disponibile — educație timpurie 2026-2027, snapshot 22.05.2026 | Inspectoratul Școlar Județean Timiș | county | 2 | 2026-05-22 | partial_search_index | expired_snapshot | https://www.isj.tm.edu.ro/public/data_files/media/gradinita2026/202605221834-858_ISJTM_2026-05-22%2018_05_25.816.pdf |
| src.isjtm.primary.page.2026_2027 | Pagina ISJ Timiș — înscriere în învățământul primar 2026-2027 | Inspectoratul Școlar Județean Timiș | county | 2 | — | blocked_by_antibot | discovered_not_normalized | https://www.isj.tm.edu.ro/inscrieri/inscrierea-in-invatamantul-primar/anul-2026-2027 |
| src.isjtm.primary.circumscriptions.timisoara.2026 | Circumscripții școlare Timișoara 2026-2027 | Inspectoratul Școlar Județean Timiș | county | 2 | 2026-03-12 | partial_search_index | blocked_by_source_access | https://www.isj.tm.edu.ro/public/data_files/media/PRIMAR2026/202603121343-TIMISOARA%20merged.pdf |
| src.isjtm.primary.places.timisoara.2026 | Număr locuri clasa pregătitoare — Timișoara 2026-2027 | Inspectoratul Școlar Județean Timiș | county | 2 | 2026-03-12 | partial_search_index | blocked_by_source_access | https://www.isj.tm.edu.ro/public/data_files/media/PRIMAR2026/202603121554-NUMAR%20LOCURI%20TIMISOARA%20primar.pdf |
| src.isjtm.highschool.guide.page.2026_2027 | Ghidul candidatului 2026-2027 | Inspectoratul Școlar Județean Timiș | county | 2 | 2026-05-20 | accessible | normalized | https://www.isj.tm.edu.ro/examene-nationale/admitere/ghidul-candidatului-2026-2027 |
| src.isjtm.highschool.brochure.2026_2027 | Broșura de admitere Timiș 2026-2027 | Inspectoratul Școlar Județean Timiș | county | 2 | 2026-05-26 | blocked_by_antibot | blocked_by_source_access | https://www.isj.tm.edu.ro/public/data_files/media/admitere2026/202605260918-Brosura%20Admitere%202026_2027_f.pdf |
| src.isjtm.institutions.kindergartens | Registrul unităților — grădinițe | Inspectoratul Școlar Județean Timiș | county | 2 | — | blocked_by_antibot | blocked_by_source_access | https://www.isj.tm.edu.ro/institutii/1 |
| src.isjtm.institutions.schools | Registrul unităților — școli gimnaziale/primare | Inspectoratul Școlar Județean Timiș | county | 2 | — | blocked_by_antibot | blocked_by_source_access | https://www.isj.tm.edu.ro/institutii/2 |
| src.isjtm.institutions.highschools | Registrul unităților — licee | Inspectoratul Școlar Județean Timiș | county | 2 | — | accessible_without_rows | discovered_not_normalized | https://www.isj.tm.edu.ro/institutii/3 |

## Registru de claim-uri

| claim_id | afirmație | source_id | locator | citat exact | confidence | effective_from/to |
|---|---|---|---|---|---|---|
| claim.jurisdiction.timis.siruta | Codul SIRUTA verificat pentru județul Timiș este 350. | src.ro.siruta.nomenclator | NRSIRUTA, p. 39 | 350 JUDEȚUL TIMIȘ | verified | None → None |
| claim.jurisdiction.timisoara.siruta | Codul SIRUTA verificat pentru municipiul Timișoara este 155243. | src.ro.siruta.nomenclator | NRSIRUTA, p. 39 | 155243 MUNICIPIUL TIMIȘOARA | verified | None → None |
| claim.ps.calendar.reenrollment | Reînscrierile sunt programate în intervalul 18-22 mai 2026. | src.preschool.order.3707.2026 | Anexă, etapa de reînscrieri | 18-22 mai 2026 | verified | 2026-05-18T00:00:00+03:00 → 2026-05-22T23:59:59+03:00 |
| claim.ps.calendar.stage1 | Etapa I se desfășoară între 25 mai și 18 iunie 2026. | src.preschool.order.3707.2026 | Anexă, etapa I | 25 mai-18 iunie 2026 | verified | 2026-05-25T00:00:00+03:00 → 2026-06-18T23:59:59+03:00 |
| claim.ps.calendar.stage2 | Etapa a II-a se desfășoară între 22 iunie și 9 iulie 2026. | src.preschool.order.3707.2026 | Anexă, etapa a II-a | 22 iunie-9 iulie 2026 | verified | 2026-06-22T00:00:00+03:00 → 2026-07-09T23:59:59+03:00 |
| claim.ps.calendar.adjustments | Etapa de ajustări se desfășoară între 17 și 27 august 2026. | src.preschool.order.3707.2026 | Anexă, etapa de ajustări | 17-27 august 2026 | verified | 2026-08-17T00:00:00+03:00 → 2026-08-27T23:59:59+03:00 |
| claim.ps.calendar.adjustment_result | Rezultatele ajustărilor și locurile rămase se afișează la 28 august 2026. | src.preschool.order.3707.2026 | Anexă, rezultat ajustări | 28 august 2026 | verified | 2026-08-28T00:00:00+03:00 → 2026-08-28T23:59:59+03:00 |
| claim.ps.calendar.siiir | Termenul de introducere a copiilor înscriși în SIIIR este 4 septembrie 2026. | src.preschool.order.3707.2026 | Anexă, introducerea în SIIIR | 4 septembrie 2026 | verified | 2026-09-04T00:00:00+03:00 → 2026-09-04T23:59:59+03:00 |
| claim.ps.three_options | Cererea de înscriere conține trei opțiuni de unități, în ordinea preferinței. | src.preschool.faq.2026 | Secțiunea documentele dosarului | trei opțiuni | verified | None → None |
| claim.ps.not_first_come | Ordinea depunerii sau numărul de înregistrare nu constituie criteriu de admitere. | src.preschool.faq.2026 | Secțiunea criterii de departajare | primul venit, primul servit | verified | None → None |
| claim.ps.criteria_specific_locked | Criteriile specifice devin publice la data din calendar și nu mai pot fi modificate ori completate după publicare. | src.preschool.methodology.4018.2024 | Art. 12 alin. (2) | modificarea ori adăugarea altor criterii specifice de departajare este interzisă | verified | None → None |
| claim.ps.isj_publish_units_places | Inspectoratul trebuie să publice unitățile, adresele, numărul de grupe/locuri și site-urile unităților. | src.preschool.methodology.4018.2024 | Art. 13 alin. (1)-(2) | pe site-ul inspectoratului școlar | verified | None → None |
| claim.ps.isj_telverde | Inspectoratul trebuie să instituie o linie Telverde pe perioada înscrierilor. | src.preschool.methodology.4018.2024 | Art. 13 alin. (1) lit. a) | instituirea și funcționarea unei linii Telverde | verified | None → None |
| claim.ps.req.application | Cererea-tip este document obligatoriu al dosarului. | src.preschool.faq.2026 | Secțiunea documentele dosarului | trei opțiuni | verified | None → None |
| claim.ps.req.birth_certificate | Dosarul include copia certificatului de naștere al copilului. | src.preschool.faq.2026 | Secțiunea documentele dosarului, pct. certificat | trei opțiuni | verified | None → None |
| claim.ps.req.parent_ids | Dosarul include copii ale actelor de identitate ale părinților/reprezentantului legal. | src.preschool.faq.2026 | Secțiunea documentele dosarului, pct. acte identitate | în prezența părintelui | verified | None → None |
| claim.ps.req.employment_extended | Pentru program prelungit și pentru antepreșcolar se solicită adeverințe de angajat pentru fiecare părinte/reprezentant sau documentul privind concediul de creștere. | src.preschool.faq.2026 | Secțiunea documentele dosarului | adeverință de angajat pentru fiecare dintre părinți | verified | None → None |
| claim.ps.req.criteria_documents | Documentele care dovedesc criteriile generale ori specifice se adaugă numai când criteriul este invocat. | src.preschool.faq.2026 | Secțiunea documentele dosarului | trei opțiuni | verified | None → None |
| claim.ps.req.remote_declaration | Transmiterea cererii prin e-mail sau poștă necesită declarație pe propria răspundere privind veridicitatea datelor. | src.preschool.faq.2026 | Secțiunea documentele dosarului | în prezența părintelui | verified | None → None |
| claim.ps.req.parental_authority | Părinții divorțați trebuie să dovedească exercitarea autorității părintești și locuința minorului. | src.preschool.faq.2026 | Secțiunea documentele dosarului | în prezența părintelui | verified | None → None |
| claim.ps.validation.in_person | Validarea dosarului se face la unitatea solicitată, în prezența părintelui/reprezentantului, cu originale pentru certificarea copiilor. | src.preschool.faq.2026 | Secțiunea validarea dosarului | în prezența părintelui | verified | None → None |
| claim.ps.medical.family_doctor | Adeverința clinică se adaugă la începutul anului și este necesară în prima zi de prezentare. | src.preschool.faq.2026 | Secțiunea documente medicale | maximum 5 zile | verified | None → None |
| claim.ps.medical.epidemiological | Avizul epidemiologic/dovada de vaccinare se emite cu maximum cinci zile înainte de începerea frecventării. | src.preschool.faq.2026 | Secțiunea documente medicale | maximum 5 zile | verified | None → None |
| claim.ps.local.snapshot.2026_05_22 | ISJ Timiș a publicat un snapshot al locurilor la 22 mai 2026; acesta este istoric și nu poate fi folosit ca disponibilitate curentă după etapele ulterioare. | src.isjtm.preschool.places.2026_05_22 | Antet/subsol raport | 22/05/2026 18:05 | expired | 2026-05-22T18:05:00+03:00 → 2026-05-22T23:59:59+03:00 |
| claim.pr.calendar.circumscriptions | Circumscripțiile și planul propus trebuiau afișate la 12 martie 2026. | src.primary.order.3334.2026 | Anexă, pregătirea înscrierii | 12 martie 2026 | verified | 2026-03-12T00:00:00+02:00 → 2026-03-12T23:59:59+02:00 |
| claim.pr.calendar.recommendation | Recomandările/evaluările și cererile de amânare se derulează în intervalul 16-30 martie 2026. | src.primary.order.3334.2026 | Anexă, recomandare/evaluare | 16 martie-30 martie 2026 | verified | 2026-03-16T00:00:00+02:00 → 2026-03-30T23:59:59+03:00 |
| claim.pr.calendar.application | Completarea, depunerea/transmiterea și validarea cererilor din etapa I se fac între 31 martie și 6 mai 2026. | src.primary.order.3334.2026 | Anexă, cereri și validare | 31 martie-6 mai 2026 | verified | 2026-03-31T00:00:00+03:00 → 2026-05-06T23:59:59+03:00 |
| claim.pr.calendar.stage2_application | Cererile pentru etapa a II-a se depun/transmit în perioada 25-29 mai 2026. | src.primary.order.3334.2026 | Anexă, etapa a II-a | 25 mai-29 mai 2026 | verified | 2026-05-25T00:00:00+03:00 → 2026-05-29T23:59:59+03:00 |
| claim.pr.calendar.final | Listele finale ale copiilor înscriși în clasa pregătitoare se afișează la 16 iunie 2026. | src.primary.order.3334.2026 | Anexă, etapa a II-a | 16 iunie 2026 | verified | 2026-06-16T00:00:00+03:00 → 2026-06-16T23:59:59+03:00 |
| claim.pr.calendar.unresolved | Situațiile copiilor încă neînscriși se centralizează și soluționează în intervalul 1-4 septembrie 2026. | src.primary.order.3334.2026 | Anexă, situații rămase | 1 septembrie-4 septembrie 2026 | verified | 2026-09-01T00:00:00+03:00 → 2026-09-04T23:59:59+03:00 |
| claim.pr.age.mandatory_august | Copiii care au frecventat preșcolarul și împlinesc șase ani până la 31 august inclusiv trebuie înscriși în clasa pregătitoare. | src.primary.methodology.4019.2024 | Art. 5 alin. (1) | 6 ani până la data de 31 august inclusiv | verified | None → None |
| claim.pr.age.september_december | Copiii care împlinesc șase ani între 1 septembrie și 31 decembrie pot fi înscriși dacă nivelul de dezvoltare este corespunzător. | src.primary.methodology.4019.2024 | Art. 6 alin. (1) | 1 septembrie-31 decembrie inclusiv | verified | None → None |
| claim.pr.recommendation.kindergarten | Pentru copilul din fereastra septembrie-decembrie care a frecventat grădinița este necesară recomandarea unității preșcolare. | src.primary.methodology.4019.2024 | Art. 6 alin. (2) | 1 septembrie-31 decembrie inclusiv | verified | None → None |
| claim.pr.recommendation.cjrae | Evaluarea/recomandarea CJRAE se aplică, în această rută, copiilor care nu au frecventat grădinița sau s-au întors din străinătate. | src.primary.methodology.4019.2024 | Art. 7 alin. (1) | 1 septembrie-31 decembrie inclusiv | verified | None → None |
| claim.pr.defer.one_year | În cazuri justificate, înscrierea copilului care împlinește șase ani până la 31 august poate fi amânată cu maximum un an. | src.primary.faq.2026 | Nota privind amânarea | maximum un an | verified | None → None |
| claim.pr.circumscription.guaranteed | Copilul pentru care se solicită școala de circumscripție este înmatriculat acolo după validarea cererii. | src.primary.methodology.4019.2024 | Art. 9 alin. (1) | școala de circumscripție | verified | None → None |
| claim.pr.other_school.free_places | Înscrierea la altă școală decât cea de circumscripție depinde de locurile libere și criteriile de departajare. | src.primary.methodology.4019.2024 | Art. 9-10 | școala de circumscripție | verified | None → None |
| claim.pr.reserve.circumscription | Părintele poate bifa păstrarea locului la școala de circumscripție dacă solicită o altă școală. | src.primary.faq.2026 | Secțiunea alegerea unității | locul la şcoala de circumscripţie să fie rezervat | verified | None → None |
| claim.pr.req.parent_id | Dosarul include copie și original după actul de identitate al părintelui/reprezentantului. | src.primary.faq.2026 | Secțiunea actele necesare | Copie şi original | verified | None → None |
| claim.pr.req.birth_certificate | Dosarul include copie și original după certificatul de naștere al copilului. | src.primary.faq.2026 | Secțiunea actele necesare | Copie şi original | verified | None → None |
| claim.pr.req.parental_authority | Părinții divorțați depun dovada modului de exercitare a autorității părintești și a locuinței minorului. | src.primary.faq.2026 | Secțiunea actele necesare | Copie şi original | verified | None → None |
| claim.pr.req.criteria_documents | Pentru o școală din afara circumscripției se depun documentele care dovedesc criteriile generale și specifice invocate. | src.primary.methodology.4019.2024 | Art. 10 și art. 14 alin. (6) | școala de circumscripție | verified | None → None |
| claim.pr.validation.electronic_possible | Metodologia permite, după caz, validarea prin semnătură la sediu sau prin mijloace electronice. | src.primary.methodology.4019.2024 | Art. 15 alin. (4) | prin mijloace electronice, după caz | verified_with_local_gap | None → None |
| claim.pr.validation.faq_in_person | Ghidul operațional indică prezentarea la unitate pentru validarea cererii completate online. | src.primary.faq.2026 | Secțiunea unde au loc înscrierile | părinții trebuie să meargă la unitatea de învățământ | verified_with_local_gap | None → None |
| claim.pr.local.circumscriptions_source_exists | ISJ Timiș a publicat documentul oficial de circumscripții Timișoara 2026-2027. | src.isjtm.primary.circumscriptions.timisoara.2026 | Antetul documentului indexat | nr. 96/CA/09.03.2026 | verified_with_local_gap | None → None |
| claim.pr.local.places_source_exists | ISJ Timiș a publicat documentul oficial privind locurile pentru clasa pregătitoare în Timișoara. | src.isjtm.primary.places.timisoara.2026 | Titlul raportului indexat | Număr locuri 2026-2027 | verified_with_local_gap | None → None |
| claim.hs.order.scope | Ordinul nr. 6.060/2025 reglementează admiterea pentru anul școlar 2026-2027. | src.highschool.order.6060.2025 | Titlul ordinului | anul școlar 2026-2027 | verified | None → None |
| claim.hs.calendar.options | Completarea și verificarea opțiunilor pentru repartizarea principală se desfășoară între 13 și 20 iulie 2026. | src.highschool.calendar.annex.2026_2027 | Secțiunea G | 13 - 20 iulie 2026 | verified | 2026-07-13T00:00:00+03:00 → 2026-07-20T23:59:59+03:00 |
| claim.hs.calendar.allocation | Repartizarea computerizată și comunicarea rezultatelor sunt programate pentru 22 iulie 2026. | src.highschool.calendar.annex.2026_2027 | Secțiunea G | 22 iulie 2026 | verified | 2026-07-22T00:00:00+03:00 → 2026-07-22T23:59:59+03:00 |
| claim.hs.calendar.dossier | Dosarele se depun la liceul unde candidatul a fost repartizat în perioada 23-28 iulie 2026. | src.highschool.calendar.annex.2026_2027 | Secțiunea G | 23 - 28 iulie 2026 | verified | 2026-07-23T00:00:00+03:00 → 2026-07-28T23:59:59+03:00 |
| claim.hs.options.risk | Un număr prea mic de opțiuni poate conduce la nerepartizarea candidatului. | src.highschool.calendar.annex.2026_2027 | Nota din secțiunea G | Numărul redus de opțiuni completate poate conduce la nerepartizarea | verified | None → None |
| claim.hs.average.national_assessment | Pentru ruta standard, media de admitere este media generală la Evaluarea Națională, calculată cu două zecimale fără rotunjire. | src.highschool.calendar.annex.2026_2027 | Anexa nr. 2, secțiunea I | 22 iulie 2026 | verified | None → None |
| claim.hs.req.enrollment_application | Dosarul de înscriere la liceul repartizat include cererea de înscriere. | src.highschool.procedure.2026_2027 | Secțiunea dosarul de înscriere | cererea de înscriere | verified | None → None |
| claim.hs.req.identity_birth | Dosarul include actul de identitate, dacă este cazul, și certificatul de naștere în forma indicată de procedură. | src.highschool.procedure.2026_2027 | Secțiunea dosarul de înscriere | certificatul de naștere | verified | None → None |
| claim.hs.req.medical | Dosarul include fișa medicală. | src.highschool.procedure.2026_2027 | Secțiunea dosarul de înscriere | fișa medicală | verified | None → None |
| claim.hs.no_dossier_loses_place | Candidatul care nu depune dosarul în termen pierde locul repartizat și intră pe ruta ulterioară aplicabilă. | src.highschool.procedure.2026_2027 | Secțiunea neprezentarea dosarului | pierd locurile | verified | None → None |
| claim.hs.local.guide_published | ISJ Timiș a publicat Ghidul candidatului 2026-2027 la 20 mai 2026. | src.isjtm.highschool.guide.page.2026_2027 | Titlul și data paginii | GHIDUL CANDIDATULUI 2026-2027 / 20.05.2026 | verified | None → None |
| claim.isjtm.contact.registry | Registratura ISJ Timiș primește documente electronic la adresa publicată și are program fizic luni-joi, 13:00-15:00. | src.isjtm.contact | Programul registraturii | registratura@isjtm.ro / 13.00 – 15.00 | verified | None → None |
| claim.isjtm.contact.phone | Numărul publicat pentru programări/audiențe ISJ Timiș este 0256 305 799. | src.isjtm.contact | Program audiențe | 0256305799 | verified | None → None |
| claim.isjtm.highschools.directory | Registrul oficial ISJ Timiș permite filtrarea liceelor după localitatea Timișoara. | src.isjtm.institutions.highschools | Filtrul localitate | TIMIŞOARA | verified_with_local_gap | None → None |

## Matrice de conflicte

| conflict_id | traseu | subiect | poziția A | poziția B | politică de rezolvare | status |
|---|---|---|---|---|---|---|
| conflict.primary.validation_channel | primary | Validarea cererii completate online | Metodologia permite validare electronică, după caz. | FAQ-ul cere prezentarea la unitatea aleasă. | Nu se alege arbitrar. Pentru fiecare școală se cere confirmarea canalului operațional; UI afișează prezentarea fizică drept ruta sigură până la confirmarea unei validări electronice active. | verified_with_local_gap |
| conflict.preschool.local_page_slug | preschool | Metadate pagină ISJ Timiș | Slug-ul URL indică 2025-2026. | Materialele asociate sunt pentru 2026-2027. | Se păstrează sursa, dar curatorul trebuie să captureze titlul, data și linkurile curente înainte de publicare. | needs_confirmation |
| conflict.preschool.places_snapshot_stale | preschool | Disponibilitatea locurilor | Snapshot oficial la 22.05.2026. | Etapele ulterioare schimbă ocuparea și locurile libere. | Snapshot-ul este istoric; nu se afișează ca disponibilitate curentă. Se cere refresh după fiecare rezultat de etapă. | expired |
| conflict.local_source_access | all | Acces automat la PDF-urile locale | Sursele oficiale sunt indexate și URL-urile sunt confirmate. | Protecția anti-bot împiedică preluarea stabilă și verificarea fiecărui rând. | Import manual/curator, snapshot local, SHA-256 și verificare cu două persoane înainte de utilizare în producție. | needs_confirmation |

## Registru de gap-uri

| gap_id | traseu | P | teritoriu | lipsă | surse așteptate | motiv | acțiune |
|---|---|---|---|---|---|---|---|
| gap.ps.timisoara.unit_inventory | preschool | P0 | RO/Timiș/Timișoara | Lista normalizată completă a unităților publice/particulare relevante, cu SIIIR, adresă, program și contacte 2026-2027. | src.isjtm.institutions.kindergartens, src.isjtm.preschool.page.2026_2027 | Directorul oficial este protejat anti-bot și nu a furnizat rândurile în mod stabil. | block_unit_specific_recommendation |
| gap.ps.timisoara.current_places | preschool | P0 | RO/Timiș/Timișoara | Locuri curente după rezultatul etapei active, pe unitate/nivel/program/limbă. | src.isjtm.preschool.page.2026_2027 | Snapshot-ul din 22.05.2026 este expirat pentru disponibilitatea curentă. | needs_confirmation |
| gap.ps.timisoara.criteria | preschool | P0 | RO/Timiș/Timișoara | Criteriile specifice și documentele doveditoare pentru fiecare unitate. | src.isjtm.preschool.page.2026_2027, src.isjtm.institutions.kindergartens | Necesită parcurgerea site-urilor fiecărei unități și snapshot al documentelor publicate. | block_compatibility_scoring |
| gap.ps.timisoara.telverde | preschool | P1 | RO/Timiș | Numărul și programul Telverde 2026 pentru educație timpurie. | src.isjtm.preschool.page.2026_2027 | Nu a fost confirmat oficial în materialele accesibile. | hide_channel |
| gap.pr.timisoara.circumscriptions_rows | primary | P0 | RO/Timiș/Timișoara | Maparea exactă stradă + interval/paritate numere → școală, pentru toate rândurile. | src.isjtm.primary.circumscriptions.timisoara.2026 | PDF-ul oficial există, dar accesul automat stabil este blocat; nu se acceptă extragere incompletă din snippeturi. | block_exact_circumscription_resolution |
| gap.pr.timisoara.places_rows | primary | P0 | RO/Timiș/Timișoara | Planul complet de școlarizare și locurile/clasele per unitate. | src.isjtm.primary.places.timisoara.2026 | PDF-ul oficial nu a putut fi normalizat rând cu rând. | needs_confirmation |
| gap.pr.timisoara.criteria | primary | P0 | RO/Timiș/Timișoara | Criteriile specifice și documentele doveditoare pentru fiecare școală. | src.isjtm.primary.page.2026_2027, src.isjtm.institutions.schools | Sunt publicate la nivelul unității; nu există încă un registru normalizat verificat. | block_out_of_circumscription_ranking |
| gap.pr.timisoara.validation_channel | primary | P1 | RO/Timiș/Timișoara | Confirmarea pe școală a validării fizice versus electronice active. | src.isjtm.primary.page.2026_2027, src.isjtm.institutions.schools | Metodologia și FAQ-ul lasă o diferență între posibilitatea juridică și practica operațională. | default_to_in_person_and_warn |
| gap.hs.timis.offer_codes | highschool | P0 | RO/Timiș | Codurile oficiale, unitățile, profilurile, specializările, limbile, locurile și ultimele medii din broșura județeană. | src.isjtm.highschool.brochure.2026_2027 | Broșura oficială a fost identificată, dar conținutul nu a putut fi normalizat din cauza accesului anti-bot. | block_code_validation_and_option_builder |
| gap.hs.timis.special_routes | highschool | P1 | RO/Timiș | Centrele, adresele și programele locale pentru probe, rromi, CES, etapa a II-a și situații speciale. | src.isjtm.highschool.guide.page.2026_2027, src.isjtm.highschool.brochure.2026_2027 | Necesită importul integral al ghidului/broșurii și al eventualelor proceduri județene ulterioare. | needs_confirmation |
| gap.all.source_snapshots | all | P0 | RO/Timiș | Snapshot-uri locale cu SHA-256 pentru documentele care vor alimenta producția. | src.isjtm.preschool.places.2026_05_22, src.isjtm.primary.circumscriptions.timisoara.2026, src.isjtm.primary.places.timisoara.2026, src.isjtm.highschool.brochure.2026_2027 | URL-ul singur nu garantează reproducerea conținutului dacă fișierul este înlocuit. | block_promotion_to_production |

## Auto-verificare

- [x] Fiecare afirmație critică folosită de regulile candidate are claim și sursă oficială.
- [x] Deadlines naționale sunt date exacte din actele oficiale; cele locale neconfirmate nu sunt inventate.
- [x] Regulile de vârstă pentru clasa pregătitoare păstrează fereastra și excepțiile.
- [x] Conflictele sunt păstrate și nu sunt „rezolvate” prin presupunere.
- [x] SIRUTA Timiș/Timișoara este verificat din nomenclatorul oficial.
- [x] Cele șase fișiere de reguli trec JSON Schema și verificări de referințe.
- [ ] Circumscripțiile Timișoara sunt normalizate integral — **gap P0**.
- [ ] Criteriile tuturor unităților sunt capturate — **gap P0**.
- [ ] Codurile și oferta liceelor Timiș sunt importate integral — **gap P0**.

## Verdict pentru Codex

Codex poate implementa imediat schema, motorul, ecranele, calendarul național, verificarea formală a actelor și gate-urile de încredere. Nu are voie să activeze în producție: resolverul exact de circumscripție Timișoara, ranking-ul pe criterii locale, locurile curente pe grădiniță sau validatorul codurilor de liceu până când task-urile P0 din `local_ingestion_queue.json` sunt închise și aprobate.
