# Admin / Research Console Checklist

Bază: `contracts/rbac_matrix.yaml`, `contracts/freshness_policy.yaml`, `contracts/openapi.yaml`, ADR-008, ADR-010, ADR-016, ADR-017.

## 1. Source claims queue
- Purpose: să arate claim-urile nou create sau importate care așteaptă verificare umană.
- Data source yaml/db table if known: `research/inbox/*/source_claims.yaml`; țintă DB per ADR-008: `content.claims` + `content.source_snapshots`.
- User action: filtrează, citește evidence excerpt, mută claim-ul în `active` / `in_review` / `withdrawn` după verificare.
- Required fields: `claim_id`, `statement`, `source_id`, `publisher`, `authority_level`, `confidence`, `status`, `freshness_class`, `accessed_at`, `locator`.
- Risk if missing: contentul critic poate ajunge în reguli fără trasabilitate sau poate rămâne blocat fără explainability.
- Acceptance criteria: un `researcher` sau `reviewer` poate vedea rapid ce claim-uri blochează un event și ce dovadă susține fiecare afirmație.

## 2. Claim verification status
- Purpose: să expună statusul real al claim-urilor și deadline-urile de review/expiry.
- Data source yaml/db table if known: `source_claims.yaml`; `POST /v1/admin/claims` -> `ClaimCreateRequest` / `ClaimResponse`; țintă DB: `content.claims`.
- User action: aprobă, retrimite la research sau marchează conflict.
- Required fields: `id`, `statement`, `status`, `review_due_at`, `hard_expiry_at`, `freshness_class`, `confidence`.
- Risk if missing: app-ul nu poate ști ce merge în banner de review și ce trebuie blocat complet.
- Acceptance criteria: dashboard-ul distinge clar `verified`, `needs_confirmation`, `conflicting`, `in_review`, `active`.

## 3. Conflicts
- Purpose: să afișeze explicit conflictele între surse, fără rezolvare silențioasă.
- Data source yaml/db table if known: `source_claims.yaml` cu `confidence=conflicting`; `GET /v1/admin/conflicts` -> `ConflictListResponse`.
- User action: deschide conflictul, vede sursele opuse și decide escaladarea la research.
- Required fields: `claim_id`, surse implicate, teritoriu, effective dates, regulile consumatoare, severitate.
- Risk if missing: UI publică poate afișa conținut normativ neverificat sau contradictoriu.
- Acceptance criteria: orice conflict critic apare ca element triabil și se leagă de event-urile afectate.

## 4. Freshness status
- Purpose: să urmărească staleness-ul pentru claim-uri și reguli după politica din `freshness_policy.yaml`.
- Data source yaml/db table if known: `source_claims.yaml`, `rules.yaml`, `freshness_policy.yaml`, țintă DB: `content.claims`, `content.rule_sets`.
- User action: prioritizează re-review-ul și blochează publicarea când apare expiry critică.
- Required fields: `freshness_class`, `review_after_days`, `hard_expiry_after_days`, `review_due_at`, `hard_expiry_at`.
- Risk if missing: traseele pot părea verzi deși sursele critice au expirat.
- Acceptance criteria: claims critice expirate apar instant ca blockere și nu pot fi publicate fără intervenție umană.

## 5. Certification verdict per event
- Purpose: să arate starea finală `go` / `conditional_go` / `no_go` / `not_checked` pe fiecare event.
- Data source yaml/db table if known: `research/inbox/<event>/*`, `app_readiness/r1_event_readiness_matrix.md`; în viitor `content.rule_sets` + output de certification.
- User action: sortează event-urile după blocaj și trimite clar la lane-ul corect (`research`, `data`, `product`, `code`).
- Required fields: `event_id`, `certification_verdict`, `blocker_summary`, `next_action`, `linked intents`.
- Risk if missing: echipa nu știe ce poate intra în preview și ce trebuie oprit complet.
- Acceptance criteria: matricea poate fi filtrată după wave, categorie, verdict și owner lane.

