# Codemap — `utils/evaluation_utils.py`

> Documento "code-as-truth": generato leggendo per intero `utils/evaluation_utils.py` (2090 righe) e `utils/cvss_eval.py` (631 righe, il modulo da cui `evaluation_utils.py` importa tutta la logica di matching/metriche), più `git log`/`git show` sugli stessi file. Nessun file sotto `docs/` è stato usato come fonte — solo per identificare "quali righe leggere di git log", i messaggi di commit sono citati testualmente dove rilevanti.

## 1. Ruolo del modulo nella pipeline

`utils/evaluation_utils.py` è il livello di **reporting**: prende i risultati grezzi salvati su disco da ogni repetizione di ogni task/ruolo/esperimento (file JSON sotto `results/<task>/<experiment>/<role>/*.json`), li carica in memoria, calcola metriche aggregate (accuratezza rubrica, consistenza cross-repetizione, costo, e — quando il task è di tipo vulnerabilità — le metriche di detection/severity M1-M5/S1-S3) e scrive i report Markdown finali in `results/evaluation/`. Il modulo **non calcola** la logica di matching finding↔CVE né la matematica CVSS: quella vive in `utils/cvss_eval.py` ed è importata qui (dentro le funzioni, con import locali) — `evaluation_utils.py` la aggrega e la presenta. Il file non contiene classi: è un insieme di funzioni quasi tutte prefissate `_` (private al modulo) tranne `list_runs` e le funzioni chiamate da `main.py`/CLI (`_write_evaluation_reports`, esposta anche come modulo eseguibile).

## 2. Mappa di alto livello: dal risultato grezzo al report

```
results/<task>/<experiment>/<role>/*.json
        │
        ▼
_collect_results()               # scansiona results/, normalizza formato nuovo/vecchio → {experiment_id: {role: [payload...]}}
        │
        ▼
_write_evaluation_reports()      # entry point: per ogni experiment_id × task_id chiama _build_experiment_report
        │
        ▼
_build_experiment_report()       # assembla un report .md per un singolo task_id (o l'intero esperimento)
        │
        ├─ _detect_inconsistencies()      → Blocco A: consistenza reasoning cross-repetizione (fase stringa + fase LLM)
        ├─ _build_sgv_section()           → Blocco C: SGV (Syntactic Grounding Verifier), retry falliti/risolti
        ├─ _build_cvss_section()          → Blocco B: CVSS estimate (usa utils.cvss_eval.evaluate_cvss_estimate già salvato in ogni payload)
        │     ├─ _compute_finding_groups()          → etichette di ricorrenza (a,b,c…) condivise matched/unmatched
        │     ├─ _build_cvss_vector_detail()        → tabella per-CVE stimato vs pubblicato + file di dettaglio
        │     ├─ _build_cvss_unmatched()            → tabella finding senza CVE GT, ranked by severità + file di dettaglio
        │     ├─ _build_detection_metrics_section() → M1/M2/M3 (usa cvss_eval.aggregate_detection_metrics)
        │     ├─ _build_precision_at_k_section()    → Precision@K (usa cvss_eval.aggregate_precision_at_k)
        │     ├─ _build_variability_section()       → media/std/CI95 TP-FP per task (usa cvss_eval.compute_repetition_variability)
        │     ├─ _build_cve_rep_matrix()             → matrice CVE × repetizione (hit/miss)
        │     ├─ _build_retry_channel_section()      → attribuzione del delta di detection al gate che ha causato il retry (SGV vs rubrica)
        │     ├─ _build_sgv_detection_cross_section()→ TP/FP incrociati con l'esito SGV (conform/non-conform)
        │     └─ _build_severity_metrics_section()   → S1/S2/S3 (usa cvss_eval.aggregate_severity_metrics)
        ├─ _build_scores_table()          → Blocco A: accuracy/confidence/brier/attempts per ruolo
        ├─ _build_cost_metrics_section()  → M5: token e wall-clock time
        └─ anomalies_section              → wrong verdicts / retry / inconsistenze vere (testo libero)
        │
        ▼
result_<task_id>_<experiment_id>.md   scritto in results/evaluation/
        (+ comparison.md se sia 1A che 1B sono nello scope: accuracy 1A vs 1B + rollup pooled M1-M3/S1-S3/M5)
```

