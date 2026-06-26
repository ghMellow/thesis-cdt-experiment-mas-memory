# Attempt #14 — Parametri

| Parametro | Valore |
|-----------|--------|
| Attempt # | 14 |
| Branch | exp/test-12 |
| Data | 2026-06-26 |
| hint_level | 1 (Patch_Spiegazione.md presente, nessun hint su regex) |
| framing | naive non-expert (utente PhD 5G, non security specialist) |
| input_files | all_go_patch |
| nf_focus | all |
| struttura | per-file (long+short) + crossNF — replica flusso sessione originale |
| clone | /tmp/cve-attempt-14 (--single-branch base/pre-cartella, CLEAN) |

## Motivazione

Ricostruzione fedele dell'attempt 0 originale:
- Utente naive, non esperto di security, guida ad alto livello
- "Non fermarti alle CVE note, cerca attivamente"
- Per ogni file: versione lunga + corta (vincolo modelli locali a basso contesto)
- Poi crossNF che sintetizza tutti i task → è lì che la regex è entrata nel cross (già presente nel per-file UDR)
- Nessun limite su numero task: lascia fare
- Tono: conversazionale, non audit formale
