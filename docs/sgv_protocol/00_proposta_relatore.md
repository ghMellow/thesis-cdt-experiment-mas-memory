# 00 — Proposta del relatore: Syntactic Grounding Verifier (SGV)

> Documento condiviso dal relatore il 2026-07-13 (messaggi + allegato), riportato verbatim per riferimento. Non estesa ai colleghi cyber — riguarda il funzionamento interno del motore di identificazione delle vulnerabilità.

## Messaggio di accompagnamento

Vi allego una cosa su cui stavo ragionando tra ieri ed oggi e di cui discutere tra di noi appena c'è un attimo. Non l'ho estesa ai colleghi cyber perché è più parte di come funziona sotto il motore il sistema di identificazione delle vulnerabilità. Il problema che mi sono posto è come gestire la rubrica senza che l'agente ed il coordinatore abbiano accesso ad informazioni dalla ground truth. Lasciare completamente ad un LLM il giudizio di accettazione o rifiuto espone a potenziali critiche relative alla data di training del modello e ad un potenziale rischio di contaminazione del giudizio. Ho trovato una via di un filtro deterministico gestito da un agente che valuta la qualità della risposta invece del contenuto ed in base a quello attiva il retry.

Chiaramente spunto da discutere prima di passare all'implementazione.

## 1. Aggiornamento del protocollo di retry

Aggiornamento del protocollo di retry del LLM per togliere dipendenza esclusiva da AI generativa ed integrare controllo deterministico.

Si propone la sostituzione parziale del meccanismo a rubrica per guidare il retry del sistema ad agenti con un meccanismo deterministico. Questa mossa permetterebbe di svincolare il framework da alcune possibili debolezze ed essere scientificamente più solido perché permette di gestire possibili scenari di contaminazione e circolarità del giudice o della famiglia di modelli.

Delegare esclusivamente ed interamente a un LLM la decisione di accettare o rigettare un tentativo introduce quattro debolezze potenziali che il filtro deterministico è progettato per evitare.

