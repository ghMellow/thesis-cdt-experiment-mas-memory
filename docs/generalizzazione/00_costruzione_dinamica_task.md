# Generalizzazione — costruzione dinamica del task

Discussione aperta il 2026-08-24, a partire dal punto del relatore in call 2026-08-20
(trascrizione in `~/Desktop/Politecnico/_Tesi/tesi-vault/raw/calls/2026-08-20-diciottesima-call.md`,
esterna a questo repo): "il sistema è agnostico da NF... l'idea potrebbe essere di puntare
su una directory, vede che è cambiato qualcosa nel codice, rilancia il valutatore — è una
delle prime funzioni di percezione del CDT". Questo file traccia l'implementazione, non
riscrive la call.

## Perché non è "solo" un problema di task

Oggi il sistema **non genera niente dinamicamente**: task, ground truth e rubrica sono
tre file statici scritti a mano per ogni CVE nota, prima ancora di lanciare una run.

- `docs/tasks/<task>.md` — il prompt esatto mandato all'agente (scenario + estratto di
  codice Go + istruzioni di formato), letto verbatim da `utils/task_utils.py::_load_task`
  (`task_content` = contenuto del file, nessuna elaborazione).
- `docs/tasks/<task>_sol.md` — **ground truth e rubrica nello stesso file**, come due
  blocchi JSON estratti per posizione (`json_blocks[0]` = GT, `json_blocks[1]` = rubrica) —
  vedi `utils/task_utils.py:57-58`. Non esiste un percorso di codice che li generi: sono
  scritti a mano conoscendo già la CVE.
- `File_Free5gc_Vulnerabili/cve_metrics_normalized.json` — dataset CVSS con
  `handler_functions` per CVE, usato dal matching deterministico in
  `utils/cvss_eval.py::_candidate_cves`/`_match_finding`. Anche questo presuppone che la
  vulnerabilità target sia già nota e mappata a funzioni specifiche.

Quindi "costruire il task dinamicamente" risolve solo il primo dei tre. Se punto il
sistema su una repo o un diff arbitrari, **non ho più GT né rubrica specifica**.

**Correzione (2026-08-24, dopo rilettura di `docs/judge_rubric/15_stato_attuale_gtfree.md`):**
metà del problema è già risolta, non è lavoro nuovo. La rubrica GT-free **v2**
(`docs/judge_rubric/gtfree/rubric_v2_draft.json`) valuta la **correttezza** di un report —
ogni finding è ancorato a evidenza reale nel codice citato, i claim di assenza mostrano il
percorso che dovrebbe avere il controllo mancante, una debolezza per finding, classe
plausibile — **senza mai guardare una GT** (CGP +0.600, zero falsi positivi/negativi sul
banco C1/C2 sintetico, doc 13). Per il flusso generico questa parte si riusa così com'è,
nessuna riscrittura.

Quello che resta aperto, e che nessuna rubrica può chiudere per costruzione (doc 15 §4), è
la **completezza**: sapere se il report ha trovato *tutte* le vulnerabilità presenti
richiede sapere quante ce ne sono — informazione che il GT-free rinuncia ad avere per
definizione. La conclusione già scritta nei doc 13-14-15 è che serve un **enumeratore
esterno di candidate** (proposta G5/SAST, mai implementata), non un'altra iterazione di
rubrica. Le metriche deterministiche M1-M3/S1-S3 (`utils/cvss_eval.py`) restano quindi
legate al dataset di CVE note del benchmark attuale e non si generalizzano da sole — sul
flusso generico la loro funzione (misurare completezza) la prenderebbe l'enumeratore
esterno, se costruito, altrimenti resta un buco noto e dichiarato, non silenzioso.

## Le due modalità

### A — analisi di una repo esistente, file per file

Punto il sistema su una directory di codice reale (non un estratto curato) e produco un
task per file (o per package/funzione) chiedendo "trova vulnerabilità qui".

Problemi aperti:
- **Selezione/chunking**: una repo intera non entra nel contesto. Serve una strategia di
  split (per file? per funzione esportata? per package?) — e quella scelta cambia cosa
  "un task" significa, quindi cambia anche cosa vuol dire TP/FP/FN nelle metriche esistenti.
