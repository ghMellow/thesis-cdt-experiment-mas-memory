# Sistema — Multi-Agent Experiment 5G

Riferimento stabile: mappa del codice, flusso di esecuzione, valutazione, report.
Per lo stato corrente e i puntatori alle call vedi [status.md](status.md).

---

## 1) Cos'e' questo progetto

Un esperimento controllato multi-agente su scenari 5G, orchestrato con LangGraph:

- un agente LLM unico risponde ai task
- due setup sperimentali (`1A` e `1B`) permettono di confrontare "stesso modello per agente e giudice" vs "modelli diversi"
- ogni task viene ripetuto piu' volte per misurare **consistenza**
- ogni run produce JSON di output + report aggregati in Markdown

> ⚠️ **Correzione (2026-07-10, call 11):** i due ruoli `expert`/`beginner` sono stati unificati in un **agente unico** con prompt neutro — 19/20 verdetti identici tra i ruoli, il framing non aggiungeva segnale. I riferimenti ai ruoli restano validi solo per i risultati storici (`results/*/*/{expert,beginner}/`); le run nuove salvano in `.../agent/`.
>
> ⚠️ **Correzione:** la documentazione originale diceva "temperatura 0". Il valore attuale in `config.py` e' `TEMPERATURE = 0.3`. Con temperatura > 0 le ripetizioni misurano varianza LLM reale, non solo stabilita' del parsing.

---

## 2) Setup sperimentali, ruoli e cosa viene misurato

### Setup 1A vs 1B

- **1A**: agente e giudice usano lo **stesso modello** (controllo).
- **1B**: agente e giudice usano **modelli diversi** (confronto).

I modelli effettivi sono definiti in `config.py` (mapping `MODELS`, chiavi `agent_1A`, `agent_1B`, `judge`, `semantic_check`): la scelta del modello è libera, basta modificare il mapping prima della run.

> ⚠️ **Correzione:** `TASK_MODEL_OVERRIDES` non esiste più nel codice — era un meccanismo della serie framing, rimosso.

Nota: se trovi riferimenti storici a modelli diversi nei documenti, fa fede `config.py`.

### Agente

Il system prompt è in `agents/prompts.py` (`SYSTEM_PROMPTS["agent"]`): profilo neutro di ingegnere 5G con esperienza di analisi e code review.

> ⚠️ **Correzione (call 11):** prima esistevano due prompt (`expert` senior / `beginner` junior); unificati in uno.

Formato di output richiesto (Markdown):

```md
### Answer
...

### Reasoning
...

### Confidence
0.0
```

### Task

I task sono in `docs/tasks/` e sono di due tipi:

- `math`: verifica numerica deterministica in Python (ground truth)
- `textual`: scoring tramite judge LLM con rubrica → l'agente produce una risposta testuale che viene valutata da un modello "giudice" (judge) che applica criteri di valutazione strutturati (rubrica) per assegnare un punteggio invece di confrontare semplicemente con una ground truth numerica

Task disponibili: 2 math (`task1_math_int`, `task2_math_real`), 2 textual 5G operativo (`task3_anomaly`, `task4_rootcause`), 4 textual security review single-file (`task5_vuln_pcf`, `task6_vuln_udr`, `task7_vuln_amf`, `task8_vuln_udm`), 1 textual security review cross-file (`task9_vuln_cross`).

I task security review (`task5`–`task9`) forniscono codice Go di network function 5G (free5GC) e chiedono all'agente una security review cieca (senza GT). Le vulnerabilità target sono CVE reali (GHSA). `task9_vuln_cross` fornisce estratti da tutti e 4 i file contemporaneamente per misurare la capacità di rilevare inconsistenze cross-NF (es. UDM valida SUPI in certi handler, UDR non lo fa mai).

---

## 3) Mappa del codice (dove sta cosa)

