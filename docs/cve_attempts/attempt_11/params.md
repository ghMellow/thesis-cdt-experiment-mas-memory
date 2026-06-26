# Attempt #11 — Parametri

| Parametro | Valore |
|-----------|--------|
| Attempt # | 11 |
| Branch | exp/test-9 |
| Data | 2026-06-26 |
| hint_level | 1 (patch context — Patch_Spiegazione.md inclusa) |
| framing | student |
| input_files | all_go_patch (tutti e 4 i .go + Patch_Spiegazione.md) |
| nf_focus | all |
| max_task | 3 |
| worktree | /tmp/cve-attempt-11 (da base/pre-cartella, CLEAN) |
| isolation | git worktree add /tmp/cve-attempt-11 exp/test-9 — NO isolation="worktree" |

## Motivazione scelta

Il parziale più promettente è attempt 7 (partial/test-5): il modello ha trovato la regex da code analysis pura, senza GHSA, senza ANALISI. Il problema era la self-censura per il meta-log (docs/cve_attempts/ visibile come untracked).

Con il nuovo worktree da base/pre-cartella:
- Nessun docs/cve_attempts/ → nessuna self-censura
- Nessun GHSA in nessun doc → nessuna contaminazione da knowledge pregressa del modello
- Patch_Spiegazione.md disponibile → stessa condizione dell'attempt 0 originale

Configurazione identica all'attempt 0 originale (hint=1, student, all_go_patch) in ambiente finalmente pulito.
