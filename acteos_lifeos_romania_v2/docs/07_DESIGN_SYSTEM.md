# 07 — Design System

## 1. Direcție

ActeOS trebuie să pară calm, precis și contemporan. Nu arată ca un portal de stat și nici ca o aplicație fintech agresivă. Interfața pune accent pe următoarea acțiune, încredere și progres verificabil.

## 2. Tokens de referință

Sursa machine-readable: `contracts/design_tokens.json`.

### Culoare

- `bg.canvas`: `#F3F6FA`
- `bg.subtle`: `#EAF0F7`
- `surface.primary`: `#FFFFFF`
- `surface.elevated`: `#FFFFFF`
- `border.default`: `#DDE5EF`
- `text.primary`: `#0F1B2D`
- `text.secondary`: `#5E6B80`
- `brand.primary`: `#315FD6`
- `brand.strong`: `#2449A8`
- `status.success`: `#18794E`
- `status.warning`: `#9A6700`
- `status.danger`: `#C4323B`
- `status.info`: `#315FD6`

Statusurile folosesc background tint și text cu contrast verificat; nu afișăm text alb pe culori deschise.

### Spațiere

Grid de 4: `4, 8, 12, 16, 20, 24, 32, 40, 48, 64`.

### Radius

- control: 12;
- card: 16;
- modal/sheet: 20;
- pill: 999.

### Elevation

Umbre discrete. Border-ul definește majoritatea cardurilor. Nu folosim umbre masive sau efect „umflat 2021”.

### Tipografie

- UI: Inter sau fontul sistemului dacă performanța/limba o cer;
- display/brand: Space Grotesk opțional;
- cifre/date: tabular numerals;
- body mobile minimum 16 px echivalent;
- legal/source excerpts minimum 14 px și extensibile.

## 3. Componente obligatorii

- `AppShell`;
- `EventInput`;
- `EventCandidateCard`;
- `QuestionCard`;
- `JourneyHeader`;
- `NextActionCard`;
- `TimelineStep`;
- `RequirementCard`;
- `ReadinessBadge`;
- `TrustStateBanner`;
- `DeadlineChip`;
- `OfficialChannelCard`;
- `SourceClaimSheet`;
- `DocumentScanCard`;
- `RecoveryActionPanel`;
- `ChangeSinceLastVisit`;
- `OfflineBanner`;
- `SensitiveDataNotice`;
- `PartnerOptionCard` cu disclosure;
- admin: `DiffViewer`, `ClaimEditor`, `RuleBuilder`, `SimulationPanel`, `PublishGate`.

## 4. State matrix

Fiecare componentă interactivă are: default, pressed, focus-visible, disabled, loading și error. Cardurile de cerință au: missing, provided, needs_review, ready, expired, rejected și not_applicable.

## 5. Motion

- 150–220 ms pentru tranziții funcționale;
- spring moderat pentru sheet-uri;
- fără celebrare excesivă la pași intermediari;
- reduced motion elimină parallax, scale și tranziții non-esențiale;
- schimbarea de ruleset este explicată, nu mascată prin animație.

## 6. Iconografie

Iconurile completează textul. Nu folosim iconuri singure pentru status sau acțiuni administrative ambigue. Instituțiile nu sunt reprezentate prin logo-uri neautorizate; folosim categorii neutre și linkuri oficiale.

## 7. Dark mode

Nu este gate R1. Tokens sunt pregătite semantic, dar dark mode intră numai după audit complet de contrast, document preview și status colors.

## 8. Design QA

- toate ecranele la 320 px lățime și text 200%;
- iOS și Android, inclusiv edge-to-edge;
- VoiceOver/TalkBack;
- contrast automat + review manual;
- capturi pentru state-urile critical/conflicting/offline;
- design tokens consumate din pachet comun, nu duplicate.
