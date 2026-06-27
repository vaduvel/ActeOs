# Mobile Screen Checklist

Bază: ADR-006 (optional account), ADR-014 (Android nativ), ADR-017 (anonymous-first + snapshot), `contracts/openapi.yaml`, `contracts/error_codes.yaml`, `contracts/feature_flags.yaml`, `contracts/retention_policy.yaml`, `contracts/design_tokens.json`.

## 1. Home / Discovery
- Purpose: să ofere intrarea principală în discovery fără cont obligatoriu și fără să forțeze userul într-un chatbot.
- Data source: `data/intent_taxonomy.yaml`, `data/r1_event_catalog.yaml`, `app_readiness/mobile_copy/r1_mobile_copy_pack.yaml`.
- API endpoint / contract: `GET /v1/discovery/home` -> `DiscoveryHomeResponse`; `GET /v1/categories` -> `CategoryListResponse`.
- Required fields: `headline_ro`, `search_placeholder_ro`, `quick_actions[]`, `categories[]`, `catalog_version`.
- Empty state: catalog gol sau nicio categorie disponibilă pentru jurisdicție -> mesaj neutru + retry.
- Loading state: skeleton pentru headline, quick actions și categorii.
- Error state: `ErrorResponse`; tratare explicită pentru `DISCOVERY_INDEX_UNAVAILABLE` și `CATALOG_VERSION_MISMATCH`.
- Privacy constraints: funcționează fără `user_id`; nu afișează documente locale sau PII; respectă ADR-006.
- Acceptance criteria: utilizatorul poate porni discovery fără cont și vede surse oficiale prioritizate, fără ofertare comercială.

## 2. Search results / intent confirmation
- Purpose: să rezolve o interogare liberă într-un intent public, păstrând confirmarea utilizatorului când există ambiguitate.
- Data source: `data/intent_taxonomy.yaml`, `data/intent_event_links.yaml`, `app_readiness/qa/r1_discovery_query_matrix.md`.
- API endpoint / contract: `POST /v1/intents/resolve-query` -> `ResolveIntentQueryRequest` / `ResolveIntentQueryResponse`; `GET /v1/intents/{intent_type_id}` -> `IntentSummary`.
- Required fields: request `query`, `locale`; response `resolution_state`, `candidates[]`, `fallback_used`, `request_id`, `catalog_version`.
- Empty state: `resolution_state=no_result` -> mesaj cu reformulare, fără inventarea unui traseu.
- Loading state: spinner cu request id intern, fără a bloca tastarea următoarei interogări.
- Error state: `INTENT_QUERY_TOO_SHORT`, `INTENT_NOT_FOUND`, `SEMANTIC_FALLBACK_DISABLED`.
- Privacy constraints: query-ul nu trebuie să includă documente sau CNP; semantic fallback rămâne controlat prin feature flag.
- Acceptance criteria: pentru interogări cu risc `high` apare un prompt explicit de disambiguizare înainte de case creation.

## 3. Event card
- Purpose: să arate ce poate vedea userul pentru un event concret: status, primul pas și documentele estimate.
- Data source: `app_readiness/mobile_copy/r1_mobile_copy_pack.yaml`, `data/r1_event_catalog.yaml`, `research/inbox/<event>/templates.yaml`.
- API endpoint / contract: `GET /v1/life-events/{event_type_id}` -> `LifeEventSummary`; date de display completate din copy pack generat.
- Required fields: `id`, `title_ro`, `category_id`, `production_status`, `app_card.status_label_ro`, `journey_preview.primary_step_title_ro`.
- Empty state: `missing_content` -> card de verificare, fără documente inventate.
- Loading state: skeleton pentru titlu, status și primul pas.
- Error state: `LIFE_EVENT_NOT_FOUND` sau `UNKNOWN_INTENT_ID_FROM_ADAPTER` mapate prin `ErrorResponse`.
- Privacy constraints: nu se afișează `installation_id` / `user_id` în card; doar date publice și copy structurală.
- Acceptance criteria: cardul distinge clar `ready_for_app_preview`, `needs_review_banner`, `blocked_not_publishable` și `missing_content`.

