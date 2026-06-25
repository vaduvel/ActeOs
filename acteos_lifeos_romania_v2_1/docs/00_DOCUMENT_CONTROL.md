# 00 — Controlul documentului

| Câmp | Valoare |
|---|---|
| Produs | ActeOS / LifeOS România |
| Versiune documentație | 2.1.0 |
| Data | 2026-06-25 |
| Limba canonică | ro-RO |
| Timezone canonic de produs | Europe/Bucharest |
| Stare | baseline executabil pentru bootstrap |
| Proprietar decizie produs | Founder / Product Owner |
| Proprietar reguli | Content & Policy Operations |
| Proprietar arhitectură | Tech Lead |

## Scop

Acest pachet definește produsul până la nivelul la care un agent de cod poate executa controlat: domeniu, limite, contracte, stări, erori, securitate, testare, date, release gates și operațiuni. Nu înlocuiește research-ul administrativ. Research-ul produce claim-uri; documentația definește cum sunt transformate în reguli publicabile.

## Ierarhia documentelor

1. `PRODUCT_DOCTRINE` prevalează asupra backlogului.
2. OpenAPI și JSON Schemas prevalează asupra exemplelor prose pentru contracte.
3. ADR-urile acceptate prevalează asupra descrierii arhitecturale mai vechi.
4. Ruleset-ul publicat și claim-urile sale prevalează asupra seedurilor de dezvoltare.
5. O regulă critică expirată nu poate fi reactivată de cache sau copy.

## Managementul schimbării

- schimbare de doctrină: major version;
- schimbare incompatibilă API/schema: major version contract;
- schimbare de comportament resolver compatibilă: minor version;
- corecție de text/documentație: patch version;
- schimbare administrativă: nouă `rule_revision`, nu neapărat release de aplicație.

## Termeni de stare

- `draft`: nepublicabil;
- `in_review`: evaluare umană în curs;
- `approved`: validat, dar încă neinclus într-un ruleset activ;
- `active`: servit în producție;
- `stale`: peste review due, încă utilizabil doar conform politicii;
- `hard_expired`: blocat pentru afirmații critice;
- `conflicting`: surse active incompatibile;
- `withdrawn`: retras explicit;
- `superseded`: înlocuit de o revizie nouă.
