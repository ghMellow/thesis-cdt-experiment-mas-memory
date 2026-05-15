# Speaker notes — presentation_new

---

## Slide 01 · Cover

Buongiorno a tutti. La domanda che guida questo lavoro è semplice e diretta: un large language model, eseguito localmente, riesce a trovare vulnerabilità reali nel codice di una rete 5G?

Non stiamo parlando di benchmark sintetici — stiamo parlando di CVE pubblicati, advisory GHSA, codice Go in produzione. Questo è il punto di partenza della mia tesi magistrale nell'ambito del CDT.

---

## Slide 02 · Motivation — From Paper-Reading to a Real Experiment

Dopo mesi a leggere paper su valutazione degli LLM e sistemi multi-agente, avevo bisogno di un esperimento concreto, su un dominio non banale.

Mi sono posto tre domande operative. Prima: cambiare il system prompt — passare da "senior 5G engineer" a "junior technician" — cambia quello che il modello trova? Seconda: la dimensione del modello domina sul framing? Terza, la più ambiziosa: un LLM può identificare CVE reali nel codice 5G senza nessun hint?

Ho scelto free5GC come dominio perché ha advisory GHSA pubblicati — quindi una ground truth misurabile — e il codice richiede simultaneamente conoscenza di Go, del framework Gin, e delle specifiche 3GPP. Non è un problema facile.

---

## Slide 03 · Experimental Design — Two Setups · Two Roles · Three Repetitions

Il design è strutturato su due setup distinti.

Nel Setup 1A — quello di controllo — Expert e Beginner girano sullo stesso identico modello. Se vedo differenze nei risultati, provengono solo dal system prompt, non dalla capacità computazionale.

Nel Setup 1B — quello comparativo — all'Expert assegno il modello più grande, al Beginner quello più piccolo. Qui misuro l'effetto combinato di framing e capacità.

In entrambi i casi ogni task viene ripetuto tre volte in modo indipendente, a temperatura fissa e bassa. Se il modello sbaglia, ha fino a tre retry automatici. L'output è sempre strutturato: ragionamento, risposta, confidence.

---

## Slide 04 · Tasks — Three Categories, Increasing Difficulty

I task sono organizzati in tre categorie a difficoltà crescente.

I primi due sono task matematici deterministici — aritmetica di rete 5G con risultato esatto. Nessun judge necessario: confronto diretto. Servono a validare il framework prima di affrontare task più complessi.

I task tre e quattro sono testuali: classificazione di anomalie e root-cause analysis su scenari 5G operativi. Qui interviene un judge LLM con rubrica.

I task cinque-nove sono il cuore dell'esperimento: code review cieco su codice Go reale, con CVE pubblicati come ground truth. Include anche varianti "full file" fino a 2891 righe di codice.

---

## Slide 05 · Architecture — LangGraph Execution Flow

L'infrastruttura è costruita su LangGraph. Il flusso per ogni run è questo.

Parto da una tupla di input: setup, ruolo, task, ripetizione. Il nodo `load_task` carica lo scenario, il file soluzione e la ground truth. Il nodo `run_agent` fa la chiamata LLM, converte il markdown in JSON strutturato. Il nodo `check_answer` valuta: per i task matematici con Python esatto, per i task testuali con il judge LLM.

Se la risposta è sbagliata e i retry non sono esauriti, si torna a `run_agent`. Quando la risposta è corretta o si raggiunge il massimo di retry, `save_result` serializza tutto su disco. Traccio anche i token in ingresso e in uscita per ogni chiamata.

---

## Slide 06 · Evaluation Method — Judge LLM + Rubric-Based Scoring

Per i task testuali e di security non posso fare confronto diretto — ho bisogno di un judge.

Il judge è un LLM separato da quello sotto esame. Riceve il codice e la rubrica, ma mai il testo della ground truth — altrimenti sarebbe una comparazione di stringhe mascherata.

La rubrica definisce criteri pesati per task: classe di vulnerabilità, posizione nel codice, impatto sulla sicurezza, qualità del fix proposto. Se il punteggio normalizzato supera 0.7, la risposta è corretta.

Il metodo si basa su RubricEval di Pan et al., 2026. C'è però una limitazione che tengo traccia: la rubrica è stata costruita con accesso alle patch dei CVE, quindi esiste un potenziale di circolarità. Ho già segnalato questo punto per la validazione esterna con esperti di dominio 5G.

A destra vedete un esempio reale: task7, run beginner — punteggio 9/9, normalizzato 1.000, verdict corretto.