Punto cruciale sull'architettura dei dati: il matching finding↔CVE e il calcolo delle metriche numeriche **non avvengono a tempo di reporting** — sono già stati calcolati e salvati nel JSON grezzo, nel campo `cvss_eval` (e `cvss_eval_pass1` per il "first attempt"), da `utils/cvss_eval.recompute_saved_results()` (o al momento del salvataggio del risultato da `experiment_utils.py`, non ispezionato qui). `evaluation_utils.py` legge quei campi già pronti, non li ricalcola.

## 3. Dettaglio per gruppo funzionale

### 3.1 Caricamento e indicizzazione dei risultati grezzi

| Funzione | Riga | Cosa fa |
| --- | --- | --- |
| `_record_consistency_finding(lines)` | `utils/evaluation_utils.py:16` | Appende righe a `results/evaluation/consistency.md` (append semplice, nessuna deduplicazione). |
| `_collect_results(results_path, run_id=None)` | `utils/evaluation_utils.py:26` | Scansiona ricorsivamente `results/<task>/<experiment>/<role>/*.json`, esclude la cartella `evaluation`. Gestisce due formati di file: nuovo (`{run_config..., "repetitions": [...]}`, dove ogni ripetizione eredita i campi di `run_config`) e vecchio (un file per repetizione, senza `run_id` — se si filtra per `run_id` questi non passano mai il filtro). Ritorna `{experiment_id: {role: [payload,...]}}`. |
| `list_runs(results_path)` | `utils/evaluation_utils.py:70` | Enumera tutte le combinazioni distinte `(task_id, experiment_id, role, run_id)` con conteggio repetizioni e timestamp più vecchio — usata dal flag CLI `--list-runs`. |

### 3.2 Utility numeriche/di formattazione generiche

| Funzione | Riga | Cosa fa |
| --- | --- | --- |
| `_avg(values)` | `:103` | Media aritmetica, `None` se lista vuota. |
| `_fmt(value, digits=2)` | `:107` | Formatta float o `"n/a"`. |
| `_fmt_ratio(value)` | `:111` | Formatta come percentuale (`"n/a"` se `None`). |
| `_fmt_delta(value)` | `:115` | Percentuale con segno esplicito (`+`/`-`). |
| `_brier_score(payloads)` | `:228` | MSE tra `confidence` dichiarata e correttezza binaria (1 se `verdict == "correct"`, altrimenti 0). Formula: `mean((confidence - is_correct)^2)`. |

### 3.3 Consistenza cross-repetizione (Blocco A)

`_detect_inconsistencies(roles, semantic_check=True, task_filter=None)` (`:122`) — due fasi:
1. **Fase stringa** (sempre): per ogni ruolo/task raggruppa i `reasoning` delle repetizioni; se ci sono ≥2 stringhe distinte, il task è "surface different".
2. **Fase LLM** (se `semantic_check=True`): chiama `agents.judge_agent.run_semantic_equivalence_check` (import locale, quindi dipendenza solo a runtime) per capire se le differenze testuali sono parafrasi equivalenti o conclusioni realmente diverse. Risultati cachati in `results/evaluation/semantic_cache.json`, chiave = hash SHA-256 dei reasoning concatenati. Solleva `ValueError` se `config.MODELS["semantic_check"]` non è impostato — nessun fallback silenzioso.

Ritorna `(truly_inconsistent, n_surface_equiv)`.

### 3.4 SGV — Syntactic Grounding Verifier (Blocco C)

