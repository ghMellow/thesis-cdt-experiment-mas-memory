# 01 — Stato attuale della modalità generica (sintesi)

> Documento di sintesi (2026-08-25). Non aggiunge esperimenti nuovi: raccoglie in un unico
> posto "a che punto siamo oggi", perché `00_costruzione_dinamica_task.md` è ormai la
> **traccia del processo** (discussione → decisioni → blocchi ✅ → A/B) e per capire cosa
> fa il sistema bisognerebbe leggerla tutta in ordine. Per il dettaglio di ogni passaggio
> e per il *perché* di ogni scelta, quello resta la fonte primaria; questo file è il punto
> di ingresso.

## 1. Cosa fa oggi

Il sistema sa puntare una cartella di codice e valutarla senza che nessun task sia stato
scritto a mano: **un file sorgente = un task**, prompt costruito in memoria, giudizio con
la rubrica GT-free v2. È la modalità A della discussione (repo file-per-file); la modalità
B (diff tra push git) non è implementata.

```bash
python main.py --source-dir File_Free5gc_Vulnerabili --repetitions 3
python main.py --source-dir <path> --exhaustive-prompt   # variante di prompt, vedi §5
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

## 6. I numeri della prima run reale (2026-08-25)

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

## 7. Limiti noti e cosa resta aperto

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
   generica misura solo correttezza. Vedi `docs/sast_tools/` per i tool già provati.
2. **Modalità B (diff git)** — richiede lo stato "ultimo commit valutato", mai progettato.
   È la forma più vicina alla "funzione di percezione del CDT" descritta dal relatore.
3. **Task di controllo negativo** — file senza vulnerabilità, per misurare il false
   positive rate. Punto §3.5 di `call_3.md`, mai risolto: su codice ignoto smette di
   essere opzionale.
4. **Criterio coverage deterministico** — resta solo in
   `utils/judge_calibration/run_gtfree_rubric.py`, non portato nel flusso principale
   (scelta esplicita del cut minimo).
5. **Provenienza `prompt_variant`** — i JSON di `dyn_1A`/`dyn_1A_exh` precedono il campo e
   riportano `n/a`; lì i bracci si distinguono per `experiment_id`.

## 8. Dove guardare

| | |
| --- | --- |
| costruzione del task, template, gate token | `utils/dynamic_task.py` |
| innesto nel grafo | `utils/task_utils.py::_load_task` (early-return `gtfree`) |
| report GT-free | `utils/gtfree_report.py` |
| timeout per-file | `agents/_llm_utils.py::LLMTimeout` + policy in `main.py` |
| processo e decisioni | `00_costruzione_dinamica_task.md` (questa cartella) |
| rubrica GT-free, perché v2 | `docs/judge_rubric/15_stato_attuale_gtfree.md` |
| baseline di detection con cui è confrontata | `docs/sgv_protocol/13_detection_table_robusta.md` |
