# Chain — Attempt #6

## File letti (in ordine)

- `File_Free5gc_Vulnerabili/PCF/api_oam.go` — letto per primo: file piccolo (65 righe), punto di partenza per capire la struttura generale degli handler Gin usata nel corpus; atteso il CORS bug già noto da literartura
- `File_Free5gc_Vulnerabili/AMF/api_communication.go` — letto secondo: file medio (501 righe), gestione del ciclo di vita UE context e N1N2; cercavo inconsistenze nel tipo di dato passato a c.Set e nel pattern switch/Content-Type
- `File_Free5gc_Vulnerabili/UDM/api_subscriberdatamanagement.go` — letto terzo: 859 righe, focus sulla consistenza di validazione SUPI tra handler dello stesso file; trovata la disuguaglianza tra HandleGetAmData (validato) e HandleGetSmfSelectData/HandleGetNssai/etc. (non validati)
- `File_Free5gc_Vulnerabili/UDR/api_datarepository.go` — letto per ultimo, più lungo (2892 righe), letto in due blocchi (0-1845, 1845-2892); cercavo il pattern missing-return già identificato nel documento ANALISI_VULNERABILITA.md, il bug regex, e nuovi pattern non ancora trasformati in task

Documenti di supporto letti:
- `File_Free5gc_Vulnerabili/ANALISI_VULNERABILITA.md` — documento di analisi statica preesistente con 8 vulnerabilità identificate (V1-V8); ha guidato la priorità ma ho cercato attivamente pattern non coperti
- `docs/tasks/task[5-9]*.md` su branch main — letti per capire cosa era già stato trasformato in task su altri branch, per evitare duplicazioni

## Candidati valutati

Per ogni pattern/problema considerato (anche quelli scartati):

- **CORS AllowAllOrigins+AllowCredentials** in `PCF/api_oam.go:21-38` — immediatamente visibile; combinazione AllowAllOrigins:true con AllowCredentials:true viola CORS spec — **incluso come task5_vuln_pcf**

- **Missing return dopo c.String(404) — handlers subs-to-notify** in `UDR/api_datarepository.go:1208-1239` — tre handler (Delete, Get, Put) con stesso pattern: c.String(404) senza return, esecuzione continua verso processor; già in ANALISI V2 — **incluso come parte di task6_vuln_udr**

- **Regex |.+ catch-all in ueId validation** in `UDR/api_datarepository.go:2569-2602` — pattern `^(imsi-...|nai-.+|...|.+)$` dove `|.+` rende l'intera regex inutile; già in ANALISI V3 — **incluso come parte di task6_vuln_udr**

- **c.Set con struct completa invece di stringa** in `AMF/api_communication.go:186,230,265,299,384` — cinque handler passano `problemDetail` (struct) invece di `problemDetail.Cause` (string) a IN_PB_DETAILS_CTX_STR; già in ANALISI V6 — **incluso come parte di task7_vuln_amf**

- **Missing default nel switch Content-Type di HTTPUEContextTransfer** in `AMF/api_communication.go:339-358` — lo switch manca del caso default, Content-Type sconosciuto lascia err=nil e chiama il processor con struct non deserializzata; già in ANALISI V7 — **incluso come parte di task7_vuln_amf**

- **HTTPCreateUEContext default case vuoto** in `AMF/api_communication.go:56` — `default:` presente ma vuoto — non genera errore, stesso problema di HTTPUEContextTransfer ma con il case almeno presente; **scartato** come finding separato perché già coperto implicitamente dalla discussione in task7; la distinzione è sottile e la rubrica diventerebbe confusa

- **HTTPN1N2MessageTransfer applicationjson always-error** in `AMF/api_communication.go:396` — `case applicationjson: err = fmt.Errorf(...)` rende impossibile POST con Content-Type JSON — **incluso come terzo finding in task7_vuln_amf**

- **Missing SUPI validation in HandleGetSmfSelectData e altri** in `UDM/api_subscriberdatamanagement.go:119-177` — sei handler omettono `validator.IsValidSupi()` mentre HandleGetAmData lo usa; già in ANALISI V8 — **incluso come task8_vuln_udm**

- **Missing return dopo c.JSON in HandlePolicyDataSubsToNotifyPost e ...Put** in `UDR/api_datarepository.go:1420-1443,1453-1477` — entrambi i handler mancano di return dopo ogni c.JSON() di errore, causando caduta verso la chiamata al processor; bug **distinto** dal pattern in task6 (che riguarda c.String, non c.JSON, e un contesto di routing diverso) — **incluso come task9_vuln_udr_policy**

