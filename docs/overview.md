# Overview

## 1) Cos'e' questo progetto

Un esperimento controllato multi-agente su scenari 5G, orchestrato con LangGraph:

- due ruoli LLM (`expert` e `beginner`) rispondono agli stessi task
- due setup sperimentali (`1A` e `1B`) permettono di confrontare "stesso modello" vs "modelli diversi per ruolo"
- ogni task viene ripetuto piu' volte per misurare **consistenza**
- ogni run produce JSON di output + report aggregati in Markdown

> ⚠️ **Correzione:** la documentazione originale diceva "temperatura 0". Il valore attuale in `config.py` e' `TEMPERATURE = 0.3`. Con temperatura > 0 le ripetizioni misurano varianza LLM reale, non solo stabilita' del parsing.

---

## 2) Setup sperimentali, ruoli e cosa viene misurato

### Setup 1A vs 1B

- **1A**: `expert` e `beginner` usano lo **stesso modello** (controllo).
- **1B**: `expert` e `beginner` usano **modelli diversi** (confronto).

I modelli effettivi sono definiti in `config.py` (mapping `MODELS`).
Nota: se trovi riferimenti storici a modelli diversi nei documenti, fa fede `config.py`.

### Ruoli

I ruoli sono definiti dai system prompt in `agents/prompts.py`:

- `expert`: profilo ingegnere 5G senior
- `beginner`: profilo tecnico 5G junior

Formato di output richiesto ad entrambi:

```json
{
  "answer": "...",
  "reasoning": "...",
  "confidence": 0.0
}
```

### Task

I task sono in `docs/tasks/` e sono di due tipi:

- `math`: verifica numerica deterministica in Python (ground truth)
- `textual`: scoring tramite judge LLM con rubrica → l'agente produce una risposta testuale che viene valutata da un modello "giudice" (judge) che applica criteri di valutazione strutturati (rubrica) per assegnare un punteggio invece di confrontare semplicemente con una ground truth numerica

> ✅ **Implementato:** aggiunto un secondo gruppo di task `textual` (`task5`–`task10`), dominio **code security review** su handler SBI reali di free5GC (Go). Ogni task presenta uno snippet di codice con una o piu' vulnerabilita' reali (analisi statica in `File_Free5gc_Vulnerabili/ANALISI_VULNERABILITA.md`, mappate a GHSA/CVE dove disponibili) e chiede di identificare vulnerabilita', impatto e fix in formato `{"vulnerability", "impact", "fix"}`. La rubrica del judge include sempre `vuln_identified_score`, `impact_assessment_score`, `fix_proposed_score`, `false_positives_score`, `clarity_score`, `confidence_calibration_score`. Mappa task → vulnerabilita':
> - `task5_vuln_pcf`: V1 — CORS misconfiguration (PCF, GHSA-98cp-84m9-q3qp)
> - `task6_vuln_udr_return`: V2 — missing `return` dopo 404 (UDR, 6 GHSA)
> - `task7_vuln_udr_regex`: V3 + V4 — regex di validazione `ueId` inefficace + assenza validazione formato (UDR)
> - `task8_vuln_amf`: V6 + V7 — `c.Set` con struct intera (information exposure) + `switch` senza `default` (AMF, GHSA-r99v-75p9-xqm5)
> - `task9_vuln_udr_nosql`: V5 — query param `supis` non validato in filtro MongoDB `$in` (UDR)
> - `task10_vuln_udm_validator`: V8 — `validator.IsValidSupi` applicato in modo incoerente tra handler SDM (UDM, GHSA-585v-hcgf-jhfr)
>
> I task vengono scoperti automaticamente da `_list_tasks` (glob su `docs/tasks/*.md` non `_sol.md`), nessuna modifica al codice e' stata necessaria.

---

## 3) Mappa del codice (dove sta cosa)

