===
# Gaps — ro.life.temporary_vehicle_authorisation

| ID | Subiect | Status | De confirmat | Sursa oficială țintă | Comportament motor |
|---|---|---|---|---|---|
| `TVA-G1` | Expirarea RCA în excepția de 5 zile | `needs_confirmation` | data exactă până la care poate fi emisă autorizația | polița RCA / SPCRPCIV | Emite rca_expiry_limits_five_day_authorisation. |
| `TVA-G2` | Certificatul temporar dealer/leasing | `needs_confirmation` | dacă cerința tranzitorie mai este activă și forma documentului | DGPCI / SPCRPCIV | Emite seller_temporary_authorisation_history_certificate. |
| `TVA-G3` | Costul exact al plăcuțelor provizorii | `needs_confirmation` | tipul de plăcuță și totalul datorat | DGPCI / SPCRPCIV | Afișează separat tariful de 13 lei și nu calculează totalul. |
| `TVA-G4` | Canale locale în afara pilotului | `verified_with_local_gap` | programarea și modul de eliberare | prefectura județului competent | Emite local_channel_outside_pilot. |

## Reguli de publicare

- `needs_confirmation`: nu devine fapt și nu produce o obligație fermă fără sursă oficială directă.
- `verified_with_local_gap`: baza națională rămâne utilizabilă, dar canalul/documentația locală se confirmă pentru UAT-ul concret.
- `conflicting`: efectul critic este blocat până la soluționarea contradicției prin revizie umană.

===
