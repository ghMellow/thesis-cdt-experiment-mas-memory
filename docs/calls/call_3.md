# Call 3 — Analisi presentazione + roadmap (2026-05-13)

Presentazione del sistema (`presentation_3.html`) ai relatori. Il documento cattura: qualità del flusso espositivo, dubbi e discussioni tecniche, problemi metodologici, estratti da preparare per validazione esterna, e tutte le direzioni di miglioramento emerse.

---

## Sezione 1 — Flusso espositivo: cosa ha funzionato e cosa no

### 1.1 Struttura complessiva

La presentazione copriva in ordine: overview → setup → ruoli → architettura → flusso → metriche → task → risultati → sfide → roadmap.

**Positivo:**
- Il filo logico dalla struttura ai risultati era corretto.
- La separazione visuale math / textual / security funzionava come introduzione progressiva alla difficoltà.
- Le card con i risultati per task erano chiare e immediate.
- I risultati task6 (fallimento sistematico 2B → risolto con 4B) hanno generato la discussione più ricca: questo è il finding più solido.

**Problemi rilevati durante la call:**
- Presentazione **troppo lunga e troppo tecnica** — un relatore ha esplicitamente chiesto di ridurla per il 19 maggio.
- Struttura pensata per chi conosce già il progetto (supervisori), non per esterni collaboratori.
- Alcune slide venivano saltate con "già dette" — segnale diretto che vanno tagliate.
- Il codice mostrato live (terminale) non era nella presentazione → dualismo confusivo.

### 1.2 Punti in cui il flusso si è interrotto

| Momento | Causa | Stato |
|---|---|---|
| Brier Score | Il tesista stesso incerto sull'interpretazione | Da approfondire prima del 19; rimuovere dalla presentazione se non è ancora chiaro |
| Soglia 0.7 | Un relatore chiede la motivazione — risposta "ho deciso io" | Documentare la scelta con una giustificazione formale (§2.3) |
| Retry con risposta precedente | Domanda su cosa impedisce di ripetere lo stesso errore | Estrarre i reasoning (§2.4); spiegazione corretta già nel documento ma non nella presentazione |
| Task 6 + special attention | Un relatore dice che invalida il test | Punto critico metodologico — separare blind da hint (§3.1) |
| Risultati task 6 2B vs 4B | Il modello 4B non era nella presentazione originale (switch avvenuto in corso) | Aggiornare la presentazione per il 19 |

---

## Sezione 2 — Metriche: stato e chiarimenti

### 2.1 Metriche confermate e chiare

**Rubrica + TEXTUAL_PASS_RATIO = 0.7** — confermata da un relatore come ragionevole. Il criterio "il modello deve coprire >70% dei criteri della rubrica" è comprensibile e giustificabile. La formula è `total_score / total_max ≥ 0.7`.

**Da verificare — riferimento in letteratura:** Un relatore ha chiesto esplicitamente se l'approccio "rubrica con punteggi per categoria usata come prompt del judge" sia descritto in qualche paper. Il tesista non ha trovato un riferimento specifico. Dato che la rubrica è la metrica principale dell'esperimento, è necessario verificare se esiste un termine tecnico consolidato e una citazione. Cercare in letteratura su: LLM-as-judge evaluation, rubric-based scoring, reference-free evaluation con LLM judge. Aggiungere la citazione nella presentazione e nel report finale.

> ✅ **Trovato:** **RUBRICEVAL** (Pan et al., 2026, Fudan University / Ant Group) — benchmark di meta-valutazione per LLM judge a livello di rubrica. Rilevante perché: (1) valida esplicitamente il paradigma "rubric-based LLM-as-judge" come approccio consolidato; (2) §5.1 dimostra empiricamente che la valutazione rubric-level supera checklist-level (+7–12 punti BAcc); (3) anche GPT-4o raggiunge solo 55.97% su casi difficili, contestualizzando l'uso di modelli small come judge. Documento salvato in `docs/RUBRICEVAL.md`.
>
> **Differenza da dichiarare:** RUBRICEVAL usa giudizi binari per criterio (soddisfatto/no), mentre qui il judge assegna punteggi scalari (0–N). Stessa famiglia metodologica, formulazione diversa — da citare come variante nella sezione metodi.

Nota: per task6 il finding primario (missing return) vale 4/9 punti e non viene mai trovato da ≤2B → il modello non supera mai la soglia indipendentemente da dove si mette la threshold. La soglia non è il bottleneck su task6.

