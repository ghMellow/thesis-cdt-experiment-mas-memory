# `utils/experiment_utils.py` — la state machine LangGraph dell'esperimento

## 1. Ruolo del modulo

`utils/experiment_utils.py` definisce lo schema di stato (`ExperimentState`) e il grafo LangGraph (`_build_graph`) che orchestra l'intero ciclo di vita di un singolo "tentativo di task": caricamento del task, invocazione dell'agente LLM, un gate sintattico deterministico opzionale (SGV, per i soli task CVSS), la valutazione di correttezza (matematica deterministica o giudice LLM per i task testuali), un eventuale retry con prompt arricchito, e infine la persistenza su disco del risultato (con supporto a ripetizioni multiple accumulate nello stesso file). Il grafo è compilato una sola volta (`_build_graph()`) e invocato da `main.py` per ogni combinazione task/esperimento/ripetizione, con l'intera invocazione (`graph.invoke`) racchiusa in un timeout esterno (`_time_limit`, gestito in `main.py`, non nel modulo — vedi §7).

## 2. Schema di `ExperimentState`

`TypedDict` con `total=False` (tutti i campi opzionali finché non popolati), righe 126–154:

| Campo | Tipo | Significato |
|---|---|---|
| `task_id` | `str` | Identificatore del task, estratto dai metadata del file `.md` (popolato in `_load_task`, non mostrato qui — vive in `utils/task_utils.py`) |
| `task_type` | `str` | `"math"` o altro (es. task testuali/CVSS); determina il ramo di `_check_answer` |
| `task_content` | `str` | Corpo del prompt (letto verbatim dal file task, eventualmente arricchito con hint SAST/istruzioni CVSS in `_load_task`) |
| `ground_truth` | `Dict` | Risposta attesa, usata solo per i task math (mai passata al judge testuale — vedi CLAUDE.md, coerente col codice: `_check_answer` per i task testuali non legge `ground_truth`) |
| `rubric` | `Dict` | Rubrica di valutazione per il judge testuale |
| `agent_role` | `str` | Chiave in `SYSTEM_PROMPTS` (agents/prompts.py) |
| `model` | `str` | Nome modello agente |
| `is_hosted` | `bool` | Se il modello è hosted (vs. locale via Ollama) |
| `attempts` | `int` | Contatore tentativi, incrementato in `_run_agent` |
| `history` | `List[Dict]` | Lista di tutte le risposte agente prodotte nei tentativi successivi, ciascuna arricchita in-place con `sgv_eval`, `judge_score`, `verdict` |
| `verdict` | `str` | `"correct"` / `"wrong"`, esito dell'ultimo `_check_answer` |
| `judge_score` | `Dict` | Punteggio/dettaglio dell'ultima valutazione (math o judge testuale) |
| `final_answer` | `Dict` | Risposta dell'ultimo tentativo (= `history[-1]`, arricchita con `elapsed_seconds`, `tokens_in/out`, `prompt_system`, `prompt_user`) |
| `agent_tokens_in/out` | `int` | Accumulo token agente su tutti i tentativi |
| `judge_tokens_in/out` | `int` | Accumulo token judge su tutte le chiamate |
| `task_path` / `sol_path` | `str` | Path ai file task/soluzione, letti da `_load_task` |
| `experiment_id` | `str` | Identificatore esperimento (parte del path di output) |
| `repetition` | `int` | Indice di ripetizione within lo stesso esperimento |
| `run_id` | `str` | Tag dell'invocazione `main.py` che ha prodotto la ripetizione (introdotto in `900340f`, per distinguere run diversi salvati sotto la stessa cartella ruolo — vedi commento riga 384-386) |
| `started_at` / `finished_at` | `str` | Timestamp ISO UTC inizio/fine |
| `elapsed_seconds` | `float` | Calcolato in `_save_result` da `start_perf` |
| `start_perf` | `float` | `time.perf_counter()` iniziale, impostato da `main.py`, non dal grafo |
| `sgv_passed` | `bool` | Esito del gate SGV (`True` di default/no-op se non applicabile) |
| `sgv_feedback` | `Optional[str]` | Feedback formale SGV, iniettato nel retry prompt se il check fallisce |

## 3. Il grafo — struttura e routing

