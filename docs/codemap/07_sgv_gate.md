# SGV — Syntactic Grounding Verifier (`utils/sgv.py`) e SAST hint (`utils/sast_hint.py`)

## 1. Ruolo nella pipeline

`utils/sgv.py` implementa un gate deterministico, senza accesso alla ground
truth, che valuta la fondatezza **formale** del report `CVSS Estimate`
prodotto dall'agente su task di security review: verifica che ogni finding
citi una funzione realmente presente nell'estratto di codice mostrato
all'agente, che (opzionalmente) lo snippet citato sia effettivamente rintracciabile
nel sorgente, e che il vettore CVSS sia sintatticamente completo/valido.
Il gate non giudica se il codice sia davvero vulnerabile — quel giudizio resta
al Judge LLM a valle — ma decide se far ripetere il tentativo all'agente
(`utils/experiment_utils.py:262-290`, nodo `check_sgv` del grafo LangGraph,
`utils/experiment_utils.py:468-476`). Il feedback restituito in caso di
fallimento è costruito per non rivelare mai quale funzione sia vulnerabile
(`utils/sgv.py:226-230`).

## 2. I controlli G1-G4

### G1 — validità dello schema (`g1_schema_check`, `utils/sgv.py:103-123`)
Verifica che:
- `cvss_estimate` non sia `None`/vuoto (`utils/sgv.py:107-108`);
- il dict non contenga la chiave `_raw` (marcatore di parsing fallito a monte)
  e che `findings` sia effettivamente una lista (`utils/sgv.py:109-113`);
- la lista `findings` non sia vuota (`utils/sgv.py:115-116`);
- ogni finding abbia i campi obbligatori `function`, `vector`, `score`
  (`_REQUIRED_FIELDS`, `utils/sgv.py:33`), più `snippet` se
  `config.SGV_SNIPPET_ENABLED` è vero (`utils/sgv.py:118-122`).

Nessuna soglia numerica; è un controllo di presenza/struttura. Se fallisce, è
l'unico controllo eseguito: G2-G4 non vengono nemmeno provati
(`run_sgv`, `utils/sgv.py:185-191`) e il feedback è generico
("errore di formato: ...").

### G2 — esistenza del simbolo (`g2_symbol_check`, `utils/sgv.py:126-133`)
Confronto case-insensitive tra il campo `function` del finding e l'insieme
`F` delle funzioni estratte dal codice mostrato all'agente
(`extract_source_functions`, `utils/sgv.py:51-62`), non la ground truth.
L'estrazione usa una regex su blocchi ` ```go ` (`_GO_FUNC_RE`,
`utils/sgv.py:35-38`) che cattura sia funzioni semplici sia metodi con
receiver, e registra entrambe le forme (`nome` e `receiver.nome`, entrambe
lowercase) nel set. Se il nome non è nel set, fallisce con messaggio
"la funzione '...' non è presente nell'estratto di codice sottoposto".

### G3 — groundedness dello snippet (`g3_groundedness_check`, `utils/sgv.py:136-158`)
Opzionale: eseguito solo se `config.SGV_SNIPPET_ENABLED` è `True`
(default in `config.py:101`). Due livelli:
1. **Substring match** dopo normalizzazione: whitespace collassato
   (`_normalize_whitespace`, `utils/sgv.py:65-66`) e spazi adiacenti a
   punteggiatura rimossi (`_normalize_code` / `_PUNCT_SPACE_RE`,
   `utils/sgv.py:74-79`) — pensato per neutralizzare l'artefatto di andare a
   capo dentro una chiamata multi-linea (es. `MatchString(\n\t\t"...")`).
2. **Fallback Jaccard su finestre**: se il substring match fallisce,
   `_windowed_jaccard` (`utils/sgv.py:89-100`) calcola la similarità Jaccard
   sui token tra lo snippet normalizzato e ogni finestra di 1-3 righe
   consecutive del sorgente (`max_window=3`, hardcoded come default
   parametro), prendendo il massimo. La soglia di accettazione è
   `config.SGV_SNIPPET_JACCARD_THRESHOLD`, default `0.8`
   (`config.py:104`, letta a runtime in `utils/sgv.py:195`).
   Se il massimo è sotto soglia, fallisce con messaggio che riporta il
   valore di similarità osservato e la soglia.