**Retry consapevole** — confermato come funzionante e sensato: al retry il modello vede la propria risposta precedente e il prompt "review your previous attempt below and then rethink from scratch". Il modello sa di aver sbagliato ma non sa perché (nessun feedback del judge). Questo è intenzionale.

### 2.2 Brier Score — da approfondire

**Stato:** aggiunto su suggerimento dell'LLM, citato in presentazione ma con interpretazione errata durante la call.

**Chiarimento corretto:**
- Formula: `mean((confidence − is_correct)²)`
- Valore 0 = calibrazione perfetta (confidence 1.0 su risposte corrette, 0.0 su sbagliate)
- Valore 0.25 = confidenza sistematicamente a 0.5 su tutte le risposte (agente "non sa di non sapere")
- Valore 0.5 = risposta casuale o confidenza calibrata al contrario

**Osservazione su task7 expert:** confidence 1.0 su risposta sbagliata → Brier Score 1.0 per quella ripetizione. Questo è il caso peggiore — overconfidence totale su errore. Brier Score medio task7 expert = 0.33.

**Azione:** approfondire la metrica e la sua interpretazione prima del 19. Se rimane nella presentazione, la formula deve comparire con una riga di spiegazione. Altrimenti toglierla.

> ✅ **Decisione:** tenerlo con caveat esplicito. Il BS misura calibrazione della confidenza rispetto al verdetto del judge (`is_correct = verdict correct/wrong`), **non** rispetto a ground truth assoluta — il verdetto è esso stesso LLM-derived e rumoroso. Questo va dichiarato come limitazione. Il valore diagnostico rimane: task7 expert rep3 (BS=1.0 su un attempt, media=0.33 > 0.25) è il segnale più forte di overconfidence sistematica. Anchor points per la slide: 0 (perfetto) · 0.25 (baseline "rispondo sempre 0.5") · 1.0 (confidence 1.0 su errore).

### 2.3 Soglia TEXTUAL_PASS_RATIO = 0.7 — giustificazione da aggiungere

**Giustificazione formale da adottare:** "criterio conservativo — il modello deve coprire almeno 2/3 dei criteri della rubrica per essere considerato corretto". Aggiungere questa frase nella presentazione.

In alternativa mostrare cosa cambia con 0.5: su task6 non cambia nulla (finding primario = 0/4 sempre). Su task7/8 potrebbe cambiare il verdict di qualche ripetizione — valutare se è utile.

### 2.4 Temperatura 0.3 — scelta da documentare meglio

**Discussione:** ogni modello ha una temperatura di default propria (alcuni modelli usano 0.7 di default). La scelta di 0.3 è arbitraria ma esplicita → garantisce riproducibilità cross-modello.

**Decisione da adottare:** mantenere 0.3 esplicito come scelta metodologica deliberata per riproducibilità, e documentarlo come tale nella presentazione (non come parametro casuale).

**Possibile esperimento futuro (non prioritario):** sweep T∈{0.1, 0.3, default, 0.7} su task7/8 e visualizzare curva accuracy vs temperatura. Un relatore ha suggerito questo approccio graficamente: "vedere come impatta la variazione di alcuni parametri per rispondere" — potrebbe essere un risultato aggiuntivo per la tesi.

---

## Sezione 3 — Problemi metodologici critici

### 3.1 Task 6 — special attention nel prompt: invalidante?

**Situazione:** task6 produceva risposte generiche su gemma4:e2b. Su suggerimento dell'LLM è stata aggiunta un'indicazione nel prompt del task (tipo "pay attention to missing return statements"). I punteggi sono migliorati.

**Problema (relatore):** aggiungere un hint guida il modello dove cercare — non è più blind review. Si misura "il modello trova il CVE dato un hint" anziché "il modello trova il CVE da solo".

**Idea emersa (potenzialmente interessante):** e se l'hint non fosse inserito manualmente ma proposto autonomamente da un LLM sulla base delle risposte fallite? Schema:
1. Modello risponde in modo generico → judge lo boccia.
2. Un LLM analizza le risposte fallite e propone un'integrazione al prompt del task (senza vedere la GT).
3. Il modello riprova con il prompt aggiornato.

Questo sarebbe una forma di **continual prompt improvement** — potenzialmente interessante ma con un rischio: se il LLM che genera il hint ha accesso alla GT o alla rubrica (che già conosce i CVE), si reintroduce il bias. Condizione necessaria: il LLM che propone l'hint non deve vedere la rubrica né la GT, solo le risposte del modello e il codice.

