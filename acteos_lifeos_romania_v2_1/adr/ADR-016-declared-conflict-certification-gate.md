# ADR-016 — Gate de certificare pentru regulile care declară conflicte (conditional_go)

- **Status:** Accepted
- **Date:** 2026-06-26
- **Owners:** Product + Architecture

## Context

ADR-004 (conținut evidence-gated) și ADR-010 (niciun conflict rezolvat silențios) cer ca o regulă **critică** care afirmă conținut normativ pe baza unui claim neverificat sau în conflict să fie blocată la certificare.

În piloții R1 (`identity_card_expired`, `identity_card_lost`) au apărut însă reguli al căror **scop chiar este** să declare un conflict — de ex. „actul vechi rămâne valabil vs. obligația de preschimbare” sau conflictul de sancțiune. Aceste reguli nu afirmă conținut: emit doar efecte de declarare/avertizare (`block`, `require_confirmation`, `flag_conflict`, plus `emit_warning`/`emit_advice` advisory) și citează tocmai claim-ul contrazis. Gate-ul inițial le trata identic cu regulile content-asserting → `no_go` fals, deși comportamentul lor este exact cel dorit de ADR-010: expun conflictul, nu îl ascund.

## Decision

Certificarea distinge **regulile de declarare a conflictului** de cele care **afirmă conținut**:

- `CONFLICT_DECLARATION_EFFECT_TYPES = {block, require_confirmation, flag_conflict}`;
- `CONTENT_ASSERTING_EFFECT_TYPES = NORMATIVE_EFFECT_TYPES − CONFLICT_DECLARATION_EFFECT_TYPES`;
- o regulă critică este *conflict-declaration* dacă are **cel puțin un** efect de declarare, **niciun** efect content-asserting (efectele advisory `emit_warning`/`emit_advice` sunt permise) și citează claim-ul contrazis;
- o astfel de regulă pe un claim în conflict / neverificat produce **warning `CRITICAL_CONFLICT_DECLARED`** și certificare **`conditional_go`** (nu `no_go`);
- o regulă care **afirmă conținut** pe un claim neverificat rămâne **hard-block** (`no_go`), conform ADR-004 și ADR-010.

`publish_db` acceptă `conditional_go` doar sub flag explicit (`--allow-conditional`). `certification.py` **nu** se editează per-pilot: un `no_go` rămas înseamnă fie date greșite (claim marcat eronat), fie o regulă care chiar trebuie să blocheze — ambele se raportează în lane-ul de research, nu se „repară” slăbind gate-ul.

## Consequences

- Piloții cu reguli de declarare a conflictului certifică `conditional_go` și pot fi publicați controlat, fără a slăbi garanția ADR-010 (conflictele rămân expuse explicit, nu rezolvate silențios).
- Regulile content-asserting pe surse neverificate continuă să blocheze livrarea.
- Distincția este testată în engine (`test_certification.py`) și devine criteriu standard pentru toate frunzele R1.

## Revisit triggers

- apar dovezi măsurabile că decizia blochează SLO, securitatea sau livrarea;
- contracte publice ori obligații legale schimbă premisele;
- costul operațional depășește beneficiul demonstrat;
- un înlocuitor este probat prin benchmark și plan de migrare.