```
                 ┌───────────┐
                 │ load_task │  (utils/task_utils._load_task, importato come nodo)
                 └─────┬─────┘
                       │ edge fisso
                       ▼
                 ┌───────────┐
        ┌───────▶│ run_agent │  experiment_utils.py:222
        │        └─────┬─────┘
        │              │ edge fisso
        │              ▼
        │        ┌───────────┐
        │        │ check_sgv │  experiment_utils.py:262
        │        └─────┬─────┘
        │              │ _route_after_sgv (riga 282)
        │   "retry" ───┘└─── "check_answer"
        │                        │
        │                        ▼
        │                 ┌──────────────┐
        └─────────────────│ check_answer │  experiment_utils.py:293
           "retry"         └──────┬───────┘
                                  │ _route_after_check (riga 453)
                       "retry" ───┘└─── "save"
                                        │
                                        ▼
                                 ┌─────────────┐
                                 │ save_result │──▶ END
                                 └─────────────┘     experiment_utils.py:359
```

Edge fissi: `load_task→run_agent` (riga 473), `run_agent→check_sgv` (riga 474), `save_result→END` (riga 481).
Edge condizionali: `check_sgv→{run_agent|check_answer}` via `_route_after_sgv` (righe 475-477), `check_answer→{run_agent|save_result}` via `_route_after_check` (righe 478-480).

Nota strutturale: **entrambi** i punti di retry rientrano su `run_agent`, non su un nodo dedicato — il ramo SGV e il ramo verdict-based condividono lo stesso arco di retry e lo stesso contatore `attempts`, quindi consumano lo stesso budget di `MAX_RETRIES` (config.py:44, valore 3).

## 4. Dettaglio dei nodi

### `_run_agent` (righe 222-259)
- **Input**: `agent_role`, `history`, `task_content`, `sgv_feedback`, `model`, `is_hosted`.
- **Comportamento**: se `history` è non vuota, il prompt effettivo non è `task_content` grezzo ma il risultato di `build_retry_task_content` (arricchito con tentativo precedente + eventuale feedback SGV); altrimenti usa `task_content` as-is. Chiama `agents.agent_runner.run_agent`, cronometra la chiamata con `time.perf_counter()`.
- **Side effect**: arricchisce `agent_response` con `elapsed_seconds`, `tokens_in/out`, `prompt_system`, `prompt_user`; incrementa `attempts`; appende `agent_response` a `history`; aggiorna `final_answer` e gli accumulatori token agente.
- **Caso limite**: `history` è mutata in-place (list) e riassegnata via `state.get("history", [])` due volte (righe 225 e 247) — ridondante ma non bug, dato che è lo stesso oggetto lista.

### `_check_sgv` (righe 262-279)
- **No-op esplicito**: se `config.SGV_ENABLED` è `False` oppure `is_cvss_task(task_id, task_type)` è `False`, imposta `sgv_passed=True`, `sgv_feedback=None` e ritorna subito (riga 266-268). Il gate si applica **solo** ai task che espongono un "CVSS Estimate" nella risposta.
- **Comportamento attivo**: estrae `cvss_estimate` da `final_answer`, chiama `run_sgv(task_content, cvss_estimate)` (definito in `utils/sgv.py`, non aperto in dettaglio) che ritorna `{"passed": bool, "per_finding": [...], "feedback": str|None}`.
- **Side effect**: scrive il risultato SGV completo (`result`) dentro `history[-1]["sgv_eval"]` (solo se `history` non vuota), oltre ad aggiornare `sgv_passed`/`sgv_feedback` nello stato. Logga in caso di fallimento.
- **Design esplicito nel commento**: "deterministic, no ground truth" — SGV valuta solo la forma del report CVSS, mai se la vulnerabilità individuata è corretta.

### `_route_after_sgv` (righe 282-290)
Condizione esatta per `retry`: `sgv_passed is False` **and** `attempts < MAX_RETRIES`. Altrimenti va a `check_answer` (compreso il caso in cui SGV non è mai stato applicato, dato che `sgv_passed` di default è `True`).

### `_check_answer` (righe 293-356)
Due rami distinti in base a `task_type`:
- **`"math"`**: chiama `_check_math_answer` (deterministica, nessuna chiamata LLM) — vedi §5 sotto per la logica.
- **altro (testuale)**: chiama `agents.judge_agent.run_judge_textual` (import riga 18) passando `rubric`, `final_answer`, un system prompt generato ad-hoc da `build_judge_prompt(rubric)` (righe 53-82), e il modello judge risolto via `resolve_model_config("judge")`. Calcola `total_score` (con fallback a somma dei campi `*_score` se il judge non fornisce `total_score`), lo clampa in `[0, total_max]`, normalizza (`normalized_score = total_score/total_max`), e deriva `verdict = "correct" if normalized >= TEXTUAL_PASS_RATIO else "wrong"` (config.py: `TEXTUAL_PASS_RATIO = 0.7`).
- In entrambi i rami, se `history` non è vuota, scrive `judge_score` e `verdict` anche dentro `history[-1]` (oltre che nello stato top-level).
- Nota: il ground truth testuale (se esiste) non entra in questo ramo — solo la rubrica, coerente con la regola di progetto "il judge non riceve la ground_truth testuale".

