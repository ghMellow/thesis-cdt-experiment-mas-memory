# Chain — Attempt #12

## File letti (in ordine)

- `File_Free5gc_Vulnerabili/Patch_Spiegazione.md` — indici CVE per NF: UDR (6 CVE, missing return), PCF (1 CVE, CORS DoS), AMF (1 CVE, missing default case), UDM (1 CVE, missing IsValidSupi). Nessuna spiegazione tecnica nel documento, solo URL advisory.
- `docs/tasks/task1_math_int.md` — formato task: header, Problem, Agent Instructions con output JSON. Template copiato per struttura.
- `docs/tasks/task1_math_int_sol.md` — formato soluzione: Ground Truth, scoring rubric.
- `File_Free5gc_Vulnerabili/AMF/api_communication.go` — analisi completa: ~500 righe, 11 handler HTTP. Pattern ripetuto correttamente (GetRawData → Deserialize → early return) in quasi tutti i handler. Anomalia trovata: `HTTPUEContextTransfer` (riga 340–345) ha switch senza `default:`, a differenza di `HTTPCreateUEContext` (riga 193–200) e `HTTPN1N2MessageTransfer` (riga 394–401) che hanno `default: err = fmt.Errorf(...)`.
- `File_Free5gc_Vulnerabili/PCF/api_oam.go` — 66 righe. Due pattern anomali: (1) `AllowAllOrigins: true` + `AllowCredentials: true` nel cors.Config, (2) `s.router.Use(cors.New(...))` chiamata dentro `setCorsHeader` che è un handler per-request → stacking unbounded di middleware.
- `File_Free5gc_Vulnerabili/UDM/api_subscriberdatamanagement.go` — 859 righe. `HandleGetAmData` (riga 30–68) ha `validator.IsValidSupi(supi)`, ma `HandleGetSmfSelectData` (riga 119–141) e altri handler con `:supi` non validano. CVE GHSA-585v-hcgf-jhfr confermato: validazione presente solo parzialmente.
- `File_Free5gc_Vulnerabili/UDR/api_datarepository.go` — 2892 righe (lette in 2 passaggi). Trovati: `HandlePolicyDataSubsToNotifyPost` (riga 1421–1443) e `HandlePolicyDataSubsToNotifySubsIdPut` (riga 1453–1477) con doppio problema: (a) nessun `return` dopo i blocchi errore, (b) `openapi.Deserialize(policyDataSubscription, ...)` — passaggio per valore invece di pointer.

---

## Candidati valutati (tutti, inclusi quelli scartati)

- **AMF: switch senza default in HTTPUEContextTransfer** in `AMF/api_communication.go:340-345` — unico handler dei 11 presenti senza `default:` case; confronto esplicito con HTTPCreateUEContext riga 198 e N1N2MessageTransfer riga 399 che hanno entrambi `default:`. **Incluso → task5_vuln_amf**

- **AMF: c.Set con problemDetail struct anziché .Cause** in `AMF/api_communication.go:186,333` — alcune chiamate usano `c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)` (struct intera) invece di `problemDetail.Cause` (stringa). Inconsistenza di tipo, potenziale panic a runtime se il middleware downstream assume una stringa. Scartato: non è un CVE documentato e l'impatto è limitato al middleware di metrics, non all'API stessa.

- **PCF: CORS AllowAllOrigins + AllowCredentials** in `PCF/api_oam.go:21-31` — combinazione vietata dalla spec CORS. **Incluso → task7_vuln_pcf**

- **PCF: router.Use() per-request** in `PCF/api_oam.go:21` — `s.router.Use(cors.New(...))` chiamata in setCorsHeader che è invocata ad ogni richiesta. Memory leak + potential data race. **Incluso come secondo punto in task7_vuln_pcf** (arricchisce il task senza richiedere un task dedicato)

- **PCF: supi non validato in HTTPOAMGetAmPolicy** in `PCF/api_oam.go:44-45` — `supi` estratto con `c.Params.ByName("supi")`, solo check `supi == ""` senza validazione del formato SUPI (es. `imsi-<15 digit>`). Scartato: UDM mostra pattern simile più ricco; il pattern PCF è meno elaborato e il CVE specifico non è listato nel documento di patch.

- **UDM: IsValidSupi assente su HandleGetSmfSelectData e altri** in `UDM/api_subscriberdatamanagement.go:126-140` e simili — `HandleGetAmData` valida, altri no. CVE GHSA-585v-hcgf-jhfr. Scartato come task autonomo: il pattern è interessante ma meno ricco per un task a sé; ridondante con altri task. Il file UDM è già incluso nella chain come documento letto.

- **UDR: missing return in HandlePolicyDataSubsToNotifyPost** in `UDR/api_datarepository.go:1425-1442` — assenza di `return` dopo entrambi i blocchi errore. **Incluso → task6_vuln_udr**

- **UDR: non-pointer in openapi.Deserialize** in `UDR/api_datarepository.go:1432,1464` — `openapi.Deserialize(policyDataSubscription, ...)` invece di `&policyDataSubscription`. Deserialization scritta su copia, struct rimane zero-valued. **Incluso in task6_vuln_udr** (bug separato ma nello stesso handler)

- **UDR: HandlePolicyDataSubsToNotifySubsIdPut identico bug** in `UDR/api_datarepository.go:1453-1477` — stesso pattern doppio bug del Post handler. Scartato come task separato: identico al task6, aggiungere un terzo sub-question lo renderebbe eccessivamente lungo. Menzionato nella soluzione.

