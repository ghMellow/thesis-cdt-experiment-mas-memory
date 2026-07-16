# 04 — Alternative e proposte per un giudice svincolato dalla ground truth

> Documento di discussione (2026-07-16). Raccoglie le alternative sul tavolo per la rubrica/giudizio: l'idea "workflow dell'esperto di sicurezza" (proposta dell'utente), la rubrica ancorata a CWE (già emersa in call 12), i criteri GT-free ispirati al paper del doc 02, e altre direzioni esplorate da Claude. Nulla è deciso — serve discussione di gruppo.

## 1. Il criterio per confrontarle

Una proposta di rubrica è buona per noi se:

- **(R1) GT-free**: scrivibile senza conoscere le vulnerabilità del codice in esame → usabile su codice nuovo (obiettivo CDT).
- **(R2) Riproducibile**: verdetti stabili tra run (o con varianza misurata e dichiarata).
- **(R3) Non-leaky**: né i criteri né l'eventuale feedback trasmettono informazione sulla soluzione.
- **(R4) Validabile**: sui task con CVE nota possiamo misurare quanto il verdetto concorda con il match deterministico M1–M3 — la GT esce dal giudizio ma resta come *metro del giudice*.

(R4) è il punto metodologicamente forte della nostra posizione: avendo già il ramo deterministico, qualunque giudice GT-free è calibrabile e difendibile empiricamente, non solo argomentativamente.

> **Caveat documentato in letteratura (aggiunto 2026-07-16):** togliere il riferimento ha un costo noto — i giudici LLM diventano sistematicamente *più generosi* quando non hanno una reference answer, con verdetti ribaltati fino all'85% quando la reference viene aggiunta, e un giudice **Gemma3-27B** (la nostra famiglia) che nel dominio a lui ostico accetta il 66% delle risposte sbagliate ("LLM Judges Can Be Too Generous When There Is No Reference Answer", arXiv:2607.12885 — paper integrale nel doc 06, discussione nel doc 07). Per noi è l'argomento in più a favore di (R4): la generosità del giudice GT-free non va assunta bassa, va **misurata** contro M1–M3 — il doc 07 §3 traspone il protocollo di calibrazione C1/C2 del paper come test di ammissione del giudice. Ed è anche un motivo per tenere il pezzo deterministico (coverage, doc 05 §3) fuori dal giudizio LLM.

## 2. Opzione A — Rubrica "workflow dell'esperto di sicurezza" (idea nata in call 12)

> Origine testuale in `00_call12_2026-07-14.md` §2: «io mi provo a immaginare di essere un esperto di sicurezza che deve trovare delle CVE — quali sono i criteri con cui io, facendo l'analisi, vado a selezionare parti di codice? […] simulare il metodo di lavoro». **La combinazione di questa opzione con la C (CWE) è sviluppata nel doc 05**, dove il giudizio dato qui viene parzialmente rivisto: insieme sono più forti che separate.

Impostare la rubrica su come lavora un esperto quando analizza codice per trovare vulnerabilità: copertura delle superfici di input, tracciamento del flusso dati, controllo dei percorsi d'errore, ecc. Il giudice valuterebbe se il *processo* dell'agente assomiglia a quello di un esperto.

**A favore.** È GT-free per costruzione (R1) e valuta il reasoning, non solo l'answer — coerente col fatto che salviamo il Reasoning strutturato. È l'analogo qualitativo dei process reward models (Lightman et al., "Let's Verify Step by Step").

