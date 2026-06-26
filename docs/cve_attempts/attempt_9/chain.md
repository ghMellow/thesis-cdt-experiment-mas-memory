# Chain — Attempt #9

## File letti (in ordine)

- `File_Free5gc_Vulnerabili/Patch_Spiegazione.md` — riferimenti CVE per NF: 6 CVE UDR (return mancanti), 1 CVE PCF (CORS DoS), 1 CVE AMF (no default case), 1 CVE UDM (missing IsValidSupi)
- `File_Free5gc_Vulnerabili/PCF/api_oam.go` — letto per primo perché più piccolo; trovato subito il CORS misconfiguration con `AllowAllOrigins: true` + `AllowCredentials: true` + header manuali ridondanti `Access-Control-Allow-Origin: *`
- `File_Free5gc_Vulnerabili/AMF/api_communication.go` — letto integralmente; identificato pattern switch Content-Type senza `default` in `HTTPUEContextTransfer` (righe 340-345); notata anche l'inconsistenza `c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)` vs `.Cause` in 5 handler
- `File_Free5gc_Vulnerabili/UDM/api_subscriberdatamanagement.go` — letto integralmente; identificato `HandleGetSmfSelectData`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetSupi` che non chiamano `validator.IsValidSupi(supi)` mentre `HandleGetAmData` lo fa correttamente (riga 40)
- `File_Free5gc_Vulnerabili/UDR/api_datarepository.go` — letto in due passate (file molto lungo, 2892 righe); identificati i `return` mancanti dopo `c.String(http.StatusNotFound, ...)` in `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete/Get/Put` (righe 1212-1219, 1226-1232, 1239-1240); identificata la regex `|.+` in `HandleCreateEeSubscriptions` e `HandleQueryeesubscriptions` che rende l'intera validazione banalmente vera

## Candidati valutati (tutti, inclusi scartati)

- **`AllowAllOrigins: true` + `AllowCredentials: true`** in `PCF/api_oam.go:21-38` — combinazione vietata dalla specifica CORS (Fetch Standard §3.2); header manuali ridondanti aggravano il problema — **incluso come task5_vuln_pcf**
- **Switch Content-Type senza `default`** in `AMF/api_communication.go:340-345` (`HTTPUEContextTransfer`) — err rimane nil per Content-Type arbitrario, il processor viene chiamato con `JsonData` non inizializzato — **incluso come task7_vuln_amf** (note: l'AMF è stato numerato task7 per lasciare task6 all'UDR che ha più findings)
- **`return` mancante dopo `c.String(404)`** in `UDR/api_datarepository.go:1212, 1226, 1239` — 3 handler (`Delete/Get/Put` per `subs-to-notify`) continuano l'esecuzione verso il processor anche dopo aver scritto un 404; double-write HTTP + processor chiamato su path rigettato — **incluso come task6_vuln_udr**
- **Regex `|.+` in fine alternativa** in `UDR/api_datarepository.go:1172, 1201` (`HandleCreateEeSubscriptions`, `HandleQueryeesubscriptions`) — l'alternativa finale `|.+` rende la regex trivialmente vera per qualsiasi stringa non-vuota, bypassando l'intera validazione — **incluso come finding secondario in task6_vuln_udr_sol**
- **`c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)` invece di `.Cause`** in `AMF/api_communication.go` — 5 handler passano l'intero struct invece della stringa `.Cause`; potenziale type-assertion panic nel middleware SBI metrics — **incluso come finding secondario in task7_vuln_amf_sol**
- **Mancanza di `validator.IsValidSupi()` in handler UDM** in `UDM/api_subscriberdatamanagement.go:126, 163, 432, 401, 409` — `HandleGetSmfSelectData`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData` non validano il SUPI mentre `HandleGetAmData` lo fa — scartato come task primario: sarebbe stato task8 ma il limite era 3 task; la CVE è reale (GHSA-585v-hcgf-jhfr) ma meno spettacolare come challenge educativa rispetto agli altri tre
- **`HandlePolicyDataSubsToNotifyPost` e `SubsIdPut` in UDR senza `return`** (righe 1421-1442, 1453-1477) — notata assenza di `return` dopo i blocchi di errore; scartata come task separato: già coperta dalla family di finding "missing return" del task6, e il limite era 3 task

