# Analisi Vulnerabilità — free5GC SBI Handlers

> ⚠️ **Provenienza:** documento scritto da Claude durante la primissima sessione di analisi del corpus free5GC (non `CVE_CVSS.md`/`Patch_Spiegazione.md`/`Correzzione_Esperto.md`, quelli sono i dati grezzi ricevuti dal relatore/esperto). Non è materiale ricevuto direttamente — trattarlo come elaborazione, non come ground truth primaria.
>
> Documento vivo. Sezione 1–3: analisi statica manuale. Sezione 4: piano sperimentale per testare il judge LLM.

---

## 1) Perimetro del corpus

| File | NF | Righe |
|---|---|---|
| `AMF/api_communication.go` | Access & Mobility Management Function | 501 |
| `PCF/api_oam.go` | Policy Control Function — OAM endpoint | 65 |
| `UDM/api_subscriberdatamanagement.go` | Unified Data Management | 859 |
| `UDR/api_datarepository.go` | Unified Data Repository | 2891 |

Tutti i file sono handler HTTP scritti in Go con il framework Gin, esposti come SBI (Service-Based Interface) tra NF nel core 5G.

---

## 2) Vulnerabilità identificate (analisi statica manuale)

### V1 — CORS Misconfiguration critica (PCF)

**File:** `PCF/api_oam.go`  
**Righe:** 18–38  
**CWE:** CWE-942 (Permissive Cross-domain Policy with Untrusted Domains)  
**Severità:** Alta

**Descrizione:**  
La funzione `setCorsHeader` configura il middleware CORS con due opzioni incompatibili che insieme creano una vulnerabilità:

```go
cors.New(cors.Config{
    AllowCredentials: true,
    AllowAllOrigins:  true,   // ← imposta Access-Control-Allow-Origin: *
    ...
})
// + manual header:
c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
```

Per la specifica CORS (RFC 6454 / Fetch Standard), `Access-Control-Allow-Credentials: true` è incompatibile con `Access-Control-Allow-Origin: *`. I browser rifiuterebbero la risposta ma un client custom (o un proxy) non ha questa limitazione. In ambiente 5G core il problema è che qualsiasi servizio interno o esterno che effettua richieste credenzializzate all'endpoint OAM del PCF bypassa di fatto il controllo di origine.

**Impatto:** Un attaccante con accesso alla rete del core può eseguire richieste cross-origin credenzializzate verso `/am-policy/:supi` senza restrizioni di origine.

**Riferimento patch:** rimuovere `AllowAllOrigins: true` e sostituire con una whitelist esplicita di origini autorizzate; eliminare gli header manuali ridondanti.

---

### V2 — Missing `return` dopo risposta 404 (UDR)

**File:** `UDR/api_datarepository.go`  
**Righe:** 1208–1239  
**CWE:** CWE-670 (Always-Incorrect Control Flow Implementation)  
**Severità:** Media-Alta

**Descrizione:**  
Tre handler — `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete`, `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet`, `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut` — condividono lo stesso pattern difettoso:

```go
influenceId := c.Param("influenceId")
if influenceId != "subs-to-notify" {
    c.String(http.StatusNotFound, "404 page not found")
    // ← MANCA return
}
// esecuzione continua con subscriptionId arbitrario
subscriptionId := c.Params.ByName("subscriptionId")
s.Processor().ApplicationDataInfluenceDataSubsToNotify...Procedure(c, subscriptionId)
```

In Gin, `c.String(...)` scrive la risposta ma **non interrompe il flusso**. Quando `influenceId != "subs-to-notify"`, il codice invia un 404 e poi esegue comunque la chiamata al processor. Il risultato è che:
1. La risposta HTTP diventa undefined (doppio write);
2. Il processor viene chiamato con un `subscriptionId` potenzialmente arbitrario estratto da un URL che avrebbe dovuto essere rifiutato.

**Impatto:** Bypass del controllo di routing — operazioni DELETE/GET/PUT su subscription ID arbitrari su un path che non dovrebbe accettarli.

**Riferimento patch:** aggiungere `return` dopo ogni `c.String(http.StatusNotFound, ...)`.

