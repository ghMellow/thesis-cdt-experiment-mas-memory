# Chain — Attempt #19

## File letti (in ordine)
- `docs/tasks/task4_rootcause.md` e `task4_rootcause_sol.md` — per capire il formato dei task esistenti (scenario, question, agent instructions con JSON schema, e per la sol: ground truth + rationale + rubrica a punteggio).
- `File_Free5gc_Vulnerabili/Patch_Spiegazione.md` — documento di patch: elenca sinteticamente 6 CVE UDR ("return non messi"), 1 CVE PCF (CORS DoS), 1 CVE AMF (no default case), 1 CVE UDM (missing validator.IsValidSupi()), con link GHSA per ciascuno. Nessun dettaglio implementativo, solo etichette.
- `File_Free5gc_Vulnerabili/AMF/api_communication.go` — letto per intero (502 righe). Notato subito il pattern ripetuto: leggi body → deserializza in base a Content-Type → gestisci errore. La maggior parte degli switch su Content-Type ha un `default:`, uno no.
- `File_Free5gc_Vulnerabili/PCF/api_oam.go` — file piccolo (66 righe), letto per intero. Un solo handler reale (`HTTPOAMGetAmPolicy`), CORS impostato in `setCorsHeader`.
- `File_Free5gc_Vulnerabili/UDM/api_subscriberdatamanagement.go` — letto per intero (~860 righe). Notato che solo alcuni handler chiamano `validator.IsValidSupi`/`IsValidGpsi`.
- `File_Free5gc_Vulnerabili/UDR/api_datarepository.go` — file grande (2892 righe), letto in due passate (offset 0-1346, poi 1347+ con grep mirato). Ho cercato subito `regexp|MustCompile|IsValid` per capire dove si concentra la validazione, e `StatusNotFound` per il pattern "return non messi" citato nel patch doc.

## Candidati valutati

- **AMF — `HTTPUEContextTransfer` switch senza `default`** (riga ~338-345) — notato confrontando con `HTTPCreateUEContext` poco sopra, che ha lo stesso schema ma con `default: err = fmt.Errorf(...)`. Deciso: incluso come task5. Il resto degli switch nel file (`HTTPN1N2MessageTransfer`) ha il default, quindi è un'omissione isolata e specifica di questa funzione.
- **PCF — CORS credenziali+wildcard** (righe 21-38) — citato nel patch doc, quindi "atteso". Deciso: incluso, ma non come unico contenuto del task.
- **PCF — `s.router.Use(...)` chiamato dentro `setCorsHeader`, invocata ad ogni richiesta** — NON citato nel patch doc. L'ho notato perché mi sono chiesto "perché una funzione che imposta solo header ha bisogno di chiamare `.Use()` sul router?" — `.Use()` è normalmente una chiamata di setup, non qualcosa che ha senso per-request. Deciso: incluso come parte centrale del task6 (insieme al CORS), perché è più sottile e più interessante del bug documentato.
- **UDM — validazione supi presente solo in `HandleGetAmData`** — il patch doc dice genericamente "missing validator.IsValidSupi()" (singolare, un CVE). Leggendo il file per intero ho fatto un grep di `ByName("supi")` vs `IsValidSupi` e ho visto che il fix è presente in UNA funzione sola, mentre almeno altre 6 funzioni (`GetSmfSelectData`, `GetNssai`, `GetSmData`, `GetTraceData`, `GetUeContextInSmfData`, `GetSupi`) condividono lo stesso pattern e non validano nulla. Deciso: incluso come task7, centrato sulla copertura parziale, non sul singolo caso.
- **UDR — regex `|.+` finale in `HandleCreateEeSubscriptions`/`HandleQueryeesubscriptions`** (righe 2569-2570, 2601-2602) — trovato cercando `regexp.MatchString` nel file. Ho letto l'alternanza `^(imsi-...|nai-.+|msisdn-...|extid-...|gci-.+|gli-.+|.+)$` carattere per carattere e mi sono accorto che l'ultima alternativa `.+` da sola cattura qualunque stringa non vuota, rendendo tutte le alternative precedenti irrilevanti ai fini del rifiuto. NON è menzionato nel patch doc (che per UDR parla solo di "return non messi"). Deciso: incluso come task8, è il finding più sottile e richiede ragionamento esplicito sulla semantica della regex, non solo lettura superficiale del codice (che al contrario sembra corretto: commento con pattern atteso, gestione errori pulita).
- **UDR — 3+ occorrenze di `c.JSON`/`c.String` senza `return`** (righe 1212, 1226, 1238 nei tre handler `...SubsToNotifySubscriptionId{Delete,Get,Put}`; righe 2780-2781 e 2790-2791 in `HandleApplicationDataInfluenceDataSubsToNotifyGet`) — questo corrisponde esattamente a quanto già annunciato nel patch doc ("UDR 6 CVE RETURN NON MESSI"). Deciso: SCARTATO come task principale perché già documentato esplicitamente nel patch doc (meno interessante come "scoperta"), ma riutilizzato come esempio di supporto nel task9 cross-NF per illustrare lo stesso meta-pattern (fix corretto altrove, non applicato ovunque) visto in AMF e UDM.

## Ragionamento per ogni task creato

### task5_vuln_amf
- **Cosa ha attirato l'attenzione:** lo switch su Content-Type in `HTTPUEContextTransfer` non ha `default`, mentre lo switch quasi identico in `HTTPCreateUEContext` (poche righe sopra) sì.
- **Perché è una vulnerabilità:** `err` resta `nil` (valore ereditato dalla `GetRawData()` riuscita), il check `if err != nil` viene saltato, e il processor riceve una request con `JsonData` vuoto/non popolato invece di un 400.
- **Perché ho deciso di includerlo:** è citato nel patch doc ma il documento non spiega il meccanismo — trovare *quale* variabile resta in che stato richiede tracciare il flusso, non solo sapere che "manca un default case".

