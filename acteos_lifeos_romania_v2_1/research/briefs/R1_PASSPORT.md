# Deep Research Brief — Pașaport adult și minor în Timiș

## Event

`ro.life.passport_first_or_renew / minor_passport`

## Territory and reference

România → Timiș → Timișoara. Cercetarea trebuie să precizeze data de referință și să nu amestece ani/perioade.

## Scope variants

- adult/minor și acorduri
- temporar/electronic unde se aplică
- taxe, programare, acte și ridicare
- pierdere/furt separat
- domiciliu în străinătate separat

## Official source targets

- Direcția Generală de Pașapoarte
- Serviciul Pașapoarte Timiș
- MAI/HUB

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
