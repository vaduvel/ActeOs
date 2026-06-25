# Deep Research Brief — Carte de identitate în Timișoara

## Event

`ro.life.identity_card_expired / lost / stolen / change_address`

## Territory and reference

România → Timiș → Timișoara. Cercetarea trebuie să precizeze data de referință și să nu amestece ani/perioade.

## Scope variants

- expirare, pierdere, furt, deteriorare, domiciliu, nume, minor/adult
- CEI vs CIS unde este aplicabil
- programare, acte, originale/copii, taxe
- proprietar/chiriaș/primire în spațiu
- dovada furtului/pierderii
- canale și competență teritorială

## Official source targets

- DGEP/MAI/HUB MAI
- SPCLEP Timișoara
- legislatie.just.ro

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
