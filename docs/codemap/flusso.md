# Flusso di esecuzione — vista trasversale

> Punto di partenza consigliato per chi arriva sul progetto. Un diagramma, un racconto minimale del flusso, e approfondimenti solo dove il flusso stesso pone una domanda non ovvia. Per il dettaglio esaustivo di un blocco vai al file tecnico (`codemap/NN_*.md`) o discorsivo (`codemap/narrativa/NN_*.md`) corrispondente, linkato da ogni approfondimento qui sotto. Fonte: gli stessi file tecnici già verificati contro codice + git log — nessun documento sotto `docs/` (eccetto `codemap/` stessa) è stato usato per scrivere questo file.

## Il diagramma

```
                                   ┌────────────────────────┐
                                   │  main.py (CLI)         │
                                   │  per ogni task × rep:  │
                                   └───────────┬────────────┘
                                               ▼
                                   ┌────────────────────────┐
                                   │  load_task             │  file .md task → prompt
                                   │  (task_utils.py:40)     │  + eventuale hint SAST
                                   └───────────┬────────────┘  + istruzioni CVSS
                                               ▼
                      ┌────────────────▶┌────────────────────────┐
                      │                 │  run_agent              │  1 chiamata LLM,
                      │  retry           │  (experiment_utils:222) │  system+user prompt
                      │  (stesso        └───────────┬────────────┘
                      │  contatore,                 ▼
                      │  MAX_RETRIES=3) ┌────────────────────────┐
                      │                 │  check_sgv              │  G1-G4: il report è
                      └─────────────────│  (experiment_utils:262) │  formalmente fondato?
                      │  fallisce       └───────────┬────────────┘  (mai la sostanza)
                      │                              ▼ passa
                      │                 ┌────────────────────────┐
                      └─────────────────│  check_answer           │  math → deterministico
                        fallisce        │  (experiment_utils:293) │  testuale → Judge+rubrica
                                        └───────────┬────────────┘  (rubrica del TASK, non
                                                     ▼ verdict     generica — vedi §3)
                                        ┌────────────────────────────────┐
                                        │  save_result (experiment_utils:359)   │
                                        │  ┌──────────────────────────────────┐│
                                        │  │ 1. SOLO se task CVSS: chiama     ││  Ramo B calcolato
                                        │  │    evaluate_cvss_estimate         ││  QUI, PRIMA di
                                        │  │    (cvss_eval.py:274) → cvss_eval ││  scrivere il JSON —
                                        │  │    indipendente dal verdict       ││  non un passo dopo,
                                        │  │ 2. Merge in un unico rep_payload: ││  non un file a parte
                                        │  │    Ramo A (verdict/judge_score,   ││
                                        │  │    già in state) + Ramo B         ││
                                        │  │    (cvss_eval/cvss_eval_pass1)    ││
                                        │  │ 3. Append/scrivi rep_payload in   ││
                                        │  │    risultato.json (1 file per     ││
                                        │  │    task×esperimento×ruolo×modello,││
                                        │  │    1 entry per ripetizione)       ││
                                        │  └──────────────────────────────────┘│
                                        └────────────────┬───────────────────┘
                                                          │  ← IL JSON è il
                        ═══════════════ fine run, a parte ═══════ tracciamento a valle:
                                                          ▼         stato grezzo persistito,
                                        ┌────────────────────────┐  non ancora un report
                                        │  evaluation_utils.py    │  legge TUTTI i JSON già
                                        │  (reporting, separato)  │  scritti (non uno alla
                                        └───────────┬────────────┘  volta), aggrega Blocco B
                                                     │              (CVSS) + C (SGV) + A
                                                     ▼              (rubrica) in result_*.md
                                        results/evaluation/*.md
```

## Il flusso, in breve

Un run parte da `main.py`, che per ogni combinazione task×esperimento×ripetizione invoca un grafo LangGraph compilato una volta sola (`utils/experiment_utils.py:_build_graph`). Il primo nodo, `load_task`, legge il file `.md` del task e costruisce il prompt iniziale, eventualmente arricchito con un hint SAST grezzo o con le istruzioni per produrre un vettore CVSS, a seconda dei flag di configurazione.

`run_agent` fa la chiamata vera e propria all'LLM: un solo ruolo, un solo prompt (il progetto ha eliminato la distinzione expert/beginner — coi modelli oggi in uso l'effetto di quel dettaglio nel prompt non era più misurabile).

La risposta passa da un gate deterministico, `check_sgv`: quattro controlli via via più costosi (G1→G4, dettaglio in §1) che verificano se il report è formalmente credibile — funzione citata esistente, snippet rintracciabile nel sorgente, vettore CVSS ben formato — senza mai giudicare se la vulnerabilità è reale. Se fallisce, l'agente riprova; il feedback non rivela mai quale funzione sia effettivamente vulnerabile.

Superato SGV, `check_answer` decide se la risposta è corretta: per i task matematici è un confronto numerico deterministico, per i task testuali (security review) è un Judge LLM che valuta contro la rubrica specifica di quel task (non contro la ground truth testuale, e non contro una rubrica generica — dettaglio in §3). Se il verdetto è "wrong", altro retry — stesso contatore di SGV, budget condiviso (`MAX_RETRIES=3`).

A questo punto entra in gioco `save_result`, ed è qui che i due rami si incontrano — **dentro la stessa funzione, prima di scrivere qualunque file**, non in un passaggio successivo. Per i task che espongono un vettore CVSS, `save_result` calcola per prima cosa il Ramo B (`evaluate_cvss_estimate`, confronto deterministico contro il dataset di CVE reali — dettaglio in §2 e §4), indipendentemente da cosa ha deciso il Ramo A. Poi costruisce un unico `rep_payload` che contiene entrambi i rami fianco a fianco — `verdict`/`judge_score` (Ramo A, già calcolato da `check_answer`) e `cvss_eval`/`cvss_eval_pass1` (Ramo B, appena calcolato) — insieme a history, timing e token. Questo payload viene scritto (o appeso, se il file esiste già da ripetizioni precedenti dello stesso task/esperimento/ruolo/modello) in un file JSON.

