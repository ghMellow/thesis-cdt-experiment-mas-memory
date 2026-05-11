# Call 1 — Prima presentazione del sistema (§8.1–8.10)

Prima call: ho presentato il sistema che avevo costruito (LangGraph, ruoli, task math/textual, judge, report).
Da questa presentazione sono emersi i dubbi operativi documentati qui sotto.
Non riscrivere — aggiungere solo annotazioni `✅` / `⚠️` sotto le proposte già implementate.
Per lo stato corrente vedi [index_overview.md](index_overview.md).

---

## 8.1 Affidabilita' del judge sui task textual

- **Dubbio (call)**: il judge puo' validare risposte plausibili senza verifiche "hard".
- **Situazione attuale**: per i textual il verdict dipende da punteggio del judge + soglia `total_max * TEXTUAL_PASS_RATIO`; la ground truth testuale non viene usata nel verdict.
- **Proposte future**: rubriche piu' osservabili, judge multipli (consenso) e/o controlli rule-based su KPI dove possibile.

---

## 8.2 Soglie e distinzione "lieve" vs "critica"

- **Dubbio (call)**: senza soglie esplicite il judge non discrimina bene classi vicine.
- **Situazione attuale**: i criteri sono nei task e nelle rubriche, ma la decisione finale resta LLM-based.
- **Proposte future**: rubriche con soglie numeriche e criteri uniformi tra task; prompt del judge che richiama esplicitamente quei criteri.

---

## 8.3 Mismatch tra rubriche per-task e schema output del judge

- **Dubbio (call)**: se il judge non segue la rubrica specifica, i punteggi diventano poco interpretabili.
- **Situazione attuale**: prompt judge con campi "standard"; rubriche dei task possono avere categorie diverse.
- **Proposte future**: generare dinamicamente il prompt dal JSON rubrica, oppure standardizzare tutte le rubriche su dimensioni fisse.

> ✅ **Implementato:** `_build_judge_prompt(rubric)` in `utils/experiment_utils.py` genera il prompt judge dinamicamente dalla rubrica del task specifico. Per ogni categoria estrae il valore `max` e il dizionario `criteri` (con soglie esplicite), costruisce un blocco descrittivo e produce uno schema JSON di output con esattamente i campi della rubrica + `total_score` + `feedback`. Il prompt non e' piu' "standard" ma specifico per ogni task.

---

## 8.4 Retry con feedback povero

- **Dubbio (call)**: senza feedback il retry rischia di ripetere lo stesso errore.
- **Situazione attuale**: retry attivo solo su verdict `wrong`, ma il feedback del judge non viene reiniettato nel prompt.
- **Proposte future**: reiniettare `feedback` nel retry o aggiungere un nodo di "revision" prima del nuovo tentativo.

> ✅ **Implementato:** al retry, `_run_agent` in `utils/experiment_utils.py` costruisce un `task_content` aumentato che include il reasoning e la risposta del tentativo precedente (`history[-1]`), con la nota neutra "That attempt was not sufficient to produce a correct result. Please reason again from scratch." Il feedback del judge NON viene iniettato (integrità del test preservata). La funzione helper `_build_retry_task_content` gestisce la composizione.

---

## 8.5 Campo `confidence` poco sfruttato