## 6. Publish readiness
- Purpose: să decidă dacă un ruleset poate intra în `publish_db` și cu ce garduri.
- Data source yaml/db table if known: `rules.yaml`, `source_claims.yaml`, `POST /v1/admin/rulesets/publish` -> `PublishRulesetRequest` / `RulesetResponse`; target DB: `content.rule_sets`.
- User action: selectează scope, approval ids și, dacă e cazul, confirmă explicit `conditional_go` conform ADR-016.
- Required fields: `scope`, `rule_revision_ids`, `manifest_sha256`, `approval_ids`, `status`, `published_at`.
- Risk if missing: publicarea poate încălca cerința de two-person approval sau poate promova conținut `no_go`.
- Acceptance criteria: `publisher` nu se poate auto-aproba și `conditional_go` cere acțiune explicită separată.

## 7. Rule trace
- Purpose: să lege un output din app de regulile și claim-urile care l-au produs.
- Data source yaml/db table if known: `rules.yaml`, `source_claims.yaml`, `CaseResponse.resolution_trace`, `JourneyResponse`, target DB per ADR-017: `app.journeys.resolution_snapshot` / `resolution_trace`.
- User action: inspectează `included_rule_ids`, `excluded_rule_ids`, `facts_hash`, `engine_version`, `ruleset_version`.
- Required fields: `canonical_rule_id`, `source_claim_ids`, `included_rule_ids`, `excluded_rule_ids`, `facts_hash`, `engine_version`, `ruleset_version`.
- Risk if missing: nu mai există explainability sau auditability pentru un traseu afișat userului.
- Acceptance criteria: dintr-un caz sau journey concret poți reconstrui ce reguli au produs pașii și warning-urile.

## 8. Event template preview
- Purpose: să previzualizeze exact ce vede userul în app pentru pași și documente.
- Data source yaml/db table if known: `templates.yaml`, `app_readiness/mobile_copy/r1_mobile_copy_pack.yaml`.
- User action: verifică primul pas, documentele estimate, empty states și etichetele de status înainte de release.
- Required fields: `step_templates`, `requirement_templates`, `status_label_ro`, `warning_label_ro`, `empty_or_blocked_state`.
- Risk if missing: app-ul poate fi tehnic verde, dar textul util pentru utilizator să fie gol sau vag.
- Acceptance criteria: pentru fiecare event cu `templates.yaml` există preview lizibil și fără copy comercială.

## 9. Official channel verification
- Purpose: să confirme că link-urile și canalele atașate rămân oficiale și teritoriale.
- Data source yaml/db table if known: `source_claims.yaml`, `rules.yaml` cu `attach_channel`, `GET /v1/official-channels` (din OpenAPI), target DB: `content.sources` / `content.rule_sets`.
- User action: validează publisher-ul, canonical URL și relația cu teritoriul.
- Required fields: `channel_id`, `publisher`, `canonical_url`, `territory_ids`, `authority_level`, `status`.
- Risk if missing: route-ul poate trimite userul către un canal greșit sau neoficial.
- Acceptance criteria: orice canal din preview are publisher verificabil și poate fi retras rapid dacă devine invalid.

## 10. Data gap triage
- Purpose: să transforme gap-urile în backlog executabil pe lane-ul corect.
- Data source yaml/db table if known: `app_readiness/gaps/r1_app_data_gaps.md`, `GET /v1/admin/gaps` -> `GapListResponse`, `codex/TASK_BACKLOG.yaml`.
- User action: etichetează owner lane, severitate și următoarea acțiune; trimite către research/data/code/product.
- Required fields: `gap_id`, `event_id`, `severity`, `source_file`, `problem`, `recommended_fix`, `owner_lane`.
- Risk if missing: echipa repară orb sau dublează munca între content, product și code.
- Acceptance criteria: fiecare gap critic are owner lane și next action clar, fără să fie „rezolvat” prin presupunere locală.
