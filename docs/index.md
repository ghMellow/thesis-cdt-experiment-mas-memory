# docs/ — indice minimale per cartella

Vista rapida: per ogni cartella (reale o virtuale) e per ogni md sparso in `docs/`, il perché esiste e cosa contiene. Per il dettaglio file-per-file vedi [README.md](README.md); questo file è un livello sopra, per orientarsi in 30 secondi.

---

## Cartelle

| Cartella | Perché esiste | Cosa si trova |
|---|---|---|
| [codemap/](codemap/) | "Code-as-truth": sapere cosa fa il codice *oggi*, senza fidarsi delle note di processo che possono essere disallineate | Un file per modulo generato solo da codice+git log, indice `00_indice.md`, vista trasversale `flusso.md`/`mappa_sistema.md`, doppio narrativo in `narrativa/` |
| [cve_experiment/](cve_experiment/) | Documentare l'esperimento "singolarità": riprodurre la scoperta spontanea della regex `\|.+` (GHSA-6gxq-gpr8-xgjp) in free5GC | Presentazione (`README.md`), guida pratica (`hands_on.md`), log autoritativo di tutti i tentativi (`attempts/log.md` + `attempts/<N>/`), dati di scan gestiti dalle skill `/cve-attempt`, `/cve-branch-scan`, `/task-branch-map` |
| [sgv_protocol/](sgv_protocol/) | Tracciare la proposta del relatore (sostituire il retry guidato da giudice con un verificatore sintattico deterministico) dalla discussione all'implementazione | Proposta originale, discussioni di team, implementazione G1–G4 (`utils/sgv.py`), metriche M/S, guida di lettura, tabelle dati per il paper |
| [judge_rubric/](judge_rubric/) | Cartella gemella di `sgv_protocol/`: discutere il giudice a rubrica e come svincolarlo dalla ground truth (oggi la rubrica è scritta a partire dalla GT) | Antecedenti di call, stato attuale, paper di riferimento (MT-Bench, LLM-as-a-Verifier, LLM Judges Too Generous), esperimenti di calibrazione v1→v3, banco di prova C1/C2 riusabile |
| [semantica_esplicita/](semantica_esplicita/) | Discussione aperta: aggiungere un validatore ontologico come controllo semantico esplicito, oggi assente (il giudice LLM è semantica solo implicita) | Nascita del tema (call 15), analisi di fattibilità — nessuna implementazione, azioni assegnate sono handoff esterno |
| [cve_matching/](cve_matching/) | Discussione chiusa (per ora): matching deterministico CVE↔handler quando una CVE copre più funzioni gemelle (oggi solo UDM) | Meccanismo e impatto misurato, opzioni valutate, decisione di lasciare il codice invariato |
| [expert_review/](expert_review/) | Prima valutazione esterna sulla rubrica-only, che ha innescato correzioni e il resto dello sviluppo del progetto | Correzione della prima versione rubrica-only, commenti in chat, materiale CVE/CVSS di riferimento |
| [results_reference/](results_reference/) | Tenere schema e pacchetto di validazione esterna separati da `results/`, per non confonderli con gli output delle run | Schema JSON (`schema_math.json`, `schema_textual.json`), cartella `validation/` |
| [sast_tools/](sast_tools/) | Ledger install/uso/rimozione dei tool SAST esterni (gosec, semgrep) usati per l'esperimento, gestito dalla skill `/sast-tools-lifecycle` | Log di installazione (`install_log.md`), ground truth vulnerabilità note (`ground_truth_vuln_files.json`) |
| [tasks/](tasks/) | I task di code review letti **verbatim** come prompt dagli agenti sotto test (`utils/task_utils.py`) — niente note di processo qui dentro, altrimenti inquinano il prompt | `task1`–`task9` (math + textual), ciascuno con file soluzione `_sol.md` |
| [supporto/](supporto/) | Materiale ausiliario: non necessario per capire lo stato attuale, utile come archivio/riferimento | Verbali call (`calls/`) + trascrizioni audio grezze, outline/presentazioni tesi, materiale esterno di riferimento, archivio storico |
| [chat_exports/](chat_exports/) | Esportazioni leggibili di sessioni Claude Code rilevanti, per condividerle senza riaprire il transcript grezzo | `judge_rubric-2026-07-17.md` |