- **Dubbio (call)**: la confidence non incide sul verdetto e quindi non misura calibrazione.
- **Situazione attuale**: la confidence viene salvata e riportata come media nei report.
- **Proposte future**: metriche di calibrazione (penalita' per overconfidence) e score composito (accuracy × calibration).

> ✅ **Implementato:** aggiunto `_brier_score` in `utils/evaluation_utils.py`: calcola `mean((confidence − is_correct)²)` per ruolo (lower = better). La colonna `brier_score` appare ora nella tabella "Scores by role" di ogni report `scores_*.md`, con nota esplicativa. Non richiede chiamate LLM aggiuntive.

---

## 8.6 Task troppo facili / differenze tra ruoli poco visibili

- **Dubbio (call)**: se l'accuracy satura, 1A vs 1B e expert vs beginner non si distinguono.
- **Situazione attuale**: task set piccolo (4 task) e spesso ben vincolato.
- **Proposte future**: task borderline e ambiguita' controllata, piu' casi e rubriche piu' discriminanti.

> ✅ **Implementato (parziale):** aggiunti 8 task security review (task5–task9 + varianti full-file) con rubrica 9 punti e soglia TEXTUAL_PASS_RATIO=0.7. La difficolta' e' genuinamente variabile: task piccoli (PCF, 65 righe) vs file interi (UDR, 2891 righe). Vedi [overview_call_security.md](overview_call_security.md) per i dettagli.

---

## 8.7 Token/costi/tempi non tracciati in modo completo

- **Dubbio (call)**: senza token/latency per chiamata non si confronta costo/qualita'.
- **Situazione attuale**: viene salvato `elapsed_seconds` a livello di ripetizione, non token in/out.
- **Proposte future**: token tracking (agent + judge) e report di costo/tempo per setup/ruolo/task.

> ✅ **Implementato:** `run_agent` e `run_judge_textual` restituiscono ora una tripla `(parsed_json, in_tok, out_tok)`. `_run_agent` accumula `agent_tokens_in` / `agent_tokens_out` nello stato (sommando su ogni retry). `_check_answer` accumula `judge_tokens_in` / `judge_tokens_out` nello stato (solo task textual). `_save_result` scrive un blocco `"tokens": {"agent_in", "agent_out", "judge_in", "judge_out"}` nel JSON di ogni ripetizione. I valori sono `null` se Ollama non restituisce i campi. I token non sono ancora aggregati nei report Markdown (`evaluation_utils.py`).

---

## 8.8 Consistenza troppo basata su equality del JSON

- **Dubbio (call)**: il confronto stringente segnala inconsistenze anche quando il senso e' identico.
- **Situazione attuale**: `_detect_inconsistencies` in `evaluation_utils.py` confronta il campo `reasoning` tra ripetizioni con string equality (non il JSON intero). `_answers_equal` in `task_utils.py` usa `json.dumps(sort_keys=True)` per confrontare il `final_answer` completo nel log di `consistency.md`. Entrambi rimangono confronti stringenti.
- **Proposte future**: confronto semantico (embedding) sul reasoning e confronto separato su `answer`.

> ✅ **Implementato:** `_detect_inconsistencies` ora opera in due fasi. **Fase 1** (invariata): string equality filtra tutti i task con reasoning diverso. **Fase 2**: per ogni task flaggato, viene chiamato `run_semantic_equivalence_check` in `agents/judge_agent.py` (modello judge, temperature=0, num_predict=256) che risponde `{"equivalent": bool, "explanation": "..."}`. I task confermati equivalenti sono conteggiati come `surface-only differences (semantically equiv.)` nel Summary e omessi dalla sezione Anomalies. Solo i task confermati semanticamente diversi compaiono come `Truly inconsistent reasoning` con la spiegazione LLM inline. `_answers_equal` in `consistency.md` rimane invariato (confronto JSON intero).

---

## 8.9 Modelli: taglia, stabilita' e latenza

- **Dubbio (call)**: hardware/VRAM e latenza influenzano scelta modello e stabilita' dei risultati.
- **Situazione attuale**: mapping in `config.py`, limite output con `OLLAMA_NUM_PREDICT`, timeout per ripetizione.
- **Proposte future**: profiling, confronto tra quantizzazioni/taglie e documentazione sistematica del modello usato per ogni run.

> ✅ **Parzialmente implementato:** il campo `model` e' salvato in ogni JSON di risultato. All'avvio `main.py` chiama `_fetch_model_context_window(model, base_url)` via `POST /api/show` a Ollama e logga la context window per ogni modello distinto nella run. Il profiling sistematico e il confronto tra quantizzazioni restano da fare.

---

## 8.10 Lingua dei prompt e memoria condivisa

- **Dubbio (call)**: prompt IT vs EN e assenza di memoria condivisa possono cambiare performance.
- **Situazione attuale**: stato per task include `history` ma non persiste cross-task.
- **Proposte future**: A/B test lingua prompt e sperimentazione di memoria condivisa (state/file) + piu' task e judge multipli.

> ⚠️ **Correzione:** la documentazione originale diceva "prompt in italiano". I system prompt in `agents/prompts.py` sono attualmente in **inglese** (sia `expert` che `beginner`). Il task content (`docs/tasks/*.md`) rimane in italiano. L'A/B test EN vs IT sui system prompt non e' ancora stato eseguito formalmente.
> ✅ **Implementato:** tutti i file `docs/tasks/*.md` (scenario e soluzione/rubrica) sono stati tradotti in **inglese**. Le label di classificazione nel task3 sono diventate `NORMAL` / `MINOR_ANOMALY` / `CRITICAL_ANOMALY`; la ground truth e i criteri della rubrica nel task4 sono stati tradotti coerentemente. System prompt e task content sono ora entrambi in inglese.
