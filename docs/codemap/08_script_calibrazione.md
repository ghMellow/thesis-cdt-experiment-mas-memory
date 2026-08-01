# Codemap 08 — `scripts/judge_calibration/`

## 1. Ruolo della cartella

I quattro file sono script standalone, eseguibili solo da riga di comando (`python scripts/judge_calibration/<script>.py [...]`), ciascuno con un blocco `if __name__ == "__main__": main()`. Nessuno dei quattro è importato o richiamato da `main.py`: un `grep -rn` di `judge_calibration|calibrate_threshold|rejudge_cross_family|run_c1c2|run_gtfree_rubric` su `main.py` non produce risultati. Non fanno quindi parte del flusso automatico dell'esperimento (agenti → giudice → report), ma sono strumenti di analisi/calibrazione a posteriori che leggono gli artefatti già prodotti in `results/` (o materiali fissi in `docs/tasks/` e `docs/judge_rubric/calibration_c1c2/`) e producono report separati in `results/evaluation/judge_calibration/`. Tutti e quattro sono stati introdotti nello stesso commit `0e1bd50` (16/7, tranne `run_gtfree_rubric.py` che nasce dopo, vedi §4) e condividono lo stesso pattern: `sys.path.insert` verso la root del progetto, import di `config`, output sia `.json` (dati grezzi) sia `.md` (report leggibile con tabelle), stessa directory di output `OUT_DIR = results/evaluation/judge_calibration/`.

Tre dei quattro (`rejudge_cross_family.py`, `run_c1c2.py`, `run_gtfree_rubric.py`) importano `run_judge_textual` da `agents/judge_agent.py` (firma a `agents/judge_agent.py:90-99`, non ri-analizzata qui) e `build_judge_prompt` da `utils/experiment_utils.py`: effettuano quindi vere chiamate LLM al giudice. `calibrate_threshold.py` è l'unico a non fare alcuna chiamata LLM (dichiarato esplicitamente nel proprio docstring, riga 3).

## 2. `calibrate_threshold.py` (157 righe)

**Input**: nessun argomento CLI. Legge ricorsivamente `results/*/*/agent/*.json` (`calibrate_threshold.py:29`) — i risultati già salvati dalle run sperimentali complete (contengono `repetitions[].judge_score` e `repetitions[].cvss_eval` già calcolati in precedenza).

**Algoritmo**:
- `collect_repetitions()` (righe 25-58) filtra solo `task_type == "textual"`, e per ogni ripetizione richiede che siano già presenti `judge_score.normalized_score` e `cvss_eval.matched`. Salta (in `skipped`) le ripetizioni con `cvss_eval.n_target_cves == 0`, perché in quel caso il match deterministico M1 è indefinito (nessuna CVE target mappata al task, es. task cross-file — commento riga 39-40).
- Per ogni riga calcola due varianti del match deterministico: `m1` = almeno una CVE target trovata (`len(matched) > 0`) e `m1_strict` = nessuna CVE mancata (`len(missed_cves) == 0`).
- `sweep()` (righe 61-73) fa uno sweep di soglie da 0.05 a 1.00 a passi di 0.05 (`range(5, 101, 5)`, riga 81) e per ciascuna soglia calcola: accordo (verdetto LLM ≥ soglia coincide col target deterministico), falsi positivi (`false_pass`: sopra soglia ma target negativo) e falsi negativi (`false_fail`: sotto soglia ma target positivo).
- `main()` esegue lo sweep sia contro `m1` sia contro `m1_strict`, trova la soglia con accordo massimo (`best`/`best_strict`) e il plateau di soglie equivalenti, e confronta col valore attualmente in uso `config.TEXTUAL_PASS_RATIO` (riga 90-93).

**Output**: `results/evaluation/judge_calibration/threshold_calibration.json` (righe grezze + curve complete) e `threshold_calibration.md` (statistiche riassuntive, tabella soglia→accordo/FP/FF, tabella per-ripetizione con verdetto salvato vs M1/M1-strict). Il risultato viene anche stampato a video (riga 153).

## 3. `rejudge_cross_family.py` (139 righe)

