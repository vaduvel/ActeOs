# Provenanță și rezolvarea conflictelor (fuziune în super-book)

Acest document fixează **un singur adevăr** acolo unde cele două surse difereau.

## Surse fuzionate

- **A. Workbook de continuitate** (`docs/product/lifeos-romania/`, acest director): model determinist matur, orchestrator eveniment→graf cu `depends_on` și `event_plan_hash`, `19_SOURCE_REGISTRY.json` cu surse oficiale **verificate real**, ADR-001…021.
- **B. Pachet GPT 5.5 Pro** (`lifeos_romania_codex_pack_v1/`): schelet buildabil — OpenAPI, `10_DATABASE_SCHEMA.sql`, `contracts/*.schema.json`, `config/*.yaml`, `seed/*.yaml`, `13_BACKLOG.yaml`, faze P0–P12, EventSession state machine, Event Resolver boundaries.

## Decizii de fuziune

| # | Tema | Conflict | Decizie canonică |
|---|------|----------|------------------|
| M1 | Acasă canonică | două directoare | `docs/product/lifeos-romania/` este unicul adevăr; `lifeos_romania_codex_pack_v1/` devine arhivă deprecată cu pointer |
| M2 | Stack mobil | B propune React Native Expo; A/original folosesc Android nativ | **Android nativ Kotlin/Compose** (ADR-001 + ADR-022). RN respins ca s-ar arunca munca existentă |
| M3 | Demo vs producție | B e demo-first (`demo_mode: true`) | **Producție**. `demo_mode` doar fixture de test marcat; default `false` (ADR-023) |
| M4 | ID-uri evenimente/obligații | A: `ro.life.move_residence` / `ro.identity.id_card.address_change`; B: `life.moved` / `identity.change_domicile` | Se adoptă convenția B (`life.*`, `<domain>.<action>`) deja cablată în seed/contracte/DB. Descompunerea bogată din A se re-exprimă pe ea (ADR-024) |
| M5 | Tier-uri | B refolosește A/B/C și pentru frecvență și pentru freshness | **Frecvență = high/medium/low**; **clase de freshness = A/B/C** (critical/operational/explanatory). Fără coliziune (ADR-025) |
| M6 | Graf de dependențe | B are `related_obligations` plată; A are `depends_on` + detecție cicluri + `event_plan_hash` | Se păstrează orchestratorul din A; taxonomia/seed-ul capătă `depends_on` |
| M7 | Surse | B are doar research briefs („du-te și găsește"); A are URL-uri oficiale verificate | `19_SOURCE_REGISTRY.json` din A devine coloana reală; briefs-urile B rămân ca task-uri de curatoriere |
| M8 | Motor | B: operatori predicat + state machine; A: algoritm resolve + canonicalizare + freshness | Se unesc în `05_RULE_ENGINE_SPEC.md` (operatori B + algoritm A + orchestrator A) |
| M9 | Confidență | identice (verified…expired/conflicting) | păstrate ca atare; se adaugă `withdrawn` din A |

## Maparea ID-urilor (A → canonic)

- `ro.life.move_residence` → `life.moved`
- `ro.life.buy_used_car` → `life.bought_vehicle`
- `ro.life.child_born` → `life.child_born`
- `ro.life.lost_documents` → `life.lost_documents`
- `ro.life.id_card_expired` → `life.id_expiring`
- `ro.identity.id_card.address_change` → `identity.change_domicile`
- `ro.auto.registration_certificate.address_update` → `vehicle.update_registration_address`
- `ro.auto.ownership.transfer_contract` → `vehicle.transcribe_ownership`
- `ro.tax_local.vehicle.declare` → `local_taxes.register_vehicle`
- `ro.tax_local.fiscal_certificate.*` → `local_taxes.request_certificate`
