# Event Card — ro.life.open_srl (life.open_srl)

**Batch:** B12_OPEN_SRL  
**Status:** research_inbox (neaprobat)  
**Pilot:** `ro.tm.timisoara`  
**Accessed_at:** 2026-06-25

## Declanșator

„Vreau să înființez un SRL.”

## Limita evenimentului

Acoperă constituirea și înmatricularea inițială a unui SRL. Nu acoperă alegerea regimului fiscal, contractarea contabilității, deschiderea contului bancar sau autorizările sectoriale post-înmatriculare.

## Fapte cerute

| fact | tip | valori / semnificație | obligatoriu |
|---|---|---|---|
| `founders_count` | `integer` | numărul asociaților fondatori | da |
| `subscribed_capital_ron` | `number` | capitalul social subscris | da |
| `real_estate_in_kind_contribution` | `boolean` | aport imobiliar în natură | condițional |
| `constitutive_act_date` | `date` | data actului constitutiv | da |
| `registered_office_is_dwelling` | `boolean` | sediu într-un condominiu | condițional |
| `activity_at_registered_office` | `boolean` | activitate efectivă la sediu | condițional |
| `beneficial_owner_data_in_constitutive_act` | `boolean` | datele beneficiarului real sunt incluse | da |
| `filing_actor` | `enum` | legal_representative, authenticated_proxy, lawyer, associate | da |
| `filing_channel` | `enum` | counter, post_courier, online | da |
| `capital_paid_percent` | `number` | procent vărsat după înmatriculare | post-eveniment |
| `local_commercial_agreement_applicable` | `boolean` | acord local aplicabil | condițional |

## Pași determinați

| step_id | rezultat | gate principal |
|---|---|---|
| `prepare_srl_constitution` | rezervare firmă și act constitutiv | formă, conținut, capital |
| `file_srl_registration` | înmatriculare la ONRC | termen, semnatar, canal |
| `pay_initial_share_capital` | vărsarea capitalului inițial | 30% și începerea operațiunilor |
| `pay_monitorul_oficial_publication_tariff` | achitarea notei de publicare | numai după admitere |
| `obtain_timisoara_commercial_agreement` | acord local pentru activitate | categoria comercială și amplasamentul |

## Reguli-cheie verificate

- Capitalul social minim al unui SRL nou este 500 lei din 18.12.2025.
- Cererea se depune, ca regulă, în 15 zile de la actul constitutiv.
- Cel puțin 30% din capital se varsă înaintea operațiunilor și în maximum trei luni.
- Tariful de publicare se achită după admiterea cererii.

## Canal pilot Timișoara / Timiș

Acordul comercial Timișoara este o procedură separată de înmatricularea SRL. Motorul nu presupune că orice cod CAEN îl declanșează și nu fixează taxa locală fără cazul selectat.

## Guvernanță

Lista exactă a documentelor se leagă de formularul și ghidul ONRC valabile la data depunerii. Regimul fiscal și autorizările sectoriale rămân evenimente copil.