### `_save_result` (righe 359-450)
- **Side effect deterministico aggiuntivo** (Blocco B, non collegato al verdetto): se `config.CVSS_ESTIMATE_ENABLED` e il task è CVSS, chiama `evaluate_cvss_estimate` due volte — una sull'ultima stima (`cvss_eval`) e una sulla prima stima in assoluto (`cvss_eval_pass1`, introdotto nel commit `32e21c1` per le metriche M1/M2 pass@1 vs pass@k). Eventuali eccezioni sono catturate e loggate, il campo risultante resta `None` (righe 378-379).
- **Persistenza**: costruisce `rep_payload` con timing, `attempts`, `history` completa, una vista sintetica di `final_answer` (solo i campi `answer`, `reasoning`, `confidence`, `cvss_estimate`), `verdict`, `judge_score`, i due `cvss_eval*`, e i token accumulati.
- **Path di output**: `config.RESULTS_PATH / task_id / experiment_id / agent_role / <model_slug>.json`, dove `model_slug` viene da `utils.task_utils._model_slug(model, is_hosted)`.
- **Accumulo ripetizioni**: se il file esiste già e ha la chiave `"repetitions"`, la nuova `rep_payload` viene appesa alla lista esistente (append-only, nessun controllo di duplicati per `repetition`/`run_id` — vedi §7); altrimenti crea il payload di primo livello (config comune) con `repetitions: [rep_payload]`.
- **Scrittura**: `result_file.write_text(json.dumps(payload, indent=2, ensure_ascii=True))` — sovrascrittura completa del file a ogni chiamata, non append su disco a basso livello.

### `_route_after_check` (righe 453-461)
Condizione esatta per `retry`: `verdict != "correct"` **and** `attempts < MAX_RETRIES`. Altrimenti va a `save`.

## 5. `_check_math_answer` (righe 93-123)

Deterministica, nessuna chiamata LLM:
- `gt_type == "exact_int"`: confronto intero esatto, `verdict = "correct" if delta == 0 else "wrong"`.
- `gt_type == "real"`: se `gt_answer` è un dict (risposta multi-campo), calcola il delta massimo tra tutte le chiavi e richiede che **tutti** i delta siano entro `tolerance`; altrimenti confronto scalare singolo con tolleranza.
- Altri `gt_type` → `ValueError("Unsupported ground truth type")`.
- `_to_float` (righe 85-90) accetta `int`/`float`/stringhe numeriche, altrimenti solleva `ValueError`.

## 6. Logica di retry — `build_retry_task_content` (righe 191-219)

Scatta quando `_route_after_sgv` o `_route_after_check` ritornano `"retry"`, sempre rientrando sul nodo `run_agent`. Limite massimo: `MAX_RETRIES = 3` (config.py:44), condiviso fra i due punti di retry tramite il singolo contatore `attempts`.

Il prompt di retry è costruito concatenando al `task_content` originale:
1. Nota esplicita "you already attempted this task... try again from scratch".
2. `### Previous Answer` — risposta precedente formattata da `_format_previous_answer` (righe 176-188): gestisce dict (con liste annidate rese come bullet) e liste semplici, altrimenti `str()`.
3. `### Previous Reasoning` — dal campo `reasoning` dell'ultimo elemento di `history`.
4. `### Previous Confidence`.
5. **Solo se `sgv_feedback` è presente** (cioè solo dopo un fallimento SGV, non dopo un fallimento di rubrica/math): blocco `### Formal Issues Found In Your CVSS Estimate`, esplicitamente etichettato come "NOT about whether the code is vulnerable, only about the report's form" — commento a riga 211-212 ribadisce che SGV non rivela mai quale funzione sia effettivamente vulnerabile.
6. Chiusura: invito a ragionare di nuovo da zero seguendo il formato di risposta del task.