---

### V3 — Regex di validazione inefficace (UDR)

**File:** `UDR/api_datarepository.go`  
**Righe:** 2569–2570, 2601–2602  
**CWE:** CWE-20 (Improper Input Validation)  
**Severità:** Media

**Descrizione:**  
Due handler (`HandleCreateEeSubscriptions`, `HandleQueryeesubscriptions`) tentano di validare il formato `ueId` con una regex che replica il pattern 3GPP:

```go
match, err := regexp.MatchString(
    "^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$", ueId)
```

Il problema è nel ramo finale **`|.+`**: essendo la disgiunzione OR valutata nell'ordine, il ramo `.+` fa sì che qualsiasi stringa non-vuota corrisponda al pattern. La validazione è quindi equivalente al semplice check `ueId != ""` già presente per gli altri handler, rendendo il regex completamente inutile.

Nota aggiuntiva: la logica di controllo errore è invertita — `err` viene controllato *dopo* il `return` su `!match` (righe 2495–2497, 2521–2523, 2583–2585, 2615–2617). Se il regex fallisse in compilazione (impossibile con stringa statica), l'errore sarebbe silenziosamente ignorato nella maggior parte dei casi.

**Impatto:** Input arbitrari come `"../../anything"`, `"{$gt:''}"` o stringhe con caratteri speciali MongoDB passano la validazione e raggiungono il layer di persistenza.

**Riferimento patch:** rimuovere il ramo `|.+` dalla regex; la corretta alternativa finale per "any other valid format" va definita esplicitamente o gestita con un validator dedicato come in UDM (`validator.IsValidSupi`).

---

### V4 — Assenza di validazione formato `ueId` in UDR (NoSQL Injection surface)

**File:** `UDR/api_datarepository.go`  
**Righe:** multipli (843, 863, 907, 950, 963, 978, 1023, 1037, 1081, 1095, 1139, 1544, 1570, ...)  
**CWE:** CWE-943 (Improper Neutralization of Special Elements in Data Query Logic)  
**Severità:** Media-Alta

**Descrizione:**  
La grande maggioranza degli handler UDR (decine di funzioni `HandleQuery*`, `HandleCreate*`, `HandleModify*`) esegue solo il controllo `ueId == ""` prima di passare il valore a MongoDB:

```go
ueId := c.Params.ByName("ueId")
if ueId == "" {
    util.EmptyUeIdProblemJson(c)
    return
}
// ueId non validato → passa a BSON filter
filter := bson.M{"ueId": ueId}
s.Processor().QueryAmfContext3gppProcedure(c, collName, ueId)
```

In UDM (stesso progetto), la stessa informazione viene invece validata:
```go
supi := c.Params.ByName("supi")
if !validator.IsValidSupi(supi) { ... return }
```

In MongoDB con il driver Go, i path parameter sono trattati come valori stringa nel filtro BSON — non c'è interpolazione diretta come in SQL. Tuttavia, l'assenza di validazione:
1. Permette `ueId` con caratteri speciali o encoding anomali che potrebbero interferire con operatori del Processor layer;
2. Amplia la superficie per eventuali query injection se il Processor costruisce filtri più complessi concatenando il `ueId` grezzo;
3. Viola la spec 3GPP (TS 29.503) che richiede che SUPI e GPSI abbiano formato validato.

**Impatto:** Inconsistenza di sicurezza rispetto a UDM (stessa codebase), potenziale data leakage su collezioni MongoDB se il ueId è usato per costruire query più articolate.

---

### V5 — NoSQL Injection via query parameter `supis` (UDR)

**File:** `UDR/api_datarepository.go`  
**Righe:** 1153–1204 (`HandleApplicationDataInfluenceDataGet`)  
**CWE:** CWE-943  
**Severità:** Media

**Descrizione:**  
Il parametro query `supis` viene splittato e inserito direttamente in un filtro `$in` di MongoDB senza alcuna validazione:

