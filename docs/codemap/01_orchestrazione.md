# 01 — Orchestrazione: `main.py` e `config.py`

> Documento "code-as-truth": generato leggendo solo `main.py`, `config.py`, i moduli che li consumano (via grep) e `git log`/`git show` sugli stessi due file. Nessun file sotto `docs/` è stato letto per produrre questo testo (eccetto questo stesso file, di nuova creazione).

## 1. Cosa fa questo modulo

`main.py` è l'entry point CLI del progetto: costruisce un grafo LangGraph (`_build_graph()`, definito in `utils/experiment_utils.py`), enumera le combinazioni (esperimento × task × ripetizione), invoca il grafo per ogni combinazione mancante con un timeout hard (SIGALRM), traccia lo stato (`ExperimentState`) risultante, rileva incoerenze tra ripetizioni consecutive dello stesso task, e alla fine richiama la generazione dei report di valutazione. `config.py` è il singolo punto di configurazione statica del progetto: mapping modelli per ruolo (agente/giudice/semantic-check), endpoint Ollama locale/hosted, timeout, soglie di valutazione, percorsi di I/O e flag booleani che attivano/disattivano feature sperimentali (stima CVSS, hint SAST, gate SGV). Non contiene logica, solo costanti lette da altri moduli tramite `import config` (accesso ad attributo, non `from config import X`, per i valori che possono essere mutati a runtime — vedi §4).

## 2. `main.py`: flusso CLI

### Setup iniziale (`main.py:1-31`)
- `load_dotenv()` viene chiamato **prima** di ogni altro import (`main.py:3-4`), così `OLLAMA_API_KEY` in `config.py:39` è già in `os.environ` quando `config.py` viene importato.
- `_SpinnerClearHandler` (`main.py:24-30`) è un `logging.StreamHandler` che sovrascrive la riga corrente dello spinner (scritto altrove con `\r`, vedi `agents/_llm_utils.py:246-259` `_start_spinner`) prima di stampare un log record, per evitare output sporco quando lo spinner e il logger scrivono sullo stesso stream.

### Argomenti CLI (`main.py:34-84`)
| Flag | Default | Effetto |
|---|---|---|
| `--experiment {1A,1B,all}` | `all` | Filtra la lista `experiments` costruita più sotto (ma vedi nota su 1B, §4) |
| `--task` (ripetibile) | tutti | Filtra i task caricati da `TASKS_PATH`; errore fatale (`SystemExit(1)`) se un id richiesto non esiste (`main.py:104-107`) |
| `--repetitions` | `config.REPETITIONS` | Override numero ripetizioni |
| `--task-timeout` | `config.TASK_TIMEOUT_SECONDS` | Secondi massimi per ripetizione; `0` disabilita il timeout |
| `--experiment-id` | `None` | Rinomina la cartella risultati (`exp["id"]`) senza toccare la risoluzione del modello, che resta legata a `--experiment` (`main.py:120-122`) |
| `--temperature` | `None` | Se presente, sovrascrive `config.TEMPERATURE` a runtime (`main.py:92-93`) — mutazione diretta dell'attributo di modulo, non una copia locale |
| `--export-graph` | `None` | Se presente, esporta il grafo in PNG (`graph.get_graph().draw_mermaid_png(...)`) e termina subito, **senza eseguire nessun task** (`main.py:96-99`) |
| `--run-id` | timestamp UTC auto-generato | Tag che finisce nel JSON di ogni ripetizione salvata in questa invocazione (`main.py:86, 214`) |

### Costruzione della lista esperimenti (`main.py:110-122`)
```python
experiments = []
for exp_id in ["1A"]:  # era ["1A", "1B"]
    model, is_hosted = resolve_model_config(f"agent_{exp_id}")
    experiments.append({"id": exp_id, "role": "agent", "model": model, "is_hosted": is_hosted})
```
Il commento sopra (`main.py:110-111`) e il commit `e017557` ("Disable 1B framing...") confermano che 1B è disabilitato deliberatamente il 2026-07-13, lasciando la entry `agent_1B` in `config.MODELS` intatta "for future reactivation". Nota di design: `--experiment 1B` o `--experiment all` con questa build **non eseguirà mai 1B**, perché il ciclo `for exp_id in ["1A"]` non lo genera — il filtro `--experiment` (riga 116-117) agisce solo su ciò che è già stato costruito. `resolve_model_config` (in `agents/_llm_utils.py:15-20`) legge `config.MODELS[role_key]` e restituisce `(hosted_name, True)` o `(local_name, False)` a seconda di `use_hosted`.