- `main.py`: entrypoint CLI; itera esperimenti/task/ripetizioni; genera report di evaluation
- `config.py`: mapping modelli + parametri globali (temperature, retry, ripetizioni, soglie)
- `utils/experiment_utils.py`: stato e grafo LangGraph; nodi `load_task`, `run_agent`, `check_answer`, `save_result`; include valutazione deterministica math, logica di retry e scrittura risultati; contiene `_fetch_model_context_window` e `_build_judge_prompt`
- `utils/task_utils.py`: parsing dei metadata (`**ID:**`, `**Tipo:**`) e lettura dei JSON dai file `_sol.md`; include `_result_exists` (skip run gia' completate) e `_answers_equal`
- `utils/evaluation_utils.py`: aggregazione risultati e generazione report anomaly-focused in `results/evaluation/`; include `_detect_inconsistencies` (fase 1: string equality, fase 2: LLM semantic check sui flagged con modello `MODELS["semantic_check"]`, obbligatorio) e `_brier_score` (calibrazione confidence)
- `agents/agent_runner.py`: chiamata LLM via Ollama + parsing Markdown in output (fallback JSON); logga token in/out quando disponibili
- `agents/judge_agent.py`: chiamata LLM judge + parsing Markdown + logging token in/out; include `run_semantic_equivalence_check` (verifica equivalenza semantica tra reasoning string)
- `agents/_llm_utils.py`: helper condivisi tra agent e judge (spinner, Markdown parsing, fallback JSON, error handling Ollama)
- `agents/prompts.py`: system prompt dell'agente (`SYSTEM_PROMPTS` dict, chiave unica `agent`)
- `utils/cvss_utils.py`: blocco prompt `CVSS Estimate` iniettato nei task vuln + estrazione della stima dall'output agente
- `utils/cvss_eval.py`: valutazione deterministica della stima CVSS (Blocco B): matching finding↔CVE per handler function, prossimità score a fasce (vs score pubblicato e vs base B), vector match exploitability/impatto; dataset GT in `File_Free5gc_Vulnerabili/cve_metrics_normalized.json`

---

## 4) Formato dei task e delle soluzioni

### Scenario (`docs/tasks/<task>.md`)

Ogni scenario e' un Markdown che include (obbligatori):

- `**ID:** <task_id>`
- `**Tipo:** math | textual`

e contiene lo scenario e le istruzioni per produrre output Markdown con sezioni `Answer`, `Reasoning`, `Confidence`.

### Soluzione (`docs/tasks/<task>_sol.md`)

Il file `_sol.md` contiene blocchi JSON racchiusi in fenced code blocks ` ```json ... ``` `.

- **Blocco 1**: `ground_truth`
- **Blocco 2** (solo `textual`): rubrica + `total_max`

Il sistema carica questi JSON nello stato interno per la valutazione.

---

## 5) Flusso di esecuzione (LangGraph)

Per ogni combinazione (setup, task, ripetizione) il runtime esegue:

1. `load_task`
   - legge scenario + `_sol.md`
   - ricava `task_id` e `task_type`
   - carica `ground_truth` (e la rubrica se `textual`)

1. `run_agent`
  - chiama l'LLM (Ollama) con il system prompt dell'agente + testo del task
  - salva l'output dell'agente (Markdown parsato) in `history` e in `final_answer`

1. `check_answer`
   - `math`: confronto deterministico in `utils/experiment_utils.py`
   - `textual`: chiama il judge LLM con scenario + rubrica + risposta

1. retry o salvataggio
   - se `verdict == "wrong"` e `attempts < MAX_RETRIES`, torna a `run_agent`
     - al retry, il `task_content` include la risposta + reasoning del tentativo precedente e un messaggio neutro
     - non viene iniettato feedback del judge, punteggio o ground truth
   - altrimenti salva e termina

### Ripetizioni vs retry

- `REPETITIONS`: ripete lo stesso task per misurare **consistenza** (con `TEMPERATURE > 0` misura varianza reale)
- `MAX_RETRIES`: tentativi dentro una singola ripetizione, solo se la valutazione e' `wrong`

### CLI flags disponibili

```bash
python main.py [--experiment 1A|1B|all]
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

**Input del judge** (payload Markdown):

```md
## Scenario
...

## Rubric
Total max score: 9
- category_name (0-3)
  - 3: ...
  - 2: ...

## Agent Response
### Answer
...

### Reasoning
...

### Confidence
0.0
```

**Cosa NON riceve il judge**:

- il blocco `ground_truth` (quindi non fa un "match" diretto con la soluzione)

**Output atteso**:

- un Markdown con sezione `Scores` (campi `*_score` + `total_score`) e sezione `Feedback`
- il prompt del judge viene generato dinamicamente da `_build_judge_prompt(rubric)` in `utils/experiment_utils.py`, con le categorie esatte della rubrica del task

**Come si calcola il verdetto** (in `utils/experiment_utils.py`):

- se manca `total_score`, viene ricostruito sommando tutte le chiavi che finiscono con `_score`
- `total_score` viene clamped a `[0, total_max]` e normalizzato: `normalized_score = total_score / total_max`
- `correct` se `normalized_score >= TEXTUAL_PASS_RATIO`, altrimenti `wrong`

**Attenzioni importanti sui judge (semantica dei punteggi)**:

- *Judge come fonte di verita'*: sui task textual, la rubrica e' di fatto la definizione operativa di "corretto".
  Se la rubrica e' ambigua o poco osservabile, il judge tende a premiare risposte plausibili.
- *Bias modello*: se il judge usa lo stesso modello dell'expert, tende a favorire risposte nel suo stesso stile.

### 6.3 Stima CVSS sui task security review (Blocco B, deterministico)

Sui task `vuln` (textual con `vuln` nel task_id, flag `CVSS_ESTIMATE_ENABLED` in `config.py`):

- `_load_task` appende al task il blocco `## CVSS Estimate` (`utils/cvss_utils.py`): l'agente deve emettere una sezione `### CVSS Estimate` in **Markdown** (convenzione di progetto: MD verso il modello, JSON lato codice) con righe `function:` / `vector:` / `score:` ripetute per ogni finding; il blocco include la legenda completa dei valori CVSS 4.0 (mai i valori corretti)
- il parser Markdown (`_extract_agent_response_markdown`) riconosce la sezione opzionale e la converte nella struttura interna `{"findings": [{"function", "vector", "score"}]}` salvata come `cvss_estimate` nel `final_answer` (accettato anche JSON come fallback per modelli che rispondono comunque in JSON)
- in `_save_result`, `evaluate_cvss_estimate` (`utils/cvss_eval.py`) confronta la stima con la GT (`File_Free5gc_Vulnerabili/cve_metrics_normalized.json`):
  - **matching finding↔CVE** per nome della handler function (le varianti `_full` includono anche le CVE con `in_task_excerpt: false`); finding non abbinati contati a parte, CVE non trovate in `missed_cves`
  - **prossimità score** a fasce (`CVSS_SCORE_BANDS` in config), calcolata sia vs lo score pubblicato (BT dove il vettore include la Threat E) sia vs il base puro `base_score_B`
  - **vector match** campo per campo, separato in exploitability (AV/AC/AT/PR/UI, 0–5) e impatto (VC/VI/VA, 0–3)
- il risultato va nel campo `cvss_eval` della ripetizione; **non influenza mai il verdetto** correct/wrong (che resta del solo judge di rubrica) e nei report compare come sezione separata "CVSS estimate" (`_build_cvss_section`)

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
- token: `tokens.agent_in`, `tokens.agent_out`, `tokens.judge_in`, `tokens.judge_out` (null se Ollama non li restituisce)

Il campo `judge_score` nei task textual include anche `normalized_score` (float in [0,1]) oltre ai campi `*_score` per categoria, `total_score` e `feedback`.

### Report aggregati (`results/evaluation/`)

Alla fine di una run, `utils/evaluation_utils.py` genera:

- `scores_1A.md`, `scores_1B.md`: tabella per ruolo con colonne `accuracy`, `avg_confidence`, `brier_score`, `avg_attempts`, `avg_math_delta`, `avg_textual_norm` + legenda metriche; Summary con contatori distinti per inconsistenze vere vs sole differenze superficiali; sezione anomalie (wrong, retried, inconsistenze reasoning confermate semanticamente)
- `comparison.md`: confronto accuracy 1A vs 1B per ruolo con delta
- `consistency.md`: segnala ripetizioni in cui il `final_answer` differisce dalla precedente

> ⚠️ **Precisazione:** il rilevamento delle inconsistenze nei report `scores_*.md` usa due fasi (string equality → LLM semantic check). Il confronto per `consistency.md` usa invece `_answers_equal` sull'intero `final_answer` (confronto JSON, invariato).

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
| `brier_score` | `mean((confidence − is_correct)²)` per ruolo |

### Passo 3 — Report di confronto: `comparison.md`

Tabella con una riga per ruolo (`expert`, `beginner`) che affianca `accuracy_1A`, `accuracy_1B` e il delta percentuale. Aggiunge un messaggio testuale se il delta e' zero.

### Passo 4 — `consistency.md` (scritto in modo incrementale)

Funziona diversamente dagli altri file: viene **aggiornato ad ogni run**, non riscritto da zero. Durante l'esecuzione, `main.py` confronta il `final_answer` della ripetizione corrente con quella precedente usando `_answers_equal` (confronto JSON con `sort_keys=True` sull'intero oggetto). Se differiscono, aggiunge una riga a `consistency_lines`. Alla fine, `_record_consistency_finding` fa **append** al file esistente — le run successive si accumulano.

### Differenza chiave tra i due confronti di inconsistenza

| file | dove | cosa confronta | quando viene scritto |
| --- | --- | --- | --- |
| `consistency.md` | `main.py` + `_record_consistency_finding` | intero `final_answer` (JSON equality) | append ad ogni run |
| sezione "Inconsistent reasoning" in `scores_*.md` | `_detect_inconsistencies` | solo campo `reasoning` (string equality) | riscritto ad ogni run |