```go
supisParam := c.QueryArray("supis")
// ...
if len(supisParam) != 0 {
    supis := strings.Split(supisParam[0], ",")
    withAnyUeIndFilter := []bson.M{
        {"supi": bson.M{"$in": supis}},
        {"interGroupId": "AnyUE"},
    }
    filter = append(filter, bson.M{"$or": withAnyUeIndFilter})
}
```

Ogni elemento della slice `supis` è una stringa grezza non sanitizzata. Sebbene Go+MongoDB driver non permettano di iniettare operatori BSON tramite semplici stringhe nel filtro `$in`, una lista arbitraria di SUPI può:
1. Causare port scanning / data enumeration senza restrizione;
2. Se il driver è configurato con query libere, ampliare la superficie verso injection di tipo documento.

**Impatto:** Enumerazione non autorizzata di dati di subscription associati a SUPI arbitrari.

---

### V6 — Inconsistenza nel campo `IN_PB_DETAILS_CTX_STR` (AMF — Information Exposure)

**File:** `AMF/api_communication.go`  
**Righe:** 185–186, 229–230, 264–265, 298–299, 383–384  
**CWE:** CWE-209 (Generation of Error Message Containing Sensitive Information)  
**Severità:** Bassa-Media

**Descrizione:**  
In cinque handler (`HTTPCreateUEContext`, `HTTPEBIAssignment`, `HTTPRegistrationStatusUpdate`, `HTTPReleaseUEContext`, `HTTPN1N2MessageTransfer`) il contesto Gin viene impostato con la **struct completa** `problemDetail` invece del solo campo stringa atteso:

```go
// Comportamento errato (questi 5 handler):
c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)   // ← struct intera

// Comportamento corretto (altri handler nello stesso file):
c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)  // ← stringa
```

Il contesto `IN_PB_DETAILS_CTX_STR` è utilizzato dal middleware di metriche SBI. Passare la struct completa (che include `Detail: err.Error()`) espone al layer di metriche/log il messaggio di errore interno del sistema, che può contenere stack trace, nomi di file o informazioni di configurazione interna.

**Impatto:** Information disclosure nei log/metriche interni; riduzione dell'osservabilità per i tool di monitoring che si aspettano una stringa.

---

### V7 — Missing `default` nel switch Content-Type (AMF)

**File:** `AMF/api_communication.go`  
**Righe:** 339–358 (`HTTPUEContextTransfer`)  
**CWE:** CWE-392 (Missing Report of Error Condition)  
**Severità:** Bassa-Media

**Descrizione:**  
Nel handler `HTTPUEContextTransfer`, lo switch sul Content-Type non ha un caso `default`:

```go
switch str[0] {
case applicationjson:
    err = openapi.Deserialize(ueContextTransferRequest.JsonData, requestBody, contentType)
case multipartrelate:
    err = openapi.Deserialize(&ueContextTransferRequest, requestBody, contentType)
// ← nessun default: err rimane nil
}

if err != nil {
    // questo blocco non viene mai raggiunto con Content-Type sconosciuto
    ...
    return
}
s.Processor().HandleUEContextTransferRequest(c, ueContextTransferRequest)
```

Con un Content-Type arbitrario, `err` rimane `nil`, il corpo HTTP non viene mai deserializzato, e il Processor viene chiamato con `ueContextTransferRequest` parzialmente inizializzato (`JsonData` è `new(models.UeContextTransferReqData)` ma il body è vuoto). Confronta con `HTTPCreateUEContext` (stessa logica ma ha `default: err = fmt.Errorf("wrong content type")`).

**Impatto:** Il Processor riceve un oggetto vuoto che potrebbe causare panic, comportamento indefinito o dati di contesto UE corrotti.

---

### V8 — Missing `validator.IsValidSupi()` in UDM per handler multipli

**File:** `UDM/api_subscriberdatamanagement.go`  
**Righe:** 119–140, 398–404, 407–414, 422–444, 447–473, 153–177  
**CWE:** CWE-20 (Improper Input Validation)  
**CVE:** GHSA-585v-hcgf-jhfr  
**Severità:** Media