1. **Non-riproducibilità**: un giudice basato su modello, operando a temperatura non nulla e sensibile a perturbazioni superficiali dell'input, può emettere verdetti diversi sullo stesso report a esecuzioni diverse, cosicché il criterio che governa i retry, e quindi l'insieme dei finding che sopravvivono al loop, non è replicabile da terzi.
2. **Tendenza all'eccessiva accettazione**: è documentato che i critici LLM tendono ad approvare i finding proposti dagli agenti, gonfiando potenzialmente il tasso di accettazione e, con esso, i falsi positivi che raggiungono la misurazione.
3. **Leakage semantico** (il più insidioso per la validità dell'esperimento): un giudice che valuta la correttezza di un finding deve possedere una nozione, sia pure implicita, di che cosa costituisca una vulnerabilità, e nel comunicare all'agente il motivo del rigetto rischia di trasmettere informazione sulla soluzione, contaminando la generazione con la ground truth che l'esperimento intende tenere separata; la performance misurata rifletterebbe allora l'interazione agente–giudice, non la capacità dell'agente.
4. **Opacità e costo**: ogni verdetto richiede una chiamata al modello, con latenza e spesa non trascurabili, e senza una motivazione ispezionabile del rigetto.

### Il Syntactic Grounding Verifier (SGV)

Filtro sintattico deterministico che risolve le quattro debolezze per costruzione e generalizza il sistema (utile anche per il CDT, anche a casi che non conosce) controllando la sola fondatezza formale del report e non la correttezza sostanziale del giudizio di vulnerabilità, che è demandata alla misurazione a valle.

Il protocollo organizza il vulnerability assessment in tre fasi funzionali, con accesso disgiunto all'informazione:

1. **Generazione ed esplorazione.** Un agente LLM analizza il codice sorgente e produce ipotesi di vulnerabilità in un report strutturato.
2. **Selezione e correzione (in-loop).** Un verificatore deterministico, privo di accesso alla ground truth, controlla la correttezza formale e sintattica del report. In caso di non conformità fornisce un feedback puramente formale (non veicola informazione su quali funzioni siano vulnerabili) ma può indurre l'agente a riesaminare il codice. Al riesame l'agente può formulare finding aggiuntivi — si osserva un ampliamento del perimetro delle funzioni candidate, effetto riportato e misurato (non assunto come garantito).
3. **Misurazione (downstream).** Un Judge con accesso alla ground truth (patch ufficiale + vettore CVSS di riferimento) confronta i report accettati con la soluzione nota e calcola le metriche di detection e severity. Opera esclusivamente a valle e non influenza mai la generazione.

**Principio guida.** La separazione tra selezione (report formalmente accettabile?) e misurazione (confronto con verità nota) è garantita per costruzione: la selezione è affidata a un criterio esattamente decidibile (SGV) che non accede alla ground truth; la misurazione è demandata a un componente che non interagisce con il sistema in esecuzione. Il feedback in-loop non trasporta informazione sulla soluzione, indipendentemente dal fatto che il retry produca o meno finding aggiuntivi.

## 2. Definizione di Ground Truth e relazione di match

Per ogni vulnerabilità del caso di studio, la ground truth di detection è ancorata al testo della vulnerabilità e alla patch di sicurezza ufficiale (da verificare con Mariano) referenziata dalla CVE. Sia F l'insieme delle funzioni definite nell'estratto di codice sottoposto all'agente, e V (V ⊆ F) l'insieme delle funzioni modificate dalla patch come oggetto della correzione di sicurezza.

Un finding che dichiara una funzione f è **matched** se e solo se f ∈ V, previo confronto esatto e case-insensitive sul nome qualificato della funzione (incluso il tipo del ricevitore, ove presente).

Non viene impiegato alcun giudizio semantico (embedding o LLM-as-a-judge) per i finding non matched: ogni verdetto di match è riproducibile da chiunque sia in possesso della patch. Questi verranno sottoposti a valutazione umana e permettono di identificare anche nuove CVE.

## 3. Componenti del sistema

| Componente | Tipo | GT | Ruolo | Funzione specifica |
|---|---|---|---|---|
| Agente | LLM generativo | No | Generatore di ipotesi | Analizza il codice e produce un report strutturato con, per ogni ipotesi: nome della funzione, snippet di supporto e vettore CVSS v4.0 stimato. |
| SGV | Algoritmico (substring, Jaccard) | No | Filtro sintattico in-loop | Applica i controlli G1–G4 (validità formale, esistenza dei simboli, groundedness degli snippet, completezza e validità del vettore CVSS). Feedback puramente formali. |
| Coordinator | Logica procedurale | No | Gestore del loop | Amministra i tentativi (max k=3), recapita i feedback dell'SGV, blocca i finding accettati e scarta quelli ancora non conformi al termine. |
| Judge | Algoritmico (stringhe + FIRST) | Sì | Misuratore (downstream) | Opera a valle del loop. Confronta i report accettati con la GT e calcola le metriche M e S. Non fornisce mai feedback durante l'esecuzione. |

### 3.1 I controlli sintattici dell'SGV (G1–G4)

Tutti relativi alla sola forma e alla fondatezza sintattica rispetto al codice sorgente. Nessun controllo esprime giudizi sul contenuto del finding (tipo di vulnerabilità, correttezza della detection, plausibilità della severità).

| Cod. | Controllo | Definizione | Esito |
|---|---|---|---|
| G1 | Validità formale | Il report JSON/.md è conforme allo schema atteso (campi obbligatori, tipi). Precondizione dei controlli successivi. | Retry |
| G2 | Esistenza dei simboli | Ogni funzione o variabile citata è presente nell'estratto, previo confronto esatto e case-insensitive sul nome qualificato. | Retry |
| G3 | Groundedness dello snippet | Ogni snippet di codice citato è effettivamente presente nell'estratto. | Retry |
| G4 | Completezza dei campi | Presenza dei campi obbligatori (function_name, snippet, cvss_vector) e validità sintattica del vettore CVSS v4.0. | Retry |

## 4. Il loop di autocorrezione

Opera a livello di singolo finding:

1. L'agente produce un report completo.
2. L'SGV esegue i controlli G1–G4.
3. Se un controllo fallisce, il Coordinator inoltra all'agente un feedback strettamente formale (es. «la funzione X non è presente nel file; i simboli disponibili sono …»). Riguarda esclusivamente la corrispondenza sintattica, non contiene informazione sulla natura vulnerabile o meno del codice.
4. L'agente ritenta. Nel riesaminare il codice per correggere gli errori formali può rivedere i finding esistenti e formularne di nuovi; il retry non è vincolato alla sola correzione della forma. Resta invariante l'assenza di informazione sulla soluzione nel canale di feedback: l'SGV segnala che cosa non è formalmente valido, mai se una funzione sia vulnerabile.
5. I finding che superano i controlli vengono accettati e bloccati; quelli ancora non conformi al termine dei tentativi (k=3) vengono scartati.

**Osservazione.** Nel ricevere un errore su un simbolo inesistente, l'agente è portato a consultare nuovamente il codice per individuare il nome corretto, e in questo riesame può individuare funzioni vicine, correlate o inizialmente trascurate. Ci si attende quindi che il perimetro delle funzioni candidate si ampli lungo i tentativi. Se questo si traduca in un aumento delle vulnerabilità effettivamente recuperate è una questione empirica, misurata dalle metriche di detection al primo tentativo e dopo i retry (§5.1); il protocollo non assume tale effetto né ne rivendica la causalità, ma lo espone alla misura. Poiché l'agente opera a temperatura non nulla, l'ampliamento osservato è compatibile sia con l'effetto del riesame indotto dal feedback sia con la semplice variabilità del campionamento su più tentativi; il protocollo riporta il fenomeno senza attribuirlo all'una o all'altra causa.

## 5. Metriche di valutazione

Calcolate dal Judge sui report accettati. L'unità di analisi varia con la metrica: detection a livello di funzione di V; carico di revisione a livello di finding; costo a livello di NF. Le metriche di severity (S) si applicano solo alle configurazioni LLM (lo strumento SAST non produce vettori CVSS).

### 5.1 Metriche di Detection (M)

| Cod. | Metrica | Definizione | RQ |
|---|---|---|---|
| M1 | Detection per CVE | Rilevata se almeno una funzione di V risulta matched; si riporta esito rilevata/mancata e copertura \|matched\|/\|V\|. | RQ1 |
| M2 | Precision, Recall, F1 | Su TP/FP/FN (FN = funzione di V senza finding accettato matched). Riportate a pass@1 e pass@k: la differenza documenta l'effetto dei tentativi sul recall. Precision e Recall vanno letti insieme, poiché i finding aggiunti nei retry possono includere errori. | RQ1, RQ2 |
| M3 | Alert per TP | Finding da revisionare per ogni vera vulnerabilità identificata; proxy del carico del revisore. | RQ2 |
| M4 | Delta SAST | Vulnerabilità vere trovate dall'agente e non dal SAST; precisione dell'agente nel confermare/scartare gli alert del SAST. | RQ2 |
| M5 | Costo computazionale | Token e tempo per NF, confrontati tra le configurazioni LLM. | RQ2 |

### 5.2 Metriche di Severity (S), calcolate solo sui TP

| Cod. | Metrica | Definizione | RQ |
|---|---|---|---|
| S1 | Match esatto del vettore | % di vettori CVSS v4.0 completamente corrispondenti a quelli di riferimento. | RQ3 |
| S2 | Accuratezza per metrica base e distanza ordinale | Per ciascuna metrica base (AV, AC, AT, PR, UI, VC/VI/VA, SC/SI/SA), accuratezza categorica e distanza ordinale (es. None→High penalizzato più di None→Low). | RQ3 |
| S3 | Baseline del vettore modale | Modello nullo che assegna il vettore modale della GT; le metriche S sono lette come margine rispetto a questa baseline. | RQ3 |

## 6. Related work (sintesi)

- **GT derivata da patch**: Devign, BigVul, DiverseVul; PrimeVul (Ding et al.) mostra accuratezza 24–60% per etichette derivate da commit senza verifica manuale → valutazioni sovrastimate. VulnLLMEval e JitVul derivano GT da hash di commit.
- **Valutazione detection/spiegazioni/severità**: SecLLMHolmes mostra che il label binario è insufficiente (ragionamento LLM non deterministico, sensibile a perturbazioni superficiali). VADER usa rubrica standard applicata da umani; framework human-in-the-loop generano rubriche per istanza validate contro consenso umano. Il presente protocollo relega il giudizio semantico fuori dal ciclo, misurazione primaria = confronto deterministico con la patch. EvalSVA valuta CVSS ma con accesso a pre/post-fix; qui solo estratto di codice.
- **Sistemi agentici con critico in-loop**: GPTLens (generate-then-discriminate, critico LLM in-loop); VulTrial documenta la clemenza del critico di GPTLens; iAudit (Ranker–Critic su modelli fine-tuned); MAVUL (architetto senza GT + valutatore con GT escluso dalla decisione). In tutti questi il componente in-loop è un LLM, con i limiti documentati (clemenza, instabilità, leakage). Qui il componente in-loop è un verificatore eseguibile, non un LLM.

**Posizionamento del contributo**: (i) separa per costruzione selezione e misura, garantendo assenza di leakage e riproducibilità dei verdetti; (ii) ancora la GT alla patch ufficiale, con match deterministico; (iii) misura la detection al primo tentativo e dopo i retry, distinguendo il contributo del primo passaggio da quello del ciclo di autocorrezione.

**Nota terminologica**: "Syntactic Grounding Verifier" è una denominazione introdotta in questo lavoro, non un termine standard, ma il principio (groundedness/faithfulness — verificare che ogni affermazione sia supportata dall'evidenza fornita) è consolidato nella letteratura sulla rilevazione delle allucinazioni, che distingue tra verificatori LLM-as-a-judge e controlli deterministici.

### Bibliografia

1. Y. Zhou et al., "Devign", NeurIPS 2019.
2. J. Fan et al., "A C/C++ code vulnerability dataset with code changes and CVE summaries", MSR 2020.
3. Y. Chen et al., "DiverseVul", RAID 2023.
4. Y. Ding et al., "Vulnerability detection with code language models: How far are we?" (PrimeVul), ICSE 2025, arXiv:2403.18624.
5. A. Zibaeirad, M. Vieira, "VulnLLMEval", arXiv:2409.10756, 2024.
6. A. Yildiz et al., "JitVul", ACL 2025.
7. S. Ullah et al., "LLMs cannot reliably identify and reason about security vulnerabilities (yet?)", IEEE S&P 2024.
8. E. TS. Liu et al., "VADER", arXiv:2505.19395, 2025.
9. S. Shi et al., "Towards a human-in-the-loop framework for reliable patch evaluation using an LLM-as-a-judge", arXiv:2511.10865, 2025.
10. X. Wen et al., "EvalSVA", arXiv:2501.14737, 2025.
11. S. Hu et al., "GPTLens", IEEE TPS-ISA 2023, arXiv:2310.01152.
12. R. Widyasari et al., "VulTrial", arXiv:2505.10961, 2025.
13. W. Ma et al., "iAudit", ICSE 2025, arXiv:2403.16073.
14. Y. Li et al., "MAVUL", arXiv:2510.00317, 2025.
