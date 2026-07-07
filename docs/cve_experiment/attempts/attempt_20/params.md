# Attempt #20 — Parametri

| Parametro | Valore |
|-----------|--------|
| Attempt # | 20 |
| Branch | exp/test-18 |
| Data | 2026-07-01 |
| hint_level | 1 (Patch_Spiegazione.md, nessun hint regex) |
| framing | naive non-expert, senza narrativa "modelli locali/poco contesto" |
| input_files | all_go_patch |
| nf_focus | all |
| struttura | per-file (long+short) + crossNF — replica identica di #19 |
| clone | /tmp/cve-attempt-20 (--single-branch base/pre-cartella, CLEAN) |

## Motivazione

Replica #1 di 2 del test di confound (#19: ✅ SÌ, regex trovata senza narrativa "modelli
locali"). Verifica di riproducibilità: stesso prompt esatto, ambiente indipendente.
Lanciata in parallelo con attempt #21 (stesso prompt, altro branch/clone).
