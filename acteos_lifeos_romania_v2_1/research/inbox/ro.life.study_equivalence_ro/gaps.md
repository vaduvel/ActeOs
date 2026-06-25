# Research gaps — ro.life.study_equivalence_ro

| gap_id | status | gap | impact | official_target | blocking |
|---|---|---|---|---|---|
| gap.eq.school_years_route | needs_confirmation | Procedura exactă pentru echivalarea claselor/foilor matricole I-XII și competența ISJ Timiș pe fiecare caz. | Ruta nu poate fi automatizată numai din pagina generală. | CNRED + ISJ Timiș | yes |
| gap.eq.non_romanian_applicant | needs_confirmation | Procedura exactă după cetățenie pentru solicitanți care nu sunt cetățeni români. | Nu se extrapolează paginile dedicate cetățenilor români. | CNRED — procedura dedicată categoriei de solicitant | yes |
| gap.eq.country_authentication | needs_confirmation | Matricea actuală pe state pentru apostilă, supralegalizare sau scutire. | Documentul poate fi respins dacă formalitatea este greșită. | CNRED + MAE/Convenția aplicabilă | yes |
| gap.eq.fee | needs_confirmation | Existența și cuantumul unei taxe pentru procedura și canalul exact. | Motorul nu afișează sumă sau cont. | pagina CNRED a procedurii + eventual ordin de taxe | yes |
| gap.eq.regulated_authority | needs_confirmation | Autoritatea competentă pentru profesia reglementată concretă. | Dosarul poate fi trimis la instituția greșită. | lista oficială a autorităților competente | yes |

## Conflict matrix

Nu există conflict între termenul de contestație de 45 de zile pentru bac și cel de 30 de zile pentru licență: sunt proceduri oficiale diferite și sunt modelate pe ramuri distincte.

## Geographic guard

Regulile naționale se aplică pe `ro`. Datele pilot sunt limitate la `ro.tm` / `ro.tm.timisoara`. Pentru orice alt UAT, rezultatul local este `verified_with_local_gap`; motorul nu reutilizează automat contacte, locuri, circumscriptii, taxe sau proceduri din Timișoara.