- **Correttezza vs completezza**: la correttezza dei claim si valuta già senza GT (rubrica
  v2, riusabile). Manca solo la completezza — senza un enumeratore esterno di candidate
  (SAST/G5, mai costruito) non si può dire "ha trovato tutto quello che c'è" su un file
  ignoto, solo "quello che ha trovato è vero".
- **Rumore/falsi positivi**: proprio il punto §3.5 di `docs/supporto/calls/call_3.md`,
  mai risolto (task di controllo negativo) — su codice reale ignoto il problema si
  amplifica, non è più opzionale.

### B — diff tra push git successivi

Punto il sistema su un repo con storia, costruisco il task dal `git diff` tra due commit
(es. ogni push, o ogni N commit) invece che da un file statico.

Vantaggi rispetto ad A:
- **Dimensione naturalmente limitata**: un diff è per costruzione più piccolo di un intero
  file/repo — meno pressione sul context window, meno il problema di degrado già osservato
  su task6_full (`docs/supporto/calls/call_3.md` §5.1, modello che perde il finding su file
  lunghi).
- **Framing più vicino al caso d'uso reale del CDT**: "è cambiato qualcosa, rilancio il
  valutatore" è letteralmente un diff-triggered check, non un audit completo — combacia
  con la funzione di percezione descritta dal relatore.
- **Stessa questione di completezza di A**: la rubrica v2 giudica se ciò che il modello
  segnala nel diff è vero; sapere se il diff introduce/lascia scoperta *un'altra*
  debolezza che il modello non ha visto resta fuori portata senza enumeratore esterno.

> ✅ **Implementato (2026-08-25): `--changed-since <ref>`** — `utils/git_diff.py`, B come
> *selettore* sopra A e non come pipeline separata.
>
> ⚠️ **Divergenza da quanto scritto qui sopra, deliberata:** il vantaggio "dimensione
> naturalmente limitata" **non** si ottiene, perché l'agente riceve comunque il **file
> intero**, non l'hunk. Il diff decide *quali* file rivedere, non *cosa mostrare*. Due
> ragioni: una modifica è giudicabile solo dentro la funzione che la contiene (un hunk di
> tre righe non dice se il `return` mancante a valle è ancora mancante), e tenere il prompt
> identico a quello di A è ciò che rende A e B confrontabili — altrimenti ogni differenza
> nei risultati sarebbe indistinguibile da un effetto del prompt. Chi volesse il beneficio
> di contesto ridotto deve considerarlo una **modalità C** ancora da progettare, non questa.
>
> Resta vero il secondo punto (framing vicino al caso d'uso del CDT) e resta invariato il
> terzo (completezza fuori portata). Lo stato "ultimo commit valutato" non è persistito: il
> ref si passa a mano, vedi `01_stato_attuale.md` §6.

## Domande aperte, non ancora decise

1. Task per file, per diff-hunk, o per intero diff multi-file? Cambia la definizione di
   "un task" nelle metriche esistenti — serve deciderlo prima di scrivere codice, non
   durante.
2. ~~Cosa sostituisce GT e rubrica quando non sono note a priori?~~ **Risolto per la metà
   correttezza**: si riusa `docs/judge_rubric/gtfree/rubric_v2_draft.json` così com'è (mai
   ancora wired in un run reale, solo calibrazione a parte — `utils/judge_calibration/
   run_gtfree_rubric.py`; portarla nel flusso principale è comunque un passo da fare, ma
   di integrazione, non di ricerca). Resta aperta solo la metà **completezza**: serve un
   enumeratore esterno di candidate (SAST/gosec/Semgrep, proposta G5 mai implementata —
   vedi `docs/sast_tools/` per i tool già provati/rimossi) oppure accettare esplicitamente
   di non poter misurare completezza sul flusso generico. Un secondo LLM cloud come "GT
   sintetica" resta un'opzione scartabile a priori: stesso bias di contaminazione già
   discusso per la rubrica GT-derivata attuale (`docs/supporto/calls/call_3.md` §3.2).