## 4. Case creation
- Purpose: să transforme intentul confirmat într-un caz API determinist, fără apel extern la rezolvare.
- Data source: `contracts/openapi.yaml`, `app_readiness/fixtures/r1_case_creation_fixtures.yaml`.
- API endpoint / contract: `POST /v1/cases` -> `CreateCaseRequest` / `CaseResponse`.
- Required fields: `intent_type_id`, `reference_date`, `timezone=Europe/Bucharest`, `jurisdiction_path`; `installation_id` sau `user_id` după ADR-017.
- Empty state: dacă nu există intent mapat sigur -> nu crea cazul, cere confirmarea intentului.
- Loading state: progres scurt cu mesaj neutru „se pregătește traseul”.
- Error state: `VALIDATION_ERROR`, `INTENT_NOT_FOUND`, `INTENT_NOT_AVAILABLE_IN_JURISDICTION`.
- Privacy constraints: răspunsul nu trebuie să echo-uiască `user_id` sau `installation_id`; logurile rămân privacy-safe.
- Acceptance criteria: un caz se poate crea fără cont, cu `installation_id`, iar contract tests rămân verzi.

## 5. Journey overview
- Purpose: să arate statusul curent al cazului, pașii, warning-urile și trust state-ul.
- Data source: `CaseResponse.events[]`, `JourneyResponse`, mobile copy pack.
- API endpoint / contract: `GET /v1/cases/{case_id}` -> `CaseResponse`; `GET /v1/journeys/{journey_id}` -> `JourneyResponse`.
- Required fields: `status`, `events[]`, `resolution_trace`, `trust_state`, `steps[]`, `next_step_id`, `warnings[]`, `conflicts[]`.
- Empty state: niciun journey sau zero pași -> fallback către event card și gaps banner.
- Loading state: skeleton pentru timeline și status badges.
- Error state: `ErrorResponse` + retry; nu pierde referința la `request_id`.
- Privacy constraints: snapshot-ul este afișat fără documente brute; respectă retention-ul anonim cu TTL scurt.
- Acceptance criteria: userul înțelege „ce fac acum”, „până când” și „ce lipsește” din primul ecran al journey-ului.

## 6. Step detail
- Purpose: să explice un pas concret și să permită actualizarea statusului local/API.
- Data source: `templates.yaml -> step_templates`, `JourneyResponse.steps[]`.
- API endpoint / contract: `PUT /v1/journeys/{journey_id}/steps/{step_id}/status` -> `UpdateStatusRequest` / `JourneyResponse`.
- Required fields: `step_id`, `status`, `version`, `instruction_ro`, `completion_evidence_ro`, `recovery_actions_ro`.
- Empty state: step fără template -> mesaj `undetermined_from_yaml` + gap intern.
- Loading state: optimistic update controlată de `version`.
- Error state: conflict/version mismatch prin `ErrorResponse`.
- Privacy constraints: `evidence_note` nu trebuie să conțină date sensibile copiate integral din documente.
- Acceptance criteria: utilizatorul poate marca pasul și vede imediat noul journey recalculat, fără comportament nedeterminist.

## 7. Requirement detail
- Purpose: să afișeze documentul/cerința, formele acceptate și verificările de readiness.
- Data source: `templates.yaml -> requirement_templates`, `JourneyResponse`.
- API endpoint / contract: `PUT /v1/journeys/{journey_id}/requirements/{requirement_id}/status` -> `UpdateStatusRequest` / `JourneyResponse`.
- Required fields: `requirement_id`, `title_ro`, `description_ro`, `accepted_forms[]`, `readiness_checks[]`, `obligation`, `timing`.
- Empty state: requirement fără template -> banner `document nedeterminat din YAML`.
- Loading state: skeleton pentru formular și accepted forms.
- Error state: `ErrorResponse`; nu rescrie statusul local dacă update-ul e refuzat.
- Privacy constraints: nu pretinde autenticitate; documentele rămân locale implicit.
- Acceptance criteria: fiecare requirement poate răspunde la întrebarea „ce am nevoie” și „cum știu că e complet”.

## 8. Document readiness
- Purpose: să ruleze verificările de readiness pe dispozitiv și să întoarcă limitările explicit.
- Data source: `contracts/openapi.yaml`, `contracts/retention_policy.yaml`, `contracts/design_tokens.json`.
- API endpoint / contract: `POST /v1/documents/{document_id}/readiness` -> `ReadinessRequest` / `ReadinessResponse`.
- Required fields: `requirement_id`, `checks[]`, `processing_mode`, `status`, `checks[].message_ro`, `limitations[]`, `authenticity_verified=false`.
- Empty state: document neatașat -> CTA pentru selectare locală.
- Loading state: progres per check, nu spinner generic opac.
- Error state: `ErrorResponse`; păstrează documentul local și mesajul de retry.
- Privacy constraints: by default fără upload de bytes sau OCR raw; `authenticity_verified` trebuie să rămână `false`.
- Acceptance criteria: verdictul de readiness funcționează fără rețea și fără a induce ideea falsă de verificare a autenticității.