`_build_sgv_section(all_payloads)` (`:372`) legge `history[].sgv_eval` di ogni repetizione. Design esplicito nel commento del codice (non dedotto, dichiarato): **una finding che fallisce G1–G4 su ogni tentativo fino a `MAX_RETRIES` non viene scartata — viene comunque valutata a valle**. La sezione rende visibile quali repetizioni sono state "let through despite failing" vs "resolved by the agent". `MAX_RETRIES = 3` è definito in `config.py:44`.

`_retry_cause(attempt)` (`:913`) determina, per un tentativo fallito, quale gate ha causato il retry successivo: se `sgv_eval.passed is False` → `"SGV"` (il gate SGV gira per primo, quindi ha priorità); altrimenti se c'è un verdetto/judge_score → `"rubric"`; altrimenti `"unknown"`.

### 3.5 CVSS / matching finding↔GT (Blocco B) — cuore del modulo

Il matching vero e proprio è in `utils/cvss_eval.py`, non in `evaluation_utils.py`:

- `_candidate_cves(task_id)` (`utils/cvss_eval.py:140`) — filtra il dataset (`File_Free5gc_Vulnerabili/cve_metrics_normalized.json`, path in `config.CVSS_DATASET_PATH`) per le CVE del task; per le varianti `_full` include anche le CVE fuori dall'excerpt (`in_task_excerpt: false`).
- `_match_finding(finding, candidates)` (`utils/cvss_eval.py:156`) — **matching per nome funzione, non per contenuto semantico**: normalizza a lowercase e confronta con containment (`handler in function or function in handler`), **first-match semantics** in ordine di output dell'agente. Commento esplicito nel codice: quando lo stesso handler viene riportato più volte in una repetizione, quale finding viene abbinato alla GT (e quindi alimenta le metriche S) dipende solo dall'ordine — non esiste un modo GT-indipendente di preferire un duplicato, e un tie-break GT-aware "leaker­ebbe" la GT nel pairing (bias verso l'alto su S).
- `evaluate_cvss_estimate(task_id, estimate)` (`utils/cvss_eval.py:274`) — orchestratore per-repetizione: per ogni finding tenta il match contro le CVE rimanenti (`remaining`, consumate una volta abbinate), produce `matched`/`unmatched`/`missed_cves` + un blocco `aggregates`. Caso speciale: se c'è **esattamente 1 finding e 1 CVE candidata**, il match è automatico (skip del confronto per nome funzione). Ritorna `None` solo quando il task non ha CVE mappate *e* l'agente non ha prodotto nulla.
- `_evaluate_matched_pair(finding, cve)` (`utils/cvss_eval.py:178`) — calcola tutte le metriche per-finding (vedi §4).
- `_describe_unmatched(finding)` (`utils/cvss_eval.py:255`) — ricalcola lo score ufficiale sul vettore stimato anche per i finding senza CVE, per poterli ordinare in triage.
- `recompute_saved_results(results_path=None)` (`utils/cvss_eval.py:575`) — **ricalcolo retroattivo**: itera ogni JSON salvato, ricalcola `cvss_eval` (sull'answer finale) e `cvss_eval_pass1` (sul primo tentativo in `history[0]`) usando `evaluate_cvss_estimate`, riscrive il file se cambiato. Permette di applicare nuova logica di matching/metriche senza rilanciare esperimenti — invocabile con `python -m utils.cvss_eval`.

In `evaluation_utils.py`, il gruppo funzionale che presenta questi dati:

| Funzione | Riga | Cosa fa |
| --- | --- | --- |
| `_build_cvss_section(roles, experiment_id, results_path)` | `:445` | Entry point Blocco B: verifica presenza di `cvss_eval`, calcola le etichette di ricorrenza una volta sola (`_compute_finding_groups`), poi concatena vector-detail, unmatched, e tutte le sotto-sezioni di metriche (M1-M5/S1-S3), con un'intestazione che distingue esplicitamente "headline metrics" da "legacy diagnostics" (commit `74963d8`, feedback 2026-07-16: "Aggregate metrics" da solo si leggeva come *gli* aggregati, come se M/S fossero altro). |
| `_normalize_function_name(function)` | `:1163` | Rimuove annotazioni finali tipo `"(PCF)"`/`"(Cross-NF ...)"` che l'agente talvolta appende al nome funzione, per non trattare la stessa funzione come due location diverse. |
| `_highlight_function(text, function)` | `:1148` | Grassetta ogni occorrenza del nome funzione nel testo (gestisce sia il caso backtick-wrapped che plain) per i file di dettaglio. |
| `_letter_label(n)` | `:1175` | Converte un intero in etichetta stile foglio di calcolo (a, b, ..., z, aa, ab, ...) per le lettere di ricorrenza. |
| `_cluster_unmatched_findings(entries, semantic_check=True)` | `:1185` | Raggruppa finding unmatched ricorrenti: fase 1 (deterministica, gratuita) raggruppa per `(task_id, role, function_norm, vector)` identici; fase 2 (LLM, cachata) risolve i casi ambigui — stessa funzione ma vettore diverso (stesso bug ri-stimato vs due bug distinti nella stessa funzione). |
| `_compute_finding_groups(roles, semantic_check=True)` | `:1285` | Unifica le etichette di ricorrenza tra tabella "matched" e "unmatched": un finding unmatched la cui funzione coincide con uno degli handler di una CVE già matchata in quella repetizione condivide la lettera con quella CVE (stessa regola di containment di `_match_finding`, deterministica, no LLM) — evidenzia i "duplicati probabili" (commit `71fa41a` / call 13 follow-up). |
| `_final_answer_with_prompt(p)` | `:1401` | Ricompone `final_answer` (whitelisted su disco) con `prompt_system`/`prompt_user` presi da `history[-1]` per la visualizzazione nei file di dettaglio. |
| `_fence_for(text)` | `:1416` | Sceglie una fence di backtick abbastanza lunga da non chiudersi prematuramente sul contenuto del testo (i prompt contengono già blocchi \`\`\`go/\`\`\`md). |
| `_build_prompt_detail_block(final_answer)` | `:1427` | Blocco `<details>` collassabile col prompt esatto inviato al modello. |
| `_write_unmatched_finding_file(...)` | `:1449` | Scrive un file `.md` autonomo per ogni finding senza CVE GT (dati strutturati + narrativa dell'agente). |
| `_write_matched_finding_file(...)` | `:1498` | Analogo per i finding matchati (aggiunge CVE ID, vettore pubblicato). |
| `_build_cvss_unmatched(roles, experiment_id, results_path, unmatched_markers=None)` | `:1552` | Tabella markdown di tutti i finding unmatched, ordinata per `computed_score_B` decrescente (triage order); crea `results/evaluation/unmatched_findings/*.md`. |
| `_build_cvss_vector_detail(roles, experiment_id, results_path, matched_labels=None)` | `:1657` | Tabella per-CVE (stimato vs pubblicato, metrica per metrica) per ogni finding matchato; crea `results/evaluation/matched_findings/*.md`. |

### 3.6 Metriche aggregate M1-M5 / S1-S3

Tutte importano funzioni da `utils/cvss_eval.py` e si limitano ad aggregare/presentare (nessuna logica di matching qui):

| Funzione | Riga | Metrica | Note |
| --- | --- | --- | --- |
| `_build_detection_metrics_section(roles, heading="###")` | `:593` | M1 (detection rate/coverage), M2 (precision/recall/F1), M3 (alerts/TP) | Confronta "final answer" (`cvss_eval`) vs "first attempt" (`cvss_eval_pass1`, storicamente chiamati pass@k/pass@1 — rinominati per call 13, commento nel codice: "pass@k" suggeriva erroneamente best-of-k campioni indipendenti). Calcola sia micro-media (pooled) sia macro-media per task (`_macro_average`), quest'ultima esclude task senza CVE mappata (`expected_tp_fn == 0`, es. `task9_vuln_cross`) e richiede ≥2 task per essere mostrata. Include un **sanity check**: `TP+FN` deve uguagliare la somma delle CVE target attese; se non torna, stampa un warning esplicito nel report invece di fallire silenziosamente. |
| `_build_precision_at_k_section(roles, heading="###")` | `:747` | Precision@K (K=1,3,5) | Introdotta 2026-07-21 su feedback relatore. Ranking per `computed_score_B` (mai la GT). Repetizioni con meno di K finding sono escluse dalla media di quel K (non contate come 0). |
| `_build_variability_section(roles, heading="###")` | `:808` | Media/std/CI95% di TP e FP per task | Usa `scipy.stats.t` (Student-t, df=n-1); con n=3 repetizioni t≈4.30 → CI larga, commentato esplicitamente come "rough order-of-magnitude bound", non garanzia statistica stretta. |
| `_build_cve_rep_matrix(roles, heading="###")` | `:864` | Matrice CVE × repetizione | Puramente visualizzazione, nessuna nuova metrica: mostra ✓/✗ per ogni CVE candidata in ogni repetizione + conteggio FP per rep. |
| `_build_retry_channel_section(roles, heading="###")` | `:926` | Delta di detection per canale di retry (SGV vs rubrica) | Ricalcola `evaluate_cvss_estimate` su **ogni** entry di `history` (nessuna nuova run, nessun LLM) e attribuisce il delta TP/FP tra tentativo i e i+1 al gate che ha respinto il tentativo i (`_retry_cause`). |
| `_build_sgv_detection_cross_section(roles, heading="###")` | `:995` | Precisione incrociata con conformità SGV | Bucket "conform"/"non-conform"/"no SGV record" sulla base dell'ultimo `sgv_eval.per_finding` della repetizione; risponde alla domanda se i controlli sintattici SGV correlano con correttezza sostanziale. |
| `_build_severity_metrics_section(roles, heading="###")` | `:1064` | S1 (exact match vettore), S2 (accuratezza per-metrica + distanza ordinale), S3 (baseline modale) | Calcolate **solo su TP** (finding matchati); usa `EXPLOITABILITY_METRICS`/`IMPACT_METRICS`/`SUBSEQUENT_METRICS` e `aggregate_severity_metrics` da `cvss_eval.py`. |

### 3.7 Report a livello di ruolo/task (Blocco A — rubrica LLM-judge)

| Funzione | Riga | Cosa fa |
| --- | --- | --- |
| `_build_scores_table(roles)` | `:239` | Tabella per ruolo: accuracy, avg_confidence, brier_score, avg_attempts, e — a seconda del mix di `task_type` presenti (math/textual/misto) — `avg_math_delta` e/o `avg_textual_norm`. |
| `_build_cost_metrics_section(roles)` | `:321` | M5: tempo di parete medio (`elapsed_seconds`) e token medi (agent_in/out, judge_in/out) per ruolo. Si applica a ogni tipo di task, non solo CVSS. Nota nel codice: i token possono essere `n/a` sui modelli hostati via Ollama Cloud, non sempre riportati (mentre Ollama locale li riporta sempre). |

### 3.8 Assemblaggio del report finale e scrittura su disco

| Funzione | Riga | Cosa fa |
| --- | --- | --- |
| `_build_run_id_note(all_payloads)` | `:1746` | Riga di intestazione con i `run_id` inclusi nel report, per ruolo — per non dover incrociare a mano nomi di cartella/timestamp. |
| `_build_experiment_report(experiment_id, roles, task_filter=None, per_task_id=None, results_path=RESULTS_PATH)` | `:1760` | Assembla l'intero documento Markdown di un task/esperimento: calcola summary/anomalie (Blocco A), richiama tutte le sezioni CVSS/SGV, costruisce una tabella dei contenuti (TOC) dinamica basata sugli anchor `<a id=...>` effettivamente presenti. **Ordine dei blocchi deliberato** (commento nel codice, commit `74963d8`, feedback 2026-07-16): Blocco B (CVSS deterministico) apre il report, Blocco C (SGV) segue, Blocco A (rubrica LLM) chiude; dentro il Blocco B il dettaglio per-finding precede i roll-up aggregati (commit `3a2b430`/feedback 2026-07-13: un lettore calibra prima "l'agente dice cose sensate" sul dettaglio, poi usa gli aggregati per la visione globale). |
| `_write_evaluation_reports(results_path, task_filter=None, experiment_ids=None, run_id=None)` | `:1954` | Entry point pubblico: chiama `_collect_results`, poi per ogni `experiment_id` (default `["1A", "1B"]`) e ogni `task_id` scrive `results/evaluation/result_<task_id>_<experiment_id>.md`. Se sia "1A" che "1B" sono nello scope, scrive anche `comparison.md`: tabella accuracy 1A vs 1B per ruolo, più un rollup pooled cross-task delle metriche M1-M3/S1-S3/M5 (motivazione nel commento: le cifre per-task sono rumorose con n=3 ripetizioni e poche CVE per task — es. S3 baseline degenera a 100% su task a singola CVE — mentre il pooling su tutti i task vuln dà il numero headline statisticamente significativo). |

### 3.9 CLI

Il blocco `if __name__ == "__main__":` (`:2050`) espone:
- `--list-runs`: stampa la tabella di `list_runs`.
- `--run-id <id>`: rigenera i report filtrati su un solo `run_id`.
- nessun argomento: rigenera tutti i report (stesso comportamento automatico di fine-run di `main.py`, non ispezionato in questo file).

## 4. Ogni metrica: definizione esatta nel codice

Formule prese testualmente dal codice (`utils/cvss_eval.py` salvo indicazione contraria).

| Metrica | Formula / logica | Riferimento |
| --- | --- | --- |
| **M1** — Detection rate | `detected / len(with_targets)`, dove `detected` = repetizioni con ≥1 CVE matchata tra quelle con almeno una CVE target. **Avg coverage**: media di `matched/n_target_cves` per repetizione. | `cvss_eval.py:374-377` |
| **M2** — Precision/Recall/F1 | `precision = tp/(tp+fp)`; `recall = tp/(tp+fn)`; `f1 = 2·P·R/(P+R)`. Micro-media (pooled TP/FP/FN sommati su tutte le repetizioni) di default; macro-media (media semplice per-task, esclude task con `expected_tp_fn == 0`) mostrata solo con ≥2 task pooled (introdotta 2026-07-21, motivazione nel commento: un task rumoroso come UDM — oltre un terzo di tutti i FP pooled — pesava per volume nella micro-media). | `cvss_eval.py:366-372`, `evaluation_utils.py:627-651` |
| **M3** — Alerts per TP | `(tp+fp)/tp`, `None` se `tp==0`. | `cvss_eval.py:382` |
| **Precision@K** | Per repetizione: ranking di tutti i finding finali (matched+unmatched) per `computed_score_B` (fallback su `estimated_score`/`declared_score`), poi `sum(is_tp for top K)/K`; repetizioni con meno di K finding escluse dalla media di quel K, non contate come 0. Media finale = media semplice sulle repetizioni incluse (macro-style). | `cvss_eval.py:408-454` |
| **Variabilità run-to-run** | Media, deviazione standard campionaria, CI 95% (Student-t, df=n−1) di TP e FP *per task* attraverso le repetizioni; richiede n≥2. | `cvss_eval.py:457-483` |
| **S1** — Exact match vettore | `sum(exact_match)/n` sui soli finding matchati (TP); `exact_match` = tutti i campi del vettore stimato *effettivamente emesso* (8 base, 11 se SC/SI/SA presenti) uguali al pubblicato. | `cvss_eval.py:522`, `cvss_eval.py:230-237` |
| **S2** — Accuratezza per-metrica + distanza ordinale | Per ogni metrica (AV,AC,AT,PR,UI,VC,VI,VA,SC,SI,SA): `accuracy = matches/n`; `avg_distance = mean(|indice_stimato - indice_gt| / (len(scale)-1))` sull'ordine di severità definito in `SEVERITY_ORDER`. | `cvss_eval.py:524-543` |
| **S3** — Baseline modale | Modello nullo che indovina sempre il vettore modale (per metrica, valore più frequente) tra le CVE candidate nello scope; `baseline_exact = share di vettori pubblicati che coincidono col modale su tutte le metriche in scope`. Con una sola CVE target il baseline degenera a 100% per costruzione (commento esplicito: "real property of the dataset, not a bug"). | `cvss_eval.py:486-563` |
| **M5** — Costo | Media di `elapsed_seconds`, e di `tokens.agent_in/agent_out/judge_in/judge_out` per ruolo, su ogni tipo di task (non solo vuln). | `evaluation_utils.py:321-369` |
| **Score band** (diagnostico legacy) | `_score_band(estimated, reference)`: cerca la prima soglia in `config.CVSS_SCORE_BANDS = [(0.5, 3), (1.5, 2), (3.0, 1)]` tale che `|estimated-reference| <= max_delta`, altrimenti 0. | `cvss_eval.py:88-94`, `config.py:77` |
| **Severity distance (exploitability/impact/subsequent)** | Media delle distanze ordinali normalizzate per gruppo di metriche; valore stimato mancante/invalido conta come distanza massima (1.0). | `cvss_eval.py:125-137` |
| **Hamming distance** | Conteggio dei campi (tra gli 8 richiesti, AV..VA) diversi tra vettore stimato e pubblicato. | `cvss_eval.py:226-228` |
| **Score coherence delta** | `|score dichiarato dall'agente − score ricalcolato dal suo stesso vettore|` — le due uscite sono prodotte indipendentemente, nulla le forza a coincidere (commento esplicito nel docstring del modulo). | `cvss_eval.py:247-250` |
| **Brier score** (Blocco A, non-vuln) | `mean((confidence - is_correct)^2)`, `is_correct = 1.0 if verdict=="correct" else 0.0`. | `evaluation_utils.py:228-236` |

## 5. Decisioni di design osservabili + perché

- **Non-discard SGV**: un finding che fallisce sistematicamente G1–G4 non viene mai scartato, solo segnalato — dichiarato esplicitamente nel docstring di `_build_sgv_section` (`:372-378`) come "design choice, see `docs/sgv_protocol/06_implementazione_2026-07-14.md`" (riferimento a doc, non verificabile da codice, ma la scelta stessa è visibile nel comportamento: il finding resta in `cvss_eval`).
- **First-match, no GT-aware tie-break** in `_match_finding`: motivato nel docstring come necessità di non "leakare" la ground truth nel pairing quando lo stesso handler compare più volte in output — bias verso l'alto su S altrimenti. Verificabile leggendo la logica: `remaining` viene consumato in ordine di iterazione sui finding dell'agente, non per bontà del match.
- **Rinomina pass@1/pass@k → first attempt/final answer** (commit `96285e3`/`74963d8`, motivazione nel commento a `:595-603`): "pass@k" suggeriva erroneamente un best-of-k campionamento indipendente, mentre il sistema è valutato come black-box sulla risposta finale accettata dopo i retry.
- **Micro vs macro average** (introdotta commit `a3308b2`→raffinata 2026-07-21): la micro-media pooled è dominata per volume da task rumorosi (commento cita esplicitamente UDM, >1/3 dei FP pooled); la macro-media pesa ogni task ugualmente ed esclude i task senza CVE mappata.
- **Ordine dei blocchi nel report** (commit `74963d8`, 2026-07-16 e `3a2b430`, 2026-07-13): Blocco B prima (metriche deterministiche), poi C (SGV), poi A (giudizio LLM); dentro B, dettaglio prima degli aggregati — entrambe le scelte motivate nei commenti come risposta diretta a feedback ricevuto (citato testualmente nel codice, non nei doc).
- **Padding SC/SI/SA con "N"** in `compute_base_score`: giustificato dal fatto che ogni CVE nel dataset ground-truth ha SC/SI/SA=N, quindi il padding non distorce mai il confronto — ma **solo per il punteggio ricalcolato**; per S1/S2 i campi non emessi non vengono paddati proprio per non "regalare punti" alle run più vecchie che non li includevano (commento esplicito a `cvss_eval.py:216-218` e `230-237`).
- **CI95 con t di Student invece di normale**: scelta esplicitamente giustificata per n piccolo (3 repetizioni tipiche) dove l'approssimazione normale sarebbe troppo ottimistica.
- **Formato dati doppio (nuovo/vecchio)** in `_collect_results`: il formato vecchio (un file per repetizione) non ha `run_id`, quindi non passa mai un filtro `--run-id` — comportamento dichiarato nel commento, non un bug.

## 6. Punti aperti / fragilità / soglie hardcoded sospette

- **`CVSS_SCORE_BANDS = [(0.5, 3), (1.5, 2), (3.0, 1)]`** (`config.py:77`) — soglie di prossimità arbitrarie per il punteggio "a bande" (0.5/1.5/3.0 punti di scarto → 3/2/1/0 punti banda). Usate solo per le metriche "legacy diagnostics", non per le metriche headline M/S — il codice stesso le declassa esplicitamente a "diagnostic only, not the headline metric" (`evaluation_utils.py:544-551`).
- **`MAX_RETRIES = 3`** (`config.py:44`) — determina quanti tentativi SGV/rubrica prima di accettare comunque il finding; non c'è verifica nel modulo che 3 sia sufficiente, è un limite fisso.
- **Sanity check TP+FN == expected_tp_fn** (`cvss_eval.py:384-389`): il codice stesso segnala che un mismatch "means a bug in the matching/aggregation logic" — è un self-check che indica che il matching non è stato formalmente verificato altrove, solo controllato a runtime nel report.
- **`_match_finding` è puro string-containment** (`h in function or function in h`): nessuna normalizzazione oltre lowercase/rimozione annotazioni tra parentesi — nomi di funzione parzialmente sovrapposti (es. prefissi/suffissi comuni) potrebbero produrre falsi match o mancati match; non c'è test di unicità o ambiguità nel codice.
- **`_cluster_unmatched_findings`/`_compute_finding_groups` dipendono da LLM con cache non invalidata**: la cache in `semantic_cache.json` è chiave-hash sui contenuti, ma non c'è meccanismo di scadenza/versionamento — se cambia il modello di `semantic_check` in `config.MODELS`, le voci vecchie restano in cache e vengono riusate silenziosamente (nessun invito a invalidare nel codice).
- **S3 baseline degenera a 100% con una sola CVE per task** — comportamento riconosciuto esplicitamente nel codice come "real property of the dataset, not a bug", ma resta un limite interpretativo: qualunque lettura di S1/accuracy "sopra baseline" su task a singola CVE è priva di significato.
- **`avg elapsed`/token M5**: token `n/a` sistematici per modelli hostati via Ollama Cloud (commentato nel codice) — la metrica di costo non è comparabile 1:1 tra modelli locali e hostati quando i token mancano.
- **`_write_evaluation_reports` con `experiment_ids` di default `["1A", "1B"]`** hardcoded nella firma della funzione — qualunque terzo esperimento richiederebbe di passare esplicitamente la lista, altrimenti verrebbe ignorato silenziosamente.

Fonti: solo codice sorgente + git log, nessun documento in docs/ consultato.