**Contro (e il dubbio dell'utente è fondato).**

- *Process ≠ outcome*: un report può seguire perfettamente la checklist dell'esperto e mancare la vulnerabilità, o trovarla per via non ortodossa. Se il verdict "correct" della rubrica diverge sistematicamente dalla detection reale, la metrica rubric accuracy perde significato.
- Giudicare un processo è *più* difficile che giudicare un esito: per valutare se "il flusso dati è stato tracciato correttamente" il giudice deve saper tracciare il flusso dati — stiamo chiedendo al giudice di rifare l'analisi, con un modello della stessa taglia dell'agente.
- Rischio di premiare la forma: gli LLM producono facilmente *l'apparenza* di un workflow esperto (sezioni, terminologia) senza la sostanza; una rubrica di processo è vulnerabile a questo gaming involontario.

**Verdetto suggerito**: non come asse portante del giudizio, ma **riciclabile come uno dei criteri** di una decomposizione (es. criterio "Systematicity": l'analisi copre le superfici rilevanti?), pesato poco e validato via (R4). Concordo con l'intuizione dell'utente che il paper sia una strada migliore come impianto.

## 3. Opzione B — Criteri GT-free "di qualità del report" (derivata dal paper, raccomandata)

Trasporre la decomposizione Specification/Output/Errors del paper al nostro dominio. Bozza di criteri, tutti valutabili senza conoscere la soluzione:

| Criterio | Domanda posta al giudice | Note |
|---|---|---|
| **Specification** | Il report risponde a ciò che il task chiede (review di sicurezza del file dato, con finding strutturati)? | erede del criterio d'aderenza |
| **Evidence quality** | Ogni finding lega chiaramente sintomo → meccanismo → impatto, con riferimento puntuale al codice? | la *esistenza* di snippet/simboli è già garantita da SGV G2/G3; qui si valuta la qualità del legame |
| **Internal consistency** | Severità CVSS dichiarata coerente con l'impatto descritto a parole? Finding non contraddittori tra loro? | validità sintattica del vettore già coperta da SGV G4 |
| **Systematicity** *(opzionale, dall'opzione A)* | L'analisi mostra copertura delle superfici del file (handler, percorsi d'errore) o si ferma al primo pattern? | da pesare poco, rischio form-over-substance |

Estrazione dello score con il metodo del doc 03 (scala 1–20, K ripetizioni, expectation se i logprob sono disponibili). **Questa è la combinazione che raccomando di portare in discussione**: massimizza il riuso (rubrica per-criterio già nel codice, SGV che assorbe i controlli formali) e soddisfa R1–R4.

Costo di transizione: le rubriche per-task nei `_sol.md` verrebbero sostituite da *una* rubrica per-dominio (task-independent) — semplifica anche la manutenzione e risolve il problema del doc 01 §3.7 (rubrica che non scala al file `_full`, perché non nomina più bug specifici).

## 4. Opzione C — Rubrica ancorata a CWE (nata in call 12)

> In call 12 il relatore l'ha formulata così: «quello potrebbe essere un modo per stilare una rubrica che non è legata a nessuna ground truth» (vedi `00_call12_2026-07-14.md` §3, con la distinzione CVE/CWE e il limite ammesso: non si scoprono weakness nuove). La declinazione 5G e il livello giusto della tassonomia sono discussi nel doc 05 §3–4.

Criteri per *classe di debolezza* (es. CWE-248 uncaught exception, CWE-754 improper check) invece che per vulnerabilità puntuale: il giudice valuta se il finding identifica correttamente una classe CWE plausibile per il codice citato.

**A favore**: livello di astrazione intermedio — meno leaky della rubrica GT-derivata (una CWE non dice *quale* funzione), più ancorato dell'opzione B; si aggancia alla proposta G5/SAST del team (i SAST parlano CWE) e alla metrica M4. **Contro**: scegliere *quali* CWE mettere in rubrica per un task è già informazione derivata dalla GT (leakage attenuato, non nullo — a meno di usare l'intera tassonomia, che diluisce il giudizio); e la corretta classificazione CWE è essa stessa un giudizio semantico difficile. **Posizione**: complementare, non alternativa — la classificazione CWE è più utile come *campo del report* misurato a valle (accuratezza CWE sui TP, analogo di S1–S2) che come criterio in-loop.

## 5. Altre direzioni esplorate (più leggere)

- **Calibrazione della soglia (da fare comunque, qualunque rubrica).** Sui dati già in `results/`: curva accordo(verdict rubrica, M1) al variare di `TEXTUAL_PASS_RATIO` → si sceglie la soglia che massimizza l'accordo e si dichiara. Costo quasi zero, toglie l'arbitrarietà dello 0.7. Primo esperimento che farei in assoluto.
- **Giudice ≠ agente.** Riattivare per il giudizio un modello di famiglia diversa (il meccanismo 1B esiste già in `config.py`) per neutralizzare il self-enhancement bias. A parità di tutto è la mitigazione più economica del doc 01 §3.4.
- **Panel di giudici / majority voting.** Variante "larga" del K del paper: K modelli diversi invece di K campioni dello stesso. Più robusto ai bias di famiglia, ma moltiplica i requisiti di modelli disponibili — da tenere per dopo.
- **Judge come verificatore di consistenza cross-repetition.** Abbiamo già REPETITIONS=3 e il semantic consistency check: un segnale GT-free quasi gratuito è *l'auto-accordo* — finding che compaiono stabilmente su più ripetizioni sono più credibili (self-consistency, Wang et al. 2022). Potrebbe diventare un criterio o un filtro pre-giudizio senza alcuna chiamata aggiuntiva.
- **Progress signal del verifier (paper §6).** Usare lo score continuo per-attempt come misura di avanzamento del loop di retry (il retry sta migliorando il report o no?): darebbe contenuto empirico alla "Osservazione" della proposta SGV §4 sull'ampliamento del perimetro, con un numero invece di un'impressione. Interessante per la tesi, non prioritario per il sistema.

## 6. Quadro riassuntivo

| Opzione | R1 GT-free | R2 riproducibile | R3 non-leaky | Sforzo | Posizione suggerita |
|---|---|---|---|---|---|
| A — workflow esperto | ✅ | ⚠️ (giudizio difficile) | ✅ | medio | un criterio dentro B, non l'impianto |
| B — criteri qualità report + estrazione probabilistica | ✅ | ✅ (con K, misurata) | ✅ | medio | **raccomandata** |
| C — ancoraggio CWE | ⚠️ | ⚠️ | ⚠️ | medio-alto | complementare, come metrica a valle |
| Calibrazione soglia | n/a | ✅ | ✅ | **basso** | fare comunque, per prima |
| Giudice ≠ agente | n/a | ✅ | ✅ | **basso** | fare comunque |

**Sequenza proposta da discutere col gruppo**: (1) calibrazione soglia + giudice di famiglia diversa sui dati esistenti (zero run nuove); (2) pilota doc 03 §5 (K, scala 1–20, rivalutazione offline dei report salvati); (3) se il pilota regge, sostituire le rubriche per-task GT-derivate con la rubrica per-dominio dell'opzione B, tenendo M1–M3/S1–S3 come metro di validazione (R4). Ogni passo è un confronto misurabile, presentabile come contributo metodologico della tesi.

> **Aggiornamento (doc 05):** per il passo (3) esiste ora una forma concreta — la matrice workflow esperto × classi CWE di alto livello, con il criterio di coverage calcolato deterministicamente in stile SGV — e un test di accettazione preciso, la controprova su file mai visto proposta dal relatore in call 12. Vedi `05_rubrica_esperto_cwe_5g.md`.
