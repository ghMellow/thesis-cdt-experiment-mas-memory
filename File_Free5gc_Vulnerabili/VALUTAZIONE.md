# Valutazione vulnerabilità — free5GC

## Contesto

Cartella raccolta da team di ricerca (tesi CDT). Contiene i file sorgente **pre-patch** di [free5GC](https://github.com/free5gc/free5gc), implementazione open-source del core 5G in Go. I file rappresentano le versioni vulnerabili di 4 network function: UDR, PCF, AMF, UDM.

### File presenti

| File | Network Function | Ruolo 5G |
|---|---|---|
| `UDR/api_datarepository.go` | Unified Data Repository | Strato di persistenza dei dati utente |
| `PCF/api_oam.go` | Policy Control Function | Gestione policy AM/SM |
| `AMF/api_communication.go` | Access and Mobility Function | Gestione contesti UE e trasferimento |
| `UDM/api_subscriberdatamanagement.go` | Unified Data Management | Gestione dati di sottoscrizione |

### CVE ufficiali di riferimento (da `Patch_Spiegazione.md`)

- UDR: 6 CVE — GHSA-wrwh-rpq4-87hf, GHSA-g9cw-qwhf-24jp, GHSA-x5r2-r74c-3w28, GHSA-jgq2-qv8v-5cmj, GHSA-gx38-8h33-pmxr, GHSA-jwch-w7wh-gqjm
- PCF: 1 CVE — GHSA-98cp-84m9-q3qp (CORS DoS)
- AMF: 1 CVE — GHSA-r99v-75p9-xqm5 (missing default case)
- UDM: 1 CVE — GHSA-585v-hcgf-jhfr (missing IsValidSupi)

---

## Vulnerabilità trovate

### [V1] UDR — Missing `return` dopo risposta 404 (3 handler)
**CVE:** ufficiale (parte dei 6 UDR)
**File:** `UDR/api_datarepository.go`
**Righe:** ~1212, ~1226, ~1239

**Handler coinvolti:**
- `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete`
- `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet`
- `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut`

**Pattern:**
```go
if influenceId != "subs-to-notify" {
    c.String(http.StatusNotFound, "404 page not found")
    // MANCA return
}
// il codice continua ed esegue la Procedure con dati potenzialmente errati
subscriptionId := c.Params.ByName("subscriptionId")
s.Processor().ApplicationDataInfluenceData...Procedure(c, subscriptionId)
```

**Impatto:** Il controllo di routing interno viene bypassato. Con `influenceId` arbitrario, la procedure viene comunque chiamata — comportamento indefinito sulla business logic.

---

### [V2] UDR — Missing `return` in `HandleApplicationDataInfluenceDataSubsToNotifyGet` (2 punti)
**CVE:** ufficiale (parte dei 6 UDR)
**File:** `UDR/api_datarepository.go`
**Righe:** 2779, 2790

**Punto A — errore parse snssai:**
```go
err := openapi.Deserialize(snssai, []byte(c.Query("snssai")), "application/json")
if err != nil {
    c.JSON(http.StatusBadRequest, problemDetails)
    // MANCA return → continua con snssai non valido
}
```

**Punto B — nessun parametro fornito:**
```go
if dnn == "" && snssai == nil && internalGroupId == "" && supi == "" {
    c.JSON(http.StatusBadRequest, problemDetails)
    // MANCA return → continua chiamando la Procedure con tutti i parametri vuoti
}
s.Processor().ApplicationDataInfluenceDataSubsToNotifyGetProcedure(c, dnn, snssai, internalGroupId, supi)
```

**Impatto:** Risposta 400 inviata al client ma la business logic viene eseguita ugualmente con input nulli/invalidi.

---

### [V3] UDR — Missing `return` in `HandlePolicyDataSubsToNotifyPost`
**CVE:** ufficiale (parte dei 6 UDR)
**File:** `UDR/api_datarepository.go`
**Righe:** ~1425–1442

```go
reqBody, err := c.GetRawData()
if err != nil {
    c.JSON(http.StatusInternalServerError, pd)
    // MANCA return → passa al Deserialize con reqBody nullo
}
err = openapi.Deserialize(policyDataSubscription, reqBody, "application/json")
if err != nil {
    c.JSON(http.StatusBadRequest, pd)
    // MANCA return → chiama la Procedure con oggetto zero-valued
}
s.Processor().PolicyDataSubsToNotifyPostProcedure(c, policyDataSubscription)
```

**Nota:** Stesso pattern ripetuto in `HandlePolicyDataSubsToNotifySubsIdPut` (righe ~1456–1476).

---

### [V4] UDR — Deserializzazione su valore non-puntatore (dati silenziosamente ignorati)
**CVE:** NON ufficiale — vulnerabilità aggiuntiva
**File:** `UDR/api_datarepository.go`
**Righe:** 1432, 1464

**Handler:**
- `HandlePolicyDataSubsToNotifyPost` (riga 1432)
- `HandlePolicyDataSubsToNotifySubsIdPut` (riga 1464)

```go
var policyDataSubscription models.PolicyDataSubscription
// ...
err = openapi.Deserialize(policyDataSubscription, reqBody, "application/json")
//                        ^^^
//                        valore, non &policyDataSubscription
//                        il corpo deserializzato viene scartato
```

**Impatto:** Qualsiasi contenuto inviato dal client viene ignorato. La Procedure riceve sempre un oggetto `PolicyDataSubscription` zero-valued, anche quando il client invia un body valido. Non genera errori, quindi il bug è invisibile nei log. Si tratta di un **logic bug** che rende inoperante l'endpoint anche se la richiesta è formalmente corretta.

**Fix atteso:** `openapi.Deserialize(&policyDataSubscription, reqBody, "application/json")`

---

### [V5] UDR — Controllo errore regex dopo il check di match (ordine invertito)
**CVE:** NON ufficiale — vulnerabilità aggiuntiva
**File:** `UDR/api_datarepository.go`
**Righe:** 2482–2496, 2508–2523, 2569–2585, 2601–2617

**Handler:**
- `HandleCreateEeGroupSubscriptions`
- `HandleQueryEeGroupSubscriptions`
- `HandleCreateEeSubscriptions`
- `HandleQueryeesubscriptions`

```go
match, err := regexp.MatchString("^(extgroupid-[^@]+@[^@]+|anyUE)$", ueGroupId)
if !match {
    c.JSON(http.StatusBadRequest, problemDetail)
    return
}
if err != nil {
    logger.DataRepoLog.Errorf("Invalid regular expression: %s", err)
    // solo log, nessun return, nessuna risposta di errore
}
s.Processor().CreateEeGroupSubscriptionsProcedure(c, ueGroupId, eeSubscription)
```

**Impatto:** Se la regex fosse invalida (es. per refactoring futuro), `match` sarebbe `false` e il check sembrerebbe funzionare correttamente (risponde 400) — ma l'errore interno non viene mai propagato né gestito. Il bug reale sarebbe mascherato. Attualmente la regex è costante e corretta, quindi non exploitabile direttamente.

---

### [V6] PCF — Middleware CORS cumulativo → DoS
**CVE:** ufficiale (GHSA-98cp-84m9-q3qp)
**File:** `PCF/api_oam.go`
**Righe:** 18–31

```go
func (s *Server) setCorsHeader(c *gin.Context) {
    s.router.Use(cors.New(cors.Config{ ... }))  // ← chiamato per ogni request
    // Ad ogni richiesta HTTP viene aggiunto un nuovo middleware allo stack del router
    // Lo stack cresce indefinitamente → memory exhaustion
    c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
    ...
}
```

**Impatto:** Ogni richiesta HTTP aggiunge un layer di middleware alla catena del router Gin. Con traffico sostenuto, la memoria esaurisce → DoS.

---

### [V7] PCF — CORS misconfiguration: wildcard origin + credentials
**CVE:** NON ufficiale — vulnerabilità aggiuntiva
**File:** `PCF/api_oam.go`
**Righe:** 21–31

```go
cors.Config{
    AllowCredentials: true,
    AllowAllOrigins:  true,  // ≡ Access-Control-Allow-Origin: *
}
```

**Impatto:** La specifica CORS (Fetch standard) vieta `Allow-Credentials: true` insieme a `Allow-Origin: *`. I browser moderni rifiutano la risposta. L'intenzione era probabilmente permettere richieste cross-origin con credenziali da origini specifiche — ma la configurazione è sbagliata e non funziona in modo sicuro.

---

### [V8] PCF — Doppia configurazione CORS (middleware + header manuali)
**CVE:** NON ufficiale — vulnerabilità aggiuntiva
**File:** `PCF/api_oam.go`
**Righe:** 33–38

```go
// In aggiunta al cors.New() del middleware:
c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, ...")
c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, ...")
```

**Impatto:** Duplicazione: il middleware e il codice manuale scrivono gli stessi header. L'ordine di applicazione dipende dall'implementazione di Gin, rendendo il comportamento non deterministico. Se i valori divergessero in futuro, il comportamento CORS dell'endpoint diventerebbe imprevedibile.

---

### [V9] AMF — Switch senza `default` in `HTTPUEContextTransfer`
**CVE:** ufficiale (GHSA-r99v-75p9-xqm5)
**File:** `AMF/api_communication.go`
**Righe:** 340–358

```go
switch str[0] {
case applicationjson:
    err = openapi.Deserialize(ueContextTransferRequest.JsonData, requestBody, contentType)
case multipartrelate:
    err = openapi.Deserialize(&ueContextTransferRequest, requestBody, contentType)
// nessun default
}

if err != nil { ... return }
// Con Content-Type arbitrario: err == nil, oggetto zero-valued
s.Processor().HandleUEContextTransferRequest(c, ueContextTransferRequest)
```

**Impatto:** Un client che invia un `Content-Type` non riconosciuto ottiene che la richiesta viene processata con un `UeContextTransferRequest` completamente vuoto (zero-valued). Nessun errore restituito. Comportamento indefinito nel Processor.

---

### [V10] AMF — Deserializzazione parziale in `HTTPCreateUEContext` su `applicationjson`
**CVE:** NON ufficiale — vulnerabilità aggiuntiva
**File:** `AMF/api_communication.go`
**Righe:** 193–200

```go
switch str[0] {
case applicationjson:
    err = openapi.Deserialize(createUeContextRequest.JsonData, requestBody, contentType)
    //                        ^^^ deserializza solo il sotto-campo JsonData
    //                            il campo BinaryDataN2Information viene ignorato
case multipartrelate:
    err = openapi.Deserialize(&createUeContextRequest, requestBody, contentType)
    //                        ^^^ deserializza l'oggetto completo (corretto)
default:
    err = fmt.Errorf("wrong content type")
}
```

**Impatto:** Quando il client invia `Content-Type: application/json`, solo `.JsonData` viene popolato. Se la spec 3GPP richiede anche dati nel campo `.BinaryDataN2Information`, questi vengono silenziosamente ignorati. Funzionalmente l'handler `applicationjson` è degradato rispetto a `multipartrelate`.

---

### [V11] UDM — `IsValidSupi()` mancante nel handler noto
**CVE:** ufficiale (GHSA-585v-hcgf-jhfr)
**File:** `UDM/api_subscriberdatamanagement.go`
**Riga:** contesto generale

Il CVE ufficiale documenta che `validator.IsValidSupi(supi)` è presente in `HandleGetAmData` (riga 40) ma assente negli altri handler che ricevono `:supi` come path parameter.

---

### [V12] UDM — Validazione SUPI/GPSI assente in 7+ handler
**CVE:** NON ufficiale — vulnerabilità aggiuntiva (estensione di V11)
**File:** `UDM/api_subscriberdatamanagement.go`

Mappatura completa della validazione:

| Handler | Riga | Valida SUPI/ueId? | Metodo |
|---|---|---|---|
| `HandleGetAmData` | 30 | ✅ | `IsValidSupi` |
| `HandleUnsubscribe` | 271 | ✅ | `IsValidGpsi \|\| IsValidSupi` |
| `HandleModify` | 304 | ✅ | `IsValidGpsi \|\| IsValidSupi` |
| `HandleGetIdTranslationResult` | 477 | ✅ | `IsValidGpsi \|\| IsValidSupi` |
| `HandleGetSmfSelectData` | 119 | ❌ | — |
| `HandleGetSupi` | 154 | ❌ | — |
| `HandleGetNssai` | 423 | ❌ | — |
| `HandleGetSmData` | 448 | ❌ | — |
| `HandleGetTraceData` | 398 | ❌ | — |
| `HandleGetUeContextInSmfData` | 408 | ❌ | — |
| `HandleSubscribe` | 233 | ❌ | — |

**Impatto:** 7 endpoint accettano `:supi` arbitrario (formato non conforme 3GPP, caratteri speciali, path traversal semantico) e lo passano direttamente ai layer interni (Processor → MongoDB). Il CVE ufficiale ne copre solo 1.

---

## Riepilogo

| ID | Componente | Tipo | CVE ufficiale |
|---|---|---|---|
| V1 | UDR | Missing return — 3 handler InfluenceData subs | ✅ |
| V2 | UDR | Missing return — SubsToNotifyGet (2 punti) | ✅ |
| V3 | UDR | Missing return — PolicyDataSubsToNotify (2 handler) | ✅ |
| V4 | UDR | Deserialize su valore non-puntatore → dati ignorati | ❌ |
| V5 | UDR | Ordine controllo errore regex invertito | ❌ |
| V6 | PCF | Middleware CORS cumulativo → DoS | ✅ |
| V7 | PCF | AllowAllOrigins + AllowCredentials → CORS misconfig | ❌ |
| V8 | PCF | Doppia configurazione CORS (middleware + header manuali) | ❌ |
| V9 | AMF | Switch senza default → dati zero-valued processati | ✅ |
| V10 | AMF | Deserializzazione parziale su applicationjson | ❌ |
| V11 | UDM | IsValidSupi mancante (handler noto da CVE) | ✅ |
| V12 | UDM | IsValidSupi/Gpsi mancante in 7+ altri handler | ❌ |

**CVE ufficiali coperti:** 9 (distribuiti su V1–V3, V6, V9, V11)
**Vulnerabilità aggiuntive trovate:** V4, V5, V7, V8, V10, V12
