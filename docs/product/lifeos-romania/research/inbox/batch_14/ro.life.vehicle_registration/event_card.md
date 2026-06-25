===
# Event Card — ro.life.vehicle_registration

| Câmp | Valoare |
|---|---|
| `batch_id` | `B14_VEHICLE_REGISTRATION` |
| `alias_event_type_id` | `ro.life.vehicle_registration` |
| `event_type_id` | `life.vehicle_registration` |
| `title_ro` | Vreau să înmatriculez sau să transcriu un vehicul |
| `category_id` | `vehicles_mobility` |
| `reference_date` | `2026-06-25` |
| `geographic_scope` | național; pilot local Timiș / Timișoara |
| `publication_status` | `research_inbox_pending_snapshot_and_human_review` |

## Declanșator

Utilizatorul urmărește prima înmatriculare ori transcrierea proprietății și trebuie clasificat în cazul procedural corect.

## Fapte de rutare

| Fact | Tip | Semnificație |
|---|---|---|
| `registration_case` | `enum` | new_domestic | new_imported | used_imported | ownership_transcription |
| `applicant_county` | `string` | TM pilot |
| `representation_type` | `enum` | self | lawyer | authorized_individual | company_delegate |
| `ownership_document_registered_local_tax` | `boolean` | cerință fiscală pentru dobândire |
| `submission_mode` | `enum` | counter | online |
| `acquisition_date` | `date|null` | ancoră pentru termenul de 90 zile la transcriere |

## Rezultat urmărit

Este selectat cazul corect, dosarul este pregătit și operațiunea este depusă la serviciul competent.

## Afirmații și reguli

| Element | Număr |
|---|---:|
| source claims | 17 |
| reguli deterministe | 28 |
| golden fixtures | 22 |
| gaps explicite | 4 |

## Acoperire verificată

- Motorul separă patru cazuri: nou intern, nou importat, uzat importat și transcriere.
- Termenul verificat pentru transcriere este 90 de zile de la dobândire.
- Regula fiscală Timiș diferă între ghișeu și transcriere online.

## Limitări controlate

- Serviciile online nu sunt presupuse pentru toate operațiunile.
- Sancțiunile pentru întârziere și documentele vamale exacte rămân needs_confirmation.

## Politica de adevăr

- Nicio taxă, listă de acte, competență sau termen nu este activat fără `source_claim_ids`.
- O informație locală din afara pilotului Timiș/Timișoara produce confirmare, nu extrapolare.
- Un gap juridic ori operațional rămâne vizibil și nu este convertit automat în cerință obligatorie.

===
