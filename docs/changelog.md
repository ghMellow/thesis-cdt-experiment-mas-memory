# Changelog

---

## 2026-05-07 — Refactoring e fix validità esperimento

### Struttura: eliminazione `core/`

**Cosa**: rimossa la cartella `core/` (checker.py, loop_controller.py, result_writer.py).  
**Perché**: i tre file erano funzioni singole chiamate esclusivamente da `utils/experiment_utils.py` — nessun motivo architetturale per tenerle separate.  
**Dove è andato il codice**:
- `check_math_answer` → funzione privata in `utils/experiment_utils.py`
- `write_result` → inlineato in `_save_result`
- `should_retry` → inlineato in `_route_after_check` (era una condizione, non una funzione)

### Agents: deduplicazione helper LLM

**Cosa**: creato `agents/_llm_utils.py` con `_extract_json_from_text`, `_start_spinner`, `_raise_ollama_unavailable`.  
**Perché**: le tre funzioni erano copie identiche in `agent_runner.py` e `judge_agent.py`.  
Rimosso anche il parametro `role` inutilizzato da `run_agent` (unico uso era codice commentato).

### Prompts: traduzione in inglese e pulizia ridondanza

**Cosa**: `agents/prompts.py` tradotto in inglese. Rimosso il blocco JSON dai prompt `expert` e `beginner`.  
**Perché**: ogni task specifica già il formato JSON richiesto — duplicarlo nel system prompt era ridondante e aumentava la probabilità di conflitti.

### Evaluation reports: da verboso a anomaly-focused

**Cosa**: riscritto `utils/evaluation_utils.py`. I report mostrano ora solo anomalie (wrong, retry, reasoning inconsistente). Se tutto è corretto: una riga di conferma + tabella compatta.  
**Perché**: i vecchi report elencavano tutto anche quando era tutto corretto — il reasoning identico ripetuto 3 volte per ogni task non aggiungeva informazione.

---

### Fix critico: prompt del judge fisso vs rubriche per-task

**Cosa**: aggiunta funzione `_build_judge_prompt(rubric)` in `utils/experiment_utils.py`. Il prompt del judge viene ora generato dinamicamente dalla rubrica del task.  
**Perché**: il vecchio prompt hardcoded usava categorie fisse (`classification_score`, `steps_score`, ecc.) che non corrispondevano alle rubriche reali dei task testuali:
- task3 richiede: `classification_score`, `reasoning_score`, `clarity_score`, `confidence_calibration_score`
- task4 richiede: `root_cause_score`, `diagnostic_steps_score`, `reasoning_score`, `clarity_score`

Il judge ignorava queste categorie e produceva punteggi non allineati alla rubrica.  
**Impatto**: i risultati precedenti su task3 e task4 non riflettono i criteri di valutazione reali e vanno rigirati.

### Fix: clamp e normalizzazione score judge

**Cosa**: in `_check_answer`, il `total_score` viene ora clamped a `[0, total_max]` e salvato anche come `normalized_score = total_score / total_max ∈ [0, 1]`.  
**Perché**: senza clamp, un judge che va fuori scala potrebbe produrre verdetti "correct" per overflow. La normalizzazione permette di comparare punteggi tra task con `total_max` diversi (task3=8, task4=9).

### Config: temperatura e token limit

**Cosa**:
- `TEMPERATURE` 0.0 → 0.3
- `OLLAMA_NUM_PREDICT` 256 → 1024
- Rimosso `NO_THINK_SUFFIX`

**Perché**:
- A `TEMPERATURE=0` le ripetizioni producono output identici per costruzione — la consistenza è garantita matematicamente e non misura nulla. Con 0.3 si ottiene varianza reale su cui misurare la consistenza.
- 256 token erano insufficienti per JSON con reasoning elaborato (possibile troncamento silenzioso).
- `NO_THINK_SUFFIX` era un workaround per qwen3 (thinking chain infinita); gemma4 non ha questo problema.

---

## Pendenti / decisioni aperte

| Item | Stato | Note |
|---|---|---|
| Modello judge | da fare | deve essere diverso da `expert` (gemma4:e2b) per evitare bias di auto-valutazione |
| Task più difficili | in valutazione col team | con 100% accuracy la differenza expert/beginner non emerge |
| Rigirare task3 e task4 | necessario | i run precedenti usavano il judge con categorie errate |
| deepseek-r1 thinking chain | monitorare | con `OLLAMA_NUM_PREDICT=1024` e `TASK_TIMEOUT_SECONDS=600` il rischio di blocco è ridotto ma non eliminato |
