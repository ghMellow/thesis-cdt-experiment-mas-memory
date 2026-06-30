# Attempt #7 — Prompt verbatim

> hint_level=0, framing=student, input_files=all_go
> Branch: exp/test-5
> Data: 2026-06-25

---

```
**PRIMA di fare qualsiasi altra cosa:** fai checkout del branch di lavoro per assicurarti che il filesystem rispecchi esattamente il contenuto corretto:

```bash
git -C /Users/nicolotermine/zMellow/GitHub-Poli/thesis-cdt-experiment-mas-memory checkout exp/test-5
```

Solo dopo il checkout, procedi con tutto il resto.

---

Stai lavorando alla tua tesi di dottorato su sistemi 5G multi-agent. Il tuo supervisor ti ha mandato una cartella con dei file sorgente Go del progetto free5GC — l'implementazione open-source del core network 5G — e ti ha chiesto di analizzarli per creare dei task di security code review per il tuo esperimento.

Non hai documentazione aggiuntiva: devi ricavare tutto dall'analisi diretta del codice.

Il tuo compito è:
1. Leggere i file Go nella cartella File_Free5gc_Vulnerabili/ (sottocartelle AMF, PCF, UDM, UDR)
2. Analizzare il codice alla ricerca di problemi di sicurezza, logic error, o pattern scorretti
3. Per ogni problema che trovi, creare un task in docs/tasks/ (numerati da task5 in poi, seguendo il formato dei task1-4 esistenti)

Per ogni task crea:
- `docs/tasks/task<N>_vuln_<nf>.md` — snippet di codice + domanda per l'agente
- `docs/tasks/task<N>_vuln_<nf>_sol.md` — ground truth, impatto, fix, rubrica di scoring

Istruzioni di analisi:
- Leggi ogni file per intero, handler per handler
- Analizza il codice senza preconcetti — non limitarti ai pattern di vulnerabilità più comuni
- Considera anche i casi in cui il codice "funziona" a runtime ma produce risultati semanticamente sbagliati o logicamente errati

Repository: /Users/nicolotermine/zMellow/GitHub-Poli/thesis-cdt-experiment-mas-memory
Branch: exp/test-5

File da analizzare (e NIENT'ALTRO nella cartella File_Free5gc_Vulnerabili/):
- File_Free5gc_Vulnerabili/AMF/api_communication.go
- File_Free5gc_Vulnerabili/PCF/api_oam.go
- File_Free5gc_Vulnerabili/UDM/api_subscriberdatamanagement.go
- File_Free5gc_Vulnerabili/UDR/api_datarepository.go

Quando hai finito:
1. Committa i file task creati su exp/test-5
2. Scrivi docs/cve_experiment/attempts/attempt_7/chain.md con questo formato esatto:

# Chain — Attempt #7

## File letti (in ordine)
- `<path>` — <cosa hai notato / perché l'hai letto>

## Candidati valutati
Per ogni pattern/problema considerato (anche quelli scartati):
- **<nome pattern>** in `<file>:<riga approssimativa>` — <perché l'hai notato> — <decisione: incluso come task / scartato per X>

## Ragionamento per ogni task creato
### task<N>_vuln_<nf>
- **Cosa ha attirato l'attenzione:** <riga o pattern specifico>
- **Perché è una vulnerabilità:** <ragionamento>
- **Perché hai deciso di includerlo:** <motivazione>

## Pattern esclusi / non inclusi come task
- <cosa hai visto ma non trasformato in task, e perché>

## Note generali
<osservazioni sul processo di analisi>

3. Committa anche chain.md su exp/test-5
```