---

## Slide 07 · Domain — 5G Core Networks & free5GC

Un po' di contesto di dominio per chi non lavora quotidianamente con reti 5G.

Il core 5G è composto da network function specializzate. La PCF gestisce le policy di QoS e le regole di charging. L'AMF è il punto di ingresso per tutti i dispositivi — gestisce registrazione, connessione e mobilità. L'UDM conserva i profili degli abbonati e le credenziali. L'UDR è lo strato di storage grezzo, esposto via REST Gin.

free5GC è un'implementazione open source completa in Go, usata sia nella ricerca accademica che in deployment reali. Ha pubblicato diversi advisory GHSA su PCF, AMF, UDM e UDR — tutti scoperti manualmente da esperti.

Il punto chiave è questo: un tool di static analysis generico non avrebbe flaggato nessuno di questi bug. Richiedono comprensione semantica e conoscenza di dominio — Go, Gin e 3GPP insieme.

---

## Slide 08 · Security Tasks — Five CVE Tasks

Ecco i cinque task di security, tutti basati su CVE reali pubblicati.

Task 5: misconfiguration CORS nel PCF — review cieco, difficoltà media.
Task 6: missing return dopo 404 negli handler Gin dell'UDR — sei advisory GHSA diversi, difficoltà alta. Questo è l'unico task con un hint esplicito, quindi i risultati vanno interpretati separatamente.
Task 7: missing default case nel switch sul Content-Type nell'AMF — review cieco, difficoltà media.
Task 8: validazione SUPI assente in sei degli otto handler UDM — review cieco, difficoltà medio-alta.
Task 9: analisi cross-NF — tutti e quattro i file insieme, sia bug per-file che pattern trasversali. Il più complesso.

---

## Slide 09 · CVE Deep Dive — task5 & task6

Entriamo nel dettaglio dei primi due task di security.

Task 5, PCF: la configurazione CORS abilita simultaneamente `AllowAllOrigins` e `AllowCredentials`. In Gin questo è un anti-pattern noto: qualsiasi origine può inviare richieste con credenziali — cookie, token, header di autenticazione esposti cross-origin. 65 righe di codice, bug immediatamente visibile.

Task 6, UDR: questo è più sottile. Nella funzione `GetSubscriptionData`, quando il fetch fallisce si scrive una risposta 404, ma manca il `return`. In Gin scrivere una risposta non interrompe l'esecuzione — il codice continua con `data` nil. Questo pattern è ripetuto su sei endpoint diversi. Richiede conoscenza specifica del comportamento di Gin per essere identificato.

---

## Slide 10 · CVE Deep Dive — task7, task8, task9

I tre task più complessi.

Task 7, AMF: lo `switch` sul Content-Type gestisce json e multipart, ma il caso `default` è vuoto — passa silenziosamente. Una richiesta con Content-Type sconosciuto arriva all'handler con uno struct nil o zero-value. Il bug è un'omissione, non un errore attivo — più difficile da notare.

Task 8, UDM: solo due degli otto handler chiamano `IsValidSupi()` — `GetAmData` e `Unsubscribe`. Gli altri sei lasciano passare SUPI non validi fino ai filtri MongoDB. Il problema non è nel codice sbagliato, ma nel codice mancante in modo inconsistente.

Task 9: il task più ambizioso. Il modello riceve tutti e quattro i file contemporaneamente e deve trovare sia i bug singoli che i pattern trasversali — lo stesso tipo di dato validato in un NF e non validato in un altro.

---

## Slide 11 · Results — Tasks 1–5, Saturation at 100%

I risultati della prima metà dell'esperimento sono chiari.

Task 1 e 2, matematici: 100% in tutte le run, sia Expert che Beginner. Il framing non produce nessuna differenza misurabile su task deterministici.

Task 3 e 4, testuali 5G: 100%, punteggio normalizzato 1.000. Stessa storia.

Task 5, CORS nel PCF: 100% per entrambi i ruoli. Il motivo è che AllowAllOrigins più AllowCredentials è un anti-pattern già presente abbondantemente nei dati di training — il modello lo riconosce immediatamente su 65 righe.

Il risultato di saturazione non è banale: conferma che il framework funziona correttamente, e che il framing inizia a fare differenza solo quando il task è genuinamente difficile.

---

## Slide 12 · Results — task6, A Hard Model Size Threshold

Il task 6 è dove il sistema mostra il primo risultato netto e inatteso.