- **UDR: HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete/Get senza return dopo check influenceId** in `UDR/api_datarepository.go:1208-1232` — quando `influenceId != "subs-to-notify"`, viene chiamato `c.String(http.StatusNotFound, ...)` senza `return`, e l'esecuzione continua col processor. Scartato: pattern interessante ma il CVE per UDR punta ai missing return nei policy handlers; aggiungere un quarto task supererebbe il limite di 3.

---

## Ragionamento per ogni task creato

### task5_vuln_amf

- **Cosa ha attirato l'attenzione:** confronto tra handler nello stesso file. HTTPCreateUEContext (riga 193) e HTTPN1N2MessageTransfer (riga 394) hanno entrambi `default: err = fmt.Errorf("wrong content type")`. HTTPUEContextTransfer (riga 340) ha lo stesso schema ma senza `default:`. L'assenza è visiva e strutturale.
- **Perché è un problema di sicurezza:** in Go, `err` non viene azzerato automaticamente tra statements; entra nel blocco switch come nil, e se nessun case corrisponde, rimane nil. Il check `if err != nil` che segue non scatta. `HandleUEContextTransferRequest` riceve un request struct parzialmente zero-valued (JsonData inizializzato ma vuoto). In un contesto 5G, il trasferimento di contesto UE coinvolge stato di sessione critico; un handler che processa dati corrotti può causare panic o stale state.

### task6_vuln_udr

- **Cosa ha attirato l'attenzione:** scansione dei pattern `if err != nil { ... }` nel file. Praticamente tutti i 30+ handler del file terminano il blocco con `return`. HandlePolicyDataSubsToNotifyPost e Put sono le eccezioni — identificate scorrendo i 1420–1477 che mostrano assenza del `return`. Poi notato che il primo argomento di `openapi.Deserialize` è `policyDataSubscription` (valore) invece di `&policyDataSubscription` (pointer) usato in tutti gli altri handler.
- **Perché è un problema di sicurezza:** (1) doppia risposta HTTP → undefined behavior in gin, possibile panic nel middleware; (2) processor chiamato con struct vuota → dati non validi persistiti in MongoDB UDR, usati da PCF per policy decisions su tutti i subscriber; (3) non-pointer significa che anche quando Deserialize non restituisce errore, i dati vengono scartati — vulnerability latente che può passare i test.

### task7_vuln_pcf

- **Cosa ha attirato l'attenzione:** il file PCF è il più corto (66 righe) ma concentra due anomalie distinte. Prima anomalia: `AllowAllOrigins: true` e `AllowCredentials: true` nella stessa struct — la spec CORS li proibisce insieme. Seconda anomalia: `s.router.Use(cors.New(...))` dentro una funzione chiamata per ogni request — aggiunge middleware globale in modo incrementale, che è sia non-thread-safe sia un memory leak.
- **Perché è un problema di sicurezza:** la combinazione CORS permette a pagine web arbitrarie di fare richieste credenziate all'OAM endpoint che espone dati di policy per SUPI (subscriber identifiers). Il router.Use per-request è un vettore DoS indipendente: dopo K richieste ci sono K middleware strati che processano ogni richiesta successiva.

---

## Pattern esclusi

- **AMF: inconsistent c.Set type (struct vs .Cause)** — presente in ~4 handler, impatto limitato al middleware di metrics, non classificato come CVE nel documento di patch. Menzionato internamente, non incluso in task.
- **PCF: supi format not validated** — solo check `== ""`, nessuna regex. Interessante ma il documento patch non lo cita per PCF e il task avrebbe richiesto conoscenza del formato SUPI (imsi-/nai-) non fornita nello snippet.
- **UDM: partial IsValidSupi coverage** — HandleGetAmData valida, altri 10+ handler no. Il CVE GHSA-585v-hcgf-jhfr è reale ma generare un task interessante richiederebbe mostrare entrambi i casi in modo affiancato; decidendo di dedicare solo 3 task totali, UDM è stato usato come documento di studio ma non ha prodotto un task autonomo.
- **UDR: influenceId guard without return** — riga 1212-1213 e 1226-1227, stesso pattern missing-return. Scartato per non superare il limite di 3 task e per evitare ridondanza con task6 che già copre missing-return in UDR.
- **UDR: HandlePolicyDataSubsToNotifySubsIdPut** — identico ai bug di HandlePolicyDataSubsToNotifyPost. Menzionato nella soluzione di task6 come pattern ripetuto, non come task separato.

---

## Note generali

Il documento `Patch_Spiegazione.md` è quasi un indice grezzo (solo URL di advisory, zero spiegazione tecnica). Ha orientato la ricerca ma non ha sostituito la lettura diretta del codice. La strategia più efficace è stata il confronto intrafilo: per AMF, trovare l'anomalia confrontando handler dello stesso file tra loro; per UDR, notare che la deviazione dal pattern dominante (return presente ovunque) è il segnale di allarme.

Il file UDR con 2892 righe è stato letto in 2 sessioni (offset 0 e 1846). La prima sessione copriva già i handler vulnerabili (1421–1477) che cadevano nella porzione iniziale del secondo segmento.

La scelta di 3 task (invece di 4–5 possibili) è deliberata: task5/6/7 coprono classi di vulnerabilità distinte (missing-default, missing-return+wrong-type, CORS), garantendo varietà tassonomica per l'esperimento multi-agent. Aggiungere task su UDM o i duplicati UDR avrebbe ridotto la diversità didattica.
