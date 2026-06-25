# Deep Research Brief — Pierderea sau furtul unui set de documente

## Event

`ro.life.lost_all_documents / documents_stolen_bundle`

## Territory and reference

România → Timiș → Timișoara. Cercetarea trebuie să precizeze data de referință și să nu amestece ani/perioade.

## Scope variants

- ordine de prioritate și limitarea riscului
- CI, permis, talon, pașaport, card sănătate și bancar ca subtrasee
- furt vs pierdere
- documente temporare și identitate fără act
- situația în România vs străinătate
- canale anti-fraudă oficiale

## Official source targets

- MAI/DGEP/DGPCI
- MAE/consulate
- CNAS
- Poliția Română
- bănci doar pentru propriile proceduri oficiale

## Required model

Pentru fiecare variantă: facts, gates, steps, requirements, deadlines, official channels, source claims, freshness, conflicts și gaps. Fiecare step răspunde: ce fac / până când / ce îmi trebuie / cum știu că e gata / ce fac dacă eșuează.

## Critical constraints

- citează exact și atașează locator;
- un claim per obligație independentă;
- marchează explicit practica locală nepublicată ca gap;
- nu deduce obligații conexe doar pentru că „de obicei” sunt făcute;
- integrarea este `DEEP_LINK` până la dovada accesului tehnic și contractual;
- rezultatul intră în `research/inbox`, nu direct în production.

## Output

Urmează integral `research/RESEARCH_BRIEF_TEMPLATE.md` și JSON Schemas din `contracts/jsonschema/`.
