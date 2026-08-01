# `utils/task_utils.py` — caricamento task, parsing metadata, deduplicazione risultati

## 1. Ruolo del modulo

`utils/task_utils.py` è il modulo che fa da ponte tra i file markdown in `docs/tasks/` e la struttura dati (`ExperimentState`, dict) che circola nel grafo LangGraph definito in `utils/experiment_utils.py`. Espone sette funzioni pure/quasi-pure: helper di naming per i file risultato (`_slugify`, `_model_slug`), lettura file (`_read_text`), parsing del metadata di un task (`_parse_task_metadata`), estrazione di blocchi JSON da testo libero (`_extract_json_blocks`), assemblaggio dello stato iniziale di un run (`_load_task`, nodo `"load_task"` del grafo — `utils/experiment_utils.py:466`), enumerazione dei task disponibili (`_list_tasks`) e due funzioni di idempotenza/consistenza usate da `main.py` per evitare di rieseguire repetition già salvate (`_result_exists`, `_answers_equal`). Non contiene logica di business sull'agente o sul giudice: è strettamente I/O + parsing + naming.

## 2. Formato atteso di un task

Dedotto da `_parse_task_metadata` (task_utils.py:24-32) e verificato contro `docs/tasks/task1_math_int.md` (math) e `docs/tasks/task5_vuln_pcf.md` (textual/vuln):

- Il file task (`<id>.md`) deve contenere, in un punto qualsiasi del testo, due righe in stile Markdown-bold:
  - `**ID:** <task_id>`
  - `**Tipo:** <task_type>` (valori osservati: `math`, `textual`)
- Il regex usato è "greedy fino a fine riga" (`.+` senza `re.MULTILINE` esplicito ma `re.search` su tutto il contenuto, quindi cattura fino al primo newline): `_task_id_match.group(1).strip()` toglie solo whitespace ai bordi, non gli eventuali doppi spazi Markdown (`  ` di fine riga usati per il line break) — vengono strippati dallo `.strip()`.
- Se manca **uno dei due marker**, viene sollevata `ValueError("Task metadata not found")` — nessun default, fail-fast.
- Nei file reali (`task1_math_int.md:3-5`, `task5_vuln_pcf.md:3-5`) c'è anche una terza riga `**Difficoltà:**` che **non** viene estratta: il parser ignora qualunque metadato oltre ID e Tipo.
- Il file soluzione (`<id>_sol.md`) non ha un formato di metadata verificato dal parser: viene letto per intero e passato a `_extract_json_blocks`, che cerca blocchi ` ```json ... ``` `. Per convenzione osservata in tutti i file `_sol.md` ispezionati:
  - il **primo** blocco JSON è la ground truth (`{"answer": ..., "type": ...}` per math, es. `task1_math_int_sol.md:19-25`; `{"answer": "...", "type": "textual_security_review"}` per textual, es. `task5_vuln_pcf_sol.md:11-16`);
  - il **secondo** blocco JSON (se presente) è la rubrica per il giudice (`{"rubrica": {...}, "total_max": N}`, es. `task5_vuln_pcf_sol.md:36-75`) — assente per i task math, dove la correttezza è un check deterministico e non serve un giudice LLM (vedi `docs/results_reference/schema_math.json`, campo `judge_score`).
- Riscontro con `schema_math.json`/`schema_textual.json`: entrambi documentano `task_id`/`task_type` come "producer: utils.task_utils._load_task" — coerente con quanto letto nel codice.

## 3. Dettaglio funzione per funzione