Nota: se il retry è scattato per fallimento della rubrica/math (non SGV), `sgv_feedback` è `None`/assente e il blocco SGV viene semplicemente omesso — il prompt di retry in quel caso contiene solo risposta/reasoning/confidence precedenti, senza alcun segnale su *cosa* fosse sbagliato nel verdetto stesso (il judge non spiega il proprio giudizio all'agente in retry, stando a quanto visibile in questo modulo).

## 7. Decisioni di design osservabili (da git log)

- **SGV è un'aggiunta successiva** (commit `02603a0`, 14 luglio 2026), inserita come "deterministic in-loop gate, no ground truth" fra `run_agent` e `check_answer`, riusando lo stesso arco di retry già esistente verso `run_agent` e lo stesso contatore `attempts`/`MAX_RETRIES` — nessun budget di retry separato per SGV.
- **`cvss_eval_pass1`** (commit `32e21c1`, stesso giorno) è stato aggiunto per confrontare la detection "prima" vs "dopo" il retry loop (M1/M2), riusando `history[0]` come riferimento del primo tentativo — conferma che `history` è pensata anche come sorgente per metriche retrospettive, non solo come log.
- **`run_id`** (commit `900340f`) risolve un problema di identificazione: run diversi salvati sotto la stessa cartella ruolo non erano altrimenti distinguibili — commento esplicito a riga 384-386.
- **`_time_limit`** è stato introdotto molto prima (commit `a899a43`, 4 maggio) insieme a `MAX_RETRIES`, ma **non è più invocato dentro `experiment_utils.py`**: oggi il suo unico chiamante è `main.py:226`, che lo usa per avvolgere l'intera `graph.invoke(initial_state)` con un timeout complessivo per task/ripetizione (con moltiplicatore per i task "full", vedi `main.py:216-224`), non per nodo. Il commit `2ac6a34` ("Add extended timeout for full tasks and track execution time for agents") ha esteso questo meccanismo. Il codice non rende esplicito nei commenti perché il timeout sia stato spostato a livello di grafo invece che di singolo nodo — è deducibile solo dal fatto che una singola invocazione `graph.invoke` può includere più retry, quindi più chiamate LLM, e un timeout per-nodo non coprirebbe il caso di un ciclo di retry che si allunga.
- **Separazione verdetto/CVSS eval** (Blocco B, commit `21cb72a`): `evaluate_cvss_estimate` è esplicitamente commentata come "never affects verdict" (riga 364) — è una misura scientifica parallela, non un criterio di pass/fail per il retry.

## 8. Punti aperti / codice fragile

- `_time_limit` resta definito in questo modulo (righe 157-173) ma il suo unico uso reale è in `main.py`, importato esplicitamente da lì (`from utils.experiment_utils import ... _time_limit`). Non è dead code, ma la sua collocazione in un modulo che si occupa di stato/nodi del grafo — mentre il suo utilizzo effettivo è a livello di orchestrazione dei task in `main.py` — rende la lettura del modulo fuorviante se ci si aspetta di trovarne l'uso qui.
- In `_save_result`, l'append a `existing["repetitions"]` (riga 431) non verifica se una `repetition`/`run_id` identica sia già presente: una doppia esecuzione con lo stesso `run_id`/`repetition` produrrebbe una entry duplicata nel file JSON, senza deduplicazione.
- `_run_agent` (righe 225 e 247) legge `state.get("history", [])` due volte nello stesso frame invece di riutilizzare una singola variabile — innocuo perché è lo stesso oggetto mutabile, ma ridondante e potenzialmente confusivo se in futuro uno dei due punti venisse modificato per creare una copia.
- Il blocco `try/except Exception` in `_save_result` (righe 368-379) per `evaluate_cvss_estimate` cattura qualunque eccezione e la logga con `logger.exception`, ma lascia silenziosamente `cvss_eval`/`cvss_eval_pass1` a `None` senza propagare l'informazione di errore nel payload salvato — un fallimento sistematico di questa funzione (es. bug di parsing) sarebbe visibile solo nei log, non nei risultati aggregati.
- Il retry via `build_retry_task_content` non comunica mai il motivo del fallimento quando il verdetto proviene dal judge testuale o dal check matematico (solo il fallimento SGV produce un feedback esplicito) — l'agente in retry per un verdetto "wrong" su base rubrica riceve solo la propria risposta precedente, senza alcun segnale su cosa il judge abbia penalizzato.

Fonti: solo codice sorgente + git log, nessun documento in docs/ consultato.
