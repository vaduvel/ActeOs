===
# Gaps — ro.life.vehicle_inheritance

| ID | Subiect | Status | De confirmat | Sursa oficială țintă | Comportament motor |
|---|---|---|---|---|---|
| `VINH-G1` | Documentul succesoral exact | `needs_confirmation` | documentul acceptat pentru dovedirea dreptului asupra vehiculului în speța concretă | notar / instanță / SPCRPCIV competent | Folosește cerința generică document_attesting_inherited_ownership; nu impune automat un formular anume. |
| `VINH-G2` | Data dobândirii pentru termenul de 90 zile | `needs_confirmation` | data juridică de la care curge termenul în succesiunea concretă | legislație succesorală / documentul succesoral / SPCRPCIV | Nu calculează termenul până la confirmarea datei. |
| `VINH-G3` | Co-moștenitori și partaj | `needs_confirmation` | atribuirea vehiculului, consimțământul și puterile de semnare | documentul succesoral / notar / instanță | Emite co_heir_consent_or_partition. |
| `VINH-G4` | Moștenitor minor | `needs_confirmation` | reprezentarea și autorizarea necesară pentru actul de dispoziție | instanța de tutelă / notar / legislație | Emite minor_heir_representation_and_authorisation. |
| `VINH-G5` | Vânzarea înainte sau după transcriere | `needs_confirmation` | traseul admis pentru situația succesorală, fiscală și contractuală concretă | SPCRPCIV / organ fiscal local / notar | Nu afirmă că transcrierea prealabilă este întotdeauna obligatorie sau inutilă. |
| `VINH-G6` | Canale locale în afara pilotului | `verified_with_local_gap` | documentele fiscale și programarea județului/UAT competent | prefectura și UAT-ul competent | Emite local_inheritance_vehicle_channel_outside_pilot. |

## Reguli de publicare

- `needs_confirmation`: nu devine fapt și nu produce o obligație fermă fără sursă oficială directă.
- `verified_with_local_gap`: baza națională rămâne utilizabilă, dar canalul/documentația locală se confirmă pentru UAT-ul concret.
- `conflicting`: efectul critic este blocat până la soluționarea contradicției prin revizie umană.

===