**Azione immediata:**
1. Separare nettamente i risultati con hint da quelli blind — non mescolarli.
2. Rieseguire task6 con gemma4:e4b senza special attention come baseline blind pulita.
3. Nella presentazione: mostrare prima i risultati blind, poi come nota "se si aggiunge un hint specifico i risultati migliorano → apre la questione di come generare hint in modo non contaminato".

### 3.2 Rubrica — contaminazione dalla GT

**Situazione:** la rubrica è stata generata chiedendo a un LLM in cloud (Claude) di analizzare i file CVE e costruire i criteri di valutazione. Il modello aveva accesso all'intera directory, inclusi i file con le patch e le spiegazioni CVE.

**Problema (relatore):** la rubrica potrebbe essere circolare — costruita sui CVE → judge valuta rispetto alla rubrica → sembra che il modello "trovi" il CVE, ma in realtà la rubrica già conosce la risposta.

**Valutazione del rischio:** il rischio è reale ma probabilmente limitato. La rubrica valuta *categorie di comportamento* (ha identificato la classe di vulnerabilità? ha localizzato nel codice? ha spiegato l'impatto?), non la risposta esatta. Gli esperti 5G — che hanno identificato le CVE manualmente — possono validare se la rubrica è ragionevole o distorta.

**Azione:** includere il testo completo della rubrica nel pacchetto per la validazione esterna (§4). Documentare il processo di generazione della rubrica come limitation metodologica nella presentazione.

### 3.3 Retry: verifica empirica

**Richiesta (relatore):** estrarre i tre reasoning del task7 expert rep3 (3 retry consecutivi falliti) e verificare se il modello ripete lo stesso ragionamento o varia.

**Ipotesi:** con temperatura 0.3, il modello potrebbe convergere sistematicamente sullo stesso errore. Se i tre reasoning sono identici, il retry senza feedback del judge è inutile a bassa temperatura.

**Azione:** estrarre i file di risultato task7 expert rep3 e confrontare i reasoning dei 3 tentativi. Questo risponde a una domanda metodologica chiara.

> ✅ **Analisi completata (2026-05-14):** I 3 reasoning dell'expert rep3 sono **quasi identici nel contenuto** — tutti e 3 trovano esattamente gli stessi 4 bug con phrasing leggermente variato:
> 1. Undefined variable `reqbody`
> 2. Hardcoded error in `HTTPN1N2MessageTransfer`
> 3. Brittle Content-Type parsing
> 4. Inconsistent error context setting in `HTTPAMFStatusChangeSubscribeModify`
>
> Nessuno dei 3 tentativi trova mai il **missing default case** nello switch di `HTTPUEContextTransfer` — il CVE target. Il 3° attempt aggiunge un 5° finding (`Incomplete Handlers`) ma ignora ancora il target. La `confidence` rimane 1.0 su tutti e 3 i tentativi.
>
> **Conclusione metodologica:** il retry senza feedback del judge non rompe la convergenza su T=0.3. Il modello non ripete la risposta verbatim ma converge sullo stesso errore strutturale — non scansiona mai lo switch statement. Il retry è utile solo se accompagnato da un segnale direzionale (quale finding manca), non come pure re-generation.

### 3.4 Inconsistenza task7: beginner batte expert

**Discussione:** beginner 100% accuracy, expert 66.7% su AMF. Un relatore suggerisce di stampare il prompt completo (system_prompt + task_content) per entrambi i ruoli e confrontarne la lunghezza/complessità.

**Ipotesi principale:** il prompt expert è più lungo e articolato → con un modello piccolo (2B) il modello "si perde" nel contesto più lungo. Fenomeno già osservato: modelli a volte funzionano peggio su task complessi perché il reasoning si allunga a dismisura.

**Azione:** estrarre e confrontare la dimensione del full prompt per expert vs beginner su task7. Salvare questo confronto come dato — è un risultato interessante di per sé.

> ✅ **Ipotesi falsificata (2026-05-14):** la differenza di lunghezza è trascurabile.
>
> | | Expert | Beginner |
> |---|---|---|
> | `system_prompt` | 268 chars | 247 chars |
> | `task_content` | 8544 chars | 8544 chars |
> | Totale | 8812 chars | 8791 chars |
> | Token stimati (log) | ~2662 | ~2654 |
>
> Differenza: 21 caratteri / ~8 token. Non è un problema di context window.
>
> **Spiegazione del paradosso:** il framing "senior expert" porta il modello ad analisi elaborate e verbosa sui bug che trova subito (undefined variable, hardcoded error) — li espande in dettaglio e non arriva mai alla scansione sistematica dello switch. Il framing "junior technician" produce una risposta più diretta e strutturata per bullet point, che scansiona il flusso di controllo del codice in ordine e cattura il default mancante.
>
> Su un modello piccolo (4B), il framing "esperto" non produce code review migliore — produce analisi più prolissa sugli stessi bug, mancando il target CVE. Il beginner trova il missing default case con phrasing diretto: *"The switch statement for content type lacks a robust default case... If an unknown content type is provided, the switch falls through, err remains nil, and the function proceeds to call the processor with potentially uninitialized or incorrectly deserialized data"* → `missing_default_score=4/4`.

### 3.5 False positive rate — non tracciato

I supervisori hanno implicitamente citato il problema ("vedere cosa si inventa"). I modelli potrebbero segnalare vulnerabilità inesistenti — non c'è nessun task con codice Go clean che misuri questo.

**Azione:** prima di creare task aggiuntivi, sfruttare le risposte già esistenti — su task5–9 i modelli potrebbero aver segnalato vulnerabilità non presenti nella GT. Gli esperti 5G, durante la validazione, possono indicare quali finding extra sono reali e quali allucinazioni: questo dà già una stima del false positive rate senza esecuzioni aggiuntive. Se serve una baseline più pulita su codice sano, la forniscono direttamente loro — non serve inventare task.

### 3.6 Struttura risultati: il modello deve diventare una dimensione esplicita

**Problema attuale:** i risultati sono organizzati per `setup / role / task`. Il modello usato è implicito nella config e non appare nel path o nel nome file. Con l'accesso a modelli più grandi (Ollama Cloud ora disponibile gratuitamente, Google API) e la necessità di confrontare più modelli sugli stessi task, questa struttura non regge.

**Problema concreto già esistente:** i file `results/1B/beginner/task5*` e `task6*` usano deepseek-r1 invece di qwen2.5-coder:1.5b-base — lo skip automatico li ha preservati quando qwen è crashato. Il confronto 1A vs 1B su beginner non è valido perché il modello è diverso da quello atteso, e non c'è modo di saperlo dal path.

**Cosa serve:** aggiungere il modello come dimensione tracciata esplicitamente. Due opzioni:

- **Opzione A — nel path dei risultati:** `results/{setup}/{role}/{model}/{task}_rep{n}.md`. Permette di confrontare direttamente più modelli sullo stesso task/setup aprendo cartelle diverse.
- **Opzione B — nel filename o in un campo del file di risultato:** mantenere il path attuale ma aggiungere `model: gemma4:e4b` come campo nel Markdown di output. Più semplice da implementare, meno immediato da confrontare.

**Azione:** decidere la struttura prima di eseguire nuove run con modelli diversi, altrimenti i risultati si accumulano disordinati. La scelta impatta anche i report aggregati (`scores_1A.md`) che dovranno distinguere per modello.

---

## Sezione 4 — Estratti per validazione esterna (Esperti 5G)

Un relatore ha chiesto esplicitamente di inviare i risultati agli esperti 5G (che hanno identificato i CVE manualmente) per validazione umana del ragionamento.

> **Nota modello:** le run nei log (docs/archive/log.md) usano `gemma4:e4b` per setup 1A — il config è stato aggiornato dopo il fallimento di una versione precedente su task6. Il file `status.md` riporta ancora la versione precedente come modello 1A: da aggiornare.

### 4.0 Dati concreti dai log di esecuzione

Riepilogo per ogni task dalle run effettive (gemma4:e4b, setup 1A, 3 ripetizioni):

**task6_vuln_udr_full** — ancora fallisce con e4b sul file completo:
- Rep 1, attempt 1: `missing_return_score=0.0`, norm 0.333 → wrong
- Rep 1, attempt 2: `missing_return_score=0.0`, norm 0.222 → wrong (peggiora)
- Rep 1, attempt 3: judge va in timeout (660s superati)
- **Il finding primario non viene trovato nemmeno con e4b sul file da 2891 righe.** Vedi §5.1 per la diagnosi.

**task7_vuln_amf** — risultati per ruolo:

| Run | Role | Rep | Attempts | `missing_default_score` | norm | verdict |
|---|---|---|---|---|---|---|
| 1A e4b | expert | 1 | 1 | 4/4 | 0.889 | correct |
| 1A e4b | expert | 2 | 1 | 4/4 | 1.000 | correct |
| 1A e4b | expert | 3 | 1 | **0/4** | 0.333 | wrong → |
| 1A e4b | expert | 3 | 2 | **0/4** | 0.556 | wrong → |
| 1A e4b | expert | 3 | 3 | **0/4** | 0.556 | wrong (max retries) |
| 1A e4b | beginner | 1 | 1 | 3/4 | 0.889 | correct |
| 1A e4b | beginner | 2 | 1 | 4/4 | 0.778 | correct |
| 1A e4b | beginner | 3 | 1 | 4/4 | 1.000 | correct |

**Osservazione critica su task7 expert rep3:** `missing_default_score=0` in tutti e 3 i retry. Il punteggio migliora da 3→5→5 ma il finding primario (`missing default` nel switch) non compare mai. Il retry porta a un miglioramento parziale (`inconsistent_context_set_score` e `impact` salgono) ma il pezzo centrale rimane assente. Questo risponde alla domanda di un relatore: il modello non ripete esattamente la stessa risposta (il punteggio varia), ma converge su uno stesso errore specifico — non trova il `missing default case` indipendentemente dal numero di tentativi.

**task8_vuln_udm** — pattern consistente su tutte le run:

| Criterio | Expert (3 rep) | Beginner (3 rep) |
|---|---|---|
| `validation_gap_identified_score` | 4/4, 4/4, 4/4 | 4/4, 4/4, 4/4 |
| `spec_reference_score` | **0/1 sempre** | **0/1 sempre** |
| `impact_assessment_score` | 2/2, 2/2, 2/2 | 2/2, 2/2, 2/2 |
| `fix_quality_score` | 1/2, 1/2, 1/2 | 1/2, 1/2, 1/2 |
| norm finale | 0.778 costante | 0.778 costante |

**Osservazione:** entrambi i ruoli trovano il validation gap (IsValidSupi assente) e l'impatto, ma `spec_reference_score=0` sistematicamente. La rubrica richiede che il modello faccia riferimento alla specifica 3GPP — né expert né beginner lo fanno mai. Domanda per gli esperti 5G: questo criterio è ragionevole? Un analista umano citarebbe esplicitamente la spec 3GPP in una code review?

**task9_vuln_cross** — risultato perfetto e stabile:

| Role | Rep 1 | Rep 2 | Rep 3 | Attempts |
|---|---|---|---|---|
| expert | 9/9 (1.000) | 9/9 (1.000) | 9/9 (1.000) | 1 ciascuno |
| beginner | 9/9 (1.000) | 9/9 (1.000) | 9/9 (1.000) | 1 ciascuno |

`cross_file_inconsistency_score=4/4`, `per_file_coverage_score=3/3`, `impact_global_score=2/2` in ogni singola run. Zero retry, zero varianza semantica.

### 4.1 Task da inviare e priorità (aggiornato con dati log)

| Task | Cosa inviare | Perché è interessante per gli esperti | Priorità |
|---|---|---|---|
| **task5 PCF** | Una run per ruolo | Il più semplice — calibra il processo di validazione prima dei casi difficili. Gli esperti 5G conoscono già questa CVE | **1** |
| **task7 AMF** | Expert rep3 (3 retry, tutti wrong) + beginner rep3 (correct al primo) | Anomalia chiara: `missing_default_score=0` in tutti i retry dell'expert. Gli esperti dicono se la risposta wrong è "quasi giusta" o completamente sbagliata | **1** |
| **task8 UDM** | Una run per ruolo (qualsiasi, sono identiche) | `spec_reference_score=0` sistematico in entrambi i ruoli — la rubrica chiede di citare la spec 3GPP: gli esperti 5G validano se il criterio è ragionevole | **2** |
| task9 Cross-NF | Una run per ruolo | Risultato perfetto e stabile — conferma che il ragionamento è plausibile e non allucinato | **3** |

**Non inviare subito:**
- task6 excerpt (con hint): risultati contaminati dal prompt modificato — inviare solo dopo riesecuzione blind con gemma4:e4b (§3.1), poi diventa priorità 2.
- task6_full: run incompleta (judge timeout al tentativo 3 di rep1).

### 4.2 Cosa includere per ogni task

Per ogni task, un documento Markdown con:

1. **Il codice Go fornito al modello** — estratto esatto, senza hint aggiuntivi.
2. **La rubrica del judge** — testo completo con punteggi max per categoria, incluse le domande specifiche per categoria (necessario per validare se la rubrica stessa è ragionevole e non circolare).
3. **Risposta expert selezionata** — Answer + Reasoning + Confidence + breakdown score per categoria + verdict.
4. **Risposta beginner selezionata** — stessa struttura.
5. **Domande al validatore:**
   - Il CVE identificato è corretto?
   - Il ragionamento è plausibile o è un'allucinazione?
   - La rubrica cattura correttamente cosa significa "corretto" per questa vulnerabilità?
   - (task7) La risposta wrong dell'expert è completamente sbagliata o "quasi corretta"?
   - (task8) È ragionevole attendersi che un analista citi esplicitamente la spec 3GPP in una code review?

---

## Sezione 5 — Modelli più grandi: accesso e piano

### 5.1 Problema attuale — diagnosi corretta dal log

Dal log di esecuzione (docs/archive/log.md), i dati effettivi su task6_full chiariscono la situazione:

- **L'agent non va in timeout:** i tre tentativi dell'agent completano regolarmente (~124s ciascuno, ~29K token in input).
- **Il finding primario non viene trovato:** `missing_return_score=0` in tutti i tentativi — questo è un problema di **capacità** del modello, non di tempo.
- **Il timeout colpisce il judge:** al tentativo 3 di rep1, il judge va in errore 13 secondi dopo l'avvio. Il judge riceve un contesto crescente (input agent ~29K token + risposta ~2.6K) e al terzo retry il contesto accumulato supera il limite.

**Quadro completo su task6_full con gemma4:e4b:**
- Problema 1 (capacità agent): il modello non identifica il pattern `missing return` nel file da 2891 righe — lo stesso che trova sull'excerpt da ~250 righe. Il contesto lungo degrada la capacità di ragionamento.
- Problema 2 (timeout judge): il contesto che il judge riceve cresce tra retry e al terzo tentativo supera il timeout configurato. Sono due problemi distinti con soluzioni distinte.

**Azione:** aumentare il timeout specifico del judge per i task full-file (separato dal timeout dell'agent), e rieseguire per verificare se il finding viene trovato con più contesto disponibile al judge. Se il finding rimane 0 → è confermato che il problema è la capacità dell'agent sul file lungo, non il tempo.

### 5.2 Accesso a modelli più grandi

**Ollama Cloud — disponibile gratuitamente:** confermato durante la call, ora accessibile. Permette di usare modelli Claude (più grandi di gemma4:e4b) senza costi. Da integrare nel codice come provider aggiuntivo accanto a Ollama locale.

**Google API con crediti gratuiti:** Google offre crediti per l'API Gemini. Un relatore stava valutando di aprire una linea di credito con i vari provider per il gruppo di ricerca.

**Prerequisito prima di eseguire:** risolvere §3.6 — definire la struttura dei risultati con il modello come dimensione esplicita. Eseguire nuove run con Claude o Gemini senza una struttura chiara significa accumulare file non confrontabili con quelli esistenti.

**Obiettivo per la presentazione del 19:** mostrare almeno un risultato con un modello più grande su task6 excerpt — confermare o estendere la curva di scaling 1.5B → 2B → 4B → Claude/Gemini.

---

## Sezione 6 — Miglioramenti tecnici del sistema

### 6.1 Tracking e storico — da migliorare

**Situazione attuale:** si salvano token in/out e tempo di esecuzione per ogni risposta. Il testo del prompt non viene salvato.

**Problema emerso (relatore):** per capire perché un modello ha sbagliato o perché un retry non ha funzionato, serve poter confrontare il prompt esatto inviato in ogni run. Senza questo, il debugging è cieco — come dimostrato dal caso task7 expert rep3 dove senza il prompt salvato non si può capire perché il modello converge sempre su `missing_default_score=0`.

**Miglioramenti da fare:**
- Salvare il prompt completo (system_prompt + task_content + eventuale retry context) per ogni run, non solo i token count.
- Il formato attuale dei risultati Markdown ha il layout da sistemare — renderlo più leggibile e uniforme.
- La struttura del path dei risultati è un problema separato trattato in §3.6 (modello come dimensione esplicita).

> ✅ **Implementato (2026-05-14):** ogni entry di `history[n]` ora contiene `prompt_system` e `prompt_user` (task_content con eventuale retry context), `elapsed_seconds`, `tokens_in`, `tokens_out`, `judge_score` (breakdown per criterio di quel tentativo), `verdict`. Aggiunti anche `temperature` e `judge_model` in `run_config`. `final_answer` a livello top è ora un subset pulito a 3 campi (`answer`, `reasoning`, `confidence`) per evitare duplicazione con `history[-1]`. Schema aggiornato in `results/schema_textual.json` e `results/schema_math.json`.

### 6.2 Visualizzazione parametrica — proposta relatore

**Idea:** visualizzare graficamente come varia la performance al variare dei parametri. Esempio: accuracy vs temperatura, o numero di step per arrivare a verdict correct vs temperatura.

Questo trasforma i risultati da una tabella statica a una curva — utile per identificare la combinazione ottimale (token minimi, accuracy massima).

**Azione futura:** implementare un piccolo script di plotting (matplotlib/seaborn) che prende i file di risultato e genera curve parametriche. Non urgente ma utile per la presentazione della tesi.

### 6.3 Context window come variabile controllata

**Discussione:** la context window non è attualmente una variabile controllata — Ollama la gestisce in automatico. Il problema: se un modello ha visto solo metà del codice (context pieno → troncamento) e un altro ha visto tutto, il confronto non è valido.

**Azione da valutare:** passare esplicitamente il parametro `num_ctx` a Ollama in modo che tutti i modelli usino la stessa dimensione di contesto, oppure loggare quanti token del prompt sono stati effettivamente processati (vs quanti erano in input) per verificare se c'è stato troncamento.

### 6.4 Secondo LLM come "flow judge"

**Idea emersa (relatore):** se il flusso di esecuzione è tracciato (quale skill/approccio ha scelto il modello, perché, con che risultato), un secondo LLM potrebbe giudicarlo e dire "il modello ha scelto male in questo punto". Questo è un secondo livello di valutazione rispetto al giudice della singola risposta.

**Stato:** non implementato, non prioritario. Tenerlo come proposta futura per la fase di analisi avanzata.

### 6.5 Ordine campi nel template risposta — bug di format compliance

**Finding (2026-05-14):** analizzando `task1_math_int` con `gemma3:4b-cloud`, tutti e 3 i rep mostravano `attempt 1 wrong` con `answer=840` nonostante il reasoning calcolasse correttamente `1260`. Il modello non sbagliava il ragionamento — sbagliava il campo `### Answer` perché il template chiedeva `Answer` **prima** di `Reasoning`.

**Causa:** il modello è forzato a committare il numero finale nel campo `### Answer` prima di sviluppare il calcolo in `### Reasoning`. Produce un'ipotesi iniziale errata (840), poi nel reasoning si autocorregge a 1260 — ma il parser legge il campo answer già committato.

**Fix applicato:** invertito l'ordine in tutti i 12 file di task (`Reasoning → Answer → Confidence`). Il parser non cambia — usa regex per nome heading, non per posizione.

> ✅ **Implementato (2026-05-14):** tutti i template ora seguono l'ordine `### Reasoning / ### Answer / ### Confidence`. Questo forza chain-of-thought prima del commit sulla risposta finale. Il fix è retroattivo su tutti i task inclusi i `*_full`.

---

## Sezione 7 — Roadmap sintetica

### 7.1 Prima del 19 maggio

- [ ] **Presentazione inglese breve** (vedi §8)
- [x] **Estrarre reasoning task7 expert rep3** (3 retry) — quasi identici, convergono su stessi 4 bug, missing default case mai trovato (§3.3)
- [x] **Estrarre full prompt** expert vs beginner task7 — differenza 21 chars / ~8 token, ipotesi contesto lungo falsificata (§3.4)
- [ ] **Rieseguire task6 blind** con gemma4:e4b (senza special attention)
- [ ] **Preparare estratti** per gli esperti 5G: task5, task7, task8 (§4)
- [ ] **Approfondire Brier Score** — decidere se tenerlo o toglierlo dalla presentazione
- [x] **Trovare riferimento in letteratura per la rubrica** — RUBRICEVAL (Pan et al., 2026) trovato e documentato in `docs/RUBRICEVAL.md`. Vedi §2.1 per dettagli e punti da citare.
- [x] **Investigare timeout task6_full** — il problema è il judge (non l'agent): aumentare il timeout del judge per i task full-file e rieseguire (vedi §5.1). Implementato: task con "full" nel nome ottengono `TASK_TIMEOUT_SECONDS × FULL_TASK_TIMEOUT_MULTIPLIER` (default ×2 = 1200s). Configurabile in `config.py`. Log stampa `Full task detected → timeout Xs → Ys`.
- [ ] **Validazione rubrica da esperti 5G** → eventuale revisione criteri

### 7.2 Medio termine (dopo esami giugno)

- [x] Accedere a modelli più grandi — **eseguito** via Ollama Cloud: B1_cloud (gemma4:31b-cloud, expert 100% su task7), B2 (31b vs 12b, expert>beginner). Curva scaling expert task7: e2b=0% → e4b=66.7% → 31b=100%. Vedi F21–F22 in `findings.md`.
- [ ] Setup 1B completo con qwen2.5-coder:1.5b-base (eliminare run vecchie deepseek)
- [x] Salvare prompt completo per ogni run (§6.1) — `history[n].prompt_system` e `history[n].prompt_user` (2026-05-14)
- [ ] Retry con feedback judge reiniettato
- [ ] Task controllo negativo (false positive rate)
- [x] Varianti full-file — B2 expert (gemma4:31b-cloud) ha eseguito excerpt + full su task6/7/8/9. task7_full e task8_full non eseguiti su local (rimangono pending per e4b).
- [x] **Tracciamento score intermedi per-attempt:** ogni `history[n]` ora include `judge_score` (breakdown completo per criterio di quel tentativo) e `verdict`. Il `judge_score` top-level rimane quello dell'ultimo attempt. Implementato in `_check_answer` via `state["history"][-1]["judge_score"] = judge_score` (2026-05-14).

### 7.3 Lungo termine / open questions

- [ ] Sweep temperatura su task7/8 — curva accuracy vs T
- [ ] Curva scaling completa: 1.5B → 2B → 4B → 7B su task6

- [ ] Continual prompt improvement: LLM propone hint dalle risposte fallite (senza vedere GT/rubrica)
- [ ] Esperimento autonomo: LLM su intero codebase free5GC per trovare CVE non documentate
- [ ] Visualizzazione parametrica (accuracy vs T, token vs accuracy)

---

## Sezione 8 — Note per la presentazione del 19 maggio

### 8.1 Vincoli

- Durata: ~15 min (tesista), ~15 min (collaboratore esterno) + discussione
- Lingua: inglese
- Audience: collaboratori esterni, relatori
- Obiettivo: cross-fertilization — non un deep dive tecnico. I relatori vogliono che i collaboratori esterni capiscano cosa stai facendo e che ci sia interazione sui punti di contatto con loro lavori (es. ontologia → knowledge graph).

### 8.2 Schema narrativo (da costruire nella prossima sessione)

Logica: **problema → approccio → risultati → domande aperte**. Non struttura del codice.

```
1. Context (1 slide)
   "5G networks run on open-source software. Real vulnerabilities exist.
   Can LLMs find them automatically?"
   → free5GC, real CVEs, code in Go

2. Experiment design (2 slides)
   → Expert vs Beginner LLM on the same task
   → Three task categories: math (deterministic) → textual → security code review
   → Automated evaluation: deterministic for math, judge LLM + rubric for text

3. Key results (2–3 slides)
   → Task 1–4: math + textual baseline, all correct, no differentiation (too easy)
   → Task 5: first security task, all models correct — upper bound of the set
   → Task 6: 2B fails systematically, 4B succeeds — model size threshold
   → Task 7: beginner beats expert — anomaly still open
   → Task 8–9: CVE found but partial rubric coverage (norm 0.778)

4. Open problems (1 slide)
   → False positive rate not measured
   → Rubric contamination risk (known limitation)
   → Full-file timeout (capacity vs latency open question)
   → Scaling curve 2B → 4B → 7B not yet complete

5. Next steps (1 slide)
   → Expert validation (esperti 5G)
   → Cloud models access for larger models
   → Negative control task
```

### 8.3 Cosa tagliare rispetto a presentation_3.html

- Mappa codice dettagliata (file per file) — va tolta del tutto
- SVG grafo LangGraph con tutti i nodi — troppo tecnico per esterni
- Card setup 1A vs 1B con dettaglio modelli — semplificare a 1 slide
- Spiegazione Brier Score se non ancora capita bene
- Slide metriche con 4 card — condensare in 1 slide con 2 concetti: accuracy e rubric coverage

### 8.4 Possibile punto di contatto con collaboratori esterni (ontologia)

Some collaborator's work estrae automaticamente concetti e relazioni da testi e li struttura in un knowledge graph. Possibile sinergia: usare un knowledge graph delle vulnerabilità 5G (con relazioni tra CVE, pattern di codice, NF coinvolte) come struttura di supporto per guidare il modello o per validare il ragionamento. Da esplorare nella discussione — non mettere in presentazione, lasciare emergere naturalmente.

---

## Agenda call 19 maggio (ore 17)

- Tesista: presentazione LLM 5G security (inglese, ~15 min)
- Collaboratore esterno: presentazione knowledge graph + ontologia per estrazione concetti/relazioni (~15 min)
- Discussione cross-fertilization
- Collaboratore esterno (supervisor/ricercatore): presente

**Ospiti:** Relatori, collaboratori esterni. **Lingua:** inglese.