- `main.py`: entrypoint CLI; itera esperimenti/ruoli/task/ripetizioni; genera report di evaluation
- `config.py`: mapping modelli + parametri globali (temperature, retry, ripetizioni, soglie)
- `utils/experiment_utils.py`: stato e grafo LangGraph; nodi `load_task`, `run_agent`, `check_answer`, `save_result`; include valutazione deterministica math, logica di retry e scrittura risultati; contiene `_fetch_model_context_window` e `_build_judge_prompt`
- `utils/task_utils.py`: parsing dei metadata (`**ID:**`, `**Tipo:**`) e lettura dei JSON dai file `_sol.md`; include `_result_exists` (skip run gia' completate) e `_answers_equal`
- `utils/evaluation_utils.py`: aggregazione risultati e generazione report anomaly-focused in `results/evaluation/`; include `_detect_inconsistencies` (fase 1: string equality, fase 2: LLM semantic check sui flagged) e `_brier_score` (calibrazione confidence)
- `agents/agent_runner.py`: chiamata LLM via Ollama + parsing JSON in output; logga token in/out quando disponibili
- `agents/judge_agent.py`: chiamata LLM judge + parsing JSON + logging token in/out; include `run_semantic_equivalence_check` (verifica equivalenza semantica tra reasoning string)
- `agents/_llm_utils.py`: helper condivisi tra agent e judge (spinner, JSON parsing, error handling Ollama)
- `agents/prompts.py`: system prompt per ogni ruolo (`SYSTEM_PROMPTS` dict, chiavi `expert` e `beginner`)

---

## 4) Formato dei task e delle soluzioni

### Scenario (`docs/tasks/<task>.md`)

Ogni scenario e' un Markdown che include (obbligatori):

- `**ID:** <task_id>`
- `**Tipo:** math | textual`

e contiene lo scenario e le istruzioni per produrre il JSON.

### Soluzione (`docs/tasks/<task>_sol.md`)

Il file `_sol.md` contiene blocchi JSON racchiusi in fenced code blocks ` ```json ... ``` `.

- **Blocco 1**: `ground_truth`
- **Blocco 2** (solo `textual`): rubrica + `total_max`

Il sistema carica questi JSON nello stato interno per la valutazione.

---

## 5) Flusso di esecuzione (LangGraph)

Per ogni combinazione (setup, ruolo, task, ripetizione) il runtime esegue:

1) `load_task`
- legge scenario + `_sol.md`
- ricava `task_id` e `task_type`
- carica `ground_truth` (e la rubrica se `textual`)

2) `run_agent`
- chiama l'LLM (Ollama) con system prompt del ruolo + testo del task
- salva il JSON dell'agente in `history` e in `final_answer`

3) `check_answer`

- `math`: confronto deterministico in `utils/experiment_utils.py`
- `textual`: chiama il judge LLM con scenario + rubrica + risposta

4) retry o salvataggio
- se `verdict == "wrong"` e `attempts < MAX_RETRIES`, torna a `run_agent`
- altrimenti salva e termina

### Ripetizioni vs retry

- `REPETITIONS`: ripete lo stesso task per misurare **consistenza** (con `TEMPERATURE > 0` misura varianza reale)
- `MAX_RETRIES`: tentativi dentro una singola ripetizione, solo se la valutazione e' `wrong`

### CLI flags disponibili

```bash
python main.py [--experiment 1A|1B|all] [--role expert|beginner|all]
               [--task <task_id> ...]   # filtra su uno o piu' task specifici
               [--repetitions N]        # sovrascrive REPETITIONS da config
               [--task-timeout N]       # secondi max per ripetizione (0 = nessuno)
               [--export-graph <file>]  # esporta il grafo LangGraph e termina
```

### Skip automatico

Se un file risultato `results/<exp>/<role>/<task_id>_repN.json` esiste gia', quella ripetizione viene saltata. Utile per riprendere una run interrotta.

### Stima worst-case time