**Questo JSON è il tracciamento a valle**: non è ancora un report leggibile, è lo stato grezzo persistito di ogni singola ripetizione, con entrambi i rami già uniti. I report finali sono un'altra cosa, prodotta in un momento separato: solo a fine run (o a comando a parte) entra in gioco `utils/evaluation_utils.py`, che legge *tutti* i JSON già scritti — l'intero insieme, non uno alla volta — e li aggrega in report Markdown, con tre blocchi distinti — B (CVSS deterministico), C (SGV), A (giudizio rubrica) — nell'ordine deliberato B→C→A, motivato nel codice stesso da un feedback ricevuto sulla leggibilità del report.

## Approfondimenti (solo dove serve)

### 1. Il gate SGV: perché un controllo "sta inventando?" prima del giudizio

I quattro controlli sono a costo crescente: G1 verifica solo che il report abbia la struttura giusta (se fallisce, blocca subito il resto); G2 verifica che la funzione citata esista davvero nel codice mostrato all'agente (non nella ground truth — l'agente non può essere punito per non conoscere informazioni che non ha); G3 (opzionale) verifica che lo snippet incollato sia davvero rintracciabile nel sorgente, prima per sottostringa poi — se fallisce — con una similarità Jaccard a finestre di 1-3 righe, soglia 0.8; G4 verifica che il vettore CVSS sia sintatticamente valido. Un dettaglio degno di nota: un commit esplicita perché G3 non ha (e non avrà) un fallback LLM per essere più tollerante — reintrodurrebbe esattamente la non-riproducibilità, il rischio di leakage e il costo che SGV esiste per evitare.
→ Dettaglio completo: [codemap/07_sgv_gate.md](07_sgv_gate.md) · [narrativa/07_sgv_gate.md](narrativa/07_sgv_gate.md)

### 2. Come un finding viene associato alla ground truth (e il suo limite noto)

Il matching fra un finding riportato dall'agente e una CVE nel dataset di verità non è semantico: è containment sul nome della funzione (case-insensitive), con semantica *first-match* — se l'agente cita la stessa funzione più volte in una ripetizione, solo la prima occorrenza viene associata alla CVE, le altre restano "unmatched". La scelta è deliberata (evitare un tie-break che "sbirci" la ground truth per scegliere quale duplicato preferire, il che gonfierebbe artificialmente le metriche di severità) ma resta un limite reale: non esiste oggi un controllo semantico esplicito sul contenuto del finding, solo questo controllo sintattico-posizionale sul nome.
→ Dettaglio completo: [codemap/06_cvss_scoring.md](06_cvss_scoring.md) · [narrativa/06_cvss_scoring.md](narrativa/06_cvss_scoring.md)

### 3. La rubrica del giudice: specifica per task, non generica

Nel flusso principale (`main.py` → `experiment_utils.py`), la rubrica che il Judge usa è quella del singolo task, letta dal secondo blocco JSON del file soluzione (`utils/task_utils.py:58`) — è quindi ancorata a quel task specifico, non alla ground truth testuale (che il giudice non vede mai) ma nemmeno una rubrica generica riusabile su qualunque report. Esiste, separatamente, una rubrica generica "GT-free" (`docs/judge_rubric/gtfree/rubric_v1.json`) pensata per valutare un report senza sapere quale sia il task — ma è usata solo da uno script standalone di calibrazione (`scripts/judge_calibration/run_gtfree_rubric.py`), non è integrata nel flusso automatico di `main.py`. Chi si aspetta di trovare la rubrica generica nel percorso principale non la troverà: oggi vive solo nel percorso di calibrazione a parte.
→ Dettaglio completo: [codemap/03_agenti_llm.md](03_agenti_llm.md) · [codemap/08_script_calibrazione.md](08_script_calibrazione.md) · versioni narrative corrispondenti

### 4. Ramo B — il calcolo CVSS deterministico, e perché non tocca mai il verdetto

Una volta che il finding è (eventualmente) associato a una CVE, tutta la matematica — score ricalcolato con la libreria ufficiale CVSS 4.0, distanze per-campo, aggregazioni M1-M3/S1-S3 — è codice Python puro, senza LLM. È esplicitamente commentato nel codice come "never affects verdict": è un secondo canale di misurazione scientifica, parallelo al giudizio pass/fail che decide i retry, non un suo sostituto né un suo correttivo.
→ Dettaglio completo: [codemap/05_valutazione_metriche.md](05_valutazione_metriche.md) · [codemap/06_cvss_scoring.md](06_cvss_scoring.md)

### 5. Il retry: cosa vede l'agente quando sbaglia, e l'asimmetria del feedback

Quando il retry scatta per un fallimento SGV, il prompt successivo include un blocco esplicito con i problemi formali riscontrati (mai quale funzione sia vulnerabile). Quando invece scatta per un verdetto "wrong" del Judge o per una risposta matematica sbagliata, il prompt di retry contiene solo la risposta precedente — nessuna spiegazione di cosa fosse sbagliato nel merito. È un'asimmetria reale nel codice attuale, non un bug documentato altrove: se in futuro si volesse dare all'agente un segnale anche sul fallimento di rubrica, andrebbe aggiunto qui.
→ Dettaglio completo: [codemap/02_langgraph_state_machine.md](02_langgraph_state_machine.md) · [narrativa/02_langgraph_state_machine.md](narrativa/02_langgraph_state_machine.md)