3. "Con SAST e senza SAST" (menzionato dal relatore in call 2026-08-20) — ora ha un
   significato preciso: non l'hint odierno iniettato nel prompt (`config.SAST_HINT_ENABLED`,
   `utils/sast_hint.py`, usato su task statici con GT nota), ma l'enumeratore di
   completezza del punto 2. "Senza SAST" = solo rubrica v2 (giudica correttezza, muto sulla
   completezza). "Con SAST" = aggiunge un segnale di copertura esterno con cui confrontare
   cosa il modello ha trovato — ruolo diverso da quello che SAST ha oggi nel codice.
4. Le metriche M1-M3/S1-S3 attuali (`utils/cvss_eval.py`) restano valide solo finché esiste
   un dataset CVE noto da matchare — su repo/diff arbitrari, se si costruisce l'enumeratore
   del punto 2, quello ne prende il posto come base per detection rate/coverage; altrimenti
   il flusso generico misura solo correttezza (rubrica v2), non completezza, e va dichiarato
   esplicitamente come limite, non nascosto.

## Decisione: si parte da A (repo/cartella, per-file), non da B

Scelta il 2026-08-24: A è più semplice di B perché **evita del tutto** il problema dello
stato persistito che B richiederebbe (B ha bisogno di ricordare "rispetto a quale commit
è cambiato qualcosa" — nessuno stato del genere esiste oggi nel codice). A non ha questo
bisogno: punti una cartella, prendi tutti i file di codice presenti, un file = un task.

### Ricetta v1 concreta

Guardando `docs/tasks/task5_vuln_pcf.md` come esempio: la struttura è già quasi un
template — `Scenario` (testo fisso, solo la frase introduttiva nomina la NF specifica) +
blocco ` ```go ` (l'unico pezzo che cambia) + `Question` (fisso, generico) + `Agent
Instructions` (fisso, generico, il template di risposta Reasoning/Answer/Confidence).
"Sopra e sotto" = tieni fisso tutto tranne il codice.

1. Punto una cartella → elenco i file per estensione (`.go` per ora, coerente col resto
   del progetto).
2. Per ogni file: `task_content` = wrapper fisso (Scenario genericizzato — non più "PCF"
   ma "this Go source file from a 5G core network function", o anche più generico se si
   vuole svincolare da 5G) + contenuto del file + Question/Agent Instructions invariati.
3. `task_id` dinamico = slug del path relativo del file (es. `pcf_internal_sbi_api_oam_go`)
   — serve solo per restare coerenti con lo storage `results/rawJson/<task_id>/...`
   esistente, nessun altro significato.
4. Nessuna GT/CVSS matching (skip M1-M3, nessun dataset di CVE note per un file ignoto),
   giudizio solo via rubrica GT-free v2 (già pronta, integrazione non ricerca).

Limiti accettati esplicitamente per il v1, non da risolvere subito:
- **Cecità cross-file**: un task-per-file non può vedere una vulnerabilità che attraversa
  due file (è proprio perché esiste `task9_vuln_cross` come caso a parte oggi, con un
  file costruito apposta). Dichiarato, non nascosto.
- **Degrado su file grandi**: già osservato su task6_full (2891 righe, il modello perde un
  finding che trova sull'excerpt). Vedi sotto per la mitigazione decisa.

### Degrado su file grandi — stima token pre-flight, non trial-and-check

Tre opzioni valutate il 2026-08-24:

1. **Stima statica pre-flight** (`len(content) / 4` o tokenizer, confrontata con la
   context window del modello, già letta da `_fetch_model_context_window` in
   `utils/experiment_utils.py:35` via `/api/show`) — nessuna chiamata LLM necessaria,
   decide *prima* se tentare o saltare il file. **Scelta.**
2. **Leggere `prompt_eval_count`/`eval_count` dalla risposta Ollama**
   (`agents/agent_runner.py:50-51`) — arrivano solo *a chiamata completata*, quindi utili
   solo per loggare/calibrare la soglia nel tempo, non per decidere prima. Scartata come
   meccanismo di gate, tenuta come fonte per calibrare la soglia empiricamente in futuro.
3. **Il crash non è già gestito**: `httpx.ReadTimeout` in `agents/agent_runner.py:39-44`
   oggi fa `raise SystemExit(1)` — uccide l'intero processo, non salta solo quel file.
   Accettabile per una run singola su un task noto (fallisce, ci si accorge, si rilancia),
   **inaccettabile** per "punto una cartella, N file": se il file 47/200 va in timeout non
   può morire l'intera batch. Fix necessario indipendentemente dalla soglia di stima:
   catturare il timeout per singolo file, marcarlo fallito/skippato, proseguire.

Nota metodologica esplicita: la stima dei token è un **proxy euristico**, non una
soluzione al problema reale. Da `docs/supporto/calls/call_3.md` §5.1, task6_full non
falliva per troncamento del contesto — il modello vedeva tutto il file (29K token in
input, nessun overflow) ma non trovava comunque il finding che trovava sull'excerpt. È
degrado di capacità/attenzione su contesto lungo, non un problema di token che non
entrano. La soglia protegge dallo spreco di tempo su file statisticamente a rischio, non
garantisce che sotto soglia il modello "funzioni" — il problema di fondo resta aperto
(`docs/status.md`, "Context window come variabile controllata", mai risolto).

## Prossimo passo

Implementare A v1: builder dinamico che sostituisce il nodo `load_task` per una cartella
puntata, stima token pre-flight con soglia configurabile, fix del timeout per non killare
la batch, wiring della rubrica GT-free v2 nel flusso principale (oggi solo in
`utils/judge_calibration/`). B (diff) resta rimandato — richiede in più lo stato
"ultimo commit valutato" non ancora progettato.

> ✅ **Implementato (2026-08-25) — cut minimo end-to-end.** `python main.py --source-dir <path>`.
>
> - `utils/dynamic_task.py` — scoperta file (`config.DYNAMIC_SOURCE_EXTENSIONS`/
>   `DYNAMIC_EXCLUDE_PATTERNS`), template genericizzato da `task5_vuln_pcf.md`,
>   `task_id` = slug del path relativo, stima token pre-flight (`len/4` vs
>   `DYNAMIC_PROMPT_CTX_RATIO` × context window). I file oltre soglia sono **saltati e
>   loggati**, mai eseguiti a vuoto.
> - **Buco trovato nella ricetta scritta sopra**: `_fetch_model_context_window`
>   interroga `/api/show` sull'Ollama *locale*, ma la config attuale gira tutta hosted
>   (`use_hosted: True`) → nessuna context window da cui derivare la soglia. Risolto con
>   `config.HOSTED_CONTEXT_WINDOW_FALLBACK` (0 = gate disattivato).
> - `utils/task_utils.py::_load_task` — early-return sul flag `gtfree` nello stato:
>   `task_content`/`task_id`/`rubric` arrivano già costruiti in memoria, nessun
>   `docs/tasks/<task>.md` né `_sol.md` letto, `ground_truth` = `{}`.
> - Rubrica: `docs/judge_rubric/gtfree/rubric_v2_draft.json` caricata così com'è
>   (`config.DYNAMIC_RUBRIC_PATH`) — `build_judge_prompt` era già agnostica, nessuna
>   modifica al giudice. **Non** portati nel flusso principale il criterio *coverage*
>   deterministico e l'addendum "motiva ogni criterio" che restano solo in
>   `utils/judge_calibration/run_gtfree_rubric.py` (scelta esplicita del cut minimo).
> - `is_cvss_task` (euristica `"vuln" in task_id`) non matcherebbe uno slug dinamico e
>   avrebbe spento **anche SGV**: sostituita da un flag esplicito `is_security_review`
>   nello stato. Il blocco CVSS resta iniettato (SGV e il criterio `severity_consistency`
>   della rubrica lo leggono); salta solo `evaluate_cvss_estimate` in `_save_result`,
>   che è la parte GT-dipendente (`cvss_eval`/`cvss_eval_pass1` = `null`).
> - **Timeout per-file**: `agents/agent_runner.py` e `agents/judge_agent.py` facevano
>   `raise SystemExit(1)` su `httpx.ReadTimeout` — su 200 file il file 47 uccideva la
>   batch. Ora sollevano `agents._llm_utils.LLMTimeout` e la policy la decide `main.py`:
>   run statica → abort come prima (Ollama va riavviato a mano), modalità dinamica →
>   il file è marcato skipped, la batch prosegue, l'elenco è loggato a fine run.
> - `_write_evaluation_reports` è saltato in modalità dinamica (costruito attorno a
>   GT/CVE note, produrrebbe tabelle vuote): al suo posto `utils/gtfree_report.py`
>   (vedi sotto).
>
> Verificato con LLM stubbati (nessuna rete): run dinamica su `File_Free5gc_Vulnerabili`
> (4 file, gli stessi NF del benchmark), gate che scarta i file oltre soglia, timeout che
> salta il singolo file e prosegue, e **regressione della modalità statica** (task5:
> rubrica GT-derivata, `cvss_eval` popolato, report scritti — invariata).
>
> Non ancora fatto: nessuna run reale contro il modello.

> ✅ **Report GT-free (2026-08-25, stessa sessione).** `utils/gtfree_report.py` →
> `results/reports/gtfree/<experiment_id>.md`. Osservazione dell'utente: saltare del
> tutto i report è troppo — *"i finding nuovi, che lo sono tutti essendo senza GT,
> almeno quelli li abbiamo"*. Corretto: su una run GT-free l'inventario dei finding
> **è** il risultato, non un bucket di scarto (non esiste uno split matched/unmatched
> da fare), quindi il report minimale tiene solo ciò che sopravvive senza risposta di
> riferimento:
>
> - **Findings inventory** — ogni finding prodotto, raggruppato per file e funzione,
>   con `seen = k/N` (in quante ripetizioni la stessa funzione è stata segnalata),
>   score CVSS auto-dichiarato, esito SGV per finding, snippet di evidenza.
> - **Repetition stability** — Jaccard medio tra gli insiemi di funzioni segnalate
>   nelle varie ripetizioni dello stesso file. Prende il posto della sezione
>   variability TP/FP, che senza GT non è calcolabile. Segnale onesto ma limitato:
>   *stabile ≠ vero*, un 1/3 è misurabilmente instabile, un 3/3 no.
> - **Rubric v2 per criterio** — media per criterio ordinata worst-first (dove il
>   report perde punti). La rubrica non è persistita nel JSON (è run config, non
>   output): criteri e massimi sono riletti da `config.DYNAMIC_RUBRIC_PATH`, che fa
>   anche da whitelist contro i campi derivati (`total_score`, `normalized_score`).
> - **SGV** e **cost (M5)**: riusate as-is da `evaluation_utils`, già GT-free.
> - **Retry channels**: solo i conteggi per gate (SGV vs rubrica). Il delta TP/FP per
>   retry della versione GT-based richiede il dataset CVE, quindi cade.
> - **Files not analyzed**: i file scartati dal gate token o andati in timeout sono
>   elencati nel report — `build_dynamic_tasks` ora ritorna `(specs, skipped)` invece
>   di limitarsi a loggare, così il denominatore di tutto il resto è dichiarato.
>
> Il report dice esplicitamente in testa cosa **non** misura (completezza), invece di
> lasciarlo dedurre dall'assenza di una tabella.

## Prima run reale + A/B sull'istruzione di review (2026-08-25)

Due run complete su `File_Free5gc_Vulnerabili` (4 file = gli stessi 4 NF del benchmark),
3 ripetizioni ciascuna, `gemma4:31b-cloud`: **24/24 ripetizioni corrette al primo
tentativo, zero retry, zero SGV fail** (~2m20s per run). Report in
`results/reports/gtfree/dyn_1A.md` e `dyn_1A_exh.md`.

Poiché i file sono gli stessi dei task statici `_full`, i finding dinamici sono stati
passati a `evaluate_cvss_estimate` col `task_id` statico corrispondente — un confronto
possibile solo su questo dataset, non una capacità della modalità generica. Tutti i
numeri sotto usano la **correzione dei match spuri UDR** di `bd0dcc0`
(`utils/generate_detection_table.py::_corrected_dataset`) e il baseline canonico `1A`
di `NF_CONFIG`:

| NF | A dinamica | B din. +esaustività | statica no-hint | statica SAST-hint |
| --- | --- | --- | --- | --- |
| PCF | 3 TP / 5 FP | 3 TP / 5 FP | 3 TP / 0 FP | 3 TP / 4 FP |
| AMF | 3 TP / 25 FP | 3 TP / 25 FP | 3 TP / 16 FP | 3 TP / 29 FP |
| UDM | 3 TP / 16 FP | 3 TP / 17 FP | 3 TP / 34 FP | 3 TP / 34 FP |
| UDR | 0 TP / 8 FP | 0 TP / 13 FP | 0 TP / 19 FP | 3 TP / 20 FP |
| **totale** | **9 TP / 54 FP** | 9 TP / 60 FP | 9 TP / 69 FP | 12 TP / 87 FP |
| **precision** | **14.3%** | 13.0% | 11.5% | 12.1% |

Le due colonne statiche (11.5% / 12.1%) coincidono esattamente con la tabella corretta
già pubblicata in `docs/sgv_protocol/13_detection_table_robusta.md` — l'harness di
confronto riproduce il baseline noto, non produce numeri propri.

**Cosa se ne ricava:**

1. La modalità dinamica trova **gli stessi 9 TP** delle statiche con **meno FP di ogni
   altro braccio**. Il wrapper scritto a mano — nome della NF, contesto free5GC,
   istruzione di esaustività — non aggiunge detection. Questo è il supporto misurato
   all'"il sistema è agnostico da NF" della call 2026-08-20, non più solo un'ipotesi.
2. **UDR resta a 0 TP in ogni braccio no-hint**, dinamico o statico: non è una regressione
   introdotta dalla modalità generica. L'unico braccio che rileva su UDR è il SAST-hint
   (3 TP, pagati con 33 FP in più sul totale).
3. L'istruzione di esaustività **non guadagna TP e costa 6 FP**. Su UDR fa però esaminare
   più funzioni (4 → 6 distinte) e stabilizza da 1/3 a 3/3 ripetizioni il finding su
   `HandleCreateEeSubscriptions` con lo snippet della regex `|.+` — la CVE al centro
   dell'esperimento "singolarità". Cioè: guadagna copertura, che è esattamente ciò che
   una run GT-free non sa misurare.

**Decisione (utente, 2026-08-25):** entrambe le varianti tenute, dietro flag.
`config.DYNAMIC_EXHAUSTIVE_PROMPT` (default `False` = variante base, la migliore per
precision misurata), override da CLI con `--exhaustive-prompt`. Le due istruzioni sono
`REVIEW_INSTRUCTION_BASE` / `REVIEW_INSTRUCTION_EXHAUSTIVE` in `utils/dynamic_task.py`;
la variante usata è salvata come `prompt_variant` nel JSON del risultato e mostrata in
testa al report, così un braccio non può essere attribuito all'altro. Nota: i due JSON
di `dyn_1A`/`dyn_1A_exh` sono precedenti all'introduzione del campo e riportano `n/a` —
i bracci lì si distinguono per `experiment_id`.

**Caveat metodologico:** i TP misurati qui restano ancorati al dataset di CVE note del
benchmark. Su una repo arbitraria quel confronto non esiste — è proprio il buco della
completezza (enumeratore G5/SAST) che resta aperto. Questo A/B è valido *perché* è stato
fatto su file con GT nota; non è ripetibile in produzione sulla modalità generica.

---

## Modalità B e braccio SAST generico (2026-08-25, sessione successiva)

**Intent (citazione):** *"per il punto 1 livello 3 al posto di andare silenziosamente sui
log chiedi all'utente esplicitamente quali sono i path da passare per ogni singolo file di
cui non hai trovato corrispondenza"* + *"punto 2 ok — procedi come meglio credi"*.

Due funzionalità nate dal confronto tra la call 2026-08-20 e lo stato del repo:

### 1. Il braccio SAST in modalità generica non esisteva (bug silenzioso)

`SAST_HINT_ENABLED=true` con `--source-dir` girava **senza iniettare niente e senza dirlo**:
il ramo `gtfree` di `_load_task` fa early-return prima del blocco SAST, e `_TASK_NF_MAP` è
comunque una mappa hardcoded dei 4 task id statici. Non era una scelta di scope: la
combinazione non era mai stata collegata, e non c'era nemmeno l'errore che l'avrebbe detto.

Il join key però esisteva già nel dataset senza che venisse usato: ogni alert porta
`component_path` (repo-root) **e** `vuln_file` (relativo alla cartella curata, cioè
esattamente il `rel_path` della modalità dinamica). `_task_nf` + `_TASK_NF_MAP` erano un
modo indiretto di fare ciò che il campo path fa direttamente.

### 2. Divergenza sulla risoluzione dei path, decisa a metà

Proposta iniziale: tre livelli di match (esatto → suffisso unico → ambiguo), con
l'ambiguità loggata. **Decisione dell'utente:** l'ambiguità non va sui log, si chiede
esplicitamente all'utente per ogni file senza corrispondenza.

**Accettata, ma raffinata durante l'implementazione** (e la modifica è emersa da un test,
non da un ragionamento a tavolino): il primo test end-to-end su un repo git di prova ha
mostrato che "nessuna corrispondenza" copre due fatti diversi. Un file può non avere match
perché il path ha forma diversa (va chiesto) oppure — molto più spesso — perché *il report
SAST elenca solo i file che hanno finding*. Chiedere per ogni file senza alert sarebbe
inutilizzabile su una repo di 500 file. Esito: gli **ambigui** si chiedono uno per uno come
richiesto; gli **assenti** (basename che non compare da nessuna parte nel report) diventano
**una domanda aggregata sola** — "sono N, li tratto tutti come 'nessun alert'? [Y/n]" — e
rispondere `n` li fa ricadere nella risoluzione per file, quindi la richiesta originale
resta raggiungibile. Le risposte si persistono in `--sast-path-map`.

### Altre divergenze registrate

- **Report congelato, tool mai lanciato dalla pipeline.** Versione del tool e ruleset sono
  la condizione sperimentale: se la pipeline rilanciasse il tool, due run a distanza di un
  mese smetterebbero di essere confrontabili senza segnali. Lo sha256 del report va
  nell'header. Costo: il tool va lanciato a mano (si sposa col ledger `/sast-tools-lifecycle`).
- **Nome del tool parametrico nel prompt.** L'header diceva "SonarQube" hardcoded; con un
  report gosec avrebbe dichiarato al modello un tool falso. Verificato che il blocco
  statico resta **byte-identico** (562 char, stesso sha) — nessuna run passata invalidata.
- **`sast_alerts` per file, `0` incluso.** Un file senza alert nel braccio SAST ha girato
  come baseline: se non fosse visibile, i totali della run sembrerebbero un A/B pulito
  senza esserlo. Il report lo dichiara in testa quando succede.

### Stato

Tutto verificato end-to-end **senza rete** (repo git di prova con file aggiunti/modificati/
cancellati/rinominati, report semgrep e gosec sintetici, LLM stubbati): selettore diff,
filtri condivisi, iniezione per file, risoluzione interattiva, path map, JSON salvato,
report generato, e regressione della modalità statica: **28 check, 0 fail**.

Poi lanciato **contro il modello vero**: `dyn_B_real` (modalità B sui 4 file free5GC, 4/4
corrette) e `dyn_1A_sast` (braccio SAST, 3 rip.). Numeri e lettura in
`01_stato_attuale.md` §8. Il risultato non previsto: il braccio SAST non aggiunge TP (0/54
alert corrispondono a una CVE target, era atteso) ma **degrada il report in modo monotòno
rispetto al numero di alert iniettati**, fino a far collassare UDR (35 alert) a 0/3
ripetizioni corrette con i retry esauriti. Il baseline `dyn_1A` ricalcolato in questa
sessione riproduce esattamente 9 TP / 54 FP / 14.3% della sezione precedente — l'harness di
confronto è coerente.
