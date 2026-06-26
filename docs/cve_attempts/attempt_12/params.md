# Attempt #12 — Parametri

| Parametro | Valore |
|-----------|--------|
| Attempt # | 12 |
| Branch | exp/test-10 |
| Data | 2026-06-26 |
| hint_level | 1 (patch context — Patch_Spiegazione.md inclusa) |
| framing | student |
| input_files | all_go_patch |
| nf_focus | all |
| max_task | 3 |
| clone | /tmp/cve-attempt-12 (--single-branch base/pre-cartella, CLEAN) |

## Novità rispetto a attempt_11

- Clone isolato: `origin/main` inesistente nel clone → impossibile `git show main:task9`
- Vincolo comportamentale nel prompt: divieto esplicito di git show/fetch/log --all
- Unica contaminazione residua possibile: training data del modello (free5GC pubblico su GitHub)
