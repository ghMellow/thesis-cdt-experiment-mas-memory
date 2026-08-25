# 01 — Stato attuale della modalità generica (sintesi)

> Documento di sintesi (2026-08-25, aggiornato con modalità B e braccio SAST). Non aggiunge esperimenti nuovi: raccoglie in un unico
> posto "a che punto siamo oggi", perché `00_costruzione_dinamica_task.md` è ormai la
> **traccia del processo** (discussione → decisioni → blocchi ✅ → A/B) e per capire cosa
> fa il sistema bisognerebbe leggerla tutta in ordine. Per il dettaglio di ogni passaggio
> e per il *perché* di ogni scelta, quello resta la fonte primaria; questo file è il punto
> di ingresso.

## 1. Cosa fa oggi

Il sistema sa puntare una cartella di codice e valutarla senza che nessun task sia stato
scritto a mano: **un file sorgente = un task**, prompt costruito in memoria, giudizio con
la rubrica GT-free v2. Sono implementate entrambe le modalità della discussione: **A**
(tutti i file sotto la cartella) e **B** (solo i file toccati da un range git). In più,
entrambe possono girare con o senza alert SAST iniettati per file.

```bash
# A — tutta la cartella
python main.py --source-dir File_Free5gc_Vulnerabili --repetitions 3
python main.py --source-dir <path> --exhaustive-prompt   # variante di prompt, vedi §5

# B — solo ciò che è cambiato (l'agente vede comunque il file intero, non l'hunk)
python main.py --source-dir <path> --changed-since HEAD~1

# braccio "con SAST" (vale per A e per B)
python main.py --source-dir <path> --sast-report gosec.json --sast-path-map map.json
```

Output: raw per task in `results/rawJson/<slug_del_path>/`, report in
`results/reports/gtfree/<experiment_id>.md`.

## 2. Cosa cambia rispetto alla modalità statica

Il grafo LangGraph è **lo stesso** (`utils/experiment_utils.py::_build_graph`): cambia solo
da dove arriva il contenuto del task e cosa è calcolabile a valle.

| | statica (`docs/tasks/`) | dinamica (`--source-dir`) |
| --- | --- | --- |
| origine del prompt | file `.md` scritto a mano, letto verbatim | costruito in memoria da `utils/dynamic_task.py::TASK_TEMPLATE` |
| `task_id` | dai metadati `**ID:**` del file | slug del path relativo del sorgente |
| ground truth | `<task>_sol.md`, blocco JSON 1 | **assente** (`{}`) |
| rubrica del giudice | `<task>_sol.md`, blocco JSON 2 (scritta conoscendo la CVE) | `config.DYNAMIC_RUBRIC_PATH` → rubrica GT-free v2, uguale per ogni file |
| blocco CVSS nel prompt | sì sui task `vuln` | sì (serve a SGV e al criterio `severity_consistency`) |
| gate SGV | sì | sì, invariato |
| matching CVE deterministico (M1-M3) | sì | **no** — il dataset è keyed su CVE note, `cvss_eval` = `null` |
| report finale | `utils/evaluation_utils.py` (detection, precision@k, variability…) | `utils/gtfree_report.py` (vedi §4) |
| timeout | abort della run (Ollama da riavviare a mano) | il singolo file è marcato skipped, la batch prosegue |
| selezione dei file | tutti i `docs/tasks/*.md` | tutta la cartella, oppure il diff di un range git (`--changed-since`) |
| hint SAST | `SAST_HINT_ENABLED` + dataset keyed per NF | `--sast-report`, alert appaiati **per path di file** (`utils/sast_ingest.py`) |

Il selettore è il flag `gtfree` nello stato: `utils/task_utils.py::_load_task` fa
early-return quando è presente, e il resto del grafo non sa di essere in modalità diversa.

## 3. Cosa misura, e cosa non misura

