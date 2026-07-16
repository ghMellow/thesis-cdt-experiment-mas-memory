# Stato del sistema — Multi-Agent Experiment 5G

> 🧭 Per la **mappa completa della documentazione** vedi [README.md](README.md). Questo file è lo **stato/snapshot del sistema**.

## Dove trovare i dettagli

| Documento | Contenuto |
| --- | --- |
| [architecture.md](architecture.md) | §1–7 + §9: mappa codice, flusso, valutazione, report — **riferimento stabile** |
| [supporto/calls/call_1.md](supporto/calls/call_1.md) | Call iniziali: judge, soglie, rubrica, retry, confidence, token, consistenza, modelli, lingua (§8.1–8.10) |
| [supporto/calls/call_2.md](supporto/calls/call_2.md) | Call 2026-05-09: security review 5G, task5–9, snapshot sistema (§8.11 + §10) |
| [supporto/calls/call_3.md](supporto/calls/call_3.md) | Call 2026-05-13: presentazione risultati, dubbi metodologici, roadmap 19 maggio |
| [findings.md](findings.md) | Registro empirico: osservazioni che hanno causato correzioni al codice o alla metodologia |
| [cve_experiment/](cve_experiment/README.md) | Esperimento "singolarità": un LLM riscopre da solo la CVE `\|.+`? Presentazione, guida pratica, log #0–#18 |

---

## Stato attuale (snapshot 2026-07-10)

> Questo snapshot copre il **workstream framing** (esperimenti A/B/C). Il workstream **esperimento CVE** (riproduzione scoperta `|.+`) procede in parallelo ed è tracciato separatamente in [cve_experiment/](cve_experiment/README.md) — ultimo aggiornamento #18 (2026-06-30).

Sistema operativo. 12 task disponibili, framework LangGraph con retry/judge/token tracking/semantic consistency.

**Serie framing completata (A1–A3, B1–B3):** il paradosso beginner>expert su task7 è completamente spiegato — effetto framing × capacità confinato alla finestra e4b. Vedi `docs/findings.md` F16–F22 e `docs/experiments_framing.md`. **Prossimo:** C1 — temperature sweep T∈{0.1, 0.7} su task7/8.

**Run 5 completata (2026-07-11):** prima run a contesto pieno (task6/7/8 `_full`) — il rubric accuracy crolla a 0/6 su task6/7 (bug di controllo di flusso/cross-handler diluiti nel file intero, resta invariato su task8/9); matching CVSS peggiora invece di migliorare nonostante più CVE candidate. Narrativa di run superata dal framework attuale (metriche M1-M3/S1-S3 in `results/evaluation/*.md`, standalone).

**Run 4 completata (2026-07-10):** prima run agente unico + matematica ufficiale + prompt a 11 metriche — lo score ricalcolato dal vettore è più affidabile di quello dichiarato; il ranking per il triage va fatto su `computed_score_B`. Narrativa di run superata dal framework attuale.

**Semplificazione post call 11 (2026-07-10):** rimosso il framing expert/beginner (19/20 verdetti identici tra i ruoli — richiesta di Andrea). Ora c'è un **agente unico** con prompt neutro (`SYSTEM_PROMPTS["agent"]`); i risultati nuovi finiscono in `results/<task>/<exp>/agent/`. Il flag CLI `--role` è stato rimosso. La scelta dei modelli resta libera in `config.MODELS`: 1A = stesso modello per agente e giudice, 1B = modelli diversi.

> ⚠️ **Ulteriore semplificazione (2026-07-13):** il framing 1B è stato disattivato in `main.py` (loop `experiments` commentato a `["1A"]`) — il progetto ora esegue solo 1A. La config `agent_1B` resta in `config.py` per riattivazione futura ma non viene più eseguita di default (anche `--experiment all` produce solo 1A).

### Modelli (`config.py`)

| Chiave | Local | Hosted | use_hosted |
| --- | --- | --- | --- |
| `agent_1A` | gemma4:e4b | gemma4:31b-cloud | True |
| `agent_1B` | gemma4:e4b | gemma4:31b-cloud | True |
| `judge` | gemma4:e4b | gemma4:31b-cloud | True |
| `semantic_check` | gemma4:e2b | gemma4:31b-cloud | True |

