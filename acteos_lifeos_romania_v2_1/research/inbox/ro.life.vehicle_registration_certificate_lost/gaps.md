===
# Gaps — ro.life.vehicle_registration_certificate_lost

| ID | Subiect | Status | De confirmat | Sursa oficială țintă | Comportament motor |
|---|---|---|---|---|---|
| `VCL-G1` | Canalul efectiv al autorității emitente | `verified_with_local_gap` | în afara Timișului, dacă autoritatea emitentă acceptă serviciul online și ce flux local folosește | SPCRPCIV emitent / DGPCI | Timiș online și ghișeu sunt modelate separat; în alte județe emite local_channel_outside_pilot. |
| `VCL-G2` | Situații în afara celor patru motive | `needs_confirmation` | încadrarea documentului distrus, inaccesibil sau nerecuperat în alte împrejurări | DGPCI | Emite certificate_replacement_reason. |
| `VCL-G3` | Termenul de eliberare/livrare | `needs_confirmation` | durata și modalitatea de primire a noului certificat | DGPCI / SPCRPCIV emitent | Nu promite o durată. |
| `VCL-G4` | Documente străine | `needs_confirmation` | forma acceptată pentru dovada încetării motivului reținerii | SPCRPCIV emitent | Păstrează cerințele generale și nu inventează formularul. |

## Reguli de publicare

- `needs_confirmation`: nu devine fapt și nu produce o obligație fermă fără sursă oficială directă.
- `verified_with_local_gap`: baza națională rămâne utilizabilă, dar canalul/documentația locală se confirmă pentru UAT-ul concret.
- `conflicting`: efectul critic este blocat până la soluționarea contradicției prin revizie umană.

===