**Misura** (tutto senza risposta di riferimento): correttezza formale e groundedness del
report (rubrica v2 + SGV), quali funzioni vengono segnalate e con quale evidenza, quanto
il risultato è stabile tra ripetizioni, costo.

**Non misura la completezza.** Sapere se il modello ha *mancato* qualcosa richiede sapere
cosa c'è: serve l'enumeratore esterno di candidate (proposta G5/SAST, mai implementata) —
vedi `00_...md` §"Domande aperte" punto 2 e `docs/judge_rubric/15_stato_attuale_gtfree.md`
§4. È un limite **dichiarato in testa al report generato**, non dedotto dall'assenza di una
tabella.

Conseguenza pratica: `verdict = correct` in questa modalità significa "il report è
ben formato e ancorato al codice", **non** "la vulnerabilità descritta è reale".

## 4. Il report GT-free

`utils/gtfree_report.py` tiene solo ciò che sopravvive senza GT:

| sezione | cosa dice | sostituisce |
| --- | --- | --- |
| Findings inventory | ogni finding, per file e funzione, con `seen = k/N` ripetizioni, score auto-dichiarato, esito SGV, snippet | il vecchio split matched/unmatched (senza GT **tutti** i finding sono nuovi: l'inventario *è* il risultato) |
| Repetition stability | Jaccard medio tra gli insiemi di funzioni segnalate nelle ripetizioni | variability TP/FP |
| Rubric v2 per criterio | media per criterio, worst-first | scores by role |
| Retry channels | quale gate ha causato il retry (SGV vs rubrica), solo conteggi | retry channel con delta TP/FP |
| SGV, Cost (M5) | riusati as-is da `evaluation_utils` — erano già GT-free | — |
| Files not analyzed | file scartati dal gate token o andati in timeout | — (nuovo: rende dichiarato il denominatore) |

## 5. Configurazione

| costante (`config.py`) | default | effetto |
| --- | --- | --- |
| `DYNAMIC_RUBRIC_PATH` | `docs/judge_rubric/gtfree/rubric_v2_draft.json` | rubrica usata dal giudice |
| `DYNAMIC_SOURCE_EXTENSIONS` | `[".go"]` | quali file diventano task |
| `DYNAMIC_EXCLUDE_PATTERNS` | `["_test.go", "vendor/", ".pb.go"]` | esclusioni sul path relativo |
| `DYNAMIC_CHARS_PER_TOKEN` | `4.0` | stima token pre-flight (proxy, nessuna tokenizzazione) |
| `DYNAMIC_PROMPT_CTX_RATIO` | `0.6` | frazione di context window usabile dal prompt |
| `HOSTED_CONTEXT_WINDOW_FALLBACK` | `128000` | context window assunta sui modelli hosted (`/api/show` interroga solo Ollama locale); `0` disattiva il gate |
| `DYNAMIC_EXHAUSTIVE_PROMPT` | `False` | istruzione di review: base vs esaustiva (override CLI `--exhaustive-prompt`) |

Il braccio SAST non ha costanti: è interamente da CLI, perché il report è un artefatto
esterno che cambia a ogni esecuzione del tool. `SAST_HINT_ENABLED` **non** attiva niente in
modalità generica — se è `true` senza `--sast-report`, la run si ferma con un errore
esplicito invece di eseguire silenziosamente la baseline.

## 6. Modalità B — solo ciò che è cambiato (`--changed-since`)

È la "funzione di percezione" descritta nella call 2026-08-20: *vede il diff, se il codice
è cambiato rilancia il valutatore*. Implementata come **selettore**, non come pipeline
separata — il diff decide *quali* file rivedere, poi entrano in `build_dynamic_tasks`
identici a prima.

```bash
python main.py --source-dir <path> --changed-since HEAD~1
```

Tre decisioni di design, tutte esplicite:

- **L'agente riceve il file intero, non l'hunk.** Una modifica è giudicabile solo dentro la
  funzione che la contiene, e tenere il prompt identico a quello della modalità A è ciò che
  rende confrontabili le run A e le run B. Il diff seleziona, non ritaglia.
- **Nessuno stato "ultimo commit valutato".** Il ref di base si passa a mano, che è il caso
  degenere di uno SHA persistito. Persisterlo per directory è il passo che rende il loop
  automatico — future work, e piccolo ora che il selettore esiste.
- **Selezione vuota = uscita pulita**, non errore: in un loop di percezione "nessun file
  rilevante è cambiato" è il caso normale, non un fallimento.

Dettagli che il selettore gestisce (`utils/git_diff.py`): la source-dir non deve essere la
radice del repo; i file cancellati sono esclusi (`--diff-filter=ACMR`) perché non c'è più
niente da rivedere; i rinominati arrivano col nome nuovo; i file fuori dalla source-dir
sono contati e scartati. Il filtro estensioni/esclusioni è **lo stesso** della modalità A
(`utils/dynamic_task.py::is_candidate`), così i due percorsi non possono divergere.

Il range effettivo (`<base_sha>..<head_sha>`, risolto in SHA corti) finisce nell'header del
report GT-free: senza, una run B non sarebbe riproducibile.

## 7. Braccio SAST in modalità generica (`--sast-report`)

Prima di oggi `SAST_HINT_ENABLED=true` con `--source-dir` girava **senza iniettare niente e
senza dirlo**: il ramo statico di `_load_task` fa early-return sui task `gtfree`, e comunque
`_TASK_NF_MAP` è una mappa hardcoded dei 4 task id noti. Ora quella combinazione si ferma
con un errore esplicito.

Il braccio generico passa da un **report congelato**, non da un tool lanciato dalla
pipeline: la versione del tool e il ruleset abilitato *sono* la condizione sperimentale, e
se la pipeline lo rilanciasse due run a distanza di un mese smetterebbero di essere
confrontabili senza che nessuno se ne accorga. Lo sha256 del report finisce nell'header.

Formati accettati (`utils/sast_ingest.py`): il JSON già normalizzato del progetto (export
SonarQube), **gosec** e **semgrep**. Il nome del tool dichiarato nel prompt segue il
formato — dire "SonarQube" al modello davanti a un report gosec sarebbe un'affermazione
falsa. Il blocco iniettato resta per il resto **byte-identico** a quello della modalità
statica: una differenza nel testo confonderebbe qualsiasi confronto tra le due modalità.

**L'appaiamento alert↔file è il punto delicato.** Il tool riporta path relativi alla radice
del repo (`NFs/amf/internal/sbi/api_communication.go`), la cartella puntata può essere una
copia curata (`AMF/api_communication.go`): spesso condividono solo il basename. Si appaia
per **suffisso di path più lungo in comune**, con tre esiti tenuti distinti:

| esito | significato | cosa succede |
| --- | --- | --- |
| match unico | un solo path vince | alert iniettati |
| **ambiguo** | due o più path pareggiano (`api_oam.go` in due package non è raro) | **si chiede all'utente**, file per file, mai indovinato |
| **assente** | il basename non compare da nessuna parte nel report | è il caso ordinario (un report SAST elenca solo i file con finding): una domanda aggregata, non una per file |

Perché la distinzione conta: attaccare a un file gli alert di un altro produce un risultato
sbagliato ma plausibile, il tipo peggiore. Mentre "questo file non ha alert" è la normalità
su una repo vera — chiedere conferma file per file sarebbe inutilizzabile su 500 file.

Le risposte si salvano in `--sast-path-map` (JSON `path_sorgente → path_nel_report`, con
`null` = "nessun alert"), riletto alla run successiva: si risponde una volta sola, e una
ri-esecuzione identica è scriptabile senza terminale.

Infine, ciò che rende il braccio leggibile a posteriori: `prompt_variant` diventa
`base+sast` / `exhaustive+sast`, e ogni file porta il proprio conteggio `sast_alerts` nel
JSON e nel report. **`0` non è cosmetico**: marca un file su cui il braccio "con SAST" ha
girato come baseline. Se capita, il report lo dichiara in testa — i totali di quella run non
sono un A/B pulito.

⚠️ Aspettativa da mettere in conto sul dataset attuale: 0/54 alert corrispondono a una CVE
target e ~93% è rumore di stile (`docs/expert_review/01`), quindi il braccio riprodurrà il
quasi-nulla già misurato. Il valore vero di questo pezzo è l'ingest gosec/semgrep, cioè far
girare un tool **vero** su codice **ignoto**, dove gli alert non sono pre-annotati.

## 8. I numeri della prima run reale (2026-08-25)

Due run × 4 file × 3 ripetizioni su `File_Free5gc_Vulnerabili`, `gemma4:31b-cloud`:
**24/24 corrette al primo tentativo, zero retry, zero SGV fail**, ~2m20s per run.

| | A dinamica | B din. +esaustività | statica no-hint | statica SAST-hint |
| --- | --- | --- | --- | --- |
| totale | **9 TP / 54 FP** | 9 TP / 60 FP | 9 TP / 69 FP | 12 TP / 87 FP |
| precision | **14.3%** | 13.0% | 11.5% | 12.1% |

Dettaglio per NF, provenienza e caveat: `00_costruzione_dinamica_task.md` §"Prima run
reale". In sintesi: la modalità dinamica trova **gli stessi TP** dei task scritti a mano
con **meno falsi positivi di ogni altro braccio** — il wrapper artigianale (nome della NF,
contesto free5GC, istruzione di esaustività) non aggiungeva detection. È il supporto
misurato all'"il sistema è agnostico da NF" della call 2026-08-20.

⚠️ Questo confronto è possibile **solo** perché i 4 file coincidono con quelli dei task
statici con GT nota: i finding dinamici sono stati passati a `evaluate_cvss_estimate` col
`task_id` statico corrispondente. Non è una capacità della modalità generica e non è
ripetibile su una repo arbitraria.

### Modalità B e braccio SAST, run reali (2026-08-25)

**Modalità B** (`--changed-since 2bb507b~1`, `dyn_B_real`): 9 file toccati sotto la
source-dir, 5 scartati dai filtri, **4 task, 4/4 corrette al primo tentativo**. Il selettore
funziona contro il modello vero; sui 4 file di sempre non aggiunge informazione rispetto ad
A — serviva a validare il percorso, non a misurare qualcosa di nuovo.

**Braccio SAST** (`--sast-report ground_truth_vuln_files.json`, `dyn_1A_sast`, 3 rip.),
confrontato col baseline `dyn_1A` sugli stessi 4 file e con lo stesso metodo:

| | senza SAST (`dyn_1A`) | con SAST (`dyn_1A_sast`) |
| --- | --- | --- |
| totale | 9 TP / 54 FP | 9 TP / **47** FP |
| precision | 14.3% | **16.1%** |
| ripetizioni corrette | 12/12 (1 tentativo) | **9/12** — UDR 0/3, 3 tentativi ciascuna |

**Nessun TP in più**, come atteso: 0/54 alert corrispondono a una CVE target. L'effetto
interessante è un altro, ed è **monotòno nel numero di alert iniettati**:

| file | alert iniettati | rubrica media | finding/rip. (vs baseline) |
| --- | --- | --- | --- |
| `pcf_api_oam.go` | 2 | 1.000 | 2.0 (2.7) |
| `amf_api_communication.go` | 4 | 1.000 | 12.0 (9.3) |
| `udm_api_subscriber…​.go` | 13 | 0.867 | 3.7 (6.3) |
| `udr_api_datarepository.go` | 35 | **0.433** | **1.0** (2.7) |

Su UDR — il file più grande, 35 alert di rumore — il report **collassa**: un solo finding,
`presence_evidence_score` e `absence_claims_score` a 0, retry esauriti 3/3 senza recupero.
Il finding superstite resta ancorato (SGV passa, snippet reale): non è groundedness che si
rompe, è il resto del report che sparisce.

⚠️ Due cautele nel leggere il calo di FP. Primo, viene in buona parte dal modello che dice
**meno** (UDR 2.7→1.0, UDM 6.3→3.7), non necessariamente meglio — e AMF va nella direzione
opposta (25→33 FP, 9.3→12.0 finding). Secondo, n=3 su un modello solo. Il segnale robusto
qui è la monotonìa rispetto al numero di alert, non il delta di precision.

## 9. Limiti noti e cosa resta aperto

Limiti **accettati** nel design attuale (dichiarati, non da risolvere subito):

- **Cecità cross-file** — un task-per-file non vede una vulnerabilità che attraversa due
  file (per quello esiste `task9_vuln_cross` come caso costruito apposta).
- **Degrado su file grandi** — il gate token protegge dallo spreco, non dal degrado: su
  `task6_full` il modello vedeva tutto il file senza overflow e perdeva comunque il
  finding (`docs/supporto/calls/call_3.md` §5.1).
- **Granularità del task** — un file = un task è una scelta, non l'unica: cambia cosa
  significa TP/FP/FN (`00_...md`, domanda aperta 1).

Aperto, in ordine di dipendenza:

1. **Enumeratore di completezza (G5/SAST)** — il vero blocco residuo. Senza, la modalità
   generica misura solo correttezza. L'ingest SAST (§7) porta gli alert *dentro il prompt*,
   che è cosa diversa dall'usarli come lista di candidate contro cui misurare cosa il
   modello ha mancato: il secondo uso non esiste ancora. Vedi `docs/sast_tools/`.
2. **Stato "ultimo commit valutato"** — la modalità B esiste (§6) ma il ref di base si
   passa a mano. Persisterlo per directory è ciò che la rende il loop automatico di
   percezione del CDT.
3. **Task di controllo negativo** — file senza vulnerabilità, per misurare il false
   positive rate. Punto §3.5 di `call_3.md`, mai risolto: su codice ignoto smette di
   essere opzionale.
4. **Criterio coverage deterministico** — resta solo in
   `utils/judge_calibration/run_gtfree_rubric.py`, non portato nel flusso principale
   (scelta esplicita del cut minimo).
5. **Provenienza `prompt_variant`** — i JSON di `dyn_1A`/`dyn_1A_exh` precedono il campo e
   riportano `n/a`; lì i bracci si distinguono per `experiment_id`.
6. **Perché il braccio SAST degrada sui file con molti alert** — misurato (§8), non
   spiegato. Le ipotesi da separare: competizione per il budget di attenzione, il modello
   che tratta la lista come agenda da coprire, o l'effetto della sola lunghezza del prompt.
   Un controllo economico: ripetere iniettando 35 alert *casuali* su un file piccolo.

## 10. Dove guardare

| | |
| --- | --- |
| costruzione del task, template, gate token, filtro file | `utils/dynamic_task.py` |
| selettore diff (modalità B) | `utils/git_diff.py` |
| ingest SAST, appaiamento path, risoluzione interattiva | `utils/sast_ingest.py` |
| rendering del blocco SAST nel prompt | `utils/sast_hint.py` + `agents/prompts.py` |
| innesto nel grafo | `utils/task_utils.py::_load_task` (early-return `gtfree`) |
| report GT-free | `utils/gtfree_report.py` |
| timeout per-file | `agents/_llm_utils.py::LLMTimeout` + policy in `main.py` |
| processo e decisioni | `00_costruzione_dinamica_task.md` (questa cartella) |
| rubrica GT-free, perché v2 | `docs/judge_rubric/15_stato_attuale_gtfree.md` |
| baseline di detection con cui è confrontata | `docs/sgv_protocol/13_detection_table_robusta.md` |
