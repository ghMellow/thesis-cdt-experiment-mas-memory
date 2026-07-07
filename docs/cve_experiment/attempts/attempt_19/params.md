# Attempt #19 — Parametri

| Parametro | Valore |
|-----------|--------|
| Attempt # | 19 |
| Branch | exp/test-17 |
| Data | 2026-07-01 |
| hint_level | 1 (Patch_Spiegazione.md, nessun hint regex) |
| framing | naive non-expert, **SENZA narrativa "modelli locali/poco contesto"** |
| input_files | all_go_patch |
| nf_focus | all |
| struttura | per-file (long+short) + crossNF — identica a #14-18 |
| clone | /tmp/cve-attempt-19 (--single-branch base/pre-cartella, CLEAN) |

## Motivazione — test di confound

Nei tentativi #14-18 la struttura "1 task per file, no cap" era sempre giustificata nel prompt
con: *"il progetto usa modelli LLM locali con finestra di contesto limitata"*. Questa frase era
**costante** sia nei successi (#14,15,17) sia nei fallimenti (#16,18) — quindi non spiega la
varianza, ma potrebbe comunque contribuire all'effetto medio (non isolato).

**Domanda:** la struttura per-file+crossNF funziona per la SUA forma (lettura esaustiva prima
di selezionare, poi sintesi comparativa) o serve anche la narrativa "modelli piccoli" a spingere
verso un'analisi più profonda?

**Manipolazione:** stesso identico prompt di base (#14/#15, "Prompt A" in hands_on.md) MA la
richiesta di 1-task-per-file è motivata SOLO con "voglio un task per ogni file, così ognuno è
autosufficiente" — nessun riferimento a modelli locali, context window, o vincoli tecnici.

**Ipotesi:** se il tasso di successo resta ~60% (vicino a 3/5), la leva causale è la struttura
(lettura esaustiva + crossNF), non la narrativa. Se crolla, la narrativa aveva un ruolo nel
motivare un'analisi più attenta.
