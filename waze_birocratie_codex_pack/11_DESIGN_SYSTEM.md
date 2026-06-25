# Design system și content design

## 1. Direcție vizuală

Calm, competent, modern, fără aspect de portal administrativ. Interfața trebuie să reducă anxietatea și să evidențieze acțiunea, nu ornamentul.

## 2. Tokens

```text
color.bg.default        #F3F6FA
color.surface.default   #FFFFFF
color.surface.subtle    #EAF0F7
color.border.default    #DDE5EF
color.text.primary      #102033
color.text.secondary    #607086
color.brand.primary     #315FDA
color.brand.onPrimary   #FFFFFF
color.success           #237A52
color.warning           #B86A00
color.danger            #C33D4A
color.info              #315FDA
radius.sm               8
radius.md               14
radius.lg               20
space.unit              4dp
```

Contrastul se verifică WCAG 2.2 AA; tokens se ajustează dacă nu trec.

## 3. Tipografie

- Headings: Space Grotesk sau fallback sans-serif;
- Body: Inter sau font sistem;
- Android Dynamic Type/font scale până la 200%;
- body minim 16sp;
- line-height generos;
- fără text critic doar în uppercase.

Nu se distribuie font files în repository dacă licența nu este documentată; buildul poate folosi fonturi prin mecanism legal sau fallback.

## 4. Componente

- IntentSearchField
- JourneyCard
- NextActionCard
- TimelineStep
- RequirementRow
- ReadinessProgress
- ConfidenceBadge
- SourceEvidenceSheet
- FindingCard
- DeadlineChip
- OfficialChannelButton
- RecalculationDiff
- EmptyState
- ErrorSummary
- PrivacyNotice
- CuratorDiffViewer
- PredicateBuilder
- ClaimEvidencePanel

## 5. Semantica statusurilor

Culoarea nu este singurul indicator. Fiecare status are icon și text.

- Gata formal — check + text;
- Atenție — triangle + text;
- Blocat — stop + text;
- Necesită confirmare — question + text;
- Expirat — clock/stop + text;
- Conflict — split arrows + text.

## 6. Content design

- propoziții scurte;
- verb la început;
- termenul juridic urmat de explicație;
- evităm „neconform”; spunem exact problema;
- evităm „succes” înainte de confirmarea instituției;
- diferențiem „poți depune”, „dosar complet formal” și „acceptat”.

### Lexicon canonic

- „traseu” — călătoria completă;
- „pas” — acțiune;
- „cerință” — document/dată/taxă;
- „dosar pregătit formal” — toate verificările noastre au trecut;
- „confirmat de instituție” — există dovadă externă;
- „necesită confirmare” — produsul nu are bază suficientă.

## 7. Microcopy interzis

- „Garantat acceptat”;
- „Document autentic” fără registry;
- „Șanse 87%” fără model validat și disclaimer;
- „Totul este în regulă” dacă există gaps;
- „AI a decis”.

## 8. Accesibilitate

- TalkBack labels complete;
- touch targets min 48dp;
- focus order logic;
- error summary și mesaje lângă câmp;
- haptic opțional, nu unic;
- reduce motion;
- contrast și high contrast mode;
- export/print checklist pentru ajutor familial;
- text simplu și posibilitate de citire audio.

## 9. Ecrane curator

Portalul nu sacrifică rigoarea pentru frumusețe. Diff-ul trebuie să arate:

- sursa veche/nouă;
- claim afectat;
- regula afectată;
- utilizatori/trasee potențial afectate;
- teste schimbate;
- butoane approve/reject cu motiv obligatoriu.
