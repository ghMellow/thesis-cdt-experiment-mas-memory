# Attempt #17 — Parametri

| Parametro | Valore |
|-----------|--------|
| Attempt # | 17 |
| Branch | exp/test-15 |
| Data | 2026-06-30 |
| hint_level | 1 (Patch_Spiegazione.md, nessun hint regex) |
| framing | naive non-expert |
| input_files | all_go_patch |
| nf_focus | all |
| struttura | per-file (long+short) + crossNF — variante migliorata su #16 |
| clone | /tmp/cve-attempt-17 (--single-branch base/pre-cartella, CLEAN) |

## Modifiche al prompt rispetto a #14/#15/#16

Motivazione: attempt #16 ha fallito perché il "finding budget" si è saturato con i 6 CVE
di missing return + Deserialize-by-value nell'UDR. La regex è stata attraversata ma non
flaggata — non appare nemmeno tra i candidati scartati nel chain.

Fix aggiunte al prompt:
1. **Anti-saturation:** "Per ogni file elenca TUTTI i pattern anomali che trovi, anche quelli
   minori o sottili — non fare selezione preventiva a questo stadio, lascia che la selezione
   avvenga quando scrivi il task finale."
2. **CrossNF su validazione:** il crossNF chiede esplicitamente di confrontare i pattern
   dove "il codice sembra fare una cosa (validare, controllare) ma in realtà non la fa
   correttamente" — questo include naturalmente la regex catch-all senza nominarla.
3. **Lettura completa prima della selezione:** "Leggi ogni file per intero prima di decidere
   quali finding includere nel task."