Il modello da 2 miliardi di parametri: zero su dodici. Non una singola run corretta, né Expert né Beginner, nemmeno dopo tre retry. Il missing_return_score è sempre 0/4. Il modello parla di security generica in Go ma non capisce il comportamento di Gin.

Il modello da 4 miliardi: 100%. Tutte le run, entrambi i ruoli. Identifica correttamente `c.String(404)` senza `return` e spiega il meccanismo di esecuzione di Gin e l'impatto downstream.

Questo è un threshold netto, non una degradazione graduale. Richiede simultaneamente Go, Gin e 3GPP SBI — un tipo di ragionamento multi-strato che non è comune nei dati di training di sicurezza generici. E il framing non chiude questo gap.

---

## Slide 13 · Results — task7, The Framing Paradox

Questo è il risultato più interessante e controintuitivo dell'intero esperimento.

Stesso modello, stesso task. Expert: 66.7% — la terza ripetizione sbaglia tutte e tre i retry. Il missing_default_score è 0/4 in ogni tentativo. La confidence rimane 1.0 per tutto il tempo — è overconfident su una risposta sistematicamente sbagliata.

Beginner: 100%. Tutte e tre le ripetizioni corrette al primo tentativo. Produce un'analisi strutturata a bullet point e identifica esattamente il problema: "lo switch manca di un caso default robusto — un Content-Type sconosciuto passa con uno struct nil".

La differenza nel system prompt è di 8 token. Non è un problema di context window. La mia ipotesi è che il framing "senior engineer" spinga il modello verso un'analisi più esplorativa e verbose, che gli fa perdere il bug di control flow più semplice che un junior avrebbe visto per primo.

---

## Slide 14 · Results — task8 & task9

Task 8, UDM: 100% di accuracy per entrambi i ruoli. Trovano `IsValidSupi()` assente in sei handler. Ma il punteggio normalizzato si ferma a 0.778 perché il criterio `spec_reference_score` è sempre 0/2 — nessun ruolo cita mai esplicitamente la specifica 3GPP TS 29.503.

Questo apre una domanda di design della rubrica: è ragionevole aspettarsi che un code reviewer citi la specifica 3GPP nel review? La risposta non è ovvia. Ho segnalato questo punto per la validazione degli esperti di dominio.

Task 9, cross-NF: 100% con copertura completa della rubrica, normalizzato 1.000. Zero retry, zero inconsistenze semantiche su tutte e sei le run. Il risultato è solido. L'unica nota curiosa: l'Expert ha confidence 0.5 nonostante il punteggio perfetto — cosa segnala questa calibrazione?

---

## Slide 15 · Open Questions — What Remains Uncertain

Cinque questioni aperte che determinano le prossime fasi.

Prima: il paradosso del framing nel task 7 è riproducibile? Devo fare ablation sistematici — prompt neutro, expert con stile vincolato, beginner con hint tecnico — per isolare la causa.

Seconda: contaminazione della rubrica. La rubrica è stata costruita con accesso alle patch dei CVE. Il judge sta valutando comprensione genuina, o sta riecheggiando linguaggio derivato dalle patch stesse?

Terza: false positive rate. Non ho ancora task di controllo negativo — handler Go puliti senza CVE. Non so quanti falsi allarmi produce il sistema.

Quarta: task 6 con hint. Quel "Pay special attention to…" cambia completamente cosa misura il task — non è blind detection, è analisi guidata. I risultati vanno interpretati in una categoria separata.

Quinta: la curva di scaling. Ho il threshold 2B→4B. Non ho ancora dati su 12B, 32B, o modelli cloud di grandi dimensioni. Il paradosso del framing persiste a capacità maggiore?

---

## Slide 16 · Summary & Next Steps

Tre conclusioni principali.

La prima è un fatto: il threshold di capacità è reale e netto. 2B non riesce su task 6 in modo sistematico; 4B lo risolve completamente. Il framing non chiude questo gap.

La seconda è un'ipotesi da testare: il framing può nuocere. "Senior engineer" sembra indurre un'analisi più elaborata che perde bug di control flow più semplici. È un risultato sorprendente che richiede ablation sistematici per essere confermato.

La terza riguarda il metodo: judge più rubrica produce punteggi consistenti e discriminanti. Ma serve validazione esterna da parte di esperti 5G per escludere circolarità dalla costruzione della rubrica.

Per citare la nota finale: il fallimento sistematico è un risultato. Il rovesciamento Expert-Beginner è un'ipotesi. Il validation package è pronto.

Grazie.
