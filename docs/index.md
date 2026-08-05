# docs/ — indice minimale per cartella

Vista rapida: per ogni cartella (reale o virtuale) e per ogni md sparso in `docs/`, il perché esiste e cosa contiene. Per il dettaglio file-per-file vedi [README.md](README.md); questo file è un livello sopra, per orientarsi in 30 secondi.

- [Cartelle](#cartelle)
- [`codemap/` — cosa guardare per primo](#codemap--cosa-guardare-per-primo-mappa_sistemamd)
- [md singoli a livello radice](#md-singoli-a-livello-radice)
  - [Cartella virtuale — md di esperimento/processo](#cartella-virtuale--md-di-esperimentoprocesso-sparsi-in-docs)
- [Report di run — `results/evaluation/*.md`](#report-di-run--resultsevaluationmd)
  - [Caso specifico: run con vs senza hint SAST](#caso-specifico-run-con-vs-senza-hint-sast-sonarqube)
- **[`sgv_protocol/` — dati tabelle in LaTeX per il paper](#sgv_protocol--cosa-guardare-per-primo-i-dati-tabelle-in-latex)**

---

## Cartelle

| Cartella | Perché esiste | Cosa si trova |
| --- | --- | --- |
| [codemap/](codemap/) | "Code-as-truth": sapere cosa fa il codice *oggi*, senza fidarsi delle note di processo che possono essere disallineate | Un file per modulo generato solo da codice+git log, indice [00_indice.md](codemap/00_indice.md), vista trasversale [flusso.md](codemap/flusso.md)/[mappa_sistema.md](codemap/mappa_sistema.md), doppio narrativo in [narrativa/](codemap/narrativa/) |
| [cve_experiment/](cve_experiment/) | Documentare l'esperimento "singolarità": riprodurre la scoperta spontanea della regex `\|.+` (GHSA-6gxq-gpr8-xgjp) in free5GC | Presentazione ([README.md](cve_experiment/README.md)), guida pratica ([hands_on.md](cve_experiment/hands_on.md)), log autoritativo di tutti i tentativi ([attempts/log.md](cve_experiment/attempts/log.md) + `attempts/<N>/`), dati di scan gestiti dalle skill `/cve-attempt`, `/cve-branch-scan`, `/task-branch-map` |
| [sgv_protocol/](sgv_protocol/) | Tracciare la proposta del relatore (sostituire il retry guidato da giudice con un verificatore sintattico deterministico) dalla discussione all'implementazione | [Proposta originale](sgv_protocol/00_proposta_relatore.md), discussioni di team, implementazione G1–G4 (`utils/sgv.py`), metriche M/S, guida di lettura, tabelle dati per il paper |
| [judge_rubric/](judge_rubric/) | Cartella gemella di `sgv_protocol/`: discutere il giudice a rubrica e come svincolarlo dalla ground truth (oggi la rubrica è scritta a partire dalla GT) | Antecedenti di call, stato attuale, paper di riferimento (MT-Bench, LLM-as-a-Verifier, LLM Judges Too Generous), esperimenti di calibrazione v1→v3, banco di prova C1/C2 riusabile |
| [semantica_esplicita/](semantica_esplicita/) | Discussione aperta: aggiungere un validatore ontologico come controllo semantico esplicito, oggi assente (il giudice LLM è semantica solo implicita) | Nascita del tema (call 15), analisi di fattibilità — nessuna implementazione, azioni assegnate sono handoff esterno |
| [cve_matching/](cve_matching/) | Discussione chiusa (per ora): matching deterministico CVE↔handler quando una CVE copre più funzioni gemelle (oggi solo UDM) | Meccanismo e impatto misurato, opzioni valutate, decisione di lasciare il codice invariato |
| [expert_review/](expert_review/) | Prima valutazione esterna sulla rubrica-only, che ha innescato correzioni e il resto dello sviluppo del progetto | Correzione della prima versione rubrica-only ([00](expert_review/00_correzione_prima_versione_solo_rubrica.md)), commenti in chat ([01](expert_review/01_chat_comments.md)), validazione manuale di Lorenzo dei finding CVE/CVSS in due round: solo no-SAST ([02](expert_review/02_CVE_CVSS.docx.md), 10 nuove CVE confermate) e no-SAST+SAST ([03](expert_review/03_CVE_CVSS_sast.md), 10+2=12 — include anche il suo commento qualitativo su perché il SAST aiuta la validazione, con relativo caveat sul confound run-count) |
| [results_reference/](results_reference/) | Tenere schema e pacchetto di validazione esterna separati da `results/`, per non confonderli con gli output delle run | Schema JSON ([schema_math.json](results_reference/schema_math.json), [schema_textual.json](results_reference/schema_textual.json)), cartella [validation/](results_reference/validation/) |
| [sast_tools/](sast_tools/) | Ledger install/uso/rimozione dei tool SAST esterni (gosec, semgrep) usati per l'esperimento, gestito dalla skill `/sast-tools-lifecycle` | Log di installazione ([install_log.md](sast_tools/install_log.md)), ground truth vulnerabilità note ([ground_truth_vuln_files.json](sast_tools/ground_truth_vuln_files.json)) |
| [tasks/](tasks/) | I task di code review letti **verbatim** come prompt dagli agenti sotto test (`utils/task_utils.py`) — niente note di processo qui dentro, altrimenti inquinano il prompt | [task1](tasks/task1_math_int.md)–[task9](tasks/task9_vuln_cross.md) (math + textual), ciascuno con file soluzione `_sol.md` |
| [supporto/](supporto/) | Materiale ausiliario: non necessario per capire lo stato attuale, utile come archivio/riferimento | Verbali call ([calls/](supporto/calls/)) + trascrizioni audio grezze, outline/presentazioni tesi, materiale esterno di riferimento, archivio storico |
| [chat_exports/](chat_exports/) | Esportazioni leggibili di sessioni Claude Code rilevanti, per condividerle senza riaprire il transcript grezzo | [judge_rubric-2026-07-17.md](chat_exports/judge_rubric-2026-07-17.md) |

---

## `codemap/` — cosa guardare per primo: `mappa_sistema.md`

`codemap/` ha tre livelli di dettaglio sullo stesso codice ([flusso.md](codemap/flusso.md) prosa minimale, [00_indice.md](codemap/00_indice.md)/[narrativa/](codemap/narrativa/) un file per modulo). **[mappa_sistema.md](codemap/mappa_sistema.md) è l'unico da leggere davvero**: copre tutta la pipeline in un solo documento, diagrammi Mermaid inclusi, con fonte codice+commit per ogni scelta — gli altri due livelli sono utili solo se serve o meno dettaglio o più prosa dello stesso contenuto.

Cosa contiene, in ordine:

- **Pipeline** (§Pipeline): 4 diagrammi — vista a blocchi, flusso completo per ripetizione, macchina a stati del retry, schema dati persistito (JSON).
- **Approfondimenti per blocco** (7 sezioni, stesso ordine del flusso): come si costruisce il prompt (hint SAST/CVSS/retry inclusi), il gate SGV G1→G4 nel dettaglio, `check_answer` matematico vs rubrica testuale, la rubrica GT-free (traccia di calibrazione separata, mai in produzione), come nasce un report Markdown, le metriche M1–M5/S1–S3 (definizioni ancorate al codice — per l'interpretazione estesa rimanda a [sgv_protocol/08_guida_metriche.md](sgv_protocol/08_guida_metriche.md)), sequenza di chiamate.
- **Decisioni architetturali** (ADR-1→ADR-11): ogni scelta di design con citazione verbatim del commit che la giustifica — es. perché G3 non ha fallback LLM (ADR-2), perché il matching CVE↔handler è first-match senza tie-break (ADR-8, collegato a [findings.md](findings.md) F23).
- **Domande aperte**: bug/inconsistenze trovate leggendo il codice (es. `_result_exists` tratta un JSON corrotto come inesistente, un commento in `config.py` in contraddizione col valore effettivo) — non narrativa, osservazioni dirette sul codice attuale.

Regola di lettura (da `CLAUDE.md`): tutto qui è "cosa fa il codice oggi", fonte esclusiva codice+git log — mai le note di call o le proposte discusse nelle altre cartelle.

---

## md singoli a livello radice

| File | Descrizione |
| --- | --- |
| [README.md](README.md) | Punto di ingresso ufficiale della documentazione — indice dettagliato file-per-file, con tre aree (sistema, esperimento CVE, supporto) |
| [status.md](status.md) | Stato/snapshot attuale del sistema: modelli, task, CLI, checklist funzionalità |
| [architecture.md](architecture.md) | Riferimento stabile: mappa del codice, flusso LangGraph, valutazione, report |
| [changelog.md](changelog.md) | Storico modifiche |
| [tasks_provenance.md](tasks_provenance.md) | Provenienza dei file task5-9: cosa è dato grezzo ricevuto vs elaborazione di Claude — tenuto fuori da `tasks/` apposta per non inquinare il prompt verbatim |
| [risultati_template.md](risultati_template.md) | Scheletro da copiare per il prossimo doc `0N_risultati_*.md`: cosa non ripetere, checklist |

### Cartella virtuale — md di esperimento/processo sparsi in `docs/`

Non sono in una cartella fisica, ma appartengono concettualmente allo stesso gruppo "processo/esperimento" delle cartelle sopra (vedi `CLAUDE.md`: fonte primaria per "perché si è deciso", non per "cosa fa il codice oggi").

| File | Perché esiste | Cosa contiene |
| --- | --- | --- |
| [findings.md](findings.md) | Registro trasversale di tutte le osservazioni empiriche che hanno causato una correzione — copre l'intero progetto, non un singolo esperimento | F1–F23: bug di template, formato output, temperatura, framing expert/beginner, timeout, matching CVE↔handler, ecc. Cross-referenziato da quasi tutte le altre cartelle |
| [experiments_framing.md](experiments_framing.md) | Coda di esperimenti autocontenuta e **chiusa** (2026-07-10): il paradosso "beginner batte expert" su task7, framing vs capacità del modello | Protocollo di esecuzione, esperimenti A1–A3 (framing) e B1–B3 (capacità/scaling), tabelle comparative, risultati — i finding sintetizzati vivono anche in [findings.md](findings.md) F16–F22 |

---

## Report di run — `results/evaluation/*.md`

**Non sono in `docs/`** (deliberatamente: non versionati salvo richiesta esplicita, vedi `CLAUDE.md`) — vivono in `results/evaluation/`, un file per combinazione `task × experiment_id`, generati automaticamente dalla pipeline di valutazione a partire dai JSON grezzi in `results/<task>/<experiment_id>/`.

**Nome file** → `result_<task>_<experiment_id>.md` (es. `result_task7_vuln_amf_1A_sast_hint.md` = task7, experiment_id `1A_sast_hint`). C'è anche [comparison.md](../results/evaluation/comparison.md) (pooled 1A vs 1B su tutti i task) e [consistency.md](../results/evaluation/consistency.md) a livello root di `results/evaluation/`.

**Come si leggono:**

- Header `> Run(s) in this report:` in cima = timestamp (`run_id`) del/dei run aggregati in quel file — usalo per capire se il file riflette dati recenti o una run superata.
- Sezione CVSS estimate → vettore stimato dall'agente vs pubblicato, per CVE matchata.
- Sezione **Detection (M1/M2/M3)** → TP/FP/FN, precision/recall/F1, `final answer` (dopo tutti i retry, il numero "ufficiale") vs `first attempt` (controfattuale come se non ci fosse il retry loop).
- Sezione **Rubric evaluation** → verdetto del giudice LLM (correct/wrong) per ripetizione, breakdown per criterio.
- Ogni tabella ha una **Legend** subito sotto che spiega le colonne — leggerla è più affidabile che indovinare dal nome colonna.
- Guida completa alla lettura (unità di analisi, perché precision è un floor, checklist anti-fraintendimento): [sgv_protocol/08_guida_metriche.md](sgv_protocol/08_guida_metriche.md). Definizioni formali M/S: [sgv_protocol/07_metriche_M_S_2026-07-14.md](sgv_protocol/07_metriche_M_S_2026-07-14.md).
- **Precision@K** (P@1/P@3/P@5, "se mi fido solo dei top-K alert più severi quanti sono veri") → codice in `utils/cvss_eval.py::aggregate_precision_at_k` (calcolo) e `utils/evaluation_utils.py::_build_precision_at_k_section` (sezione report); dato pooled in [../results/evaluation/comparison.md](../results/evaluation/comparison.md) §Precision@K e nella sezione omonima di ogni `result_task*.md`; tabella LaTeX Tab.5 (vedi mappa Overleaf sotto).

### Caso specifico: run con vs senza hint SAST (SonarQube)

Sintesi già pronta, non serve ricostruirla dai report grezzi: **[sgv_protocol/11_sast_hint_noise_test_2026-07-21.md](sgv_protocol/11_sast_hint_noise_test_2026-07-21.md)** — conclusione: su excerpt l'hint non fa danni misurabili (pooled 31.0% vs 30.5% precision); su file `_full` l'effetto è reale ma **task-dipendente** (UDR migliora, AMF peggiora nettamente, UDM identico), poi confermato a n=10 rep su UDR.

Report grezzi sottostanti — solo le versioni `_full`, quelle effettivamente usate come dati per le tabelle LaTeX (`sast_hint` = con hint, `no_hint`/baseline `_1A` = senza). Gli excerpt (`_excerpt`, non elencati qui) sono stati solo di test preliminare, mai la fonte dei numeri riportati — vedi nota sopra: "su excerpt l'hint non fa danni misurabili... su file `_full` l'effetto è reale":

| Task | Con hint | Senza hint |
| --- | --- | --- |
| PCF (task5, unica versione = full) | [result_task5_vuln_pcf_1A_sast_hint.md](../results/evaluation/result_task5_vuln_pcf_1A_sast_hint.md) | [result_task5_vuln_pcf_1A.md](../results/evaluation/result_task5_vuln_pcf_1A.md) |
| UDR full (task6, esteso a n=10) | [result_task6_vuln_udr_full_1A_sast_hint_full.md](../results/evaluation/result_task6_vuln_udr_full_1A_sast_hint_full.md) | [result_task6_vuln_udr_full_1A_no_hint_full.md](../results/evaluation/result_task6_vuln_udr_full_1A_no_hint_full.md) |
| AMF full (task7) | [result_task7_vuln_amf_full_1A_sast_hint_full.md](../results/evaluation/result_task7_vuln_amf_full_1A_sast_hint_full.md) | [result_task7_vuln_amf_full_1A.md](../results/evaluation/result_task7_vuln_amf_full_1A.md) (baseline 1A riusato, non un file `_no_hint` dedicato) |
| UDM full (task8) | [result_task8_vuln_udm_full_1A_sast_hint_full.md](../results/evaluation/result_task8_vuln_udm_full_1A_sast_hint_full.md) | [result_task8_vuln_udm_full_1A.md](../results/evaluation/result_task8_vuln_udm_full_1A.md) (baseline 1A riusato) |

---

## `sgv_protocol/` — cosa guardare per primo: i dati tabelle in LaTeX

`sgv_protocol/` è la cartella più densa di `docs/` (16 documenti, verbali + implementazione + dati) — non è pensata per essere letta tutta. Se serve solo il **codice LaTeX delle tabelle del paper**, i due file da linkare direttamente sono:

- **[sgv_protocol/10_dati_paper_no_sonarqube.tex](sgv_protocol/10_dati_paper_no_sonarqube.tex)** — condizione baseline, senza hint SAST (run `20260714T152535Z`): Tab.1 precision/alerts-per-TP, Tab.2 exact vector match, Tab.3 accuratezza per-metrica CVSS, Tab.4 costo computazionale, Tab.5 Precision@K, Tab.6 variabilità run-to-run, Tab.7-8 ablation del retry loop (SGV vs rubrica).
- **[sgv_protocol/12_dati_paper_sast_hint.tex](sgv_protocol/12_dati_paper_sast_hint.tex)** — stessa identica struttura di tabelle (Tab.1-8), condizione con hint SAST attivo, per il confronto punto-a-punto affiancato al file precedente.

Entrambi: numeri rigenerati dai payload grezzi con le stesse funzioni di `utils/evaluation_utils.py` (non ricalcolati a mano), richiedono `\usepackage{booktabs}` e `\usepackage{multirow}`. Nessuno dei due copre RQ1 (SAST come strumento standalone, serve ancora SonarQube integrato) né il task cross-NF nel caso hint (mai eseguito in quella condizione).

**Prima di incollare i numeri**, leggi la versione prosa della condizione no-SAST — **[sgv_protocol/10_dati_paper_no_sonarqube.md](sgv_protocol/10_dati_paper_no_sonarqube.md)** — non solo il `.tex`: contiene le note di lettura per ogni tabella (es. "effetto non uniforme, non sempre meglio" su Tab.1bis) e il box di chiusura sulla riconciliazione dei numeri di Lorenzo ([expert_review/02](expert_review/02_CVE_CVSS.docx.md) vs [03](expert_review/03_CVE_CVSS_sast.md), 10 vs 10+2 nuove CVE — due conteggi reali distinti, uno per condizione, non un fraintendimento). Il `.tex` da solo non basta a evitare lo stesso giro di dubbi emerso in call sul 29/07.

### Associazione tabelle locali ↔ tabelle su Overleaf

I due `.tex` sopra sono la fonte dei dati; il paper vero vive su Overleaf e la sua struttura (numerazione, quali tabelle restano nel main body vs finiscono in appendice) **può cambiare nel tempo** senza che questi file lo riflettano subito — quindi questa mappa va trattata come "ultimo aggiornamento noto", non come verità sincronizzata automaticamente. Se una `\label{...}` qui sotto non esiste più su Overleaf, fidati di Overleaf e segnala la voce come da correggere.

| Tabella (contenuto) | Label locale (`no_sonarqube` / `sast_hint`) | Sezione/numero su Overleaf | Divergenze note |
| --- | --- | --- | --- |
| Precision & alerts-per-TP per NF | `tab:detection-no-sast` / `tab:detection-sast-hint` | §IV.B, Tab. 1 / Tab. 1bis (SAST hint) | **Sì, vedi nota sotto** — Tab. 1 su Overleaf è stata modificata a mano. Codice: `utils/cvss_eval.py::aggregate_detection_metrics` / `utils/evaluation_utils.py::_build_detection_metrics_section` |
| Exact CVSS v4.0 vector match (S1) vs baseline modale (S3) | `tab:s1-s3` / `tab:s1-s3-hint` | §IV.B / RQ3, Tab. 2 | Codice: `utils/cvss_eval.py::aggregate_severity_metrics` (+ `_modal_vector`) / `utils/evaluation_utils.py::_build_severity_metrics_section` |
| Accuratezza per-metrica CVSS (S2) | `tab:s2` / `tab:s2-hint` | §IV.B / RQ3, Tab. 3 | Codice: `utils/cvss_eval.py::aggregate_severity_metrics` (+ `_severity_distance`) / `utils/evaluation_utils.py::_build_severity_metrics_section` |
| Costo computazionale (wall-clock) | `tab:cost` / `tab:cost-hint` | §IV.B, Tab. 4 | Codice: `utils/evaluation_utils.py::_build_cost_metrics_section` (nessuna funzione dedicata in `cvss_eval.py` — legge `elapsed_seconds`/tokens già salvati) |
| Precision@K | `tab:precision-at-k` / `tab:precision-at-k-hint` | §IV.B / RQ2, Tab. 5 | Codice: `utils/cvss_eval.py::aggregate_precision_at_k` / `utils/evaluation_utils.py::_build_precision_at_k_section` |
| Variabilità run-to-run (TP/FP, mean±std, CI95) | `tab:variability` / `tab:variability-hint` | §IV.B, Tab. 6 | Codice: `utils/cvss_eval.py::compute_repetition_variability` / `utils/evaluation_utils.py::_build_variability_section` |
| Ablation retry loop (first attempt vs final answer) | `tab:ablation-retry` / `tab:ablation-retry-hint` | §IV.B, Tab. 7 | Codice: stessa `aggregate_detection_metrics` di Tab. 1, applicata a `first attempt` (pre-retry) vs `final answer`, dentro `_build_detection_metrics_section` |
| Attribuzione per canale di retry (SGV vs rubrica) | `tab:ablation-channel` / `tab:ablation-channel-hint` | §IV.B, Tab. 8 | Codice: `utils/evaluation_utils.py::_build_retry_channel_section` (+ `_retry_cause`) |

**Nota su Tab. 1 (`tab:detection-no-sast`, 2026-08-05):** la versione su Overleaf non è più una copia 1:1 del `.tex` locale. Modifiche a mano:

- TP normalizzato a conteggio **per CVE distinta** (1 per NF), non più il pooled raw su 3 ripetizioni (`utils/evaluation_utils.py` dava TP=3/6/3/3 — qui diventa 1/1/1/1) — quindi niente più "×3 ripetizioni" nel conteggio mostrato.
- Aggiunta colonna **New CVE**: candidati tra i finding non matchati, de-duplicati across le 3 ripetizioni (non conteggio per-ripetizione) e confermati genuini da review umana, ma senza CVE catalogata — sottoinsieme della colonna FP, non contano come TP e non entrano in Precision.
- FN mostrato solo su UDR (5, in grassetto nell'originale) — le altre righe a 0.
- Precision e Alerts/TP azzerate/non ricalcolate nella tabella incollata (valori a 0% / 0 in tutte le righe) — probabile placeholder in attesa di rifare il calcolo sul TP normalizzato, da verificare prima della submission.

Questa tabella richiede quindi lettura diretta da Overleaf per i numeri effettivi, non dal `.tex` locale — il file locale resta la fonte per Tab. 2-8 e per il dato grezzo pre-normalizzazione di Tab. 1.

Quando si aggiorna il paper su Overleaf (rinumerazione tabelle, spostamento in appendice, split/merge, altre modifiche a mano come questa), **aggiorna questa mappa nello stesso passaggio** — non aspettare un audit successivo.

---

> Questo file è un indice *di orientamento*, non la fonte di verità sui contenuti — se un file viene spostato/rinominato e questa tabella non è stata aggiornata, fidati della struttura reale di `docs/` e di [README.md](README.md).
