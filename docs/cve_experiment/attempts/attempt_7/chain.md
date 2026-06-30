# Chain — Attempt #7

## File letti (in ordine)

- `File_Free5gc_Vulnerabili/AMF/api_communication.go` — letto per intero, handler per handler; cercato pattern di errori logici, gestione content-type, missing validation
- `File_Free5gc_Vulnerabili/PCF/api_oam.go` — letto per intero; file breve, un solo handler funzionale (HTTPOAMGetAmPolicy) più setCorsHeader
- `File_Free5gc_Vulnerabili/UDM/api_subscriberdatamanagement.go` — letto per intero; file lungo con routing manuale (OneLayer/TwoLayer/ThreeLayerPathHandlerFunc) e validazione SUPI/GPSI
- `File_Free5gc_Vulnerabili/UDR/api_datarepository.go` — letto in due pagine (2892 righe); file più denso, contiene la maggior parte delle vulnerabilità significative

## Candidati valutati

- **AMF: applicationjson branch unconditionally sets error in HTTPN1N2MessageTransfer** in `api_communication.go:396` — notato perché il case `applicationjson` assegna `err = fmt.Errorf(...)` invece di chiamare Deserialize, al contrario di tutti gli altri handler simili nel file — **incluso come task5**

- **AMF: missing default case in HTTPUEContextTransfer** in `api_communication.go:340-345` — notato confrontando con HTTPCreateUEContext che ha `default: err = fmt.Errorf("wrong content type")`; HTTPUEContextTransfer non ha il default, lasciando passare content-type arbitrari con err==nil — **incluso come task6**

- **UDR: pass-by-value deserialization + missing return in HandlePolicyDataSubsToNotifyPost** in `api_datarepository.go:1432,1430` — notato perché `openapi.Deserialize(policyDataSubscription, ...)` passa il valore invece del puntatore (bug semantico silenzioso), e i due blocchi if-err non hanno `return` — **incluso come task7**; HandlePolicyDataSubsToNotifySubsIdPut (riga ~1464) ha lo stesso bug identico, annotato come duplicato nel sol

- **UDR: missing return after 404 guard in influenceData handlers** in `api_datarepository.go:1212,1226,1238` — notato perché tutti e tre gli handler fanno `c.String(404,...)` senza `return`, poi eseguono comunque la procedura sul DB; il DELETE in particolare diventa una cancellazione non autorizzata — **incluso come task8**

- **PCF: CORS misconfiguration (AllowAllOrigins + AllowCredentials)** in `api_oam.go:21-32` — notato perché `AllowAllOrigins: true` e `AllowCredentials: true` sono impostati simultaneamente; per la spec CORS questo non dovrebbe funzionare con wildcard, ma alcune implementazioni lo permettono, esponendo cookie/auth a origini arbitrarie — **scartato**: il bug è reale ma è una misconfiguration di policy (non una logic error nel codice del handler); il suo impatto dipende fortemente dal deployment context e non ha una ground truth netta per un esperimento LLM. Annotato in "Pattern esclusi".

- **UDR: regex `|.+` nei validator di ueId** in `api_datarepository.go:2569-2570,2601-2602` — la regex `"^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$"` termina con `|.+` che annulla tutta la validazione — **scartato come nuovo task**: è il CVE GHSA-6gxq-gpr8-xgjp già documentato nell'ambito degli altri attempt di questo progetto; includerlo come task distinto sarebbe ridondante rispetto al focus del progetto CVE. Annotato comunque.

- **AMF: inconsistenza nel campo passato a c.Set(sbi.IN_PB_DETAILS_CTX_STR, ...)** in vari handler — alcuni passano `problemDetail` (la struct intera), altri `problemDetail.Cause` (la stringa). Non è una vulnerabilità di sicurezza ma una inconsistenza di logging/tracing. **Scartato**: impatto troppo basso e non classificabile come security issue per il task.

- **UDM: HandleGetSmfSelectData non valida SUPI** in `api_subscriberdatamanagement.go:119-141` — a differenza di HandleGetAmData (che valida con `validator.IsValidSupi(supi)`), HandleGetSmfSelectData non valida il SUPI prima di passarlo al processor. **Valutato ma scartato**: il pattern è interessante ma il file UDM non è nella lista "File_Free5gc_Vulnerabili" come sorgente primario di vulnerabilità nuove rispetto agli altri, e il task sarebbe molto simile per struttura a task5-8.

## Ragionamento per ogni task creato