### Task disponibili

| ID | Tipo |
| --- | --- |
| `task1_math_int`, `task2_math_real` | math |
| `task3_anomaly`, `task4_rootcause` | textual 5G |
| `task5_vuln_pcf` | security review PCF |
| `task6_vuln_udr` | security review UDR excerpt |
| `task6_vuln_udr_full` | security review UDR file completo (2891 righe) |
| `task7_vuln_amf` | security review AMF excerpt |
| `task7_vuln_amf_full` | security review AMF file completo (501 righe) |
| `task8_vuln_udm` | security review UDM excerpt |
| `task8_vuln_udm_full` | security review UDM file completo (858 righe) |
| `task9_vuln_cross` | security review cross-NF |

### Funzionalità implementate / aperte

- [x] Judge con rubrica dinamica per-task (`_build_judge_prompt`)
- [x] Brier score per calibrazione confidence
- [x] Semantic consistency check a due fasi (string equality → LLM)
- [x] Token tracking agent + judge per ripetizione
- [x] Context window logging all'avvio via Ollama `/api/show`
- [x] Task security review task5–task9 (CVE reali free5GC)
- [x] Retry neutro con risposta precedente (senza feedback judge)
- [x] Output Markdown per agent/judge (template Answer/Reasoning/Confidence + parsing)
- [x] Prompt completo salvato per ogni run (`history[n].prompt_system` + `prompt_user`)
- [x] Score intermedi per-attempt in `history[n].judge_score` + `verdict`
- [x] Framing experiments A1–A3: effetto framing beginner isolato e spiegato (F16–F18)
- [x] Framing experiments B1–B3: paradosso confermato come framing × capacità — scala e2b→e4b→31b (F19–F22)
- [x] Accesso modelli cloud (gemma4:31b, gemma3:12b via Ollama Cloud — usati in B1_cloud/B2)
- [x] **Esperimento 2b — stima CVSS (Blocco B)**: sui task vuln l'agente emette anche una stima CVSS 4.0 strutturata, valutata deterministicamente (`utils/cvss_eval.py`) contro `File_Free5gc_Vulnerabili/cve_metrics_normalized.json`; sub-score separati nel report, verdetto non influenzato (vedi `docs/judge_rubric/00_proposta_rubrica_cvss.md`)
- [x] **Esperimento 2b — hint di contesto NF** (`config.CVSS_CONTEXT_HINT_ENABLED`): paragrafo di contesto free5GC/OAuth2/TLS iniettato prima del blocco CVSS, per testare se l'impatto sbagliato dipende da mancanza di contesto di sistema — non ha risolto il problema
- [x] **Semplificazione call 11**: framing expert/beginner rimosso — agente unico con prompt neutro, chiavi `agent_1A`/`agent_1B` in `config.MODELS`, flag `--role` eliminato; i vecchi risultati per-ruolo restano leggibili dai report (aggregazione per cartella)
- [x] **Esperimento 2b — run 3 (REPETITIONS=3)**: stesso hint, 3 ripetizioni per combinazione (60 run). Chiude il dubbio "erano rumore?": il presunto effetto di ruolo su task7 sparisce (era rumore a 1 rep), mentre gli altri effetti osservati si confermano reali con più campioni
- [x] **Valutazione CVSS con matematica ufficiale 4.0** (post call 11): score ricalcolato dal vettore stimato via libreria `cvss` (algoritmo FIRST macrovettori+lookup, validato 10/10 sui vettori GT); coerenza interna score↔vettore, distanza in spazio score, distanza ordinale di severità per campo, Hamming; recompute retroattivo con `python -m utils.cvss_eval` senza rilanciare run
- [x] **Prompt CVSS esteso alle 11 metriche base**: il blocco chiede anche SC/SI/SA (impatto sui sistemi a valle); valutate separatamente (`subsequent_match`/`subsequent_distance`) solo quando emesse, così le run 1–3 restano confrontabili
- [x] **SGV — Syntactic Grounding Verifier** (`utils/sgv.py`, `config.SGV_ENABLED`): gate deterministico in-loop sui task CVSS, senza accesso alla ground truth — G1 (validità formale/schema), G2 (esistenza dei simboli contro l'estratto di codice mostrato all'agente, non la GT), G3 (groundedness dello snippet, opzionale via `config.SGV_SNIPPET_ENABLED`, default attivo — substring poi Jaccard a finestra), G4 (completezza e validità sintattica del vettore CVSS, riusa `_parse_vector`/`SEVERITY_ORDER` di `utils/cvss_eval.py`). Nodo `check_sgv` nel grafo LangGraph tra `run_agent` e `check_answer`, indipendente dal retry guidato dal giudice rubrica (kept separato per ora). Feedback di retry puramente formale, mai sulla natura vulnerabile del codice. Vedi `docs/sgv_protocol/`.
- [x] **Metriche M1/M2/M3 (detection, pass@1 vs pass@k)** (`utils/cvss_eval.py::aggregate_detection_metrics`, `config.CVSS_ESTIMATE_ENABLED`): TP/FP/FN a livello di CVE, precision/recall/F1, detection rate, coverage, alert-per-TP — calcolati sia sul primo tentativo (`cvss_eval_pass1`) sia sull'ultimo dopo i retry (`cvss_eval`, già esistente). Sezione dedicata nel report (Blocco B).
- [x] **Metriche S1/S2/S3 (severity)** (`utils/cvss_eval.py::aggregate_severity_metrics`): match esatto del vettore sui TP (S1), accuratezza e distanza ordinale per singola metrica base (S2), baseline con modello nullo che indovina il vettore modale tra le CVE target del task (S3) — non divisa pass@1/pass@k, misura downstream sulla risposta finale. Sezione dedicata nel report (Blocco B).
- [x] **Metrica M5 (costo)** (`utils/evaluation_utils.py::_build_cost_metrics_section`): token e tempo medi per ripetizione, per ogni tipo di task (non solo CVSS) — legge `elapsed_seconds`/`tokens` già salvati. Sui run hosted via Ollama Cloud i token risultano `n/a` (il backend non riporta sempre `prompt_eval_count`/`eval_count`); `avg elapsed` è sempre disponibile. Vedi `docs/sgv_protocol/07_metriche_M_S_2026-07-14.md`. Con questa, tutte le metriche della proposta del relatore sono implementate tranne M4 (delta SAST), rimandata per assenza di un tool SAST nel progetto.
- [x] **Rollup pool-ato M1-M3/S1-S3/M5 cross-task** (`results/evaluation/comparison.md`): oltre all'aggregazione per singolo task (n=ripetizioni), le stesse metriche sono ora pool-ate su tutti i task per ruolo, dentro `comparison.md` — riusa 1:1 i tre section builder per-task, `aggregate_severity_metrics` generalizzata da `task_id` singolo a lista per il baseline S3. Vedi `docs/sgv_protocol/07_metriche_M_S_2026-07-14.md`.
- [ ] Distanza vettoriale con interpolazione ufficiale FIRST tra vettori (materiale Mariano) — per ora la distanza in spazio score usa i due score ricalcolati
- [ ] **C1 — Temperature sweep** T∈{0.1, 0.7} su task7/8 expert e4b (prossimo esperimento)
- [ ] Retry con feedback del judge reiniettato
- [ ] Rieseguire task6 blind (senza special attention) — baseline pulita
- [ ] False positive rate tracking / task "controllo negativo"
- [ ] Preparare estratti per validazione esperti 5G (task5, task7, task8)
- [ ] Convertire output JSON in report Markdown strutturato per l'AI
- [ ] Profiling sistematico VRAM/latency per modello

