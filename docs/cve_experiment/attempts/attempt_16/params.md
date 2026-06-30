# Attempt #16 — Parametri

| Parametro | Valore |
|-----------|--------|
| Attempt # | 16 |
| Branch | exp/test-14 |
| Data | 2026-06-26 |
| hint_level | 1 (Patch_Spiegazione.md, nessun hint regex) |
| framing | naive non-expert |
| input_files | all_go_patch |
| nf_focus | all |
| struttura | per-file (long+short) + crossNF — terza replica identica di #14/#15 |
| clone | /tmp/cve-attempt-16 (--single-branch base/pre-cartella, CLEAN) |

## Motivazione

Terza replica — n=3 per valutare robustezza della condizione: struttura per-file + crossNF → regex committata.
Risultati precedenti: #14 ✅ (regex in per-file UDR), #15 ✅ (regex in crossNF).
