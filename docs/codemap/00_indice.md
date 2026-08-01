# Codemap — indice

Documentazione "code-as-truth" del progetto: ogni file in questa cartella è stato scritto leggendo **esclusivamente il codice sorgente eseguito** (file `.py`, più `docs/tasks/*.md` e `docs/results_reference/*.json` solo quando letti come *dati/schema consumati dal codice*, mai come narrativa) e `git log`/`git blame`/`git show` sugli stessi file per ricostruire il "perché" di una scelta quando è dichiarato in un commit o in un commento. Nessuna delle altre cartelle sotto `docs/` (`supporto/`, `sgv_protocol/`, `judge_rubric/`, `cve_experiment/`, `expert_review/`, `findings.md`, `changelog.md`, ecc.) è stata usata come fonte: quei documenti sono verbali di call, proposte discusse, esperimenti narrati — utili per capire *il processo* con cui si è arrivati al codice attuale, ma non affidabili come descrizione di *cosa il codice fa oggi*, perché possono divergere da come le cose sono state poi effettivamente implementate.

Se un claim in questi file e un claim in `docs/architecture.md` o `docs/status.md` si contraddicono, questa cartella ha la precedenza per "cosa fa il codice": è generata leggendo il codice direttamente, non riassumendo discussioni su di esso.

Snapshot: HEAD `acf6e21`, 2026-07-23. Se il codice è cambiato da allora, i file citano righe che potrebbero essersi spostate — vedi `/codemap-refresh` per aggiornare.

**Quattro modi di leggere questa documentazione:**

1. **[flusso.md](flusso.md) — inizia da qui.** Vista trasversale, minimale, in prosa: un diagramma ASCII globale del flusso di esecuzione, un racconto lineare breve, e approfondimenti solo dove il flusso pone davvero una domanda.
2. **[mappa_sistema.md](mappa_sistema.md)** — stessa idea di vista trasversale, ma in formato Mermaid/ADR: diagrammi (flowchart, state, sequence, ER) + decisioni architetturali come Architecture Decision Record (ognuna con fonte da commit/commento obbligatoria) + sezione dedicata alle domande aperte (TODO, passaggi manuali, logica non automatizzata).
3. **Questa cartella (file `NN_*.md`)** — versione densa e tabellare per area di codice, ottima per verificare un fatto puntuale.
4. **[narrativa/00_indice.md](narrativa/00_indice.md)** — stessa area, stessa profondità di (3), ma in prosa continua, per possedere davvero la conoscenza e argomentare/ragionare su modifiche future.

## Mappa dei moduli

```
main.py (CLI, entry point)
   │  arg parsing, timeout SIGALRM, ciclo esperimento × task × ripetizione
   ▼
config.py (costanti: modelli per ruolo, endpoint, soglie, path, feature flag)
   │
   ▼
utils/task_utils.py ──── load_task ────▶ utils/experiment_utils.py (grafo LangGraph)
(parsing file .md task,                        │
 dedup/idempotenza run)                          │  load_task → run_agent → check_sgv → check_answer → save_result → END
                                                  │        │            │            │
                                                  │        ▼            ▼            ▼
                                          agents/agent_runner.py   utils/sgv.py   agents/judge_agent.py
                                          agents/_llm_utils.py     utils/sast_hint.py   (rubrica testuale)
                                          agents/prompts.py             │
                                                  │                     │
                                                  ▼                     ▼
                                          utils/cvss_eval.py ◀── utils/cvss_utils.py
                                          (matching finding↔GT, metriche M/S,
                                           salvato in ogni risultato JSON)
                                                  │
                                                  ▼
                                          utils/evaluation_utils.py
                                          (reporting: aggrega i JSON grezzi in
                                           results/evaluation/*.md)

scripts/judge_calibration/*.py — standalone, non richiamati da main.py,
leggono risultati già salvati o materiale di calibrazione fisso per
validare/calibrare il giudice a posteriori.
```

## File di questa cartella

| File | Copre | Perché è centrale | Versione discorsiva |
|---|---|---|---|
| [01_orchestrazione.md](01_orchestrazione.md) | `main.py`, `config.py` | Entry point CLI e unico punto di configurazione statica; ogni altro modulo la consuma | [narrativa/01_orchestrazione.md](narrativa/01_orchestrazione.md) |
| [02_langgraph_state_machine.md](02_langgraph_state_machine.md) | `utils/experiment_utils.py` | Il cuore del progetto: schema di stato, grafo LangGraph, routing di retry, persistenza risultato | [narrativa/02_langgraph_state_machine.md](narrativa/02_langgraph_state_machine.md) |
| [03_agenti_llm.md](03_agenti_llm.md) | `agents/agent_runner.py`, `agents/_llm_utils.py`, `agents/judge_agent.py`, `agents/prompts.py` | Come si parla davvero con l'LLM (agente e giudice), parsing, retry di rete | [narrativa/03_agenti_llm.md](narrativa/03_agenti_llm.md) |
| [04_task_loader.md](04_task_loader.md) | `utils/task_utils.py` | Ponte tra i file task in `docs/tasks/` e lo stato del grafo; formato atteso, deduplicazione | [narrativa/04_task_loader.md](narrativa/04_task_loader.md) |
| [05_valutazione_metriche.md](05_valutazione_metriche.md) | `utils/evaluation_utils.py` | Livello di reporting: da JSON grezzi a report Markdown, tutte le metriche M1-M5/S1-S3 definite riga per riga | [narrativa/05_valutazione_metriche.md](narrativa/05_valutazione_metriche.md) |
| [06_cvss_scoring.md](06_cvss_scoring.md) | `utils/cvss_eval.py`, `utils/cvss_utils.py` | Matching finding↔ground truth CVE e matematica CVSS — la logica che `05` si limita ad aggregare | [narrativa/06_cvss_scoring.md](narrativa/06_cvss_scoring.md) |
| [07_sgv_gate.md](07_sgv_gate.md) | `utils/sgv.py`, `utils/sast_hint.py` | Gate sintattico deterministico G1-G4 e iniezione hint SAST nel prompt | [narrativa/07_sgv_gate.md](narrativa/07_sgv_gate.md) |
| [08_script_calibrazione.md](08_script_calibrazione.md) | `scripts/judge_calibration/*.py` | Strumenti standalone di validazione/calibrazione del giudice, fuori dal flusso automatico | [narrativa/08_script_calibrazione.md](narrativa/08_script_calibrazione.md) |

## Come leggere questi file

- Ogni claim tecnico è ancorato a un riferimento `file.py:riga`.
- Ogni file ha una sezione "decisioni di design osservabili + perché": quando il perché è dichiarato in un commit o in un commento, è riportato; quando non è deducibile dal codice/git, è dichiarato esplicitamente come tale invece di essere inventato.
- Ogni file chiude con "punti aperti / codice fragile": problemi reali osservati nel codice (eccezioni silenziate, euristiche non calibrate, codice vestigiale), utili come base per discussione tecnica col gruppo.
- Per il *processo* con cui si è arrivati a queste scelte (call, proposte scartate, dibattiti) usa `docs/README.md` e le cartelle `sgv_protocol/`, `judge_rubric/`, `supporto/` — questa cartella non li sostituisce, li integra dal lato opposto (codice vs discussione).