---

## `codemap/` — cosa guardare per primo: `mappa_sistema.md`

`codemap/` ha tre livelli di dettaglio sullo stesso codice (`flusso.md` prosa minimale, `00_indice.md`/`narrativa/` un file per modulo). **`mappa_sistema.md` è l'unico da leggere davvero**: copre tutta la pipeline in un solo documento, diagrammi Mermaid inclusi, con fonte codice+commit per ogni scelta — gli altri due livelli sono utili solo se serve o meno dettaglio o più prosa dello stesso contenuto.

Cosa contiene, in ordine:

- **Pipeline** (§Pipeline): 4 diagrammi — vista a blocchi, flusso completo per ripetizione, macchina a stati del retry, schema dati persistito (JSON).
- **Approfondimenti per blocco** (7 sezioni, stesso ordine del flusso): come si costruisce il prompt (hint SAST/CVSS/retry inclusi), il gate SGV G1→G4 nel dettaglio, `check_answer` matematico vs rubrica testuale, la rubrica GT-free (traccia di calibrazione separata, mai in produzione), come nasce un report Markdown, le metriche M1–M5/S1–S3 (definizioni ancorate al codice — per l'interpretazione estesa rimanda a `sgv_protocol/08_guida_metriche.md`), sequenza di chiamate.
- **Decisioni architetturali** (ADR-1→ADR-11): ogni scelta di design con citazione verbatim del commit che la giustifica — es. perché G3 non ha fallback LLM (ADR-2), perché il matching CVE↔handler è first-match senza tie-break (ADR-8, collegato a `findings.md` F23).
- **Domande aperte**: bug/inconsistenze trovate leggendo il codice (es. `_result_exists` tratta un JSON corrotto come inesistente, un commento in `config.py` in contraddizione col valore effettivo) — non narrativa, osservazioni dirette sul codice attuale.

Regola di lettura (da `CLAUDE.md`): tutto qui è "cosa fa il codice oggi", fonte esclusiva codice+git log — mai le note di call o le proposte discusse nelle altre cartelle.

---

## Cartella virtuale — md di esperimento/processo sparsi in `docs/`

Non sono in una cartella fisica, ma appartengono concettualmente allo stesso gruppo "processo/esperimento" delle cartelle sopra (vedi `CLAUDE.md`: fonte primaria per "perché si è deciso", non per "cosa fa il codice oggi").

| File | Perché esiste | Cosa contiene |
|---|---|---|
| [findings.md](findings.md) | Registro trasversale di tutte le osservazioni empiriche che hanno causato una correzione — copre l'intero progetto, non un singolo esperimento | F1–F23: bug di template, formato output, temperatura, framing expert/beginner, timeout, matching CVE↔handler, ecc. Cross-referenziato da quasi tutte le altre cartelle |
| [experiments_framing.md](experiments_framing.md) | Coda di esperimenti autocontenuta e **chiusa** (2026-07-10): il paradosso "beginner batte expert" su task7, framing vs capacità del modello | Protocollo di esecuzione, esperimenti A1–A3 (framing) e B1–B3 (capacità/scaling), tabelle comparative, risultati — i finding sintetizzati vivono anche in `findings.md` F16–F22 |

---

## md singoli a livello radice (non esperimento/processo)

| File | Descrizione |
|---|---|
| [README.md](README.md) | Punto di ingresso ufficiale della documentazione — indice dettagliato file-per-file, con tre aree (sistema, esperimento CVE, supporto) |
| [status.md](status.md) | Stato/snapshot attuale del sistema: modelli, task, CLI, checklist funzionalità |
| [architecture.md](architecture.md) | Riferimento stabile: mappa del codice, flusso LangGraph, valutazione, report |
| [changelog.md](changelog.md) | Storico modifiche |
| [tasks_provenance.md](tasks_provenance.md) | Provenienza dei file task5-9: cosa è dato grezzo ricevuto vs elaborazione di Claude — tenuto fuori da `tasks/` apposta per non inquinare il prompt verbatim |
| [risultati_template.md](risultati_template.md) | Scheletro da copiare per il prossimo doc `0N_risultati_*.md`: cosa non ripetere, checklist |

---

## Report di run — `results/evaluation/*.md`

**Non sono in `docs/`** (deliberatamente: non versionati salvo richiesta esplicita, vedi `CLAUDE.md`) — vivono in `results/evaluation/`, un file per combinazione `task × experiment_id`, generati automaticamente dalla pipeline di valutazione a partire dai JSON grezzi in `results/<task>/<experiment_id>/`.

**Nome file** → `result_<task>_<experiment_id>.md` (es. `result_task7_vuln_amf_1A_sast_hint.md` = task7, experiment_id `1A_sast_hint`). C'è anche `comparison.md` (pooled 1A vs 1B su tutti i task) e `consistency.md` a livello root di `results/evaluation/`.

**Come si leggono:**

- Header `> Run(s) in this report:` in cima = timestamp (`run_id`) del/dei run aggregati in quel file — usalo per capire se il file riflette dati recenti o una run superata.
- Sezione CVSS estimate → vettore stimato dall'agente vs pubblicato, per CVE matchata.
- Sezione **Detection (M1/M2/M3)** → TP/FP/FN, precision/recall/F1, `final answer` (dopo tutti i retry, il numero "ufficiale") vs `first attempt` (controfattuale come se non ci fosse il retry loop).
- Sezione **Rubric evaluation** → verdetto del giudice LLM (correct/wrong) per ripetizione, breakdown per criterio.
- Ogni tabella ha una **Legend** subito sotto che spiega le colonne — leggerla è più affidabile che indovinare dal nome colonna.
- Guida completa alla lettura (unità di analisi, perché precision è un floor, checklist anti-fraintendimento): [sgv_protocol/08_guida_metriche.md](sgv_protocol/08_guida_metriche.md). Definizioni formali M/S: [sgv_protocol/07_metriche_M_S_2026-07-14.md](sgv_protocol/07_metriche_M_S_2026-07-14.md).

### Caso specifico: run con vs senza hint SAST (SonarQube)

Sintesi già pronta, non serve ricostruirla dai report grezzi: **[sgv_protocol/11_sast_hint_noise_test_2026-07-21.md](sgv_protocol/11_sast_hint_noise_test_2026-07-21.md)** — conclusione: su excerpt l'hint non fa danni misurabili (pooled 31.0% vs 30.5% precision); su file `_full` l'effetto è reale ma **task-dipendente** (UDR migliora, AMF peggiora nettamente, UDM identico), poi confermato a n=10 rep su UDR.

Report grezzi sottostanti, per task (`sast_hint` = con hint, `no_hint`/baseline `_1A` = senza):

| Task | Con hint | Senza hint |
| --- | --- | --- |
| PCF (task5, unica versione = full) | `result_task5_vuln_pcf_1A_sast_hint.md` | `result_task5_vuln_pcf_1A_no_hint_excerpt.md` |
| UDR excerpt (task6) | `result_task6_vuln_udr_1A_sast_hint.md` | `result_task6_vuln_udr_1A_no_hint_excerpt.md` |
| UDR full (task6, esteso a n=10) | `result_task6_vuln_udr_full_1A_sast_hint_full.md` | `result_task6_vuln_udr_full_1A_no_hint_full.md` |
| AMF excerpt (task7) | `result_task7_vuln_amf_1A_sast_hint.md` | `result_task7_vuln_amf_1A_no_hint_excerpt.md` |
| AMF full (task7) | `result_task7_vuln_amf_full_1A_sast_hint_full.md` | `result_task7_vuln_amf_full_1A.md` (baseline 1A riusato, non un file `_no_hint` dedicato) |
| UDM excerpt (task8) | `result_task8_vuln_udm_1A_sast_hint.md` | `result_task8_vuln_udm_1A_no_hint_excerpt.md` |
| UDM full (task8) | `result_task8_vuln_udm_full_1A_sast_hint_full.md` | `result_task8_vuln_udm_full_1A.md` (baseline 1A riusato) |

---

> Questo file è un indice *di orientamento*, non la fonte di verità sui contenuti — se un file viene spostato/rinominato e questa tabella non è stata aggiornata, fidati della struttura reale di `docs/` e di [README.md](README.md).