### Conteggio ripetizioni mancanti e timeout dinamico (`main.py:124-159`)
- Prima del ciclo di esecuzione vero e proprio, un doppio ciclo enumera tutte le combinazioni esperimento/task/ripetizione e conta quelle il cui file risultato non esiste già (`_result_exists`, `utils/task_utils.py:83-97`) — serve solo per stimare `worst_case_seconds` da loggare, non altera il comportamento.
- Se almeno un task ha `FULL_TASK_SUFFIX` ("full") nello stem, il timeout Ollama globale (`config.OLLAMA_TIMEOUT_SECONDS`) viene alzato per coprire il caso peggiore (task "full" × moltiplicatore × 1.1), **ma solo se `args.task_timeout > 0`** — con `--task-timeout 0` il calcolo del caso "full" è saltato (`main.py:142`) e `desired_ollama_timeout` diventa `0 * 1.1 = 0`, quindi il confronto a riga 145 non alza mai il timeout in quel ramo (nessun bug: `0` significa "nessun timeout" a valle, coerente con `_time_limit`).
- Questa è una mutazione diretta di `config.OLLAMA_TIMEOUT_SECONDS` (riga 146), non un parametro passato esplicitamente: qualunque modulo che legge quell'attributo dopo questo punto (es. `agents/_llm_utils.py:41`, `agents/agent_runner.py:41`, `agents/judge_agent.py:117,166`) vede il valore aggiornato, perché tutti accedono via `config.OLLAMA_TIMEOUT_SECONDS` e non via `from config import OLLAMA_TIMEOUT_SECONDS` (import per valore, che congelerebbe il default al momento dell'import).

