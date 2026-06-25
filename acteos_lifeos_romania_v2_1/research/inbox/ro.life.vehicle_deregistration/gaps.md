===
# Gaps — ro.life.vehicle_deregistration

| ID | Subiect | Status | De confirmat | Sursa oficială țintă | Comportament motor |
|---|---|---|---|---|---|
| `VDER-G1` | Dovada calității de moștenitor | `needs_confirmation` | documentul și regulile de reprezentare pentru unul sau mai mulți moștenitori | DGPCI / notar / instanță, după caz | Emite proof_of_legal_heir_capacity. |
| `VDER-G2` | Temeiuri atipice de radiere | `needs_confirmation` | încadrarea situațiilor din afara celor patru motive publicate | DGPCI / Ordinul MAI nr. 181/2024 | Emite deregistration_ground_eligibility. |
| `VDER-G3` | Radierea din oficiu | `needs_confirmation` | autoritatea inițiatoare, notificarea și efectele fiscale | DGPCI / UAT | Separă ruta ex_officio de cererea utilizatorului. |
| `VDER-G4` | Canale locale în afara Timișului | `verified_with_local_gap` | certificatul fiscal, programarea și canalul local | prefectura/UAT competent | Emite local_channel_outside_pilot. |

## Reguli de publicare

- `needs_confirmation`: nu devine fapt și nu produce o obligație fermă fără sursă oficială directă.
- `verified_with_local_gap`: baza națională rămâne utilizabilă, dar canalul/documentația locală se confirmă pentru UAT-ul concret.
- `conflicting`: efectul critic este blocat până la soluționarea contradicției prin revizie umană.

===