- **Passaggio by-value di policyDataSubscription a openapi.Deserialize** in `UDR/api_datarepository.go:1432,1464` — `Deserialize(policyDataSubscription, ...)` invece di `Deserialize(&policyDataSubscription, ...)` — trovato durante l'analisi del task9; incluso come finding secondario nel solution di task9 perché co-localizzato con il bug principale

- **Wrong collName in HandleCreateSdmSubscriptions** in `UDR/api_datarepository.go:1779` — `collName := "subscriptionData.contextData.amfNon3gppAccess"` è la collection degli AMF non-3GPP context, non delle SDM subscriptions; nuovo bug non presente in ANALISI_VULNERABILITA.md — **incluso come task10_vuln_udr_collname**

- **V4 NoSQL injection surface (bare ueId, multipli handler)** in `UDR/api_datarepository.go:multipli` — già documentato in ANALISI come V4, già parzialmente coperto dall'analisi cross-NF; non trasformato in task dedicato perché richiederebbe uno snippet molto lungo e la rubrica sarebbe difficile da rendere discriminante rispetto a task8 e task6 — **scartato come task separato**

- **V5 NoSQL supis param senza validazione** in `UDR/api_datarepository.go:1153-1204` — il parametro query `supis` viene splittato e inserito in filtro $in MongoDB senza validazione; **scartato** perché il rischio reale con il driver Go+BSON è più teorico che pratico (non c'è interpolazione diretta) e la rubrica sarebbe debole

- **OneLayerPathHandlerFunc strings.Contains routing** in `UDM/api_subscriberdatamanagement.go:570` — `strings.Contains(route.Pattern, supi)` invece di uguaglianza esatta per il routing; potenziale per route confusion se supi contiene un substring del pattern — **scartato** come task perché è un routing design pattern specifico del codice UDM custom router e il rischio concreto di exploitation è limitato e richiederebbe conoscenza approfondita dei pattern di routing registrati

## Ragionamento per ogni task creato

### task5_vuln_pcf
- **Cosa ha attirato l'attenzione:** Linee 21-31 di api_oam.go: `AllowCredentials: true` e `AllowAllOrigins: true` nella stessa cors.Config struct; linee 33-38: header manuali ridondanti che ripetono la stessa misconfiguration
- **Perché è una vulnerabilità:** La spec CORS (Fetch Standard §3.2) proibisce esplicitamente `Access-Control-Allow-Origin: *` combinato con `Access-Control-Allow-Credentials: true`; qualsiasi client non-browser può fare richieste credenzializzate da qualsiasi origine verso `/am-policy/:supi`
- **Perché hai deciso di includerlo:** Vulnerabilità chiara, ben mappata a CVE (GHSA-98cp-84m9-q3qp), ottima come task baseline per testare la capacità dei modelli di riconoscere misconfiguration CORS in un contesto non-web

### task6_vuln_udr
- **Cosa ha attirato l'attenzione:** Tre handler consecutivi (righe 1208-1239) con identico pattern: `c.String(http.StatusNotFound, ...)` senza `return`; poi la regex a riga 2569 con il ramo `|.+` finale
- **Perché è una vulnerabilità:** Go non ha exception, c.String non interrompe l'esecuzione; il processor viene chiamato con subscriptionId estratto da URL che avrebbe dovuto essere rifiutato. La regex con `|.+` è logicamente equivalente a `ueId != ""` quindi non filtra nulla
- **Perché hai deciso di includerlo:** Due bug correlati ma distinti che testano la comprensione della semantica di controllo del flusso Go e della logica regex; mappati a GHSA multipli

### task7_vuln_amf
- **Cosa ha attirato l'attenzione:** Pattern `c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)` (struct) vs `c.Set(..., problemDetail.Cause)` (stringa) — inconsistenza sistemica tra handler; switch senza default in HTTPUEContextTransfer vs switch con default in HTTPCreateUEContext e HTTPN1N2MessageTransfer; `case applicationjson: err = fmt.Errorf(...)` nel handler N1N2
- **Perché è una vulnerabilità:** Il type mismatch in c.Set espone dati di errore interni al layer di metriche; missing default causa processor invocato con struct zero-value; N1N2 JSON case è una logica sempre-fallente
- **Perché hai deciso di includerlo:** Test di osservazione di inconsistenza intra-file, richiede analisi comparativa tra handler dello stesso file; le tre issues sono correlate ma distinte

### task8_vuln_udm
- **Cosa ha attirato l'attenzione:** HandleGetAmData usa `validator.IsValidSupi(supi)` (riga 40), HandleGetSmfSelectData non lo usa (riga 126), stesso pattern ripetuto per 5 altri handler — inconsistenza immediata
- **Perché è una vulnerabilità:** Violazione di TS 29.503 §6.1.3.5.2; i SUPI non validati raggiungono il layer di persistenza UDR con potenziale per probing di subscription data
- **Perché hai deciso di includerlo:** Vulnerabilità mappata a CVE (GHSA-585v-hcgf-jhfr), test di capacità del modello di rilevare inconsistenza di policy in file con molti handler

### task9_vuln_udr_policy
- **Cosa ha attirato l'attenzione:** Righe 1420-1443 (HandlePolicyDataSubsToNotifyPost) e 1453-1477 (HandlePolicyDataSubsToNotifySubsIdPut): entrambi i blocchi `if err != nil { c.JSON(...) }` non hanno `return`; nelle righe immediatamente dopo si chiama il processor. Diverso da task6 perché qui è `c.JSON` (non `c.String`) e il contesto è la creazione di subscription records
- **Perché è una vulnerabilità:** L'assenza di `return` causa doppia risposta HTTP e chiamata al processor con struct zero-value, creando subscription record vuote nel policy data store del UDR
- **Perché hai deciso di includerlo:** Pattern di missing-return non identico a task6 (diversi handler, diverso verbo HTTP, contesto policy data diverso); aggiunge il finding secondario del passaggio by-value invece di by-pointer a Deserialize; non presente in ANALISI_VULNERABILITA.md come istanza separata

### task10_vuln_udr_collname
- **Cosa ha attirato l'attenzione:** Riga 1779: `collName := "subscriptionData.contextData.amfNon3gppAccess"` dentro HandleCreateSdmSubscriptions. Subito dopo aver letto HandleCreateAmfContextNon3gpp (riga 1940): stesso collName, ma handler completamente diverso. Il nome "amfNon3gppAccess" in un handler che crea SDM subscriptions è semanticamente assurdo
- **Perché è una vulnerabilità:** Scrive documenti SdmSubscription nella collection di AmfNon3GppAccessRegistration; corrompe lo schema di quella collection e rende le SDM subscriptions irrecuperabili tramite la normale query path
- **Perché hai deciso di includerlo:** Vulnerabilità semantica (non sintattica o di flusso): il codice compila, nessun errore a runtime, il comportamento errato emerge solo nell'operazione sul DB. Testa la capacità del modello di ragionare sulla semantica delle variabili e sull'architettura dei dati UDR, non solo sulla sintassi Go

## Pattern esclusi / non inclusi come task

- **V4 (bare ueId in handler UDR multipli)**: troppo disperso nel file (decine di handler), richiederebbe snippet enorme; il rischio NoSQL via BSON string values è teorico con driver Go; coperto implicitamente dalla discussione in task8
- **V5 (supis query param senza validazione)**: il driver Go+MongoDB tratta stringhe in $in come valori scalari, non c'è interpolazione di operatori BSON; rischio reale più vicino a information leakage per enumerazione che a injection
- **HTTPCreateUEContext empty default**: tecnicamente stesso problema di HTTPUEContextTransfer (missing default), ma ha il case vuoto — distinguerlo richiederebbe spiegazioni molto sottili che renderebbero la rubrica poco discriminante; coperto implicitamente dal task7
- **OneLayerPathHandlerFunc strings.Contains**: design pattern del router custom UDM, non un handler di sicurezza standard; exploitation richiederebbe pattern di attacco molto specifici e conoscenza dell'architettura interna

## Note generali

L'analisi ha beneficiato enormemente del documento ANALISI_VULNERABILITA.md già presente nel repository: ha permesso di orientare la lettura dei file verso le sezioni critiche invece di fare una scansione lineare di ~4000 righe totali. I due finding nuovi (task9, task10) sono stati identificati leggendo il file UDR in sequenza con l'ANALISI come mappa.

Il finding più interessante da prospettiva di research è task10 (wrong collName): è un bug semantico puro che non lascia traccia sintattica, non genera errori a compile-time né a runtime, e causa data corruption silente in una collection MongoDB. Questo tipo di bug testa la comprensione dell'architettura dati dell'applicazione piuttosto che pattern Go generici — un segnale utile per discriminare modelli con conoscenza del dominio 5G da modelli che fanno pattern matching superficiale.

Il finding task9 aggiunge un'istanza di missing-return in contesto diverso da task6 (policy data vs influenceData routing): utile per testare se un modello generalizza il pattern o lo riconosce solo nel contesto specifico già visto in task6.