---

## CLI comandi rapidi

```bash
# Run tutti i task security review, 1B (agente unico — --role rimosso post call 11)
# ⚠️ Correzione: --task è action="append", va ripetuto per ogni task (non accetta valori multipli)
python main.py --experiment 1B --task task5_vuln_pcf --task task6_vuln_udr --task task7_vuln_amf --task task8_vuln_udm --task task9_vuln_cross

# Includi anche le varianti full-file
python main.py --experiment 1B --task task6_vuln_udr_full --task task7_vuln_amf_full --task task8_vuln_udm_full

# Test rapido singolo task
python main.py --task task5_vuln_pcf --repetitions 1 --task-timeout 120

# Export grafo LangGraph
python main.py --export-graph docs/graph.png
```

---

## Presentazione (`docs/presentation.html`)

### Come aggiornare la presentazione

Quando viene chiesto di aggiornare o rigenerare la presentazione, seguire questo ordine:

**1. Leggi prima questi file (in ordine):**

1. `docs/status.md` — stato attuale: modelli, task, checklist
2. `docs/architecture.md` — mappa codice e flusso (slide architettura)
3. `docs/supporto/calls/call_1.md` — sfide e decisioni base (slide sfide aperte)
4. `docs/supporto/calls/call_2.md` — risultati security review, decisioni recenti (slide risultati/prossimi passi)
5. `results/evaluation/scores_1A.md` e `scores_1B.md` — se ci sono risultati da mostrare

