# Chain — Attempt #10

## File letti (in ordine)

- `File_Free5gc_Vulnerabili/AMF/api_communication.go` — file con handler HTTP del AMF per comunicazioni inter-NF. Notato subito che `HTTPUEContextTransfer` ha uno switch su Content-Type senza `default` branch, mentre `HTTPCreateUEContext` e `HTTPN1N2MessageTransfer` ce l'hanno. Notato anche il pattern `sbi.IN_PB_DETAILS_CTX_STR` con tipi inconsistenti (a volte `problemDetail.Cause`, a volte `problemDetail` intero).
- `File_Free5gc_Vulnerabili/PCF/api_oam.go` — file breve. `setCorsHeader` richiama `s.router.Use()` dentro un handler per-request, e configura `AllowAllOrigins: true` con `AllowCredentials: true` — combinazione proibita dalla spec W3C CORS e dal middleware gin-contrib/cors.
- `File_Free5gc_Vulnerabili/UDM/api_subscriberdatamanagement.go` — file lungo (~860 righe). Validazione SUPI corretta in `HandleGetAmData` tramite `validator.IsValidSupi()`. `HandleGetSmfSelectData` e `HandleGetSupi` non validano il SUPI prima di passarlo al processor — candidato scartato perché il contesto non suggerisce che sia intenzionalmente vulnerabile (potrebbe essere architetturale). Notato uso di `validator` già importato nel file.
- `File_Free5gc_Vulnerabili/UDR/api_datarepository.go` — file molto lungo (~2892 righe). A riga 2569-2570 e 2601-2602: regex `^(imsi-[0-9]{5,15}|nai-.+|...|.+)$` con ultimo branch `|.+`. Anche `HandlePolicyDataSubsToNotifyPost` (riga 1421-1443) e `HandlePolicyDataSubsToNotifySubsIdPut` (riga 1453-1477): mancano `return` dopo `c.JSON(...)` negli error branch, quindi il processor viene chiamato anche in caso di errore. La nota `Patch_Spiegazione.md` cita 6 CVE per UDR.
- `File_Free5gc_Vulnerabili/Patch_Spiegazione.md` — documento di riferimento che mappa NF → CVE. Confermato: AMF=GHSA-r99v-75p9-xqm5, PCF=GHSA-98cp-84m9-q3qp, UDR=6 CVE (incluso il regex), UDM=GHSA-585v-hcgf-jhfr.

## Candidati valutati (tutti, inclusi scartati)

- **Missing `default` in Content-Type switch** in `AMF/api_communication.go:340-345` — notato perché `HTTPCreateUEContext` (riga 193-200) e `HTTPN1N2MessageTransfer` (riga 394-401) hanno il `default`, ma `HTTPUEContextTransfer` no — **incluso come task5**
- **Inconsistenza tipo in `c.Set(sbi.IN_PB_DETAILS_CTX_STR, ...)`** in AMF — alcune funzioni passano `problemDetail.Cause` (string), altre `problemDetail` (struct). Candidato rilevante ma non accompagnato da CVE esplicito, e meno grave degli altri — **scartato** (potrebbe essere task futuro, ma non tra i top 3)
- **CORS `AllowAllOrigins + AllowCredentials` + `router.Use()` in handler** in `PCF/api_oam.go:18-39` — doppia vulnerabilità: invalid CORS spec + middleware growth — **incluso come task6**
- **Regex `|.+` bypass** in `UDR/api_datarepository.go:2569-2570` e `2601-2602` — il branch finale `.+` rende la validazione sempre vera — **incluso come task7** (questo è il CVE principale GHSA-6gxq-gpr8-xgjp)
- **Missing `return` dopo `c.JSON` in error handler** in `UDR/api_datarepository.go:1429-1430` e `1461-1462` (`HandlePolicyDataSubsToNotifyPost`, `HandlePolicyDataSubsToNotifySubsIdPut`) — mancano `return` dopo le call `c.JSON()` nei branch di errore, quindi `PolicyDataSubsToNotifyPostProcedure` viene chiamato anche in caso di errore di lettura/deserializzazione. Candidato forte (logic error con conseguenze dirette), ma scelto di prioritizzare la regex CVE già documentata — **scartato per questa run**, da considerare per task8
- **SUPI non validato in `HandleGetSmfSelectData` e `HandleGetSupi`** in `UDM/api_subscriberdatamanagement.go:126` e `162` — supi passato direttamente al processor senza `validator.IsValidSupi()` (che invece è presente in `HandleGetAmData`). CVE UDM noto (GHSA-585v-hcgf-jhfr cita "missing validator.IsValidSupi()"). Candidato scartato perché il pattern è meno self-contained per un task di code review (richiede confronto tra più funzioni dello stesso file) — **scartato**, potrebbe essere task8

