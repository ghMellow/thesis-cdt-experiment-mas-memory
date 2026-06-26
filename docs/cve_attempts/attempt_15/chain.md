# Attempt 15 — Chain of Reasoning

**Data:** 2026-06-26  
**Branch:** exp/test-13  
**Commit:** see git log

---

## File letti in ordine

1. `File_Free5gc_Vulnerabili/Patch_Spiegazione.md` — indice CVE per NF (AMF, PCF, UDM, UDR)
2. `docs/tasks/task1_math_int.md` + `task1_math_int_sol.md` — formato task base
3. `docs/tasks/task3_anomaly.md` + `task3_anomaly_sol.md` — formato task testuale con rubrica
4. `docs/tasks/task4_rootcause.md` — formato task multi-step
5. `File_Free5gc_Vulnerabili/AMF/api_communication.go` — 502 righe, handler SBI AMF
6. `File_Free5gc_Vulnerabili/PCF/api_oam.go` — 66 righe, handler OAM PCF
7. `File_Free5gc_Vulnerabili/UDM/api_subscriberdatamanagement.go` — 859 righe, handler SDM UDM
8. `File_Free5gc_Vulnerabili/UDR/api_datarepository.go` — 2892 righe, handler UDR completo

---

## Task 5 — AMF (api_communication.go)

### Cosa ha colpito

La CVE citata nel documento è "no DEFAULT CASE" — ovvio, ma il punto non è il fatto in sé,
è il *perché è pericoloso in Go*. In Go, uno switch senza `default` e senza matching case
semplicemente non esegue niente. `err` resta `nil` (dal successo della `GetRawData` precedente).
Il check `if err != nil` subito dopo passa silenziosamente. Il processor viene chiamato con un
`ueContextTransferRequest` che ha `JsonData` puntatore a una struct zero-value e niente altro.

Il confronto diretto con `HTTPCreateUEContext` — che nello stesso file ha il `default` — rende
il task molto più leggibile e insegnabile. L'agente deve riconoscere la differenza strutturale,
non solo "manca il default".

Ho scelto `HTTPUEContextTransfer` e non altri handler AMF perché:
- È il caso CVE diretto
- Il confronto con l'handler "gemello" già corretto nella stessa funzione è una prova
  di ragionamento per differenza, non di memorizzazione
- L'impatto nel contesto 5G (handover UE con contesto vuoto) è concretamente spiegabile

### Cosa ho scartato

- `HTTPN1N2MessageTransfer` ha un default che lancia errore per `applicationjson` (linea 396),
  che è un comportamento strano (rifiuta JSON puro per N1N2) ma non è una vulnerabilità
  di sicurezza classica — è più un errore di design del protocollo. Scartato.
- `HTTPCreateUEContext` ha il default corretto — usato come riferimento positivo nel task.

---

## Task 6 — PCF (api_oam.go)

### Cosa ha colpito

Il file è piccolo (66 righe) ma concentra due problemi concettualmente distinti che molti
strumenti di analisi statica non segnalerebbero insieme:

1. **`s.router.Use()` dentro un handler**: questo è il DoS. `s.router` è il gin Engine
   condiviso. Ogni richiesta al path `/am-policy/:supi` aggiunge un middleware CORS alla catena
   globale. La catena cresce senza limite. Non è un memory leak classico — è una crescita
   *controllata dall'attaccante* e permanente per la durata del processo.

2. **`AllowAllOrigins: true` + `AllowCredentials: true`**: la spec CORS vieta questa
   combinazione. gin-contrib/cors stesso va in panic se entrambi sono impostati. Il codice
   manuale che imposta `Access-Control-Allow-Credentials: true` + `Access-Control-Allow-Origin: *`
   aggiunge confusione sopra alla configurazione già sbagliata.

Il punto più interessante per il task cross-NF: questo è l'unico bug che deriva da un errore
architetturale (router = stato condiviso mutable) piuttosto che da input validation mancante.
Distingue il PCF dagli altri NF in modo netto.

### Cosa ho scartato

Non c'era molto altro da esaminare nel file. La funzione `HTTPOAMGetAmPolicy` è corretta
(valida SUPI non vuoto) — scartata come materiale di vulnerabilità.

---

## Task 7 — UDM (api_subscriberdatamanagement.go)

### Cosa ha colpito

La CVE citata è "missing validator.IsValidSupi()" — ma il documento non dice dove manca.
Leggendo il codice, ho trovato che `HandleGetAmData` valida il SUPI e altri 4+ handler no.
La narrazione "un handler lo fa, gli altri no" è la struttura ideale per un task di code review:
il modello deve riconoscere il pattern, non solo segnalare "manca la validazione".

La vulnerabilità secondaria di `HandleGetTraceData` è quella che mi ha colpito di più:
usa `plmnID := c.Query("plmn-id")` come stringa raw, mentre tutti gli altri handler che usano
plmn-id lo parsano come JSON struct via `getPlmnIDStruct`. Questa non è nella CVE, ma è
un'inconsistenza reale con impatto pratico (parametro strutturato trattato come stringa libera).

Ho scelto questa come "what's not obvious" richiesto: richiede leggere abbastanza handler
diversi per vedere il pattern comparativo.

### Cosa ho scartato