All'avvio `main.py` logga il tempo massimo stimato (`remaining_repetitions * task_timeout`) e la context window del modello recuperata da Ollama via `_fetch_model_context_window`.

### Export del grafo

```bash
python main.py --export-graph docs/graph.png
```

![LangGraph](graph.png)

---

## 6) Valutazione: come si decide correct/wrong

### 6.1 Task `math` (deterministici)

La valutazione avviene in `utils/experiment_utils.py` usando `ground_truth`:

- `type: exact_int`: conversione a int e match esatto (delta = 0)
- `type: real`: match float con `tolerance` (supporta anche answer come oggetto con piu' campi)

Output nel risultato:

- `verdict: correct | wrong`
- `judge_score`: contiene `delta` e una `note` descrittiva

### 6.2 Task `textual` (judge LLM) — approfondimento

Nei task textual il judge viene chiamato in `agents/judge_agent.py`.

**Input del judge** (payload JSON):

```json
{
  "scenario": "...",
  "rubrica": {"rubrica": {"...": "..."}, "total_max": 9},
  "agent_response": {"answer": "...", "reasoning": "...", "confidence": 0.0}
}
```

**Cosa NON riceve il judge**:

- il blocco `ground_truth` (quindi non fa un "match" diretto con la soluzione)

**Output atteso**:

- un JSON con i campi `*_score` della rubrica del task + `total_score` + `feedback`
- il prompt del judge viene generato dinamicamente da `_build_judge_prompt(rubric)` in `utils/experiment_utils.py`, con le categorie esatte della rubrica del task

**Come si calcola il verdetto** (in `utils/experiment_utils.py`):

- se manca `total_score`, viene ricostruito sommando tutte le chiavi che finiscono con `_score`
- `total_score` viene clamped a `[0, total_max]` e normalizzato: `normalized_score = total_score / total_max`
- `correct` se `normalized_score >= TEXTUAL_PASS_RATIO`, altrimenti `wrong`

**Attenzioni importanti sui judge (semantica dei punteggi)**:

- *Judge come fonte di verita'*: sui task textual, la rubrica e' di fatto la definizione operativa di "corretto".
  Se la rubrica e' ambigua o poco osservabile, il judge tende a premiare risposte plausibili.
- *Bias modello*: se il judge usa lo stesso modello dell'expert, tende a favorire risposte nel suo stesso stile.

---

## 7) Risultati: cosa viene salvato e come leggere i report

### File per ogni task e ripetizione

Per ogni ripetizione vengono scritti due file:

- `results/<experiment_id>/<role>/<task_id>_repN.json` (risultato completo)
- `results/<experiment_id>/<role>/<task_id>_repN_solution.json` (snapshot della ground truth)

Dentro il JSON di risultato (campi principali):

- metadati: `task_id`, `task_type`, `agent_role`, `model`, `repetition`
- esecuzione: `attempts`, `history`, `final_answer`, `verdict`, `judge_score`
- tempi: `started_at`, `finished_at`, `elapsed_seconds`

Il campo `judge_score` nei task textual include anche `normalized_score` (float in [0,1]) oltre ai campi `*_score` per categoria, `total_score` e `feedback`.

### Report aggregati (`results/evaluation/`)

Alla fine di una run, `utils/evaluation_utils.py` genera:

- `scores_1A.md`, `scores_1B.md`: tabella per ruolo con colonne `accuracy`, `avg_confidence`, `brier_score`, `avg_attempts`, `avg_math_delta`, `avg_textual_norm` + legenda metriche; Summary con contatori distinti per inconsistenze vere vs sole differenze superficiali; sezione anomalie (wrong, retried, inconsistenze reasoning confermate semanticamente)
- `comparison.md`: confronto accuracy 1A vs 1B per ruolo con delta
- `consistency.md`: segnala ripetizioni in cui il `final_answer` differisce dalla precedente

> ⚠️ **Precisazione:** il rilevamento delle inconsistenze nei report `scores_*.md` usa due fasi (string equality → LLM semantic check). Il confronto per `consistency.md` usa invece `_answers_equal` sull'intero `final_answer` (confronto JSON, invariato).

---

## 8) Dubbi (call) → situazione attuale → proposte future

### 8.1 Affidabilita' del judge sui task textual

- **Dubbio (call)**: il judge puo' validare risposte plausibili senza verifiche “hard”.
- **Situazione attuale**: per i textual il verdict dipende da punteggio del judge + soglia `total_max * TEXTUAL_PASS_RATIO`; la ground truth testuale non viene usata nel verdict.
- **Proposte future**: rubriche piu' osservabili, judge multipli (consenso) e/o controlli rule-based su KPI dove possibile.

### 8.2 Soglie e distinzione “lieve” vs “critica”

- **Dubbio (call)**: senza soglie esplicite il judge non discrimina bene classi vicine.
- **Situazione attuale**: i criteri sono nei task e nelle rubriche, ma la decisione finale resta LLM-based.
- **Proposte future**: rubriche con soglie numeriche e criteri uniformi tra task; prompt del judge che richiama esplicitamente quei criteri.

### 8.3 Mismatch tra rubriche per-task e schema output del judge

- **Dubbio (call)**: se il judge non segue la rubrica specifica, i punteggi diventano poco interpretabili.
- **Situazione attuale**: prompt judge con campi “standard”; rubriche dei task possono avere categorie diverse.
- **Proposte future**: generare dinamicamente il prompt dal JSON rubrica, oppure standardizzare tutte le rubriche su dimensioni fisse.

> ✅ **Implementato:** `_build_judge_prompt(rubric)` in `utils/experiment_utils.py` genera il prompt judge dinamicamente dalla rubrica del task specifico. Per ogni categoria estrae il valore `max` e il dizionario `criteri` (con soglie esplicite), costruisce un blocco descrittivo e produce uno schema JSON di output con esattamente i campi della rubrica + `total_score` + `feedback`. Il prompt non e' piu' “standard” ma specifico per ogni task.

### 8.4 Retry con feedback povero

- **Dubbio (call)**: senza feedback il retry rischia di ripetere lo stesso errore.
- **Situazione attuale**: retry attivo solo su verdict `wrong`, ma il feedback del judge non viene reiniettato nel prompt.
- **Proposte future**: reiniettare `feedback` nel retry o aggiungere un nodo di “revision” prima del nuovo tentativo.

### 8.5 Campo `confidence` poco sfruttato

- **Dubbio (call)**: la confidence non incide sul verdetto e quindi non misura calibrazione.
- **Situazione attuale**: la confidence viene salvata e riportata come media nei report.
- **Proposte future**: metriche di calibrazione (penalita' per overconfidence) e score composito (accuracy × calibration).

> ✅ **Implementato:** aggiunto `_brier_score` in `utils/evaluation_utils.py`: calcola `mean((confidence − is_correct)²)` per ruolo (lower = better). La colonna `brier_score` appare ora nella tabella "Scores by role" di ogni report `scores_*.md`, con nota esplicativa. Non richiede chiamate LLM aggiuntive.

### 8.6 Task troppo facili / differenze tra ruoli poco visibili

- **Dubbio (call)**: se l'accuracy satura, 1A vs 1B e expert vs beginner non si distinguono.
- **Situazione attuale**: task set piccolo (4 task) e spesso ben vincolato.
- **Proposte future**: task borderline e ambiguita' controllata, piu' casi e rubriche piu' discriminanti.

### 8.7 Token/costi/tempi non tracciati in modo completo

- **Dubbio (call)**: senza token/latency per chiamata non si confronta costo/qualita'.
- **Situazione attuale**: viene salvato `elapsed_seconds` a livello di ripetizione, non token in/out.
- **Proposte future**: token tracking (agent + judge) e report di costo/tempo per setup/ruolo/task.

> ✅ **Implementato:** `run_agent` e `run_judge_textual` restituiscono ora una tripla `(parsed_json, in_tok, out_tok)`. `_run_agent` accumula `agent_tokens_in` / `agent_tokens_out` nello stato (sommando su ogni retry). `_check_answer` accumula `judge_tokens_in` / `judge_tokens_out` nello stato (solo task textual). `_save_result` scrive un blocco `"tokens": {"agent_in", "agent_out", "judge_in", "judge_out"}` nel JSON di ogni ripetizione. I valori sono `null` se Ollama non restituisce i campi. I token non sono ancora aggregati nei report Markdown (`evaluation_utils.py`).

### 8.8 Consistenza troppo basata su equality del JSON

- **Dubbio (call)**: il confronto stringente segnala inconsistenze anche quando il senso e' identico.
- **Situazione attuale**: `_detect_inconsistencies` in `evaluation_utils.py` confronta il campo `reasoning` tra ripetizioni con string equality (non il JSON intero). `_answers_equal` in `task_utils.py` usa `json.dumps(sort_keys=True)` per confrontare il `final_answer` completo nel log di `consistency.md`. Entrambi rimangono confronti stringenti.
- **Proposte future**: confronto semantico (embedding) sul reasoning e confronto separato su `answer`.

> ✅ **Implementato:** `_detect_inconsistencies` ora opera in due fasi. **Fase 1** (invariata): string equality filtra tutti i task con reasoning diverso. **Fase 2**: per ogni task flaggato, viene chiamato `run_semantic_equivalence_check` in `agents/judge_agent.py` (modello judge, temperature=0, num_predict=256) che risponde `{"equivalent": bool, "explanation": "..."}`. I task confermati equivalenti sono conteggiati come `surface-only differences (semantically equiv.)` nel Summary e omessi dalla sezione Anomalies. Solo i task confermati semanticamente diversi compaiono come `Truly inconsistent reasoning` con la spiegazione LLM inline. `_answers_equal` in `consistency.md` rimane invariato (confronto JSON intero).

### 8.9 Modelli: taglia, stabilita' e latenza

- **Dubbio (call)**: hardware/VRAM e latenza influenzano scelta modello e stabilita' dei risultati.
- **Situazione attuale**: mapping in `config.py`, limite output con `OLLAMA_NUM_PREDICT`, timeout per ripetizione.
- **Proposte future**: profiling, confronto tra quantizzazioni/taglie e documentazione sistematica del modello usato per ogni run.

> ✅ **Parzialmente implementato:** il campo `model` e' salvato in ogni JSON di risultato. All'avvio `main.py` chiama `_fetch_model_context_window(model, base_url)` via `POST /api/show` a Ollama e logga la context window per ogni modello distinto nella run. Il profiling sistematico e il confronto tra quantizzazioni restano da fare.

### 8.10 Lingua dei prompt e memoria condivisa

- **Dubbio (call)**: prompt IT vs EN e assenza di memoria condivisa possono cambiare performance.
- **Situazione attuale**: stato per task include `history` ma non persiste cross-task.
- **Proposte future**: A/B test lingua prompt e sperimentazione di memoria condivisa (state/file) + piu' task e judge multipli.

> ⚠️ **Correzione:** la documentazione originale diceva "prompt in italiano". I system prompt in `agents/prompts.py` sono attualmente in **inglese** (sia `expert` che `beginner`). Il task content (`docs/tasks/*.md`) rimane in italiano. L'A/B test EN vs IT sui system prompt non e' ancora stato eseguito formalmente.
> ✅ **Implementato:** tutti i file `docs/tasks/*.md` (scenario e soluzione/rubrica) sono stati tradotti in **inglese**. Le label di classificazione nel task3 sono diventate `NORMAL` / `MINOR_ANOMALY` / `CRITICAL_ANOMALY`; la ground truth e i criteri della rubrica nel task4 sono stati tradotti coerentemente. System prompt e task content sono ora entrambi in inglese.

---

## 9) Come funziona la generazione dei report

### Trigger

In `main.py` (dopo che tutti gli esperimenti sono finiti) vengono chiamate in sequenza:

```python
_record_consistency_finding(consistency_lines)  # scrive/aggiorna consistency.md
_write_evaluation_reports(RESULTS_PATH)         # scrive scores_*.md e comparison.md
```

### Passo 1 — Raccolta dati: `_collect_results`

Scansiona `results/` cercando cartelle `<experiment_id>/<role>/`. Per ogni file `.json` che **non** finisce con `_solution.json`, carica il contenuto. Il risultato e' un dizionario annidato:

```python
data = {
    "1A": {
        "expert":   [ {rep1}, {rep2}, ... ],
        "beginner": [ {rep1}, ... ],
    },
    "1B": { ... }
}
```

### Passo 2 — Report per esperimento: `scores_1A.md` e `scores_1B.md`

Per ogni `experiment_id` in `["1A", "1B"]` viene chiamata `_build_experiment_report`, che costruisce il Markdown in tre sezioni:

**Sezione Summary** (contatori globali):

| metric | valore |
| --- | --- |
| total results | N totale di JSON caricati |
| correct | quanti hanno `verdict == "correct"` |
| wrong | quanti non sono correct |
| retried | quanti hanno `attempts > 1` |
| inconsistent tasks | quanti task hanno reasoning diverso tra ripetizioni |

**Sezione Anomalies** (solo se ci sono anomalie), con tre sotto-tabelle:

- *Wrong verdicts*: una riga per ogni risultato con `verdict != "correct"` — mostra role, task_id, rep, attempts, confidence, score/delta.
- *Retries triggered*: una riga per ogni risultato con `attempts > 1`.
- *Inconsistent reasoning*: generata da `_detect_inconsistencies`, che raggruppa i payload per task e confronta il campo `reasoning` del `final_answer` tra ripetizioni con **string equality**. Se almeno due ripetizioni hanno reasoning diverso, il task viene segnalato con tutte le versioni quotate.

**Sezione Scores by role** (tabella aggregata per ruolo):

| colonna | come si calcola |
| --- | --- |
| `accuracy` | `correct / total` |
| `avg_confidence` | media di `final_answer.confidence` |
| `avg_attempts` | media di `attempts` |
| `avg_textual_norm` | media di `judge_score.normalized_score` (solo task textual) |
| `avg_math_delta` | media di `judge_score.delta` (solo task math) |

### Passo 3 — Report di confronto: `comparison.md`

Tabella con una riga per ruolo (`expert`, `beginner`) che affianca `accuracy_1A`, `accuracy_1B` e il delta percentuale. Aggiunge un messaggio testuale se il delta e' zero.

### Passo 4 — `consistency.md` (scritto in modo incrementale)

Funziona diversamente dagli altri file: viene **aggiornato ad ogni run**, non riscritto da zero. Durante l'esecuzione, `main.py` confronta il `final_answer` della ripetizione corrente con quella precedente usando `_answers_equal` (confronto JSON con `sort_keys=True` sull'intero oggetto). Se differiscono, aggiunge una riga a `consistency_lines`. Alla fine, `_record_consistency_finding` fa **append** al file esistente — le run successive si accumulano.

### Differenza chiave tra i due confronti di inconsistenza

| file | dove | cosa confronta | quando viene scritto |
| --- | --- | --- | --- |
| `consistency.md` | `main.py` + `_record_consistency_finding` | intero `final_answer` (JSON equality) | append ad ogni run |
| sezione "Inconsistent reasoning" in `scores_*.md` | `_detect_inconsistencies` | solo campo `reasoning` (string equality) | riscritto ad ogni run |