**2. Mapping slide → sorgente (struttura attuale come riferimento):**

| Slide | Contenuto | Sorgente |
| --- | --- | --- |
| 01 Titolo | nome progetto, tagline | fisso |
| 02 Cos'è | obiettivo, ruoli, setup, consistenza | `architecture.md` §1 |
| 03 Setup 1A vs 1B | controllo vs confronto | `architecture.md` §2 |
| 04 Ruoli | expert / beginner / JSON output | `architecture.md` §2 |
| 05 Task | math vs textual, SVG | `architecture.md` §2 + task list da questo file |
| 06 Mappa codice | file e responsabilità | `architecture.md` §3 |
| 07 Flusso LangGraph | SVG grafo nodi | `architecture.md` §5 |
| 08 Ripetizioni vs retry | parametri esecuzione | `architecture.md` §5 |
| 09 Judge LLM | input/output, SVG | `architecture.md` §6.2 |
| 10 Output | file risultati, report | `architecture.md` §7 |
| 11 Metriche | accuracy / confidence / consistenza | `architecture.md` §6 |
| 12 Sfide aperte | problemi da risolvere | `supporto/calls/call_1.md` §8.1–8.10 (proposte non ancora implementate) |
| 13 Chiusura | tagline | fisso |

Aggiungere slide nuove (es. risultati security, confronto modelli) dopo la slide 11, prima della chiusura.

**3. Stile da preservare:**

- CSS e variabili `:root` invariate (palette `--gold`, `--accent`, `--bg`)
- Font stack: `Playfair Display` (serif, titoli), `IBM Plex Mono` (codice), `Inter` (corpo)
- Struttura HTML: `<section>` con classi `left-align` o centrata, componenti `.card`, `.mem-card`, `.code-block`, `.callout`
- SVG inline per diagrammi (non immagini esterne)
- Navigation JS invariato (frecce, touch, sidebar, progress bar)
- **Non aggiungere dipendenze esterne** oltre ai Google Fonts già presenti

**4. Quando aggiornare:**

- Quando cambiano i task disponibili → aggiorna slide 05
- Quando cambiano i modelli → aggiorna slide 03 e aggiorna le card
- Quando ci sono risultati da mostrare → aggiungi slide dopo la 11
- Quando cambiano le sfide aperte (nuove implementazioni) → aggiorna slide 12
- Non riscrivere slide già corrette — modificare solo quelle impattate

---

## Regola di aggiornamento

Dopo ogni modifica al codice:

- Aggiorna il file `architecture.md` se cambia la mappa codice, il flusso o la valutazione.
- Aggiungi una nuova sezione `§8.N` in `supporto/calls/call_1.md` o crea `docs/supporto/calls/call_<N>.md` per nuove call.
- Aggiorna questo index (tabelle modelli/task e checklist) se cambia la configurazione.
- Usa `> ✅ **Implementato:**` / `> ⚠️ **Correzione:**` inline nel documento di dettaglio corrispondente.
