===
# Gaps — ro.life.vehicle_registration

| ID | Subiect | Status | De confirmat | Sursa oficială țintă | Comportament motor |
|---|---|---|---|---|---|
| `VREG-G1` | Disponibilitatea serviciilor online | `needs_confirmation` | operațiunile integral online și condițiile de cont pentru fiecare caz | DGPCI | Emite online_service_availability_for_case în afara transcrierii confirmate local. |
| `VREG-G2` | Documente vamale pentru stat terț | `needs_confirmation` | forma documentelor vamale și dovada plății/scutirii | Autoritatea Vamală Română | Emite customs_document_set. |
| `VREG-G3` | Canale locale în afara pilotului | `verified_with_local_gap` | programarea, sediul și excepțiile județului | prefectura competentă | Emite local_channel_outside_pilot. |
| `VREG-G4` | Sancțiunile pentru depășirea celor 90 de zile | `needs_confirmation` | efectele și sancțiunile actuale, separat de termenul procedural | legislatie.just.ro / Poliția Română / DGPCI | Marchează termenul și overdue, fără a inventa amendă. |

## Reguli de publicare

- `needs_confirmation`: nu devine fapt și nu produce o obligație fermă fără sursă oficială directă.
- `verified_with_local_gap`: baza națională rămâne utilizabilă, dar canalul/documentația locală se confirmă pentru UAT-ul concret.
- `conflicting`: efectul critic este blocat până la soluționarea contradicției prin revizie umană.

===
