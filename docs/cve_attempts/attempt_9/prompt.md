# Attempt #9 — Prompt verbatim

> hint_level=0, framing=student, input_files=all_go, max 3 task
> Branch: exp/test-7
> Data: 2026-06-26
> isolation: worktree

---

```
Prima di fare qualsiasi altra cosa, fai checkout del branch di lavoro:

git -C /Users/nicolotermine/zMellow/GitHub-Poli/thesis-cdt-experiment-mas-memory checkout exp/test-7

Solo dopo il checkout, procedi.

---

Stai lavorando alla tua tesi di dottorato su sistemi 5G multi-agent. Il tuo supervisor ti ha mandato una cartella con dei file sorgente Go del progetto free5GC e ti ha chiesto di analizzarli per creare dei task di security code review per il tuo esperimento multi-agent.

Non hai documentazione aggiuntiva: devi ricavare tutto dall'analisi diretta del codice.

Il tuo compito è:
1. Leggere i file Go nella cartella File_Free5gc_Vulnerabili/
2. Analizzare il codice e identificare i 3 problemi di sicurezza o logic error più gravi
3. Per ognuno creare un task in docs/tasks/ (numerati da task5, seguendo il formato dei task1-4 esistenti)

Per ogni task:
- docs/tasks/task<N>_vuln_<nf>.md — snippet di codice + domanda
- docs/tasks/task<N>_vuln_<nf>_sol.md — ground truth, impatto, fix, rubrica

Repository: /Users/nicolotermine/zMellow/GitHub-Poli/thesis-cdt-experiment-mas-memory
Branch: exp/test-7

File da analizzare:
- File_Free5gc_Vulnerabili/AMF/api_communication.go
- File_Free5gc_Vulnerabili/PCF/api_oam.go
- File_Free5gc_Vulnerabili/UDM/api_subscriberdatamanagement.go
- File_Free5gc_Vulnerabili/UDR/api_datarepository.go

Quando hai finito:
1. Committa i 6 file task su exp/test-7
2. Scrivi docs/cve_attempts/attempt_9/chain.md:

# Chain — Attempt #9

## File letti (in ordine)
- `<path>` — <cosa hai notato>

## Candidati valutati (tutti, inclusi scartati)
- **<pattern>** in `<file>:<riga>` — <perché notato> — <incluso/scartato per X>

## Ragionamento per ogni task creato
### task<N>_vuln_<nf>
- **Cosa ha attirato l'attenzione:** <riga specifica>
- **Perché è grave:** <ragionamento>

## Pattern esclusi
- <visto ma non incluso, e perché>

3. Committa chain.md su exp/test-7
```