- `OneLayerPathHandlerFunc` usa `strings.Contains(route.Pattern, supi)` per routing dinamico.
  Questo è potenzialmente problematico (un SUPI che contiene pattern strings potrebbe matchare
  route sbagliate) ma è troppo dipendente dall'implementazione interna di `getOneLayerRoutes()`
  per costruirci un task autonomo con snippet limitato. Scartato per complessità di contesto.

- Handler `HandleModifyForSharedData` non valida `supi` — incluso implicitamente nel task
  come parte dell'inconsistenza, non come caso separato.

---

## Task 8 — UDR (api_datarepository.go)

### Cosa ha colpito

Il file ha 2892 righe e contiene molti handler. Ho trovato tre classi distinte di bug:

1. **Missing return dopo c.JSON() in più handler** — la classe CVE principale. In Snippet C
   (DELETE handler) la conseguenza è la più grave: il 404 è scritto ma la delete esegue.
   In un data repository, questo significa che una request *esplicitamente rifiutata* modifica
   dati persistenti. Questa è la differenza da sottolineare rispetto agli altri NF.

2. **`openapi.Deserialize(policyDataSubscription, ...)` per valore, non pointer** —
   in `HandlePolicyDataSubsToNotifyPost` (riga 1432) e stessa funzione Put (1464).
   Il pattern sbagliato è nascosto da un pattern corretto usato in quasi tutti gli altri handler
   (`&sdmSubscription`, `&patchItemArray`, ecc.). Richiede confronto con altri handler per essere
   individuato — esattamente il tipo di ragionamento che voglio testare.

3. **`HandleCreateEeSubscriptions`/`HandleQueryeesubscriptions`: regex `|.+`** — questo è
   il bug CVE GHSA-6gxq-gpr8-xgjp nella sua forma originale. L'alternazione termina con `.+`
   che rende l'intera regex universalmente vera. Ho scelto di includerlo nel task 8 come
   Snippet D implicito (il task 9 lo espande nel cross-NF). Nel task 8 mi sono concentrato
   sui missing return e value-not-pointer perché sono più ricchi come classe di bug per l'UDR.

   Nel task 8 ho lasciato fuori il regex `|.+` — lo uso nel task 9 cross-NF dove ha più
   valore didattico nel confronto.

4. **`HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete/Get`**: manca return
   dopo il check `influenceId != "subs-to-notify"`. Questo è il caso più severo di missing
   return: non solo si risponde con 404, ma si esegue un'operazione side-effectful (delete).

### Cosa ho scartato

- Il bug in `HandlePolicyDataSubsToNotifyPost` dove `reqBody` può essere nil se GetRawData
  fallisce, e poi si prova a Deserialize su nil — questo deriva già dal missing return, non
  è un bug separato. Non l'ho incluso come quarto bug distinto per non sovraccaricare il task.

---

## Task 9 — Cross-NF

### Come ho scelto cosa mettere

Criteri per la selezione dei pattern cross-NF:

1. **Silent passthrough** (AMF Snippet 1 + UDR Snippet 3): il pattern più pericoloso. Due NF,
   due meccanismi diversi (switch no-default vs missing return), stesso effetto: un controllo
   di sicurezza che non blocca nulla. Questo contrasto è il cuore del task 9.

2. **Inconsistent validation** (UDM Snippet 2): un pattern completamente diverso dal precedente.
   Qui non è che il guard è rotto — è che è semplicemente assente per alcuni handler.
   Il confronto Snippet 2 (guard assente) vs Snippet 3 (guard presente ma inefficace) è la
   domanda chiave del task — richiede precisione linguistica per rispondere correttamente.

3. **Regex universalmente vera** (UDR Snippet 4): ho incluso il `|.+` perché è il cuore della
   CVE GHSA-6gxq-gpr8-xgjp — il fatto che sembri validation ma non lo sia è la proprietà
   più interessante. Un modello deve capire la semantica della regex alternation, non solo
   flaggare "regex presente = buono".

4. **Resource exhaustion da stato condiviso** (PCF Snippet 5): un pattern ortogonale a tutti
   gli altri. Non è input validation — è architettura. Lo includo per testare se il modello
   riesce a classificare correttamente un bug architetturale in mezzo a bug di control flow.

### Cosa ho scartato dal cross-NF

- Il bug value-not-pointer di UDR: è un errore Go-specifico importante ma meno generalizzabile
  come anti-pattern cross-NF. Non ha paralleli negli altri file. Lasciato al task 8.
- Il routing via `strings.Contains` in UDM: troppo dipendente dal contesto della funzione
  `OneLayerPathHandlerFunc` per essere presentato come snippet autonomo in un task cross-NF.
- Doppio header CORS in PCF: già coperto dal task 6; non aggiunge valore nel cross-NF
  dove il pattern è già il router.Use() dentro handler.

### Note finali sul formato

Ho privilegiato snippet corti nei task short (<30 righe) per adattarmi alla finestra di
contesto limitata. I task long includono il contesto di confronto (handler corretto vs
vulnerabile) perché senza di esso la domanda sarebbe solo "trova il bug" invece di
"capisci la struttura del problema".

Le rubriche sono calibrate per distinguere tra:
- Risposta che identifica il sintomo ("manca return")
- Risposta che identifica la meccanica ("err resta nil / processor chiamato con zero-value")
- Risposta che identifica l'impatto nel contesto 5G ("handover con security context vuoto /
  delete eseguita su richiesta rifiutata")

Questo schema a tre livelli permette al judge di discriminare tra modelli con capacità diverse.