**Descrizione:**  
Alcuni handler in UDM implementano correttamente la validazione SUPI/GPSI (es. `HandleGetAmData` righe 39–51 usa `validator.IsValidSupi(supi)`), mentre altri handler nella stessa funzione omettono la validazione e passano `supi` direttamente al processor:

```go
// Handler con validazione (corretto):
func (s *Server) HandleGetAmData(c *gin.Context) {
    supi := c.Params.ByName("supi")
    if !validator.IsValidSupi(supi) { ... return }
    ...
}

// Handler senza validazione (vulnerabile):
func (s *Server) HandleGetSmfSelectData(c *gin.Context) {
    supi := c.Params.ByName("supi")
    // ← nessuna validazione formato
    s.Processor().GetSmfSelectDataProcedure(c, supi, plmnID, supportedFeatures)
}
```

Gli handler mancanti di validazione includono: `HandleGetSmfSelectData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetSupi`.

**Impatto:** SUPI con formato non valido (o contenenti caratteri speciali) raggiungono il layer di persistenza senza essere filtrati, con la stessa superficie di rischio di V4 in UDR.

---

## 3) Riepilogo, priorità e mapping CVE

| ID | NF | File | Righe | Categoria | Severità | CVE/GHSA |
| --- | --- | --- | --- | --- | --- | --- |
| V1 | PCF | `api_oam.go` | 18–38 | CORS Misconfiguration / DoS | **Alta** | GHSA-98cp-84m9-q3qp |
| V2 | UDR | `api_datarepository.go` | 1208–1239 (+5 analoghi) | Missing return / Control Flow | **Media-Alta** | GHSA-wrwh, GHSA-g9cw, GHSA-x5r2, GHSA-jgq2, GHSA-gx38, GHSA-jwch |
| V4 | UDR | `api_datarepository.go` | multipli | Input Validation / NoSQL surface | **Media-Alta** | (incluso nella superficie V2/V3) |
| V8 | UDM | `api_subscriberdatamanagement.go` | multipli | Missing SUPI Validator | **Media** | GHSA-585v-hcgf-jhfr |
| V3 | UDR | `api_datarepository.go` | 2569–2602 | Ineffective Regex Validation | **Media** | — (non mappato a CVE specifico) |
| V5 | UDR | `api_datarepository.go` | 1153–1204 | NoSQL Injection surface (query params) | **Media** | — (non mappato a CVE specifico) |
| V7 | AMF | `api_communication.go` | 339–358 | Missing default case / error condition | **Bassa-Media** | GHSA-r99v-75p9-xqm5 |
| V6 | AMF | `api_communication.go` | 185–384 | Information Exposure (struct leak) | **Bassa-Media** | — (non mappato a CVE specifico) |

**Note sul mapping:**

- V2 corrisponde a **6 GHSA distinti** — Francesco ha probabilmente identificato 6 istanze separate del pattern missing-return nel codice UDR (il corpus ha almeno 3 istanze visibili nel snippet esaminato + altre nel resto del file da 2891 righe).
- V3 e V6 sono stati identificati dall'analisi manuale ma non risultano nei CVE ufficiali — o perché considerati di severità insufficiente per un advisory, o perché il fix è implicito nelle patch di V2/V4.
- V5 (NoSQL via query params) potrebbe essere coperto dal CVE UDR ma non è esplicitato.

---

## 4) Piano sperimentale: testare il judge LLM

### 4.1 Domanda di ricerca

> Un LLM (con ruolo `expert` o `beginner`) riesce a identificare le vulnerabilità reali in codice Go di NF 5G? Con quale precisione, profondità e consistenza tra ripetizioni?

Questo estende il framework esistente (task3/task4 su anomalie 5G) a un dominio **code security review**.

### 4.2 Struttura proposta dei task

Ogni vulnerabilità (o gruppo di vulnerabilità correlate) diventa un **task testuale** con:

- **Scenario** (`docs/tasks/taskX_vuln_<nf>.md`): il codice Go (snippet rilevante) + contesto minimo dell'architettura 5G SBI
- **Soluzione** (`docs/tasks/taskX_vuln_<nf>_sol.md`): ground truth (descrizione della vulnerabilità) + rubrica per il judge

