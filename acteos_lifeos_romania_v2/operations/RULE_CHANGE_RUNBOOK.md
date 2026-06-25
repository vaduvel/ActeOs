# Runbook — schimbare de regulă

1. Detectorul sau curatorul deschide `source_change` cu diff și impact estimat.
2. Se creează snapshot nou fără a suprascrie versiunea veche.
3. Se atomizează claim-urile modificate; cele vechi devin superseded numai după confirmare.
4. Se generează draft rule revision.
5. Se rulează static validation, conflict detection, unit fixtures și impact simulation pe cazurile active.
6. Reviewerul independent aprobă, respinge sau cere clarificare.
7. Publisherul creează ruleset imutabil și staged rollout.
8. Se monitorizează erori, recalculări și feedback de respingere.
9. La anomalie: se oprește rolloutul sau se revine la rulesetul anterior; auditul rămâne intact.
10. Utilizatorii afectați primesc notificare numai dacă schimbarea le modifică traseul și au consimțit.