### task5_vuln_amf
- **Cosa ha attirato l'attenzione:** riga 396 — `case applicationjson: err = fmt.Errorf(...)` invece di `openapi.Deserialize(...)`; tutti gli altri handler simili (HTTPCreateUEContext, HTTPUEContextTransfer) usano Deserialize nel branch JSON
- **Perché è una vulnerabilità:** ogni richiesta JSON valida è rigettata con HTTP 400 con un messaggio hardcoded fuorviante ("N1 and N2 datas are both Empty"); i caller JSON-only (es. NEF/SMF che inviano solo N2) sono silenziosamente bloccati
- **Perché ho deciso di includerlo:** è un errore logico chiaro con impatto misurabile sul piano funzionale; richiede al modello di capire il confronto con altri handler e la spec 3GPP TS 29.518

### task6_vuln_amf
- **Cosa ha attirato l'attenzione:** switch senza `default` in HTTPUEContextTransfer (righe 340-345), confrontando il codice con HTTPCreateUEContext (che ha `default: err = fmt.Errorf("wrong content type")`)
- **Perché è una vulnerabilità:** un content-type arbitrario (es. attacker-controlled) bypassa la validazione; il processor riceve una struct vuota senza che venga segnalato alcun errore
- **Perché ho deciso di includerlo:** il task chiede esplicitamente un confronto tra due handler, che è un esercizio di analisi differenziale tipico del security code review; la presenza del pattern corretto nell'handler A rende la domanda ben calibrata

### task7_vuln_udr
- **Cosa ha attirato l'attenzione:** riga 1432 — `openapi.Deserialize(policyDataSubscription, ...)` senza `&`; e assenza di `return` dopo i blocchi di errore (righe 1428-1430, 1433-1438)
- **Perché è una vulnerabilità:** due bug distinti con effetti diversi — il pass-by-value è un silent data loss; il missing return è un double-response + chiamata al processor su dati garbage
- **Perché ho deciso di includerlo:** è il task più difficile del set — richiede conoscenza del modello a memoria di Go (value vs pointer semantics) e comprensione del flow control; mette alla prova se il modello distingue i due bug

### task8_vuln_udr
- **Cosa ha attirato l'attenzione:** pattern ripetuto tre volte in `api_datarepository.go:1212-1218,1226-1232,1238-1276` — `c.String(http.StatusNotFound, "404 page not found")` senza `return`
- **Perché è una vulnerabilità:** la guard non blocca l'esecuzione; il caso peggiore è la procedura DELETE che cancella dati reali dopo aver già inviato una 404 al caller
- **Perché ho deciso di includerlo:** il pattern "missing return after early response" è comune e ad alto impatto; avere tre istanze identiche nello stesso file rende il task più interessante (il modello deve capire che il bug è sistematico, non isolato)

## Pattern esclusi / non inclusi come task

- **PCF CORS misconfiguration** (`api_oam.go:21-32`): `AllowAllOrigins: true` + `AllowCredentials: true` simultaneamente. È un problema reale ma la ground truth dipende dal contesto di deployment e dalla versione del browser/lib usata. Non produce un errore deterministico analizzabile dal judge senza conoscenza dell'ambiente.
- **UDR CVE regex `|.+`** (`api_datarepository.go:2569,2601`): La regex usata per validare ueId nei handler EE subscription contiene `|.+` come ultima alternativa, annullando ogni filtro. È il pattern CVE GHSA-6gxq-gpr8-xgjp già oggetto degli attempt 1-6 di questo progetto. Non incluso per evitare ridondanza interna al progetto.
- **UDR HandleApplicationDataInfluenceDataSubsToNotifyGet e Post senza return su snssai error** (`api_datarepository.go:2780-2791`): Nella funzione HandleApplicationDataInfluenceDataSubsToNotifyGet, gli errori di Deserialize e la validazione parametri non fanno return. Simile al pattern task8 ma meno severo; scartato per non sovraccaricare il task set con varianti dello stesso pattern.
- **AMF/UDR inconsistenza IN_PB_DETAILS_CTX_STR**: alcuni handler passano la struct ProblemDetails intera, altri solo il campo Cause. Non è una vulnerabilità di sicurezza ma un bug di logging/metrics che potrebbe causare panic in downstream se il consumer si aspetta solo string. Scartato per impatto troppo basso.

## Note generali

L'analisi è stata condotta senza bias verso pattern noti: ho letto ogni handler intero prima di classificarlo. I bug più interessanti sono stati trovati per contrasto (confrontando handler simili nello stesso file) piuttosto che per pattern matching su vulnerabilità note. Il file UDR è di gran lunga il più ricco di anomalie, probabilmente perché è il più lungo e il più eterogeneo nella struttura degli handler (mix di helper function e inline handling).

La scelta di escludere il CVE regex è stata deliberata: il progetto ha già un flusso dedicato (cve-attempt) per quel pattern e includerlo come task darebbe un vantaggio non controllato ai modelli che hanno già visto quel contesto nelle sessioni precedenti.
