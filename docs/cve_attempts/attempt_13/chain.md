# Chain — Attempt #13

## File letti (in ordine)

- `File_Free5gc_Vulnerabili/Patch_Spiegazione.md` — lista sintetica dei CVE per NF: UDR (6 CVE, return mancanti), PCF (1 CVE CORS DoS), AMF (1 CVE, no default case), UDM (1 CVE, missing IsValidSupi). Ha orientato la lettura verso i pattern specifici per NF.
- `File_Free5gc_Vulnerabili/AMF/api_communication.go` — letto per intero. Confronto immediato tra `HTTPCreateUEContext` (ha `default:`) e `HTTPUEContextTransfer` (non ce l'ha). Nessuna regex interna.
- `File_Free5gc_Vulnerabili/PCF/api_oam.go` — file breve. CORS middleware con `AllowAllOrigins: true` + `AllowCredentials: true`, doppiato da header manuali con `*` e `true`. Combinazione esplicitamente vietata dalla specifica CORS.
- `File_Free5gc_Vulnerabili/UDM/api_subscriberdatamanagement.go` — letto per intero. Usa `validator.IsValidSupi` e `validator.IsValidGpsi` correttamente nei punti documentati dal CVE. Nessuna regex vulnerabile interna visibile nel file stesso.
- `File_Free5gc_Vulnerabili/UDR/api_datarepository.go` — file da 2892 righe, letto in due pagine. A riga 2563-2570 e 2595-2602: regex `|.+` catch-all in `HandleCreateEeSubscriptions` e `HandleQueryeesubscriptions`. A riga 2482 e 2508: regex `ueGroupId` con pattern corretto (no catch-all). A riga 1421-1442 e 1453-1476: `HandlePolicyDataSubsToNotifyPost` e `HandlePolicyDataSubsToNotifySubsIdPut` chiamano `openapi.Deserialize` passando `policyDataSubscription` by value invece che by pointer — possibile bug di correttezza, non incluso come task principale.

---

## Candidati valutati (tutti, inclusi quelli scartati)

- **`|.+` catch-all** in `UDR/api_datarepository.go:2570` e `:2602` — regex alternation termina con `.+` che matcha qualsiasi stringa non vuota, rendendo la validazione sempre vera — **incluso come task5**
- **Missing `default:` in switch Content-Type** in `AMF/api_communication.go:340-345` (funzione `HTTPUEContextTransfer`) — identico pattern a `HTTPCreateUEContext` che ha il default — **incluso come task6**
- **CORS `AllowAllOrigins + AllowCredentials`** in `PCF/api_oam.go:21-38` — combinazione vietata dalla specifica + header manuali ridondanti che forzano `*` + `true` — **incluso come task7**
- **`openapi.Deserialize` by value** in `UDR/api_datarepository.go:1432` e `1464` (`HandlePolicyDataSubsToNotifyPost`, `HandlePolicyDataSubsToNotifySubsIdPut`) — `policyDataSubscription` passata non come pointer, la deserializzazione non aggiorna la variabile locale — bug di correttezza ma non direttamente un vulnerability di sicurezza sfruttabile dall'esterno senza ulteriore analisi del comportamento del processor — **scartato** (limite 3 task)
- **`HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete/Get` missing `return`** in `UDR/api_datarepository.go:1212-1218` — dopo `c.String(http.StatusNotFound, ...)` non c'è `return`, la funzione continua — candidato plausibile ma richiede lettura più approfondita del flusso successivo; scartato per il limite di 3 task
- **Regex `ueGroupId`** in `UDR/api_datarepository.go:2482` e `2508` — pattern `^(extgroupid-[^@]+@[^@]+|anyUE)$` senza catch-all, corretto — **scartato** (non vulnerabile)
- **UDM `HandleGetSmfSelectData`, `HandleGetSupi`, etc. senza validazione SUPI** — solo `HandleGetAmData` valida con `IsValidSupi`; altri handler leggono `supi` senza validarlo — potenziale problema di validazione inconsistente; non incluso perché richiederebbe conoscenza della specifica 3GPP per formulare una rubrica di valutazione precisa e il limite di task era 3

---

## Ragionamento per ogni task creato

### task5_vuln_udr
- **Cosa ha attirato l'attenzione:** riga 2563 ha un commento che riporta il pattern spec (`Pattern: "^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$"`), poi la riga 2570 usa esattamente quella stringa. L'ultima alternativa `|.+` è identica alla CVE GHSA-6gxq-gpr8-xgjp nota.
- **Perché è un problema di sicurezza:** la regex è intesa come whitelist dei formati SUPI/GPSI validi, ma la presenza di `|.+` in ultima posizione fa sì che qualsiasi stringa non vuota corrisponda. Il controllo `if !match` non viene mai raggiunto per input arbitrari (tranne la stringa vuota, già esclusa dal check precedente). L'attaccante può iniettare qualsiasi `ueId` nelle query MongoDB a valle, bypassando completamente la validazione.

### task6_vuln_amf
- **Cosa ha attirato l'attenzione:** leggendo sequenzialmente le funzioni nel file, `HTTPCreateUEContext` (riga ~193) ha `default: err = fmt.Errorf("wrong content type")`. La funzione analoga `HTTPUEContextTransfer` (riga ~340) ha lo stesso `switch` ma senza `default:`. La differenza è visibile a confronto diretto.
- **Perché è un problema di sicurezza:** senza `default:`, un `Content-Type` inatteso lascia `err == nil` e nessuna deserializzazione avvenuta. Il processor riceve una struct vuota (zero-value) senza che l'errore venga notificato al client o al sistema. Può causare comportamenti imprevedibili nel trasferimento di contesto UE, potenziali nil-pointer e DoS.

### task7_vuln_pcf
- **Cosa ha attirato l'attenzione:** `AllowAllOrigins: true` e `AllowCredentials: true` nella stessa struct cors.Config, seguiti da header manuali che impostano `Access-Control-Allow-Origin: *` e `Access-Control-Allow-Credentials: true` direttamente sulla risposta.
- **Perché è un problema di sicurezza:** la specifica CORS vieta esplicitamente la combinazione wildcard-origin + credentials. Alcuni middleware (incluse versioni precedenti di gin-contrib/cors) aggirano il problema riflettendo l'Origin del client, rendendo di fatto qualsiasi origine autorizzata con credenziali. I header manuali ridondanti aggravano il problema forzando sempre `*` + `true`. In un contesto di gestione OAM del PCF, un attaccante può exfiltrare dati di policy per-subscriber o eseguire azioni privilegiate tramite CSRF da un browser operatore.

---

## Pattern esclusi

- **`openapi.Deserialize` by value in `HandlePolicyDataSubsToNotifyPost/SubsIdPut`** (UDR:1432, 1464): bug funzionale che causa la deserializzazione su una copia locale non osservabile dal caller; non costituisce di per sé una vulnerabilità di sicurezza sfruttabile direttamente, ma potrebbe portare a comportamenti nulli silenziosi. Scartato per priorità.
- **Missing `return` dopo `c.String(http.StatusNotFound, ...)` in `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete/Get`** (UDR:1212-1218): senza `return` la funzione continua con `subscriptionId` anche quando `influenceId != "subs-to-notify"`. Potenzialmente un bug di logica (risposta 404 ma elaborazione continuata), scartato perché il terzo slot task era già occupato da PCF CORS.
- **Validazione SUPI assente su molti handler UDM** (es. `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`): solo `HandleGetAmData` chiama `validator.IsValidSupi`; gli altri handler passano `supi` non validato al processor. Omesso perché richiederebbe una rubrica basata sulla specifica TS 29.503, e il limite di 3 task era raggiunto.

---

## Note generali

- Il file UDR (`api_datarepository.go`, 2892 righe) conteneva il maggior numero di pattern interessanti. La ricerca con grep per `regexp` e `MatchString` ha permesso di localizzare rapidamente le righe rilevanti senza leggere l'intero file.
- La CVE GHSA-6gxq-gpr8-xgjp (`|.+`) era visibile immediatamente una volta cercato il pattern `regexp.MatchString` nel file UDR. Il commento con il pattern spec alla riga precedente ha reso ancora più evidente il contrasto tra l'intenzione dichiarata e l'implementazione effettiva.
- La distinzione tra la regex `ueGroupId` (corretta, senza catch-all) e la regex `ueId` (vulnerabile, con `|.+`) è un buon elemento discriminante per testare se un agente capisce realmente la struttura delle alternation regex o si limita a pattern-matching superficiale.
- Il task AMF richiede una capacità di confronto contestuale (due versioni della stessa struttura nello stesso file) piuttosto che solo riconoscimento di un pattern isolato.