### Ciclo di esecuzione (`main.py:161-251`)
Per ogni `experiment` × `task_path` × `repetition` in `1..args.repetitions`:
1. Skip se `_result_exists(...)` è già vero (idempotenza: rilanciare lo script non rifà lavoro già salvato).
2. Costruisce `initial_state: ExperimentState` (TypedDict definito in `utils/experiment_utils.py:126-151`) con `task_path`, `sol_path` (convenzione: file soluzione = `<task_stem>_sol.md` nello stesso folder, `main.py:184`), `agent_role="agent"`, `model`, `is_hosted`, `attempts=0`, `history=[]`, `experiment_id`, `repetition`, `started_at`, `start_perf` (per `time.perf_counter()`, usato per l'elapsed time), `run_id`.
3. `effective_timeout` = `args.task_timeout`, raddoppiato (× `FULL_TASK_TIMEOUT_MULTIPLIER`) se lo stem del task contiene `FULL_TASK_SUFFIX` **e** `args.task_timeout > 0` (`main.py:218-224`) — logica duplicata rispetto al calcolo di §"conteggio" sopra, ma qui applicata per-task invece che come massimo globale.
4. `graph.invoke(initial_state)` viene eseguito dentro `with _time_limit(effective_timeout):` (context manager basato su `signal.SIGALRM`/`signal.setitimer`, definito in `utils/experiment_utils.py:158-173`; no-op se `seconds <= 0`).
5. Se scatta `TimeoutError`, il programma logga e **termina l'intero processo** con `raise SystemExit(1)` (`main.py:228-236`) — non continua con il prossimo task. Il messaggio di log ("Exiting after timeout to allow manual restart of Ollama") indica che il design assume che un timeout sia sintomo di un server Ollama locale bloccato, da riavviare manualmente prima di rilanciare lo script (che riprenderà dal punto grazie allo skip di `_result_exists`).
6. Confronto di consistenza: se esiste una `previous_answer` (ripetizione precedente sullo stesso task) e differisce da `final_answer` (confronto per uguaglianza di JSON serializzato con chiavi ordinate, `_answers_equal` in `utils/task_utils.py:100-101`), viene accodata una riga di log testuale in `consistency_lines`.

### Chiusura (`main.py:253-258`)
- `_record_consistency_finding(consistency_lines)` (in `utils/evaluation_utils.py`) persiste le eventuali differenze rilevate.
- `_write_evaluation_reports(RESULTS_PATH, task_filter=..., experiment_ids=...)` rigenera i report solo per i task/esperimenti effettivamente eseguiti in questa invocazione (`executed_tasks`, `executed_experiment_ids` derivati dalle liste locali, non da un giro su tutto `results/`).

**Gestione errori osservata**: non c'è try/except generico attorno al ciclo principale — un'eccezione non gestita in `graph.invoke` (a parte `TimeoutError`, intercettato esplicitamente) si propaga e termina lo script. Le uniche uscite controllate sono `SystemExit(1)` per task id sconosciuti (riga 107), per timeout (riga 236), e per assenza di esperimenti dopo il filtro (`raise ValueError`, riga 119 — questa non è un `SystemExit` esplicito, quindi termina con traceback Python standard, non con messaggio di log pulito: incoerenza minore rispetto alle altre guardie).

## 3. `config.py`: sezioni e consumatori

### `MODELS` (`config.py:14-35`)
Dizionario a 4 chiavi: `agent_1A`, `agent_1B`, `judge`, `semantic_check`. Ogni valore ha `local`/`hosted`/`use_hosted`. Consumato da:
- `agents/_llm_utils.py:18` (`resolve_model_config`) — usato da `main.py:114` per instanziare `experiments`.
- `utils/evaluation_utils.py:173-174,1238-1239` — verifica difensiva `if "semantic_check" not in config.MODELS: raise ValueError(...)` prima di usare il modello per i controlli di consistenza semantica.
- `scripts/judge_calibration/run_c1c2.py` — usa di default `config.MODELS['judge']`.

Storia (git log): il commit `b7fea95` ("Unify expert/beginner into a single agent — call 11 simplification") ha collassato 4 chiavi di ruolo (`expert_1A`/`beginner_1A`/`expert_1B`/`beginner_1B`) in 2 (`agent_1A`/`agent_1B`), motivato nel messaggio di commit come "19/20 identical verdicts" tra le due persona — cioè la distinzione expert/beginner non produceva verdetti diversi, quindi è stata rimossa insieme al flag `--role` in `main.py`. Il commento a `config.py:13` ("Expert/beginner framing removed after call 11...") conferma la stessa motivazione.

Tutti e tre gli ambienti (`agent_1A`, `agent_1B`, `judge`) sono attualmente configurati identici (`gemma4:e4b` locale / `gemma4:31b-cloud` hosted, `use_hosted: True`) — quindi 1A e "il giudice" oggi usano lo stesso modello hosted; solo `semantic_check` usa un modello locale più piccolo (`gemma4:e2b`) come hosted fallback, con commento inline `"framing_A1: use local to avoid hosted 500 errors"` (`config.py:33`) — nota che il commento dice "use local" ma il valore è `True` (hosted): il commento sembra vestigiale/non aggiornato rispetto all'ultimo valore effettivo (vedi §5).

### Endpoint hosted (`config.py:37-39`)
`OLLAMA_HOSTED_BASE_URL` e `OLLAMA_API_KEY` (quest'ultima da env var, letta una sola volta al modulo-import time). Consumati in `agents/_llm_utils.py:32-33` (costruzione `ChatOpenAI`). Ri-letta esplicitamente da `os.getenv` anche in `utils/evaluation_utils.py:2058` e `utils/cvss_eval.py:624` — pattern di refresh manuale della env var, probabilmente perché quei moduli vengono invocati come script standalone dove il modulo `config` potrebbe essere stato importato prima che `.env` fosse caricato (questi script fanno il proprio `import config` — vedi `scripts/judge_calibration/*.py:20-38` con `# noqa: E402`, segno che l'import avviene dopo un `sys.path` setup, non in cima al file).

### Parametri di generazione ed esecuzione (`config.py:41-63`)
- `TEMPERATURE = 0.3` — commento: "use > 0 to measure real consistency across repetitions" (`config.py:41`), cioè temperatura non-zero è una scelta deliberata per lo scopo del progetto (misurare varianza tra ripetizioni), non un default trascurato. Consumata in `utils/experiment_utils.py:236,315,442` e negli script di calibrazione giudice.
- `MAX_RETRIES = 3` — usata in `utils/experiment_utils.py:283,454` come limite ai retry sia del gate SGV (`state["attempts"] < MAX_RETRIES`) sia della verifica giudice standard.
- `REPETITIONS = 3` — default di `--repetitions` in `main.py:50`.
- `TASK_TIMEOUT_SECONDS = 600` — default di `--task-timeout` in `main.py:56`.
- `TEXTUAL_PASS_RATIO = 0.7` — soglia di superamento per i task testuali (`utils/experiment_utils.py:341`, `verdict = "correct" if ... normalized >= TEXTUAL_PASS_RATIO else "wrong"`); esiste uno script dedicato `scripts/judge_calibration/calibrate_threshold.py` che confronta questa soglia con una curva di soglie alternative — segno che il valore 0.7 è stato scelto/validato empiricamente, non a caso.
- `FULL_TASK_SUFFIX = "full"` / `FULL_TASK_TIMEOUT_MULTIPLIER = 2.0` — meccanismo di naming-convention: qualunque file task il cui stem contiene la sottostringa "full" riceve un timeout raddoppiato. Consumato solo in `main.py` (§2 sopra); nessun altro modulo lo referenzia, quindi la logica "full task = più lento" è interamente nel CLI, non nel grafo.
- `OLLAMA_BASE_URL = "http://localhost:11434"` — endpoint locale, usato da `main.py:168` per interrogare la context window del modello locale (`_fetch_model_context_window`), e da `utils/experiment_utils.py:237,316` per costruire i client `ChatOllama`.
- `OLLAMA_NUM_PREDICT = 1024` — commento: "1024 is sufficient for a full JSON with reasoning" (`config.py:58`); consumato solo in `agents/_llm_utils.py:26` come default se non passato esplicitamente.
- `OLLAMA_TIMEOUT_SECONDS = TASK_TIMEOUT_SECONDS * 1.1` — calcolato a import-time come derivato di `TASK_TIMEOUT_SECONDS`, poi eventualmente rialzato a runtime da `main.py` (vedi sopra). Commento esplicito: "Keep this >= TASK_TIMEOUT_SECONDS to avoid client timeouts before task timeouts" (`config.py:61-62`) — cioè la guardia serve a evitare che il client HTTP Ollama scada prima del timeout applicativo (`_time_limit`), che altrimenti mascererebbe l'errore reale con un errore di libreria HTTP invece del `TimeoutError` gestito esplicitamente in `main.py`.

### Percorsi I/O (`config.py:65-67`)
`TASKS_PATH = "docs/tasks/"`, `RESULTS_PATH = "results/"` — entrambi path relativi (dipendono dalla working directory da cui si lancia `python main.py`). Consumati ampiamente: `_list_tasks(TASKS_PATH)` in `main.py:100`, e `RESULTS_PATH` in tutta la catena di salvataggio/valutazione (`utils/experiment_utils.py:413`, `utils/evaluation_utils.py` più punti, `utils/cvss_eval.py:580,630`, e tutti gli script `scripts/judge_calibration/*.py`).

### Blocco CVSS (`config.py:69-82`)
- `CVSS_ESTIMATE_ENABLED = True` — gate per l'emissione/valutazione della stima CVSS strutturata sui task di tipo "vuln" (verificato con `is_cvss_task(...)` in `utils/experiment_utils.py:367` e `utils/task_utils.py:63`).
- `CVSS_DATASET_PATH` — dataset di riferimento per il matching deterministico (`utils/cvss_eval.py:74`).
- `CVSS_SCORE_BANDS = [(0.5, 3), (1.5, 2), (3.0, 1)]` — bande di prossimità punteggio→punti, commento: "Initial values from call 10 discussion — to be calibrated" (`config.py:76`), cioè valori esplicitamente segnalati come provvisori nel codice stesso. Consumate in `utils/cvss_eval.py:91` con logica "first match wins" (prima banda il cui delta massimo è rispettato).
- `CVSS_CONTEXT_HINT_ENABLED = True` — aggiunge un hint di contesto NF (OAuth2/TLS su SBI) al prompt, letto via `getattr(config, "CVSS_CONTEXT_HINT_ENABLED", False)` in `utils/cvss_utils.py:47` (uso di `getattr` con default invece di accesso diretto — guardia difensiva per import parziali/versioni vecchie di `config.py` senza questo attributo).

### Blocco SAST hint (`config.py:84-90`)
`SAST_HINT_ENABLED` è l'unico flag di `config.py` letto da env var con default esplicito a `false` (`os.getenv("SAST_HINT_ENABLED", "false").lower() == "true"`, `config.py:89`), motivato dal commento: mantenere il comportamento di baseline "committed default" mentre si testa l'effetto degli alert SonarQube grezzi iniettati nel prompt (`SAST_HINT_ENABLED=true python main.py ...`). Consumato in `utils/task_utils.py:60-61` per decidere se accodare il blocco costruito da `build_sast_hint_block(...)` (in `utils/sast_hint.py`, non incluso in questa analisi) leggendo `SAST_HINT_DATASET_PATH`.

### Blocco SGV — Syntactic Grounding Verifier (`config.py:92-104`)
- `SGV_ENABLED = True` — gate letto con `getattr(config, "SGV_ENABLED", False)` in `utils/experiment_utils.py:266`, combinato con `is_cvss_task(...)`: il nodo `check_sgv` del grafo (vedi `_build_graph`, §2) è quindi condizionale sia al flag sia al tipo di task.
- `SGV_SNIPPET_ENABLED = True` — rende opzionale il campo aggiuntivo `snippet` nel report dell'agente (letto in `utils/sgv.py:42` e `utils/cvss_utils.py:37`, sempre via `getattr` con default `False`).
- `SGV_SNIPPET_JACCARD_THRESHOLD = 0.8` — soglia di similarità token-Jaccard per il fallback quando lo snippet non combacia per substring esatta (`utils/sgv.py:195`, anche qui `getattr` con default `0.8` identico al valore in `config.py` — ridondanza consapevole, il default hardcoded coincide col valore configurato).

Pattern osservabile: i flag SGV/CVSS-hint più recenti sono sempre letti con `getattr(config, "NOME", default)` mentre i flag più "vecchi" (`MODELS`, `TEMPERATURE`, `MAX_RETRIES`, ecc.) sono letti con accesso diretto ad attributo o `from config import X`. Ipotesi di design (non confermata da commento esplicito, dedotta dalla struttura): i moduli che leggono con `getattr` sono quelli introdotti più tardi (SGV: commit `02603a0`; SAST hint: commit `c5e5dd3`) e la guardia serve a non rompere l'esecuzione se qualcuno importa una versione di `config.py` antecedente all'introduzione del flag (es. run storici rieseguiti, o script di rianalisi puntati a un `config.py` diverso).

## 4. Decisioni di design osservabili

1. **Mutabilità di `config` come modulo condiviso, non "frozen config object"** — `main.py:93,146` mutano `config.TEMPERATURE` e `config.OLLAMA_TIMEOUT_SECONDS` a runtime, e questo si propaga correttamente solo perché i consumatori (`agents/_llm_utils.py`, `agents/agent_runner.py`, `agents/judge_agent.py`) fanno `import config` e leggono `config.ATTR` invece di importare il valore per nome. `main.py` stesso importa alcuni simboli per valore con `from config import ...` (riga 15) — quei simboli (`FULL_TASK_SUFFIX`, `MODELS`, `OLLAMA_BASE_URL`, `REPETITIONS`, `RESULTS_PATH`, `TASK_TIMEOUT_SECONDS`, `TASKS_PATH`, `FULL_TASK_TIMEOUT_MULTIPLIER`) sono usati come default statici degli argomenti CLI e non hanno bisogno di essere mutabili dopo l'avvio, coerente col fatto che nessuno di essi viene riassegnato più avanti in `main.py`.
2. **1B "spento ma non rimosso"** — `main.py:112-113` disabilita 1B con una riga di codice commentata accanto, non rimuovendo la config in `config.py`. Scelta esplicita per riattivazione futura a basso costo (un solo punto di modifica), confermata dal messaggio del commit `e017557`.
3. **Timeout a due livelli con motivazione esplicita nel commento** — il commento a `config.py:61-62` chiarisce che `OLLAMA_TIMEOUT_SECONDS` deve restare ≥ `TASK_TIMEOUT_SECONDS` per evitare che l'errore di timeout venga sollevato dal client HTTP di Ollama invece che dal meccanismo applicativo (`_time_limit` in `utils/experiment_utils.py`), che è quello gestito esplicitamente con logging e uscita pulita in `main.py:228-236`.
4. **Fail-fast su timeout invece di skip-and-continue** (`main.py:236`) — un singolo timeout termina l'intero processo con `SystemExit(1)`, non salta solo quella ripetizione. Combinato con l'idempotenza di `_result_exists`, il design assume un ciclo manuale "run → timeout → riavvia Ollama → rilancia lo stesso comando", non un'esecuzione unattended a lungo termine.
5. **`--experiment-id` disaccoppia il nome della cartella risultati dalla risoluzione del modello** (`main.py:120-122`) — permette di rietichettare un run (es. per un framing sperimentale con nome custom) senza toccare quale voce di `config.MODELS` viene usata, che resta sempre legata a `--experiment`.
6. **Verifica difensiva esplicita per `semantic_check`** (`utils/evaluation_utils.py:173-174`) — `raise ValueError` se la chiave manca da `config.MODELS`, invece di un `KeyError` implicito: unico punto in cui l'assenza di una chiave di `MODELS` produce un errore con messaggio dedicato piuttosto che lasciare propagare l'eccezione nativa del dizionario.

## 5. Punti aperti / codice vestigiale o incoerente

- **`config.py:33`**, commento inline su `semantic_check.use_hosted`: il testo dice `"framing_A1: use local to avoid hosted 500 errors"` ma il valore impostato è `True` (hosted). Il commento sembra riferirsi a una configurazione precedente (probabilmente `use_hosted: False`) e non essere stato aggiornato quando il valore è stato cambiato a `True` — non deducibile con certezza da `git log` senza uno scavo per-riga aggiuntivo, ma la contraddizione testo/valore è visibile nel file attuale.
- **`main.py:119`**, `raise ValueError("No experiments matched...")` non è wrappato in `SystemExit` come le altre guardie di validazione CLI (righe 107, 236): produce un traceback Python invece di un messaggio di errore pulito via `logger.error`. Incoerenza minore nello stile di gestione errori, non un bug funzionale.
- **`config.py:52` `FULL_TASK_SUFFIX = "full"`**: è un match per sottostringa (`FULL_TASK_SUFFIX in task_path.stem`, `main.py:142,219`) non per suffisso di nome file nonostante il nome della costante suggerisca un suffisso — qualunque stem che contenga "full" in qualunque posizione attiva il timeout esteso, non solo quelli che terminano con "_full".
- **Duplicazione della condizione "full task"** tra `main.py:142-144` (calcolo del timeout Ollama globale, guardia `if args.task_timeout > 0`) e `main.py:219-223` (calcolo per-task, stessa guardia ripetuta): stessa logica scritta due volte con la stessa condizione, non estratta in una funzione comune — non è un bug (i due calcoli servono scopi diversi: uno stima il caso peggiore per il timeout del client HTTP, l'altro applica il timeout reale alla singola invocazione) ma è duplicazione di logica che potrebbe divergere silenziosamente in futuro se una delle due copie viene modificata senza l'altra.
- **`agents/_llm_utils.py:15-20,23-26`**: `import config` viene fatto localmente dentro le funzioni (`resolve_model_config`, `build_llm`) invece che a livello di modulo — pattern ripetuto anche in `utils/task_utils.py:41` e `agents/judge_agent.py`/`agents/agent_runner.py` (import di modulo in testa, però). Non chiaro dal codice perché l'import sia locale in `_llm_utils.py` specificamente; ipotesi plausibile (non confermata da commento o commit) è evitare import circolari, ma non è deducibile con certezza dal solo codice.

Fonti: solo codice sorgente + git log, nessun documento in docs/ consultato.