### G4 — validità del vettore CVSS (`g4_vector_check`, `utils/sgv.py:161-173`)
- Il campo `vector` deve essere una stringa non vuota.
- Riusa `utils.cvss_eval._parse_vector` per estrarre le metriche dal vettore,
  poi verifica che ogni metrica in `REQUESTED_METRICS` (import da
  `utils.cvss_eval`) abbia un valore ammesso secondo `SEVERITY_ORDER[metric]`
  (stesso modulo). Nessuna soglia propria: la validità è definita
  interamente dai dizionari di `cvss_eval.py`.
- Il campo `score` deve essere presente e numerico (`int`/`float`).

### Orchestrazione (`run_sgv`, `utils/sgv.py:176-231`)
Per ogni finding esegue G2, (opzionale) G3, G4 e li combina in AND
(`finding_ok = g2_ok and g3_ok and g4_ok`, `utils/sgv.py:214`). Il report
finale è `passed` = AND su tutti i finding. In caso di fallimento, il
`feedback` testuale elenca, per ciascun finding fallito, il codice del check
(G2/G3/G4) e il messaggio d'errore associato, prefissato da un chiarimento
esplicito che non riguarda la correttezza sostanziale
(`utils/sgv.py:226-230`).

## 3. `sast_hint.py`: costruzione dell'hint SonarQube