**Input**: argomenti CLI `--model` (default `gpt-oss:20b`) e `--local` (usa Ollama locale invece dell'API hosted, riga 60-63). Legge gli stessi file `results/*/*/agent/*.json`, ma a differenza dello script precedente usa anche `data["task_path"]` e `data["sol_path"]` per rileggere il task originale e la rubrica (tramite `load_rubric_and_task`, righe 35-39, che estrae il secondo blocco JSON dal file soluzione con `_extract_json_blocks` — funzione importata da `utils/task_utils.py`, non ri-analizzata qui) e `rep["final_answer"]`, cioè il report testuale prodotto dall'agente.

**Algoritmo**: per ogni ripetizione textual già giudicata, richiama `run_judge_textual` (da `agents/judge_agent.py`) con lo stesso prompt (`build_judge_prompt(rubric)`, da `utils/experiment_utils.py`), la stessa temperatura di sistema (`config.TEMPERATURE`) e lo stesso `final_answer`, ma con un modello giudice diverso passato da CLI — quindi nessuna nuova esecuzione degli agenti, solo un secondo giudizio "cross-family" sullo stesso materiale. Il punteggio nuovo viene rinormalizzato con `normalize()` (righe 42-54), che replica esattamente la logica di normalizzazione del nodo giudice in-loop (somma dei campi `*_score` se `total_score` assente, clamp fra 0 e `total_max`, divisione per `total_max`). Calcola poi il delta fra normalized_score originale e nuovo, e il numero di "flip" di verdetto a due soglie fisse (0.7 e 0.65, funzione `verdicts()` righe 108-113).

**Output**: `cross_family_<model_slug>.json` (righe con delta e nuovi punteggi/feedback) e `cross_family_<model_slug>.md` (delta medio, conteggio flip a t=0.7/0.65, tabella per ripetizione). Lo slug del nome modello è generato da `_model_slug()` (da `utils/task_utils.py`).

## 4. `run_c1c2.py` (139 righe)

**Input**: argomenti `--model` (default: `None` → risolve il modello giudice di sistema via `resolve_model_config("judge")` da `agents/_llm_utils.py`), `--local`, `-k` (ripetizioni per report, default 3). Legge un set fisso di materiali di calibrazione preconfezionati in `docs/judge_rubric/calibration_c1c2/task*_C[12].json` (righe 34, 63): per ogni task esistono due varianti già scritte a mano/generate — **C1** (report corretto, riscritto) e **C2** (report plausibile ma sbagliato) — più il task originale (`docs/tasks/<task_id>.md`) e la soluzione/rubrica (`docs/tasks/<task_id>_sol.md`).

**Algoritmo**: per ciascun report C1/C2, ripete il giudizio K volte (default 3) con lo stesso giudice/prompt/temperatura del flusso normale, poi calcola:
- `CGP` (Calibration Gap) = media(punteggio C1) − media(punteggio C2), complessivo e per task (righe 118-119, 127-132);
- tasso di promozione di C2 (falso positivo del giudice, cioè un report sbagliato che supera la soglia) a t=0.7 e t=0.65;
- tasso di bocciatura di C1 (falso negativo) a t=0.65.

Questo è l'unico degli script che introduce esplicitamente un test di ammissione binario per il giudice basato su materiale "verità nota per costruzione" (C1 sempre corretto, C2 sempre sbagliato), a differenza di `calibrate_threshold.py` che calibra una soglia numerica sui dati reali già raccolti, e di `rejudge_cross_family.py` che confronta giudici diversi sullo stesso materiale reale.

**Output**: `c1c2_<model_slug>.json` (righe con punteggi/scores/feedback per k-esima ripetizione) e `c1c2_<model_slug>.md` (CGP complessivo, promozioni/bocciature, tabella per task con media e min-max di C1/C2).

## 5. `run_gtfree_rubric.py` (292 righe)

**Input**: argomenti `--set {c1c2,saved}` (obbligatorio), `--model`, `--local`, `-k` (default 3), `--rubric` (default `docs/judge_rubric/gtfree/rubric_v1.json`), `--coverage {functions,surfaces}` (default `functions`), `--motivations` (flag). A differenza degli altri tre, la rubrica non è più quella "ground-truth-derivata" del task (`*_sol.md`) ma una rubrica **task-independent** caricata da file esterno (righe 206-207), pensata per valutare un report senza conoscere la soluzione attesa.

**Algoritmo — doppio meccanismo di punteggio**:
1. **Componente LLM**: `judge_k()` (righe 91-121) giudica K volte con la rubrica GT-free e — se `--motivations` è attivo — un'istruzione aggiuntiva (`MOTIVATION_INSTRUCTION`, righe 61-68) che obbliga il giudice a motivare ogni criterio sotto il massimo e a cercare attivamente controesempi prima di dare punteggio pieno.
2. **Componente coverage deterministica** (0-2, stile "SGV G2"): `task_functions()` (righe 71-76) estrae dal testo del task le funzioni Go citate, con due modalità via regex — `GO_FUNC_RE` (tutte le funzioni, v1) o `GO_SURFACE_RE` (solo funzioni con parametro `*gin.Context`, cioè handler HTTP esposti a input esterno o middleware, v2 — commento righe 54-57). `coverage_score()` (righe 79-88) calcola il rapporto fra funzioni citate nel report e il minimo fra funzioni totali e un cap `COVERAGE_DENOM_CAP = 6` (il cap esiste perché — commento righe 49-51 — sui file `_full` con ~100 funzioni un rapporto assoluto renderebbe la copertura piena irraggiungibile per qualunque report onesto); soglie 2/3 → punteggio 2, 1/3 → 1, altrimenti 0.
3. `combined()` (righe 124-128) unisce le due componenti: `(media punteggi LLM + coverage) / (total_max_rubrica + 2)`.

Due modalità `--set` con logica separata:
- **`c1c2`** (`run_c1c2()`, righe 135-152): stesso materiale C1/C2 di `run_c1c2.py`, ma giudicato con la rubrica GT-free — permette di confrontare il CGP GT-free con il CGP baseline GT-derivato (+0.948, hard-coded come commento/stringa di confronto riga 231, proveniente dal run del commit `0e1bd50`).
- **`saved`** (`run_saved()`, righe 155-190): rilegge i report reali salvati in `results/*/*/agent/*.json` (stesso pattern degli altri script), calcola il flip rate fra verdetto GT-derivato originale e nuovo verdetto GT-free combinato, e l'accordo con M1-strict (stesso concetto usato in `calibrate_threshold.py`, qui ricalcolato localmente riga 178-181 anziché riusato).

Il nome del file rubrica determina automaticamente il prefisso di output e il riferimento doc: `version = regex r"v(\d+)"` sul nome file (righe 208-212) — `v1`→prefix `gtfree`, `v2`→`gtfree_v2`, ecc. (mappatura versione→doc `{"1":"10","2":"12","3":"14"}` hard-coded riga 212, usata solo per l'intestazione del report, non per logica).

**Output**: `<prefix>_<set>_<model_slug>.json` e `.md`, con tabelle diverse per i due `--set` (CGP e promozioni per `c1c2`; flip rate e accordo M1-strict per `saved`).

## 6. Tabella di confronto rapido

| Script | Cosa calibra/testa | Chiamate LLM | Input principale | Metrica chiave | Quando usarlo |
|---|---|---|---|---|---|
| `calibrate_threshold.py` | Soglia numerica `TEXTUAL_PASS_RATIO` | Nessuna (rilegge punteggi già salvati) | `results/*/*/agent/*.json` | Accordo soglia↔M1/M1-strict su sweep 0.05–1.00 | Dopo ogni batch di run reali, per verificare se la soglia in `config.py` è ancora quella ottimale |
| `rejudge_cross_family.py` | Bias di famiglia del giudice (self-enhancement) | Sì, 1 giudizio extra per ripetizione con modello diverso | `results/*/*/agent/*.json` (stesso `final_answer`) | Delta medio + flip rate a t=0.7/0.65 | Per verificare se il giudice di sistema favorisce report generati da modelli della propria famiglia |
| `run_c1c2.py` | Ammissione del giudice su materiale a verità nota (rubrica GT-derivata) | Sì, K giudizi per report C1/C2 | `docs/judge_rubric/calibration_c1c2/task*_C[12].json` | CGP = media(C1) − media(C2); promozioni C2 / bocciature C1 | Per certificare che un giudice/modello distingue in modo affidabile un report corretto da uno plausibile-ma-sbagliato, prima di fidarsene in produzione |
| `run_gtfree_rubric.py` | Ammissione di rubriche GT-free (senza soluzione nota) + variante coverage | Sì, K giudizi per report, su due `--set` | `calibration_c1c2/` oppure `results/*/*/agent/*.json` + rubrica esterna JSON | CGP GT-free (vs baseline +0.948) e flip rate / accordo M1-strict | Per iterare su varianti di rubrica task-independent (v1/v2/v3...) quando si vuole valutare senza dipendere dalla soluzione di riferimento |

## 7. Decisioni di design osservabili

- **Riuso della stessa formula di normalizzazione in tre punti** (`calibrate_threshold.py` non la ha perché rilegge score già normalizzati; ma `rejudge_cross_family.py:42-54`, `run_c1c2.py:38-47` e `run_gtfree_rubric.py:110-118` la ricalcolano ciascuno per conto proprio) — nessun commit message spiega perché non sia stata fattorizzata in `utils/`; è un fatto osservabile dal codice, non una scelta motivata rintracciabile.
- **`COVERAGE_DENOM_CAP = 6`** in `run_gtfree_rubric.py:51` è giustificato esplicitamente nel commento adiacente (righe 49-51): senza cap, i task `_full` con ~100 funzioni renderebbero la copertura piena irraggiungibile. Decisione di design motivata nel codice stesso.
- **Introduzione progressiva delle rubriche GT-free**: dal git log, `run_gtfree_rubric.py` nasce nel commit `e0f76ec` insieme alla rubrica v1, che secondo il messaggio di commit "non supera la propria ammissione" (CGP crolla da +0.948 a +0.437, 2/5 falsi positivi promossi). Il commit successivo `26914a2` introduce v2 con ammissione solo parziale (CGP +0.600, 0/5 promossi ma non specificato se supera del tutto). Il commit `8803cb9` ("test fallimentare gt free v3") indica che anche una terza iterazione non ha superato il test — ma il messaggio di commit è troppo breve per dedurre in che modo v3 fallisca; non deducibile dal solo commit senza leggere docs/.
- **`--coverage surfaces`** (v2) restringe la copertura alle sole funzioni con parametro `*gin.Context`: motivato nel commento righe 54-57 come "risk surface" — handler HTTP/middleware esposti a input esterno — ma il *perché* si sia scelto proprio questo sotto-insieme (anziché altri euristiche di rischio) non è spiegato nel codice né nei commit visibili; è presentato come riferimento a un "doc 12 par. 4" che non è stato consultato per questa analisi.
- **`--motivations`** in `run_gtfree_rubric.py` (righe 61-68, 202-203) è un'istruzione di prompt aggiuntiva per forzare il giudice a cercare controesempi prima di dare punteggio massimo — tentativo di mitigare un bias di acquiescenza osservato empiricamente (deducibile dal fatto che esiste come flag opzionale, introdotto dopo la rubrica v1 base); il commit associato a questo flag specifico non è isolabile dal log raccolto (compare già nel file al momento della sua introduzione più recente, non tracciabile riga per riga senza `git log -L`).

## 8. Punti aperti / fragilità / duplicazione di codice

- **Duplicazione della logica di normalizzazione punteggio** (somma `*_score`, clamp, divisione per `total_max`) ripetuta identica in tre file (`rejudge_cross_family.py:42-54`, `run_c1c2.py:38-47`, `run_gtfree_rubric.py:110-118` con lievi differenze di stile) — nessuna funzione condivisa in `utils/`.
- **Pattern di lettura `results/*/*/agent/*.json` con lo stesso filtro `task_type == "textual"`** duplicato in tutti e quattro gli script (`calibrate_threshold.py:29-32`, `rejudge_cross_family.py:66-70`, `run_gtfree_rubric.py:157-160`); `run_c1c2.py` non lo fa perché legge sempre dal set fisso C1/C2.
- **Calcolo di `m1_strict`** (nessuna CVE mancata) è implementato due volte con logica leggermente diversa: in `calibrate_threshold.py:53` (`len(cvss["missed_cves"]) == 0`) e in `run_gtfree_rubric.py:178-181` (stessa condizione ma con guardia esplicita su `n_target_cves > 0` altrimenti `None`) — la prima versione non gestisce esplicitamente il caso `n_target_cves == 0` nel calcolo di `m1_strict` stesso (lo fa a monte, escludendo la riga interamente in `collect_repetitions`), quindi le due implementazioni non sono meccanicamente identiche pur calcolando lo stesso concetto.
- **Mappatura versione-rubrica→documento hard-coded** in `run_gtfree_rubric.py:212` (`{"1": "10", "2": "12", "3": "14"}`) è fragile: se si introduce una v4 senza aggiornare questo dizionario, il riferimento doc nel report stampato sarà silenziosamente `"??"` (comportamento di fallback esplicito, non un crash, ma un'informazione persa senza segnalazione).
- **Hard-coding di valori di baseline nel testo del report**: `run_gtfree_rubric.py:231` stampa `"baseline GT-derivata (doc 09): +0.948"` e riga 269 `"(baseline GT-derivata: 12/12)"` come stringhe letterali nel codice — se il baseline cambia (nuova run di `run_c1c2.py`), questi valori nel report di `run_gtfree_rubric.py` non si aggiornano automaticamente e richiedono modifica manuale del sorgente.
- **Nessuna gestione di errori per rubric/task file mancanti**: tutti gli script che leggono `docs/tasks/<task_id>.md` o `docs/judge_rubric/...` assumono l'esistenza dei file (nessun try/except attorno a `Path.read_text`), quindi un file mancante causa un traceback non gestito piuttosto che un messaggio d'errore mirato.
- **Soglie 0.7/0.65 hard-coded in più punti** (`rejudge_cross_family.py:122-123`, `run_c1c2.py:110-112`, `run_gtfree_rubric.py:232-234,249-256`) invece di essere lette da `config.TEXTUAL_PASS_RATIO` come fa `calibrate_threshold.py:90` — incoerenza: se la soglia in `config.py` cambiasse, questi tre script continuerebbero a riportare le soglie 0.7/0.65 come riferimento fisso, scollegate dal valore configurato.

---

Fonti: solo codice sorgente + git log, nessun documento in docs/ consultato.