### task6_vuln_pcf
- **Cosa ha attirato l'attenzione:** oltre al CORS (atteso), la riga `s.router.Use(cors.New(...))` dentro una funzione chiamata ad ogni richiesta.
- **Perché è una vulnerabilità:** `.Use()` accoda un middleware alla catena del router; chiamata per-request fa crescere la catena senza limite, con degrado di latenza su TUTTO il router (non solo l'endpoint OAM) — un DoS a bassissimo sforzo.
- **Perché ho deciso di includerlo:** è il tipo di bug che sopravvive a una review superficiale perché il resto della funzione (header CORS impostati a mano) sembra innocuo boilerplate.

### task7_vuln_udm
- **Cosa ha attirato l'attenzione:** `validator.IsValidSupi` compare una sola volta nel file nonostante 7 funzioni condividano lo stesso parametro `:supi` e lo stesso schema di utilizzo.
- **Perché è una vulnerabilità:** il supi non validato arriva al layer di persistenza via `Processor().Get*Procedure(c, supi, ...)`.
- **Perché ho deciso di includerlo:** il patch doc parla di "1 CVE, missing validator.IsValidSupi()" al singolare — il codice mostra che la patch ufficiale è stata applicata a UNA funzione sola, lasciando scoperte le altre 6. Questo è un livello di dettaglio che il documento di patch non dà.

### task8_vuln_udr
- **Cosa ha attirato l'attenzione:** la regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` usata in due handler UDR per validare `ueId`.
- **Perché è una vulnerabilità:** l'ultima alternativa `.+` (senza vincoli) cattura qualsiasi stringa non vuota; essendo dentro lo stesso gruppo racchiuso da `^...$`, rende l'intera validazione equivalente al solo controllo "non vuoto" già fatto dalle righe precedenti — le sei alternative specifiche (imsi-, nai-, ecc.) non possono mai causare un rifiuto.
- **Perché ho deciso di includerlo:** è il finding più significativo dei quattro file — non è menzionato nel patch doc, richiede lettura carattere-per-carattere della regex per essere colto, e il codice attorno (commento con pattern atteso, gestione errori, logging) è ingannevolmente corretto in apparenza.

### task9_vuln_cross
- **Come ho scelto cosa mettere nel cross-NF:** ho cercato il denominatore comune tra i quattro task file-specifici. Tre di quattro (AMF, UDM, UDR-return) condividono la stessa forma: un safeguard implementato correttamente in UNA funzione "di controllo" ma non propagato a funzioni sorelle strutturalmente identiche. UDR-regex è diverso in natura (il safeguard non manca, è presente ma rotto — più difficile da individuare perché non c'è un "confronto tra fratelli" che lo evidenzi). PCF è diverso ancora: non ha handler fratelli (uno solo sulla route), quindi non può nemmeno rientrare nel pattern "inconsistenza tra sibling" — è un bug auto-contenuto in un'unica funzione con due nature (valore sbagliato + posizionamento sbagliato della chiamata).
- Ho costruito le domande del task9 per verificare che l'agent testato distingua esplicitamente queste tre categorie (assenza mecanicamente rilevabile / presenza rotta semanticamente / bug strutturalmente diverso) invece di appiattire tutto su "ci sono bug in ogni NF".

## Pattern esclusi / non inclusi come task

- Il pattern "return non messi" in UDR (righe 1212, 1226, 1238, 2780-2781, 2790-2791) non è diventato un task a sé perché già esplicitamente annunciato nel patch doc — meno interessante come finding indipendente. Riusato solo come esempio di supporto nel task9.
- In UDR, `HandleRemoveEeGroupSubscriptions` e `HandleUpdateEeGroupSubscriptions` non validano affatto `ueGroupId` (nessun controllo, nemmeno di vuoto), a differenza di `HandleCreateEeGroupSubscriptions`/`HandleQueryEeGroupSubscriptions` che validano con lo stesso pattern regex (anch'esso senza `.+` finale in questo caso specifico — quello per `ueGroupId` è `^(extgroupid-[^@]+@[^@]+|anyUE)$`, senza catch-all, quindi effettivamente restrittivo). Notato ma scartato: sarebbe stato un quinto pattern nello stesso file, ridondante con il tema "copertura incompleta" già coperto da task7/task8.
- Nel file UDM, `ModifyForSharedData` usa `supi` come parte del path ma per un caso d'uso diverso (identifica la subscription, non recupera dati soggetto); scartato come possibile quinto esempio perché la semantica è diversa e avrebbe complicato il confronto diretto nel task7.
- Non ho approfondito i modelli (`models.*`) o il pacchetto `validator`/`util` referenziati ma non inclusi nella cartella — fuori dal vincolo operativo (solo file fisicamente presenti in questa directory).

## Note generali

Ho letto ogni file per intero prima di scegliere cosa includere nei task, usando grep mirato solo per UDR (troppo grande per una lettura lineare comoda, 2892 righe) una volta capito lo schema ripetitivo degli handler. La scoperta più significativa (la regex UDR con l'alternativa catch-all `.+`) non era menzionata nel documento di patch fornito ed è emersa esclusivamente dalla lettura diretta del codice sorgente — l'ho notata cercando `regexp.MatchString` nel file e poi leggendo l'espressione carattere per carattere, non perché mi aspettassi di trovarla.