- **`_slugify(value)`** (task_utils.py:9-11): sostituisce ogni sequenza di caratteri non alfanumerici con `_` e strippa `_` iniziali/finali. Usata per costruire nomi di file sicuri a partire da nomi di modello arbitrari (es. `gpt-oss:20b` → `gpt_oss_20b`).
- **`_model_slug(model, is_hosted)`** (task_utils.py:14-17): applica `_slugify` al nome modello e antepone `hosted_` se `is_hosted=True`. Determina il nome file `<slug>.json` dentro la cartella risultati (coerente con `is_hosted` documentato in entrambi gli schema come "Reflected in the filename prefix hosted_").
- **`_read_text(path)`** (task_utils.py:20-21): wrapper di `Path.read_text(encoding="utf-8")`, nessuna gestione errori — un file mancante propaga `FileNotFoundError` al chiamante.
- **`_parse_task_metadata(task_content)`** (task_utils.py:24-32): due `re.search` su marker `**ID:**` e `**Tipo:**`; solleva `ValueError` se uno dei due manca; ritorna `{"task_id": ..., "task_type": ...}`. Vedi §2 per il dettaglio del formato.
- **`_extract_json_blocks(text)`** (task_utils.py:35-37): `re.findall(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)` seguito da `json.loads` su ogni match. Euristica non-greedy (`.*?`) che si ferma al primo `}` seguito da whitespace e ` ``` ` — vedi §6 per i rischi.
- **`_load_task(state)`** (task_utils.py:40-75): nodo del grafo LangGraph, riceve/ritorna `ExperimentState`.
  1. Legge `task_path` e `sol_path` da `state` (main.py li popola come stringhe assolute/relative ai file in `docs/tasks/`).
  2. Legge verbatim il contenuto del task (`task_content`) — questo testo **è** il corpo del prompt inviato all'agente (commento esplicito a task_utils.py:48-51 rimanda a `agents/prompts.py` per l'ordine di assemblaggio completo).
  3. Estrae metadata (`_parse_task_metadata`) e i blocchi JSON dal file soluzione (`_extract_json_blocks`); `ground_truth = json_blocks[0]` se presente altrimenti `{}`, `rubric = json_blocks[1]` se presente altrimenti `{}`.
  4. Side-effect condizionali sul testo del prompt, in ordine: se `config.SAST_HINT_ENABLED`, appende un blocco hint SAST (`utils.sast_hint.build_sast_hint_block`, keyed su `task_id`); se `config.CVSS_ESTIMATE_ENABLED` e `is_cvss_task(task_id, task_type)` (da `utils.cvss_utils`), inietta le istruzioni CVSS nel prompt. Questi due branch mutano `task_content` **dopo** che i metadata sono già stati estratti dal contenuto originale — quindi l'iniezione non può rompere il parsing di ID/Tipo.
  5. Aggiorna `state` con `task_id`, `task_type`, `task_content` (finale, con eventuali iniezioni), `ground_truth`, `rubric` e lo ritorna.
- **`_list_tasks(tasks_path)`** (task_utils.py:78-80): `Path(tasks_path).glob("*.md")`, filtrando via ogni file il cui nome termina in `_sol.md`; risultato ordinato alfabeticamente (`sorted`). Verificato contro il contenuto reale di `docs/tasks/`: la directory contiene sia varianti `_full` (es. `task6_vuln_udr_full.md`, `task7_vuln_amf_full.md`, `task8_vuln_udm_full.md`) sia le rispettive `_sol.md`/`_full_sol.md` — il glob le tratta come **task indipendenti** (non varianti secondarie di un unico task), perché il filtro guarda solo la desinenza `_sol.md`, non un pattern di famiglia. `main.py:142` distingue poi runtime-timeout in base a `FULL_TASK_SUFFIX in task_path.stem`.
- **`_result_exists(results_path, experiment_id, role, task_id, repetition, model, is_hosted=False)`** (task_utils.py:83-97): vedi §4.
- **`_answers_equal(a, b)`** (task_utils.py:100-101): vedi §4.

## 4. Logica di deduplicazione/idempotenza

- **Path del file risultato**: `<results_path>/<task_id>/<experiment_id>/<role>/<_model_slug(model, is_hosted)>.json` (task_utils.py:84-90) — un file per la quadrupla (task, experiment, role, model); tutte le repetition di quella quadrupla sono nell'array `repetitions` dentro lo stesso file (coerente con `schema_math.json`/`schema_textual.json`, "One file per (task, experiment, role, model); all repetitions are stored in the top-level 'repetitions' array").
- **`_result_exists`**: se il file non esiste → `False`. Se esiste, lo carica con `json.loads` e verifica se **esiste già una repetition con lo stesso indice** (`r.get("repetition") == repetition` per un qualunque `r` in `data.get("repetitions", [])`). Qualsiasi eccezione durante lettura/parsing (file corrotto, JSON malformato) viene catturata da un `except Exception` generico e trattata come "non esiste" (`return False`) — quindi un file corrotto **non blocca** una nuova esecuzione, anzi la forza silenziosamente (rischio di duplicare la repetition se il file esisteva ma era illeggibile).
- **Chiave di deduplicazione effettiva**: `(task_id, experiment_id, role, model, is_hosted, repetition)`. `main.py:128-138` la usa per contare le repetition mancanti (`remaining_repetitions`) prima di stimare il tempo worst-case, e di nuovo `main.py:188-198` dentro il loop di esecuzione vero e proprio per fare skip (`logger.info("Skip %s rep %s (already exists)", ...)`) senza richiamare l'agente/il giudice.
- **`_answers_equal(a, b)`**: confronto per **uguaglianza strutturale esatta** via `json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)` — non è usata per la deduplicazione dei risultati, ma per un check di **consistenza inter-repetition** in `main.py:246-251`: dopo ogni repetition, se la risposta finale (`final_answer`) differisce da quella della repetition precedente per lo stesso (experiment, task), viene loggata una riga in `consistency_lines`, poi scritta da `_record_consistency_finding` (main.py). Non impedisce l'esecuzione, è solo un report di variabilità del modello a `temperature > 0` sullo stesso prompt.

## 5. Decisioni di design osservabili + perché

Da `git log --follow --oneline -- utils/task_utils.py`:
```
c5e5dd3 Test empirico: rumore SonarQube grezzo iniettato nel prompt agente, nessun effetto misurato
567837b Centralize prompt text in agents/prompts.py; show full prompt in finding detail files
21cb72a Implement CVSS estimate evaluation (Blocco B) and share run 1 results
1865400 add hosted models and refactoring of result organization and track all info also the one printed in console
a9e5728 Refactor model configuration (online models now usable), enhance result collection, and improve logging for hosted models
3d1992a refactoring
```
- Il modulo nasce in `3d1992a` ("refactoring") già con l'insieme completo delle funzioni attuali tranne la firma di `_result_exists`, che allora era `(results_path, experiment_id, role, task_id, repetition)` — **senza** `model`/`is_hosted`.
- `a9e5728` ("add hosted models... enhance result collection") estende la firma di `_result_exists` aggiungendo `model: str, is_hosted: bool = False`: la deduplicazione è stata ristretta da "un file per (task, experiment, role)" a "un file per (task, experiment, role, model)" — decisione guidata dal supporto multi-modello/hosted introdotto in quel commit (più modelli → serve un file risultato per modello, altrimenti un secondo modello sovrascriverebbe o farebbe skip erroneamente sulle repetition del primo).
- I commit successivi (`21cb72a`, `567837b`, `c5e5dd3`) non toccano più `_result_exists`/`_answers_equal`/`_list_tasks`/`_parse_task_metadata`: il nucleo di parsing/deduplicazione è stabile dal 2026 in poi; i cambi riguardano solo `_load_task`, che ha accumulato i due branch condizionali di iniezione (SAST hint, CVSS) man mano che l'esperimento si espandeva, senza mai toccare l'estrazione di metadata/ground truth a monte.
- Nessun commit rinomina o cambia il contratto marker `**ID:**`/`**Tipo:**`: è la convenzione originale del progetto, non deducibile ulteriormente da git log oltre a "esisteva già al primo commit del modulo" — non ho trovato una discussione esplicita del perché di questo formato specifico nei commit ispezionati.

## 6. Punti aperti / fragilità

- **Regex di `_parse_task_metadata` fragile su varianti di formattazione**: richiede esattamente `**ID:**` e `**Tipo:**` (case-sensitive, keyword in italiano per `Tipo` mentre il resto del progetto è in inglese); un file che usasse `**Type:**` o un markup diverso (es. heading `## ID` invece di bold) fallirebbe con `ValueError` generico, senza indicare quale file è la causa (l'eccezione non include il path).
- **`_extract_json_blocks` non distingue semanticamente ground truth da rubrica**: si basa puramente sull'**ordine** dei blocchi ` ```json ` nel file `_sol.md` (primo = GT, secondo = rubrica). Se un file soluzione avesse un blocco JSON di esempio/illustrativo prima della GT vera, o se mancasse la GT ma fosse presente solo la rubrica, l'assegnazione sarebbe silenziosamente sbagliata (nessuna validazione di schema sul contenuto del blocco).
- **`_result_exists` inghiotte errori di parsing come "non esiste"**: un file risultato corrotto o parzialmente scritto (es. crash a metà `json.dump`) fa sì che quella repetition venga **rieseguita e probabilmente riappesa in coda** all'array `repetitions` esistente (dipende da come `_save_result` in `experiment_utils.py` scrive il file) invece di segnalare un errore esplicito — rischio di file risultato con repetition duplicate se il file esisteva-ma-illeggibile viene poi sovrascritto invece che accodato.
- **`_list_tasks` tratta le varianti `_full` come task a sé stanti**, non come parametro/variante di un task base: non c'è alcun collegamento esplicito nel codice tra `task6_vuln_udr.md` e `task6_vuln_udr_full.md` se non la convenzione di naming (`FULL_TASK_SUFFIX`, controllata solo per il timeout in `main.py`, non qui). Se in futuro si aggiungesse un file tipo `task10_extra_full_backup.md`, verrebbe incluso come task valido senza alcun controllo di coerenza con l'esistenza di un file `_sol.md` corrispondente — un `_load_task` con `sol_path` inesistente fallirebbe solo a runtime (`FileNotFoundError` da `_read_text`), non in fase di enumerazione.
- **`_answers_equal` è un confronto strutturale rigido**: due risposte semanticamente equivalenti ma con differenze di whitespace/ordine non deterministico in una lista annidata, o differenze minime di floating point (es. `confidence: 0.7` vs `0.70`), risultano "diverse" e generano un falso positivo nel report di consistenza — non è un problema di correttezza del check di deduplicazione (quello usa solo l'indice `repetition`, non `_answers_equal`), ma può gonfiare il conteggio di "risposte incoerenti" riportato da `_record_consistency_finding`.

Fonti: codice sorgente + git log + file dati in docs/tasks/docs/results_reference letti come schema, nessuna discussione in docs/ consultata.