| Task proposto | Contenuto | Vulnerabilità target |
|---|---|---|
| `task5_vuln_pcf` | Snippet `setCorsHeader` da PCF | V1 (CORS) |
| `task6_vuln_udr_return` | Snippet 3 handler con missing return | V2 |
| `task7_vuln_udr_regex` | Snippet regex + confronto con UDM validator | V3 + V4 |
| `task8_vuln_amf` | Snippet switch + c.Set inconsistente | V6 + V7 |

### 4.3 Design della rubrica (esempio per task5_vuln_pcf)

```json
{
  "rubrica": {
    "vuln_identified": {
      "max": 3,
      "criteri": {
        "0": "Non identifica nessuna vulnerabilità CORS",
        "1": "Identifica che AllowAllOrigins è pericoloso ma non spiega perché è critico con AllowCredentials",
        "2": "Identifica la combinazione AllowAllOrigins + AllowCredentials come violazione CORS spec",
        "3": "Identifica la violazione CORS spec, spiega l'impatto concreto (credentialed cross-origin requests) e individua anche il duplicate manual header come problema"
      }
    },
    "impact_assessment": {
      "max": 2,
      "criteri": {
        "0": "Nessuna valutazione di impatto",
        "1": "Impatto generico ('rischio sicurezza')",
        "2": "Impatto specifico al contesto 5G core (accesso non autorizzato a policy AM endpoint)"
      }
    },
    "fix_proposed": {
      "max": 2,
      "criteri": {
        "0": "Nessuna proposta di fix",
        "1": "Fix generico ('usare whitelist')",
        "2": "Fix specifico e corretto (rimuovere AllowAllOrigins, usare AllowOrigins con lista, rimuovere header manuali ridondanti)"
      }
    },
    "false_positives": {
      "max": 2,
      "criteri": {
        "2": "Nessun falso positivo segnalato",
        "1": "1 falso positivo minore",
        "0": "Falsi positivi fuorvianti o risposta generica non contestualizzata"
      }
    }
  },
  "total_max": 9
}
```

### 4.4 Domande aperte (da discutere in call)

1. **Granularità del task**: fornire un singolo file intero o solo lo snippet rilevante? Con snippet si rischia di "guidare" troppo; con file intero si supera facilmente la context window di modelli piccoli.

2. **Ground truth per il judge**: la rubrica è "corretto per definizione" come negli altri task textual. Ma qui esiste una verità esterna (analisi statica di Francesco) — conviene avere una sezione separata di "verifica esterna" non vista dal judge?

3. **Modelli candidati**: `qwen2.5-coder` sembra il candidato più naturale (coder specialist). Il confronto interessante è coder vs general (es. llama3.x) sullo stesso task — corrisponde già al setup 1A (stesso modello) vs 1B (modelli diversi).

4. **Metriche aggiuntive**:
   - *False positive rate*: quante vulnerabilità il modello "inventa" che non esistono?
   - *Severity calibration*: il modello assegna la severità giusta? (alta per V1, bassa per V6)
   - *Localizzazione*: il modello cita le righe corrette?

5. **Baseline**: confrontare la risposta LLM con l'output di uno strumento di static analysis (es. `gosec`) sullo stesso codice. Se gosec trova V1 e V2 e il LLM non le trova, il gap è misurabile.

### 4.5 Prossimi passi tecnici

- [ ] Leggere `Patch_Spiegazione.docx` (binario — serve tool esterno) per allineare le vulnerabilità identificate manualmente con quelle di Francesco
- [ ] Creare i task Markdown per almeno V1 e V2 (più nette, più facili da scrivere una rubrica discriminante)
- [ ] Decidere se il corpus per ogni task è lo snippet rilevante o il file intero
- [ ] Discutere in call mercoledì la struttura del task e i modelli da testare

---

## 5) Note di sessione

| Data | Note |
|---|---|
| 2026-05-09 | Prima analisi manuale del corpus. Identificate 7 vulnerabilità (V1–V7). Piano sperimentale abbozzato in §4. `Patch_Spiegazione.docx` non ancora letto (binario). Confronto con analisi Francesco pendente. |