Modulo indipendente da SGV, usato per un esperimento separato (iniezione di
rumore SAST grezzo nel prompt, per misurarne l'effetto).

- `is_sast_hint_task(task_id)` (`utils/sast_hint.py:41-43`): vero se il
  `task_id` inizia con uno dei prefissi mappati in `_TASK_NF_MAP`
  (`utils/sast_hint.py:18-23`: `task5_vuln_pcf→PCF`, `task6_vuln_udr→UDR`,
  `task7_vuln_amf→AMF`, `task8_vuln_udm→UDM`).
- `_load_alerts(dataset_path)` (`utils/sast_hint.py:33-38`): legge un JSON da
  `dataset_path`, ritorna la lista sotto la chiave `"alerts"` (lista vuota se
  il file non esiste).
- `build_sast_hint_block(task_id, dataset_path)` (`utils/sast_hint.py:46-65`):
  determina l'NF dal `task_id`, filtra gli alert del dataset per
  `nf_abbr == nf`, li ordina per `line` (`utils/sast_hint.py:63`, chiave
  `a.get("line") or 0`), e per ciascuno formatta una riga con il template
  `SAST_HINT_ALERT_LINE` (`agents/prompts.py:88`:
  `"- L{line} [{severity}] {rule_key}: {message}"`). Il blocco finale è
  `SAST_HINT_HEADER + righe + SAST_HINT_FOOTER` (`agents/prompts.py:71-85`),
  dove l'header include un'istruzione esplicita all'agente di non assumere
  che ogni alert sia una vulnerabilità reale. Ritorna stringa vuota se non
  c'è NF mappata o non ci sono alert per quell'NF.

Il dataset consumato è indicato da commento come proveniente da
`docs/sast_tools/ground_truth_vuln_files.json` (non ispezionato in questa
analisi: fuori dallo scope dei due file assegnati).

## 4. Punti di chiamata

- `utils/task_utils.py:60-61`: se `config.SAST_HINT_ENABLED`, il blocco viene
  concatenato al `task_content` prima dell'eventuale iniezione delle
  istruzioni CVSS.
- `agents/prompts.py:14-15`: documenta la posizione del blocco SAST hint
  nell'ordine di assemblaggio del prompt finale (punto 3 su 6).
- `utils/experiment_utils.py:271`: `run_sgv(state["task_content"], cvss_estimate)`
  invocato dentro `_check_sgv`, che a sua volta è collegato nel grafo
  LangGraph come nodo `check_sgv` (`utils/experiment_utils.py:468`), con edge
  da `run_agent` (`utils/experiment_utils.py:474`) e routing condizionale
  `retry`/`check_answer` tramite `_route_after_sgv`
  (`utils/experiment_utils.py:476`).

Non è stata rianalizzata la logica interna di `experiment_utils.py` o
`task_utils.py` oltre ai punti di chiamata sopra.

## 5. Decisioni di design osservabili (da git log)

- Commit `02603a0` (2026-07-14, "Implement SGV G1-G4"): introduzione
  originaria di tutti e quattro i controlli in un solo commit, insieme al
  wiring come nodo `check_sgv` nel grafo di retry, indipendente dal retry
  guidato dal Judge sulla rubrica. Il messaggio di commit dichiara
  esplicitamente G2 verificato "against the source shown to the agent (not
  the GT)" — coerente con quanto osservato nel codice (`extract_source_functions`
  legge solo i blocchi ` ```go ` del task, mai la ground truth).
- Commit `5d97f35` (stesso giorno, ~1h dopo, "Fix SGV G3 false positive on
  multi-line source statements + G2 multi-function prompt gap"): a seguito
  di una prima run reale (15 casi su task5-9, variante "1A"), due bug
  emersi e corretti, esplicitamente non attribuiti ad allucinazioni del
  modello:
  - G3 dava falsi positivi/negativi per via di una normalizzazione
    whitespace troppo grezza che lasciava uno spazio spurio accanto alla
    punteggiatura quando una chiamata Go va a capo su più righe; risolto
    con `_normalize_code` (rimozione spazi adiacenti a punteggiatura) e
    `_windowed_jaccard` (confronto su finestre di 1-3 righe invece che
    riga-singola).
  - Il commit dichiara esplicitamente una scelta di design: **non**
    aggiungere un fallback LLM per G3, perché reintrodurrebbe il problema di
    non-riproducibilità/leakage/costo che SGV esiste per evitare nel loop
    (citazione dal commit message: "Deliberately not adding an LLM fallback
    level for G3 — would reintroduce the non-reproducibility/leakage/cost
    the SGV exists to avoid in the loop").
  - Il gap G2 (un finding che copre più funzioni impacchettate in un solo
    campo `function`) non è stato risolto nel codice di `sgv.py` stesso, ma
    tramite modifica al prompt (`agents/prompts.py`), istruendo l'agente a
    ripetere il blocco di finding una volta per funzione coinvolta.
- Commit `c5e5dd3` (2026-07-21, "Test empirico: rumore SonarQube grezzo..."):
  introduzione di `sast_hint.py` come esperimento a sé stante, con dataset
  dichiarato (nel commento di modulo e nel commit message) come 54 alert di
  cui 0 corrispondenti a una CVE target — l'iniezione è deliberatamente
  "grezza"/non curata per misurare l'effetto del rumore così com'è, non
  quello di un sottoinsieme filtrato.

Il "perché" della scelta delle soglie numeriche specifiche (0.8 per Jaccard,
finestra max 3 righe) non è deducibile dai commit message: sono presentate
come valori scelti, non derivati da una misurazione riportata nel codice o
nei messaggi di commit.

## 6. Punti aperti / fragilità osservabili nel codice

- **Soglia Jaccard 0.8 hardcoded come default** (`config.py:104`) senza
  alcuna calibrazione visibile nel codice: nessun test o dato di
  validazione è referenziato nei commenti o nei commit per giustificare
  proprio questo valore.
- **Finestra massima 3 righe hardcoded** come default del parametro
  `max_window` in `_windowed_jaccard` (`utils/sgv.py:89`): copre statement Go
  che si spezzano su fino a 3 righe fisiche; uno statement più lungo non
  avrebbe alcuna finestra di confronto valida e G3 fallirebbe anche per uno
  snippet corretto.
- **G2 case-insensitive puro**: due funzioni con lo stesso nome ma package/
  receiver diversi nello stesso estratto di codice collasserebbero sullo
  stesso elemento del set `F` (`utils/sgv.py:59-61`), un falso negativo
  teorico per gate G2 non rilevabile dal solo codice.
- **Regex `_GO_FUNC_RE`** (`utils/sgv.py:35-38`) è un parser regex-based del
  Go, non un vero parser AST: costruzioni sintattiche non standard (es.
  funzioni generiche con parametri di tipo, receiver con puntatori a slice,
  ecc.) potrebbero non essere catturate, con conseguente falso negativo di
  G2 per funzioni realmente presenti.
- **`extract_source_blocks`** concatena tutti i blocchi ` ```go ` del task
  con un semplice `"\n".join(...)` (`utils/sgv.py:45-48`): se il task
  contiene più blocchi di codice appartenenti a file diversi, la
  concatenazione perde ogni informazione di provenienza per-file, e
  `g3_groundedness_check`/`_windowed_jaccard` potrebbero far matchare uno
  snippet contro righe di un file diverso da quello effettivamente citato.
- **`sast_hint.py` dipende da un mapping statico `_TASK_NF_MAP`**
  (`utils/sast_hint.py:18-23`) limitato a 4 prefissi di task; un nuovo task
  con un NF non mappato non riceve mai l'hint senza modifica del codice.
- **`_load_alerts`** non valida lo schema del JSON oltre `.get("alerts", [])`
  (`utils/sast_hint.py:33-38`): un file malformato o con chiave assente
  ritorna silenziosamente lista vuota, senza segnalazione di errore.

Fonti: solo codice sorgente + git log, nessun documento in docs/ consultato.