## 9. Warning / confirmation banner
- Purpose: să expună explicit conflictul, nevoia de confirmare sau staleness-ul, fără rezolvare tăcută.
- Data source: `JourneyResponse.warnings[]`, `JourneyResponse.conflicts[]`, `freshness_policy.yaml`, ADR-010, ADR-016.
- API endpoint / contract: `GET /v1/journeys/{journey_id}` -> `JourneyResponse`; `GET /v1/cases/{case_id}` -> `CaseResponse`.
- Required fields: `trust_state`, `warnings[]`, `conflicts[]`, `resolution_trace`.
- Empty state: niciun warning -> banner absent, nu placeholder gol.
- Loading state: placeholder compact în header-ul journey-ului.
- Error state: nu ascunde bannerul pe eroare; păstrează ultima stare cunoscută până la retry.
- Privacy constraints: mesajele nu includ text brut de document sau date personale.
- Acceptance criteria: `conditional_go` și `no_go` sunt vizibile și diferențiate corect în UI.

## 10. Blocked route state
- Purpose: să oprească publicarea/servirea unui traseu nesigur și să explice de ce este blocat.
- Data source: `app_readiness/r1_event_readiness_matrix.md`, `gaps/r1_app_data_gaps.md`, `JourneyResponse`.
- API endpoint / contract: `GET /v1/life-events/{event_type_id}`, `GET /v1/cases/{case_id}`, `ErrorResponse`.
- Required fields: status derivat `blocked_not_publishable`, `blocker_summary`, `next_action` intern.
- Empty state: nu există blocaj -> ecranul nu trebuie afișat.
- Loading state: card compact cu motivul blocajului, nu spinner full-screen inutil.
- Error state: fallback neutru „ruta nu este disponibilă momentan”.
- Privacy constraints: nu expune intern claim ids userului final; doar formulări neutre în UI publică.
- Acceptance criteria: userul nu poate fi împins într-un traseu `no_go` fără o explicație clară și non-comercială.

## 11. Local-only / anonymous-first identity state
- Purpose: să explice de ce aplicația funcționează fără cont și ce se schimbă dacă userul activează sync.
- Data source: ADR-006, ADR-017, `retention_policy.yaml`, `feature_flags.yaml`.
- API endpoint / contract: `POST /v1/cases`; orice endpoint care acceptă `installation_id` sau `user_id`.
- Required fields: `installation_id`, opțional `user_id`, consimțământ pentru sync, TTL anonim, mesaje locale-only.
- Empty state: niciun caz creat încă -> explică stocarea locală și faptul că serverul nu devine sursă implicită pentru documente.
- Loading state: nu e necesar ecran separat; doar badge sau info panel.
- Error state: dacă sync-ul nu e configurat, fallback la local-only fără pierdere de funcționalitate.
- Privacy constraints: cazurile anonime au retenție scurtă pe server; documentele rămân locale implicit.
- Acceptance criteria: aplicația poate fi folosită end-to-end fără cont, iar upgrade-ul la cont rămâne explicit și reversibil.

## 12. Feedback / institution rejection report
- Purpose: să colecteze refuzuri din teren fără a reinterpreta legal rezultatul.
- Data source: `contracts/openapi.yaml`, `contracts/error_codes.yaml`.
- API endpoint / contract: `POST /v1/feedback/rejections` -> `FeedbackRejectionRequest` / `FeedbackResponse`.
- Required fields: `journey_id`, `step_id`, `occurred_on`, `institution_label`, `category`, `description`, `evidence_document_id` optional.
- Empty state: fără refuz -> CTA discret, nu interstițial blocant.
- Loading state: upload/procesare doar pentru metadata consimțită.
- Error state: păstrează draftul local și oferă retry cu `request_id` dacă există.
- Privacy constraints: nu cere upload de imagine/document by default; cere consimțământ explicit pentru orice sync.
- Acceptance criteria: userul poate raporta un refuz instituțional fără să trimită documente brute și fără să piardă traseul local.