## Ragionamento per ogni task creato

### task5_vuln_pcf

- **Cosa ha attirato l'attenzione:** riga 29 `AllowAllOrigins: true` in `cors.Config{}` insieme a riga 30 `AllowCredentials: true`; poi righe 33-38 che impostano manualmente `Access-Control-Allow-Origin: *` e `Access-Control-Allow-Credentials: true` — duplicazione sospetta
- **Perché è grave:** La specifica CORS vieta esplicitamente la combinazione wildcard-origin + credenziali. Un client non-browser (altri NF, strumenti di attacco) può fare richieste credenzializzate cross-origin verso `/am-policy/:supi` per leggere o esaurire policy data di UE arbitrari. In un 5G core dove il PCF è accessibile da segmenti di gestione più ampi, questo è un vettore DoS e data-exposure diretto sull'AM Policy di ogni UE nel sistema.

### task6_vuln_udr

- **Cosa ha attirato l'attenzione:** riga 1212 in `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete`: `c.String(http.StatusNotFound, "404 page not found")` senza `return` immediatamente dopo; pattern ripetuto identico righe 1226 e 1239 nei due handler paralleli
- **Perché è grave:** In Go/Gin, `c.String()` scrive il body HTTP ma non interrompe l'esecuzione della funzione. Il codice successivo (estrazione `subscriptionId` e chiamata al processor) viene eseguito comunque, causando: (1) double-write sul wire, comportamento indefinito lato client; (2) il processor UDR riceve e processa un `subscriptionId` arbitrario su un URL che avrebbe dovuto essere rigettato — bypass dell'access control sulla collection `applicationData.influenceData.subs-to-notify`. La regex `|.+` in `HandleCreateEeSubscriptions` è il secondo finding: rende la validazione del `ueId` equivalente a un semplice check non-empty, permettendo a qualsiasi stringa di raggiungere il layer MongoDB.

### task7_vuln_amf

- **Cosa ha attirato l'attenzione:** righe 340-345 in `HTTPUEContextTransfer`: switch con soli due case e nessun `default`; confronto immediato con `HTTPCreateUEContext` (righe 193-200) che ha `default: err = fmt.Errorf("wrong content type")` — la differenza è il punto critico
- **Perché è grave:** Con un Content-Type arbitrario (es. `text/plain`), entrambe le branch del switch vengono saltate, `err` rimane `nil`, e il blocco `if err != nil` non scatta. Il processor AMF viene chiamato con `ueContextTransferRequest.JsonData` che è un struct allocato vuoto (`new(models.UeContextTransferReqData)`) ma mai popolato. Questo può causare nil-dereference o panic nel processor, oppure portare l'AMF a processare un trasferimento di contesto UE con dati vuoti — operazione critica in una procedura di handover 5G. Ripetibile come vettore DoS.

## Pattern esclusi

- **UDM — missing `IsValidSupi()` in 5+ handler** (`HandleGetSmfSelectData`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetSupi`): CVE reale (GHSA-585v-hcgf-jhfr), ma scartato per rispettare il limite di 3 task. La vulnerabilità consiste nell'assenza di chiamata a `validator.IsValidSupi(supi)` prima di passare il SUPI al processor, mentre `HandleGetAmData` lo fa correttamente. Incluso in task8_vuln_udm (già esistente sul branch da attempt precedente).
- **UDR — `HandlePolicyDataSubsToNotifyPost` e `HandlePolicyDataSubsToNotifySubsIdPut` senza `return`** (righe 1430, 1438, 1462, 1470): stesso pattern "missing return" del finding primario di task6, ma su una coppia diversa di handler (policy data subscriptions anziché influence data). Non incluso come task separato per evitare duplicazione didattica e rispettare il limite di 3 task.
- **AMF — `c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)` struct invece di `.Cause`**: incluso come finding secondario in task7_vuln_amf_sol ma non come task autonomo — troppo sottile come challenge educativa da sola, più utile come secondo finding nello stesso task.
