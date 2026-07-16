# 01 — Stato attuale: il giudice LLM a rubrica

> Documento di discussione (2026-07-16). Fotografa **come funziona oggi** la valutazione a giudice+rubrica nel progetto, la teoria su cui poggia, le debolezze osservate usandola e i limiti strutturali — in particolare la dipendenza della rubrica dalla ground truth, da cui vogliamo svincolarci. Cartella gemella di `docs/sgv_protocol/` (che copre il *prima*, l'in-loop deterministico); qui si discute il *giudizio* vero e proprio.

## 1. Come funziona oggi

### 1.1 Il flusso

Per i task testuali (inclusi i security review task5–9):

1. L'agente produce la risposta strutturata (Answer / Reasoning / Confidence).
2. *(solo task CVSS, se `SGV_ENABLED`)* il nodo `check_sgv` applica i controlli formali G1–G4 — vedi `docs/sgv_protocol/`.
3. Il nodo `check_answer` invoca il **giudice LLM** (`agents/judge_agent.py::run_judge_textual`): riceve scenario (senza le Agent Instructions), rubrica per-task e risposta dell'agente, con system prompt generato da `utils/experiment_utils.py::build_judge_prompt`.
4. Il giudice assegna un punteggio 0–max per ogni criterio della rubrica; il totale viene normalizzato e confrontato con la soglia `config.TEXTUAL_PASS_RATIO = 0.7` → verdict `correct`/`wrong`.
5. Il verdict guida il retry (max `MAX_RETRIES = 3`, retry *neutro*: la risposta precedente viene rimostrata senza il feedback del giudice).

### 1.2 La rubrica

La rubrica vive nel file `_sol.md` del task (secondo blocco JSON, caricato da `utils/task_utils.py::_load_task`): per ogni dimensione (es. `missing_default_score`, `inconsistent_context_set_score`, `impact_assessment_score` in task7) definisce un massimo e descrittori testuali per ogni livello di punteggio. Il giudice **non riceve la `ground_truth` testuale** (regola di progetto: la rubrica è la definizione operativa di "corretto"), e dalla run 4 lo score CVSS è valutato da un ramo deterministico separato (`utils/cvss_eval.py`), non dal giudice.

### 1.3 Accorgimenti di robustezza già presenti

- Output del giudice vincolato a template Markdown (`## Scores` / `## Feedback`), con fallback di parsing JSON.
- `total_score` ricalcolato dalla somma dei sub-score se mancante, e clampato in `[0, total_max]`.
- Il giudizio è per-criterio (criteria decomposition ante litteram), non un voto olistico unico.
- Token e tempo del giudice tracciati per ripetizione (base della metrica M5).

## 2. La teoria: LLM-as-a-judge con rubrica

Il paradigma è quello introdotto sistematicamente da **MT-Bench / Chatbot Arena** (Zheng et al., 2023, arXiv:2306.05685): usare un LLM come valutatore scalabile al posto dell'umano, in tre varianti — pairwise comparison, single-answer grading (la nostra), reference-guided grading. La variante a **rubrica** aggiunge criteri espliciti e descrittori per livello, sul modello della valutazione educativa: rende il giudizio più ancorato e ispezionabile rispetto al voto olistico. Filoni rilevanti:

- **G-Eval** (Liu et al., 2023, arXiv:2303.16634): valutazione con chain-of-thought e form-filling; introduce l'idea di usare le *probabilità* dei token di punteggio per ottenere score continui — antenato diretto del paper LLM-as-a-Verifier (doc 02).
- **Prometheus** (Kim et al., 2024, arXiv:2310.08491): giudice open-source addestrato specificamente a seguire rubriche fini per-istanza; dimostra che la capacità di *seguire una rubrica* non è gratis nei modelli piccoli.
- **RUBRICEVAL** (già in `docs/supporto/reference/paper_RUBRICEVAL.md`): meta-valutazione a livello di singola voce di rubrica; anche GPT-4o si ferma al ~56% sul subset HARD → il giudizio a rubrica "non è un problema risolto", e gli errori per-criterio si propagano nell'aggregazione. Conferma però che rubric-level > checklist-level e che il reasoning esplicito aiuta.
- **Bias documentati del giudice LLM**: position bias e verbosity bias (Zheng et al.), self-enhancement bias (il modello preferisce output della propria famiglia — rilevante per il setup 1A dove agente e giudice sono lo stesso modello), leniency/eccessiva accettazione (documentata in ambito vulnerability da **VulTrial**, arXiv:2505.10961, sul critico di GPTLens — già citata nella proposta SGV), non-determinismo e sensibilità a perturbazioni superficiali (**SecLLMHolmes**, IEEE S&P 2024).

La proposta del relatore (`sgv_protocol/00_proposta_relatore.md` §1) riassume le quattro debolezze del giudice LLM in-loop: non-riproducibilità, eccessiva accettazione, leakage semantico, opacità/costo. L'SGV le risolve *per l'in-loop*; questo documento discute quanto restano vere per il giudizio di accettazione a valle.

## 3. Debolezze osservate in questo progetto

Empiriche, dal registro `docs/findings.md` e dalle run 1–6:

1. **Non-riproducibilità del verdetto.** Il giudice gira a `TEMPERATURE = 0.3`: lo stesso report può passare o fallire la soglia in run diverse. Con soglia secca a 0.7 il problema è massimo proprio dove il giudizio conta (punteggi borderline 0.6–0.8).
2. **Un solo campione di giudizio per attempt.** Nessuna ripetizione né aggregazione del giudizio: la varianza del giudice entra direttamente nel verdict e quindi nel loop di retry.
3. **Soglia arbitraria.** `0.7` non è calibrata su nulla: non sappiamo quale ratio massimizzi l'accordo con il match deterministico M1–M3 (che oggi, avendo il ramo CVSS, potremmo usare come riferimento per calibrarla).
4. **Giudice = agente (setup 1A).** Stesso modello per generare e giudicare → self-enhancement bias non controllato; il confronto 1B (modelli diversi) è disattivato.
5. **Granularità grossolana.** Sub-score interi su scale 0–2/0–4, totale 0–9: molti report distinti collassano sullo stesso punteggio (esattamente il problema di tie/coarseness quantificato nel doc 02).
6. **Capacità del modello giudice.** I gemma usati come giudice sono piccoli rispetto a quelli meta-valutati in RUBRICEVAL (dove pure GPT-4o fatica a livello di rubrica): il giudizio per-criterio su codice Go di un core 5G è probabilmente vicino al limite di capacità del giudice, non solo dell'agente.
7. **Fragilità nel contesto pieno.** Le run 5–6 (F21–F24, F25–F28) mostrano il crollo della rubric accuracy su task6/7 `_full`: la rubrica scritta sull'estratto non "scala" al file intero — i descrittori presuppongono che i bug siano l'oggetto saliente del testo.
8. **Retry poco informato per costruzione.** Il feedback del giudice non viene reiniettato (scelta deliberata anti-leakage): coerente col protocollo, ma significa che il costo del giudizio in-loop compra solo un bit (retry sì/no).

## 4. Limiti strutturali: la dipendenza dalla ground truth

Il limite di fondo, ed è il motivo di questa cartella: **la rubrica è scritta a partire dalla ground truth**. I descrittori di task7 nominano `HTTPUEContextTransfer`, il default mancante nello switch, l'inconsistenza su `c.Set` — cioè la soluzione, riformulata come criteri di punteggio. Conseguenze:

- **Formalmente il giudice non vede la GT, sostanzialmente sì.** La separazione "il giudice non riceve la ground_truth" vale per il campo `answer`, ma la rubrica è una proiezione quasi-verbatim della GT. Il giudizio misura l'aderenza alla soluzione nota, non la qualità del lavoro di analisi.
- **Non generalizza a codice senza CVE nota.** Per usare il sistema come strumento (obiettivo CDT: valutare codice *nuovo*), non possiamo scrivere una rubrica per-task che richiede di conoscere già le vulnerabilità. È lo stesso argomento con cui la proposta SGV motiva il filtro deterministico ("utile anche per il CDT, anche a casi che non conosce"), applicato al giudizio invece che alla selezione.
- **Circolarità potenziale nella misura.** Se la rubrica codifica la GT e il verdict della rubrica guida il retry, il loop è indirettamente guidato dalla GT — attenuato dal retry neutro, ma non eliminato: il *quando fermarsi* dipende comunque da un criterio GT-derivato.

**Rapporto con la discussione SGV.** La cartella `sgv_protocol/` ha già affrontato il problema per la fase *in-loop* (selezione): lì la risposta è stata rimuovere l'LLM e usare controlli sintattici GT-free. Per la fase di *giudizio/misura* la risposta attuale del protocollo è il Judge deterministico (match sui nomi di funzione + metriche M/S), che però esiste **solo dove esiste una patch di riferimento**. Resta scoperto il caso che ci interessa per svincolarci: giudicare la qualità di un report su codice di cui non abbiamo la soluzione. Il giudice a rubrica potrebbe beneficiare delle implementazioni fatte per l'SGV (groundedness, esistenza dei simboli, vettore CVSS ben formato sono *già* verificati a monte: la rubrica non deve più spenderci criteri), ma **è da valutare** — vedi doc 03 e 04 per le direzioni.

## 5. Sintesi

| Proprietà | Oggi | Problema |
|---|---|---|
| Criteri | Rubrica per-task, GT-derivata | Non generalizza, circolarità soft |
| Score | Interi per-criterio, somma, soglia 0.7 | Granularità grossolana, soglia non calibrata |
| Campionamento | 1 giudizio per attempt, T=0.3 | Verdetti non riproducibili |
| Giudice | Stesso modello dell'agente (1A) | Self-enhancement bias |
| Uso del verdict | Gate retry + accuracy nel report | Un bit per chiamata, costo alto |

I candidati per uscirne sono discussi nei doc successivi: **02** (paper LLM-as-a-Verifier, riportato verbatim), **03** (discussione del paper e applicabilità qui), **04** (alternative: rubrica process-based "da esperto di sicurezza", rubrica ancorata a CWE, calibrazione della soglia, e altre).