## Ragionamento per ogni task creato

### task5_vuln_amf

- **Cosa ha attirato l'attenzione:** La funzione `HTTPUEContextTransfer` (riga 340-345) ha uno switch `case applicationjson / case multipartrelate` senza `default`. Nella stessa riga 193-200, `HTTPCreateUEContext` ha il `default: err = fmt.Errorf("wrong content type")`. La differenza è visivamente evidente confrontando le due funzioni adiacenti.
- **Perché è grave:** In Go, `err` è `nil` di default. Se il Content-Type non è né `applicationjson` né `multipartrelate`, nessun branch esegue, `err` rimane `nil`, il check `if err != nil` viene saltato, e `HandleUEContextTransferRequest` riceve un `UeContextTransferRequest` con `JsonData` allocato ma tutti i campi zero-value. In un AMF il trasferimento di contesto UE è critico per l'handover: elaborare un contesto vuoto può causare panic nel processor (nil dereference) o corruzione silente dello stato di mobilità.

### task6_vuln_pcf

- **Cosa ha attirato l'attenzione:** Riga 21: `s.router.Use(...)` dentro `setCorsHeader` che è chiamata da ogni handler per-request (riga 42). Riga 29: `AllowCredentials: true` insieme a `AllowAllOrigins: true`. Poi righe 33-38: header manuali che impostano `Access-Control-Allow-Origin: *` e `Access-Control-Allow-Credentials: true` contemporaneamente.
- **Perché è grave:** (1) La combinazione `AllowAllOrigins + AllowCredentials` viola la CORS spec e causa panic/configurazione non valida in gin-contrib/cors versioni recenti. (2) Chiamare `router.Use()` dentro un handler aggiunge middleware allo stack ad ogni request, causando crescita illimitata della chain (memory leak → OOM → DoS). (3) I due problemi sommati rendono l'endpoint OAM sia semanticamente rotto (CORS invalido per browser) sia vulnerabile a DoS via traffico sostenuto.

### task7_vuln_udr

- **Cosa ha attirato l'attenzione:** Riga 2570: `"^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$"`. L'ultimo branch `|.+` è immediatamente riconoscibile come il CVE GHSA-6gxq-gpr8-xgjp. Il commento al codice stesso (riga 2563) riporta il pattern inteso, che non include `|.+`.
- **Perché è grave:** L'alternazione regex prova i branch in ordine; `.+` match qualsiasi stringa non vuota. Siccome `ueId == ""` è già escluso dal check precedente, `|.+` rende il match sempre `true`, quindi il blocco `if !match` è dead code. Qualsiasi stringa arbitraria può essere usata come `ueId` per creare o interrogare EE subscriptions nel database UDR — inclusi pattern di injection MongoDB o identificatori di altri subscriber, violando l'isolamento dei dati per UE.

## Pattern esclusi

- **Missing `return` dopo `c.JSON` in error branch** (UDR `HandlePolicyDataSubsToNotifyPost` riga 1429-1430 e `HandlePolicyDataSubsToNotifySubsIdPut` riga 1461-1462) — logic error grave (processor chiamato su body non deserializzato), ma scartato per questa run in favore della regex CVE più documentata. Da candidare per task8.
- **SUPI non validato in UDM `HandleGetSmfSelectData` / `HandleGetSupi`** — validazione assente rispetto a `HandleGetAmData`, CVE GHSA-585v-hcgf-jhfr. Scartato perché meno self-contained per un task isolato.
- **Inconsistenza tipo in `c.Set(sbi.IN_PB_DETAILS_CTX_STR, ...)` in AMF** — alcune funzioni passano la struct intera, altre solo il campo `.Cause` o `.Title`. Non accompagnato da CVE esplicito e l'impatto è sul metrics/tracing, non sulla sicurezza primaria.
