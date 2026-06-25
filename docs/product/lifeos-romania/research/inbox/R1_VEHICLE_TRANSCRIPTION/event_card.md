# Event Card — ro.life.vehicle_transcription (life.vehicle_transcription)

**Batch:** R1A-veh4  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Trebuie să transcriu pe numele meu o mașină înmatriculată în România".

> Eveniment-document focalizat pe transcrierea dreptului de proprietate (Ordinul MAI 1501/2006, art. 8). Latura fiscală (declararea la taxe locale în 30 zile) este eveniment separat.

## Fapte cerute

| fact | tip | valori |
|---|---|---|
| `contract_date` | date | data contractului |
| `has_valid_itp` | boolean | ITP în termen |
| `has_valid_civ` | boolean | CIV valabil |
| `has_fiscal_proof` | boolean | dovada declarării fiscale la organul local |
| `keeps_old_plates` | boolean | păstrează numerele |

## Reguli cheie

- Transcrierea cere (art. 8, Ordinul 1501/2006): cererea, documentul de proprietate (orig+copie), **CIV valabil**, **ITP în termen**, dovada declarării fiscale la organul fiscal local.
- Termen orientativ **90 de zile** de la dobândire (în verificare față de textul exact al ordinului).
- Sursa primară: `https://legislatie.just.ro/Public/DetaliiDocument/77009`.

## Canale (Timișoara)

SPCRPCIV Timiș (`https://www.drpciv.ro`), programare `https://dgpci.mai.gov.ro/drpciv-booking/`.
