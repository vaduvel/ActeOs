# Event Card — ro.life.identity_card_expired (life.id_card_expired)

**Batch:** R1A-3  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Îmi expiră / mi-a expirat cartea de identitate".

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `id_card_type` | enum | `buletin`, `ci_simpla`, `cei` |
| `expiry_date` | date | data expirării înscrisă în act |
| `has_all_documents` | boolean | are toate actele de stare civilă + dovada adresei |

## Reguli cheie (verificate)

- Solicitare act nou în fereastra **[expirare − 180 zile, expirare − 15 zile]** (OUG 97/2005, art. 19 alin. 2 lit. a). Critic.
- Vechiul act se păstrează până la emiterea noului; se predă la ridicare.
- Dacă lipsesc documente → carte de identitate **provizorie** (art. 20 alin. 1 lit. a), valabilă 30 zile–1 an.

## Conflict deschis (nu se ascunde)

Cuantum sancțiune contravențională: surse oficiale divergente — **40–80 lei** (majoritar) vs **500–1000 lei** (EVP Arad). Status `conflicting`; afișăm ambele + `needs_confirmation`, nu alegem una.

## Canale (Timișoara)

Programare prin `https://hub.mai.gov.ro/cei/programari/create?judet=TM`; DEP Timișoara L–V 08:00–16:00.
