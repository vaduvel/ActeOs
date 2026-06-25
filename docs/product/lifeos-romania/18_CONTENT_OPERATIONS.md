# Operațiuni de conținut — LifeOS România

## Ciclul de curatoriere

1. Identifică sursa oficială (vezi `19_SOURCE_REGISTRY.json`).
2. Captează snapshot imutabil (URL + dată + sha256).
3. Extrage `SourceClaim` tipat cu citat și locator.
4. Doi curatori validează (two-person rule) → `verified`.
5. Leagă claim → `Rule` → `RuleBundle` → publicare.
6. Pentru evenimente: claim-uri și pentru includerea obligației și pentru fiecare `depends_on` critic.

## Priorități R1

- Auto + identitate (DRPCIV, pașapoarte, CEI, RAR) — vezi `research_briefs/`.
- Taxe locale Timișoara (DFMT, Primăria Timișoara).
- ANAF SPV, CNAS, beneficii (MMANPIS/AJPIS).

## Reguli

- Fără forum/blog ca sursă primară.
- Conflict → păstrează ambele claim-uri, marchează `conflicting`.
- Lacună locală → `verified_with_local_gap`, niciodată informație inventată.
