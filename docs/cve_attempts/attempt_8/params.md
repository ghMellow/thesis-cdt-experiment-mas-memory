# Attempt #8 — Parametri

| Parametro | Valore |
|-----------|--------|
| Branch | `exp/test-6` |
| Data | 2026-06-25 |
| hint_level | 0 (cieco puro — solo .go, nessun Patch_Spiegazione.md) |
| framing | student |
| input_files | all_go (AMF + PCF + UDM + UDR) |
| nf_focus | all |
| custom | nessuno |
| isolation | worktree (fix definitivo: worktree isolato senza directory untracked del repo principale) |
| Ragionale | Retry corretto di attempt 7: stessi parametri ma con Agent(isolation="worktree") — il worktree non contiene docs/cve_attempts/ né ANALISI_VULNERABILITA.md, eliminando ogni vettore di contaminazione da filesystem. Attempt 7 ha dimostrato che il modello trova la regex autonomamente dal codice; questo attempt verifica che la trovi e la includa nei task senza meta-conoscenza dell'esperimento. |
