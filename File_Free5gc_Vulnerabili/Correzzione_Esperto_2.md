> altro responso dopo aver fornito i report all'esperto

---

UDR

UDR 6 CVE RETURN NON MESSI, causano esecuzione imprevista del codice e leak di informazioni sensibili
CVE-2026-40245 permette get di dati sensibili 
HandleApplicationDataInfluenceDataSubsToNotifyGet
api_datarepository.go
CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N 8.7
Information Disclosure: La mancanza di return dopo l'errore fa proseguire l'esecuzione e restituisce dati di sottoscrizione anche su richiesta malformata. 
CVE-2026-40246 permette delete di utenti 
HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete
api_datarepository.go
CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N 8.7
Improper Access Control → Denial of Service / perdita dati: Il controllo sull'influenceId risponde 404 ma non interrompe il flusso: la delete viene eseguita comunque. 
CVE-2026-40247 permette get di dati sensibili 
HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet
api_datarepository.go
CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N 8.7
Information Disclosure: Stesso pattern missing-return: la GET restituisce i dati anche quando la richiesta è stata rifiutata. 
CVE-2026-40248 permette una put di dati 
HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut
api_datarepository.go
CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N 8.7
Improper Access Control -> Integrity violation: La PUT viene applicata nonostante la risposta 404, permettendo modifica non autorizzata dei dati. 
CVE-2026-40249 permette una put di dati
HandlePolicyDataSubsToNotifySubsIdPut
api_datarepository.go
 CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N 6.9
LLM C’È SOLO QUESTA CVE, LA STIMA BENE, VI HIGH VA BENISSIMO, ERO STATO BUONO IO
Integrity violation (missing return): Scrittura di dati di policy subscription non validata perché l'esecuzione continua dopo l'errore. 
CVE-2026-40343 permette post di dati 
HandlePolicyDataSubsToNotifyPost
api_datarepository.go
CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N 6.9
Integrity violation (missing return): Come sopra, sul path POST delle policy subscription. 
CVE-2026-47780, CVE TROVATA INSIEME AL primo tentativo, Inserimento arbitrario ueid nella subscription: REGEX
HandleCreateEeSubscriptions and HandleQueryeesubscriptions.
api_datarepository.go
CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N 6.9
Improper Input Validation (CWE-20, regex bypass): Il .+ finale nella regex annulla tutti i pattern stretti, permettendo ueId arbitrari in sottoscrizione. 

ANALISI LLM SENZA ANALISI STATICA DEL CODICE
FINDINGS UDR:


Incorrect Pointer Usage in Deserialization (Logic Error/Data Loss):
Location: HandlePolicyDataSubsToNotifyPost and HandlePolicyDataSubsToNotifySubsIdPut.
Pattern: The code calls openapi.Deserialize(policyDataSubscription, reqBody, "application/json"). In Go, policyDataSubscription is a struct passed by value. The Deserialize function requires a pointer to populate the object.
Impact: The variable remains empty (zero-valued). The UDR will store empty subscription objects in the database. This causes a functional Denial of Service (DoS) for policy notifications as the intended configuration is lost.
Fix: Pass the address of the variable: openapi.Deserialize(&policyDataSubscription, reqBody, "application/json").
E’ GIA FIXATA, MA ERA UNA VULNERABILITA’ NUOVA, praticamente mancava il & puntatore al deserialize e quindi non inseriva in memoria i dati ma un qualcosa di vuoto, non c’entra con le CVE
LUI PENSA SIA LA CVE-2026-40249, È LO STESSO PUNTO MA DUE VULNERABILITÀ DIVERSE, LUI SI SOFFERMA SOLO SUL DESERIALIZE


Silent Failure in Parameter Parsing (Data Integrity):
Location: HandleCreateSmfContextNon3gpp
Pattern: pduSessionId, err := strconv.ParseInt(c.Param("pduSessionId"), 10, 64) is called, but the error is only logged as a warning (logger.DataRepoLog.Warnln(err)), and the function continues.
Impact: If the pduSessionId is not a valid integer, it defaults to 0. The UDR will store the SMF context under ID 0, potentially overwriting other sessions or creating an invalid state, leading to PDU session failures for the UE.
Fix: Return a 400 Bad Request response if strconv.ParseInt fails.
NON E’ FIXATA, TESTATA E CVE RICHIESTA
https://github.com/free5gc/free5gc/security/advisories/GHSA-x8rx-jxgm-29mf
Improper Input Validation → Data IntegrityErrore di ParseInt solo loggato: il pduSessionId diventa 0 e può sovrascrivere/corrompere contesti SMF. 
Unsafe JSON Unmarshaling of Query Parameters:
Location: HandlePolicyDataUesUeIdSmDataGet and HandleQuerySmData.
Pattern: Raw strings from URL queries (sNssaiQuery) are passed directly to json.Unmarshal([]byte(sNssaiQuery), &sNssai).
Impact: This bypasses standard API validation. While the impact is limited by the struct definition, it is a fragile pattern that can lead to unexpected behavior or internal server errors if the query string contains malformed JSON.
Fix: Use a dedicated parser or validate the string format before attempting to unmarshal.
NON È FIXATO, PICCOLA VULN, SEGNALATA COMUNQUE Permette una chiamata con json malformato ma che restituisce dati ottenibili comunque con altre chiamate valide https://github.com/free5gc/free5gc/security/advisories/GHSA-w32m-4wv3-5g29
Improper Input Validation (JSON injection in query param): Stringhe di query passate direttamente a json.Unmarshal, bypassando la validazione API standard. 
Potential Resource Exhaustion (Over-fetching):
Location: HandleApplicationDataInfluenceDataGet.
Pattern: Query parameters (e.g., influence-Ids, dnns) are split by commas and used directly in MongoDB $in operators without size limits.
Impact: An authorized NF could send an extremely large list of IDs, causing the UDR to perform massive database queries, leading to high memory consumption and potential Denial of Service (DoS) of the UDR.
Fix: Implement a maximum limit on the number of elements allowed in the comma-separated query parameters.
NON E’ FIXATO, ho provato l’attacco ma il server ha come meccanismo di sicurezza interno il blocco di query superiori a 1MB quindi impedisce il Dos ma il problema effettivamente rimane ma non è sfruttabile
https://github.com/free5gc/free5gc/security/advisories/GHSA-vh4x-chcw-j8c7
Resource Exhaustion / DoS (non sfruttabile): Liste comma-separated senza limite finiscono in $in MongoDB; mitigato dal limite di 1 MB sulla query. 
Denial of Service (Unbounded Request Body): 
Multiple handlers (e.g., HandleAmfContext3gpp, HandleCreateAmfContext3gpp, HandleCreateAuthenticationStatus, etc.) use c.GetRawData(). This Gin method reads the entire request body into a byte slice without a size limit. A compromised NF or an attacker with network access to the SBI could send an extremely large payload, causing the UDR to crash due to Out-Of-Memory (OOM) exhaustion.
NON È FIXATO, VULN GROSSA, DOS SU MOLTE API, NE SEGNALO UNA PER CORRETTEZZA MA L’USO IMPROPRIO DI GETRAWDATA PORTA AD UN DOS, HO FATTO CRASHARE L’UDR
https://github.com/free5gc/free5gc/security/advisories/GHSA-57x5-mv7x-wrvr
Denial of Service (OOM, CWE-400/789): GetRawData() legge il body senza limiti di dimensione: crash dell'UDR per esaurimento memoria. 
Ineffective Input Validation (Regex Bypass):
Location: HandleCreateEeSubscriptions and HandleQueryeesubscriptions.
Pattern: The regex ^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$ contains a trailing .+ alternative.
Impact: The .+ matches any non-empty string, rendering all previous strict patterns useless. This allows malformed ueId values to enter the system. While mTLS protects the interface, this can lead to data corruption or crashes in downstream NFs that expect strict 3GPP formats.
Fix: Remove the .+ alternative from the regular expression.
CVE-2026-47780 trovata nel primo test tutti insieme e ritrovata


Logic Error: Missing Return after Error Response (Potential Panic/DoS)
Location: HandleApplicationDataInfluenceDataSubsToNotifyGet.
Pattern: When openapi.Deserialize fails for the snssai query parameter, the code calls c.JSON(http.StatusBadRequest, problemDetails) but does not return.
Impact: Execution continues to s.Processor().ApplicationDataInfluenceDataSubsToNotifyGetProcedure. Since the deserialization failed, the snssai pointer remains nil or partially initialized. If the processor attempts to dereference this pointer, the UDR will panic, leading to a Denial of Service (DoS).
Fix: Add a return statement immediately after the c.JSON call.
Trovata la CVE-2026-40245 iniziale, unica che trova nell’UDR 


ANALISI LLM + ANALISI STATICA DEL CODICE
UDR
Logic Error: Missing Return after Error Response (Potential Panic/DoS)
Logic Error (Incorrect Parameter Handling): In HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete, HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet, and HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut, the code checks if influenceId != "subs-to-notify". If it is not equal, it calls c.String(http.StatusNotFound, "404 page not found"). However, it does not return after this call. The execution continues to the Processor call, meaning the operation is performed even if the "404" response was sent, leading to inconsistent state and unexpected API behavior
TROVA LE CVE: CVE-2026-40246, CVE-2026-40247, CVE-2026-40248 in un unico punto, prima non le trovava
Logic Error (Incorrect Error Handling Sequence): rep 7
Location: HandleCreateEeGroupSubscriptions, HandleQueryEeGroupSubscriptions.
Pattern: The code checks if !match and returns a response before checking if err != nil from regexp.MatchString.
Impact: If the regex engine fails, the code reports an "Invalid ueGroupId" (client error) instead of a system failure (server error), masking internal errors and violating proper error handling patterns.
Fix: Check if err != nil immediately after the MatchString call.
NON UNA PROPRIA VULNERABILITÀ, PIÙ UN SUGGERIMENTO DI CODING, NON SFRUTTABILE
Regular Expression Denial of Service (ReDoS): rep 8
In HandleCreateEeGroupSubscriptions, HandleQueryEeGroupSubscriptions, HandleCreateEeSubscriptions, and HandleQueryeesubscriptions, 
regexp.MatchString is used with patterns containing multiple greedy matches and overlapping groups (e.g., .+ at the end of the ueId pattern). While the patterns are relatively simple, the use of .+ combined with other alternatives can lead to catastrophic backtracking if a very long, specially crafted string is provided, potentially causing CPU exhaustion and a Denial of Service (DoS) of the UDR NF.
NON UNA PROPRIA VULNERABILITÀ, NON SFRUTTABILE


----------------------------------------------------------------------------------------------------------------------

PCF 
1CVE, CORS DoS	
CVE-2026-41135 
SetCorsHeader(), called by HTTPOAMGetAmPolicy()
pcf/internal/sbi/api_oam.go
CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N 8.7
LLM non trova availability, si ferma su confidenzialità
Denial of Service (memory leak) + CORS Misconfiguration: Il middleware CORS viene riagganciato al router a ogni richiesta, con catena che cresce indefinitamente; la policy AllowAllOrigins + AllowCredentials è comunque insicura. 

ANALISI LLM SENZA ANALISI STATICA DEL CODICE
FINDINGS PCF:
CORS Misconfiguration (Permissive Policy):
Location: setCorsHeader function.
Analysis: The code implements an extremely permissive Cross-Origin Resource Sharing (CORS) policy. It sets AllowAllOrigins: true and explicitly sets the header Access-Control-Allow-Origin: "*". Furthermore, it sets AllowCredentials: true.
5G Context Impact: In a 5G Core, the SBI is intended for inter-NF communication. While SBI is typically protected by mTLS/OAuth2, if this OAM interface is exposed to a management network or a web-based dashboard, a permissive CORS policy allows any website visited by an administrator to make authenticated requests to the PCF. The combination of AllowAllOrigins: true and AllowCredentials: true is a critical security flaw that can lead to Cross-Site Request Forgery (CSRF) or unauthorized data extraction if the browser session is used for authentication.
Fix: Replace AllowAllOrigins: true and "*" with a strict whitelist of trusted management domains. Remove AllowCredentials: true unless explicitly required by a secure authentication mechanism.


Inefficient/Incorrect Middleware Application:
Location: setCorsHeader function.
Analysis: The function calls s.router.Use(cors.New(...)) inside a request handler. In the Gin framework, .Use() attaches middleware to the router globally or for a group. Calling this inside a handler means the middleware is re-added to the router on every single request to HTTPOAMGetAmPolicy.
5G Context Impact: This leads to a memory leak and performance degradation (DoS) as the middleware chain grows indefinitely with every request. In a high-traffic 5G core, this could crash the PCF OAM handler, impacting the availability of policy management.
Fix: Move the CORS middleware configuration to the server initialization phase (e.g., in getOamRoutes or a dedicated setup function) so it is applied once at startup.


Lack of Input Validation/Sanitization (Potential IDOR/Injection):
Location: HTTPOAMGetAmPolicy function, line supi := c.Params.ByName("supi").
Analysis: The supi (Subscription Permanent Identifier) is taken directly from the URL path and passed to the processor without any validation or sanitization.
5G Context Impact: While the processor might handle validation, the handler allows any string to be passed. If the underlying processor uses this value in a database query or log without escaping, it could lead to injection. More importantly, it facilitates Insecure Direct Object Reference (IDOR) if the OAM layer doesn't verify that the requester has the authority to access the policy of that specific SUPI.
Fix: Implement a regex check to ensure the supi conforms to the expected 3GPP format (numeric string) before passing it to the processor.


TUTTE E TRE SONO INSIEME LA CVE-2026-41135, IN PIÙ TROVA QUESTA MANCANZA DI VALIDAZIONE NEL SUPI CHE AVEVO GIÀ TROVATO MA NON COMPORTA A NESSUN ATTACCO VALIDO, IL DB BLOCCA I SUPI MANOMESSI PERÒ È SICURAMENTE UN ERRORE DI PROGRAMMAZIONE
IL VALIDATORE METTE CONFIDENTIALITY ANCHE SE IN REALTÀ NEL RAGIONAMENTO PARLA DI DOS, FORSE SI CONCENTRA SOLO SU QUEST'ULTIMA E PERDE IL FOCUS MA COMUNQUE POCO MALE, RICONOSCE LE VULNERABILITÀ E LO SCORE È CORRETTO


ANALISI LLM + ANALISI STATICA DEL CODICE
PCF
CORS Misconfiguration (Permissive Policy)
Inefficient/Incorrect Middleware Application
Broken Access Control / Missing Authorization:
Location: HTTPOAMGetAmPolicy function (Lines 41-56)
STESSO IDENTICO DISCORSO PRECEDENTE, STESSE VULNERABILITÀ
TUTTE E TRE SONO INSIEME LA CVE-2026-41135, IN PIÙ TROVA QUESTA MANCANZA DI VALIDAZIONE NEL SUPI CHE AVEVO GIÀ TROVATO MA NON COMPORTA A NESSUN ATTACCO VALIDO, IL DB BLOCCA I SUPI MANOMESSI PERÒ È SICURAMENTE UN ERRORE DI PROGRAMMAZIONE




-----------------------------------------------------------------------------------------------------------------
AMF
1 CVE, NO DEFAULT CASE, comportamento sbagliato interno ma non si ricavano informazioni sensibili
CVE-2026-41136 
HTTPUEContextTransfer
amf/internal/sbi/api_communication.go 
CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N/E:P 5.5
LLM si impunta su availability, non trova integrity
Improper Input Validation → Integrity violation: Assenza di default nello switch sul Content-Type: il processor viene invocato con una request vuota non inizializzata. 

ANALISI LLM SENZA ANALISI STATICA DEL CODICE
FINDINGS AMF:
Logic Error / Uninitialized Data Processing:
Location: HTTPUEContextTransfer.
Pattern: In the switch str[0] block, there is no default case. If the content type is invalid, err is not set. The subsequent if err != nil check is skipped, and the handler calls the processor with an empty ueContextTransferRequest.
Impact: This leads to the processor handling a "null" or empty request, which could cause a panic (Nil Pointer Dereference) in the processor layer, leading to a Denial of Service (DoS) of the AMF.
Fix: Add a default case that sets an error.
CORRISPONDE ALLA CVE-2026-41136, NON TROVA INTEGRITY PERCHÈ MISCHIA TUTTI I FINDINGS COME CON LE ALTRE A MIO AVVISO IN CUI C’È DOS


Denial of Service (DoS) via Unbounded Request Body:
Location: All handlers calling c.GetRawData() (e.g., HTTPAMFStatusChangeSubscribeModify, HTTPCreateUEContext, HTTPEBIAssignment, HTTPRegistrationStatusUpdate, HTTPReleaseUEContext, HTTPUEContextTransfer, HTTPN1N2MessageTransfer, HTTPN1N2MessageSubscribe, HTTPAMFStatusChangeSubscribe).
Pattern: The use of c.GetRawData() in Gin reads the entire request body into memory without a size limit.
Impact: A compromised or malicious NF within the SBI can send a massive payload, causing the AMF to exhaust memory (OOM), leading to a crash. This results in a total loss of availability for all UEs managed by that AMF.
Fix: Use http.MaxBytesReader or a Gin middleware to limit the maximum allowed request body size.
VULN COME NELL’UDR SU GETRAWDATA, COMPORTA DOS
buttato giu amf, vuln seria e report fatto
https://github.com/free5gc/free5gc/security/advisories/GHSA-xwh9-c546-w74j
Denial of Service (OOM): GetRawData() senza limiti su nove handler SBI: crash dell'AMF confermato empiricamente. 
Type Mismatch in Context Storage (Logic Error/Potential Panic):
Location: Inconsistent use of sbi.IN_PB_DETAILS_CTX_STR across handlers.
Pattern: In HTTPAMFStatusChangeSubscribeModify and HTTPN1N2MessageSubscribe, the code stores a string (problemDetail.Cause). In HTTPCreateUEContext, HTTPEBIAssignment, HTTPRegistrationStatusUpdate, HTTPReleaseUEContext, HTTPUEContextTransfer, and HTTPN1N2MessageTransfer, it stores the entire models.ProblemDetails struct.
Impact: If a downstream middleware or logger attempts to retrieve this value using a type assertion (e.g., val.(string)), the application will panic when it encounters the struct, causing a DoS of the request handler.
Fix: Consistently store only one type (preferably the string cause or the full struct) across all handlers.
DA SCARTARE, E’ UN DIFETTO DI QUALITÀ DEL CODICE MA NON PORTA A VULNERABILITÀ PERCHÈ IL PROBLEMA DI DOS NON SI VERIFICA, È GESTITO DA GETSTRING CHE È DIFENSIVO E SICURO


Information Exposure via Error Messages:
Location: All handlers returning models.ProblemDetails (e.g., HTTPAMFStatusChangeSubscribeModify, HTTPCreateUEContext, etc.).
Pattern: The Detail field of the response is populated directly with err.Error().
Impact: This leaks internal implementation details, such as Go library errors or internal data model constraints. While mTLS/OAuth2 limits the attacker to other NFs, this aids in reconnaissance for crafting more precise attacks.
Fix: Use generic error messages for the client and log the detailed error internally.
Multiple SBI handlers in the free5gc AMF component (internal/sbi/api_communication.go) return the raw Go error.Error() string directly in the Detail field of the ProblemDetails JSON response when request body deserialization fails. This exposes internal implementation details — specifically, the fully-qualified names of internal Go structs used to model the API's data types — to any client able to reach the SBI endpoint.
BASSA VULNERABILITÀ MA SEGNALATA , DATA LEAK NELL’ERROR
https://github.com/free5gc/free5gc/security/advisories/GHSA-xw5p-5pgh-4xq5
Information Exposure through Error Message (CWE-209): err.Error() restituito nel campo Detail espone i nomi qualificati delle struct Go interne. 
Fragile Content-Type Parsing:


Location: HTTPCreateUEContext, HTTPUEContextTransfer, HTTPN1N2MessageTransfer.
Pattern: contentType := c.GetHeader("Content-Type") followed by strings.Split(contentType, ";") and accessing str[0].
Impact: If the Content-Type header is missing, c.GetHeader returns an empty string. strings.Split("", ";") returns a slice of length 1 containing an empty string. While it doesn't panic, it leads to a "wrong content type" error. More importantly, it lacks validation for the existence of the header before processing.
Fix: Validate that the Content-Type header is present and non-empty before attempting to split and switch on it.
COPERTA DA CVE-2026-41136
ANALISI LLM + ANALISI STATICA DEL CODICE
AMF
Logic Error / Functional Disablement: In HTTPN1N2MessageTransfer, the applicationjson case is explicitly hardcoded to return an error: err = fmt.Errorf("N1 and N2 datas are both Empty in N1N2MessgeTransfer"). This prevents the AMF from processing N1/N2 messages sent via JSON, which is a standard requirement for SBI communication, effectively breaking a core 5G signaling path.
BUG FUNZIONALE PIÙ CHE VULNERABILITÀ DI SICUREZZA
----------------------------------------------------------------------------------------------------------------
UDM
1 CVE, missing validator.IsValidSupi(), si può fare get per ottenere informazioni sensibili
CVE-2026-42459 
nudm-sdm
udm/internal/sbi/api_subscriberdatamanagement.go
CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:P 7.7
LLM STIMA OTTIMAMENTE
Improper Input Validation → Information Disclosure: Manca validator.IsValidSupi() su più handler SDM: identificatori arbitrari raggiungono il livello dati. 

ANALISI LLM SENZA ANALISI STATICA DEL CODICE
FINDINGS UDM:
Missing Input Validation (SUPI/UEID):
Location: HandleGetSmfSelectData, HandleGetSupi, HandleGetNssai, HandleGetSmData, HandleGetTraceData, HandleGetUeContextInSmfData, HandleModifyForSharedData.
Pattern: These handlers extract supi or ueId from c.Params.ByName() but fail to call validator.IsValidSupi() or validator.IsValidGpsi() before passing the value to the Processor layer.
Impact: While the SBI is protected by mTLS/OAuth2, allowing unvalidated identifiers into the business logic can lead to unexpected behavior in the database layer (e.g., querying for malformed keys) or potential injection if the downstream processor does not sanitize inputs.
Fix: Implement the same validation check used in HandleGetAmData or HandleUnsubscribe.
E’ LA CVE-2026-42459, la trova e la valida ottimamente


Unsafe JSON Unmarshaling of Query Parameters:
Location: getPlmnIDStruct
Pattern: The code takes a string directly from a URL query parameter (plmn-id) and passes it to json.Unmarshal([]byte(plmnIDJson), plmnIDStruct).
Impact: This is a highly unusual pattern. Query parameters are typically key-value pairs, not JSON blobs. If an attacker can bypass the API gateway or if an internal NF is compromised, they can send specially crafted JSON strings. While Go's json.Unmarshal is generally safe from memory corruption, this pattern is prone to "JSON injection" or logic errors if the PlmnId model allows unexpected fields.
Fix: Use standard query parameter parsing (e.g., ?mcc=xxx&mnc=yyy) instead of embedding JSON in a URL parameter.
EFFETTIVAMENTE NON CONTROLLA LA GRANDEZZA DEI PARAMETRI E L’UDM LI PASSA ALL’UDR FACENDOLO RALLENTARE E SOPRATTUTTO FACENDOGLI MANDARE INDIETRO INFO SENSIBILI, APERTO REPORT, vuln bassa
https://github.com/free5gc/free5gc/security/advisories/GHSA-42jf-j68x-57gx 
Information Exposure + Resource ConsumptionIl plmn-id non sanificato viene propagato nell'URL verso l'UDR, causando rallentamenti e leak di hostname interni. 


Information Leakage via Error Messages:
Location: HandleSubscribeToSharedData, HandleSubscribe, HandleModify, HandleModifyForSharedData
Pattern: The code returns err.Error() from c.GetRawData() or openapi.Deserialize directly in the ProblemDetails.Detail field sent back to the client.
Impact: Returning raw internal error strings can leak implementation details (e.g., library versions, internal structure names, or parsing logic) to a potentially malicious NF.
Fix: Use generic error messages for the client (e.g., "Invalid request body") and log the detailed error internally.
STESSA VULN TROVATA NELL’UDR, APERTO REPORT, SEMPRE LOW
https://github.com/free5gc/free5gc/security/advisories/GHSA-999x-p7pg-f5hm
Information Exposure through Error Message (CWE-209)Errori interni di deserializzazione restituiti verbatim al client. 


Inconsistent Parameter Handling (Logic Error):
Location: HandleGetTraceData
Pattern: plmnID := c.Query("plmn-id") is used here, whereas other "Get" handlers use the getPlmnIDStruct helper to parse a JSON object.
Impact: This creates a discrepancy in the API. If the UDM expects a JSON object for plmn-id (as per getPlmnIDStruct), HandleGetTraceData will receive the raw JSON string as the PLMN ID, likely causing the Processor to fail or look up the wrong data.
Fix: Use getPlmnIDStruct consistently across all handlers requiring PLMN ID.
CVE CONFERMATA, VULN MOLTO BASSA
https://github.com/free5gc/free5gc/security/advisories/GHSA-cm3j-hf76-5fg8
Inconsistent Input Handling (logic error): HandleGetTraceData usa c.Query() invece di getPlmnIDStruct: PLMN ID interpretato in modo diverso dagli altri handler. 


Logic Error in Route Matching (Path Traversal/Collision): The OneLayerPathHandlerFunc and TwoLayerPathHandlerFunc use strings.Contains(route.Pattern, supi) to match routes.
Impact: This is highly fragile. If a supi contains a substring that matches another route pattern, the wrong handler may be invoked. For example, if a SUPI was somehow named "shared-data", it could collide with the shared data routes.
Fix: Use a proper router (like Gin's built-in tree router) instead of manual string matching and loop-based dispatching.
CVE CONFERMATA, È VULNERABILE ma lieve vulnerability
https://github.com/free5gc/free5gc/security/advisories/GHSA-m8pq-hjj3-5x93
Route Collision / Improper Path Matching: Il dispatch basato su strings.Contains() può invocare l'handler sbagliato in caso di SUPI collidente con un pattern di route. 

ANALISI LLM + ANALISI STATICA DEL CODICE
UDM
Denial of Service (DoS) via Unbounded Request Body: The functions HandleSubscribeToSharedData, HandleSubscribe, and HandleModify use c.GetRawData(). This Gin method reads the entire request body into memory without any size limit. A malicious or compromised NF could send a massive payload, leading to memory exhaustion (Out-of-Memory) and crashing the UDM, impacting the availability of the entire 5G core's subscriber management.
NUOVA CVE, VULNERABILITÀ CHE GIÀ AVEVAMO RISCONTRATO NELLE ALTRE NF, MOLTO FORTE, NON SO PERCHÈ NON L’AVESSE TROVATA PRIMA, quel getrawdata()
https://github.com/free5gc/free5gc/security/advisories/GHSA-52p6-gfg7-hrw8
Denial of Service (OOM)GetRawData() senza limiti su HandleSubscribe, HandleSubscribeToSharedData, HandleModify. 


Unsafe Context Parameter Manipulation: In TwoLayerPathHandlerFunc and ThreeLayerPathHandlerFunc, the code manually modifies the c.Params slice (e.g., c.Params = append(...) or c.Params = tmpParams). This is a dangerous pattern in the Gin framework. Manually overwriting the parameters slice can lead to unpredictable routing behavior or logic errors where the wrong identifier is associated with a request, potentially leading to unauthorized data modification or access if the framework's internal state becomes inconsistent.
PROVATO MA NON SI VERIFICA, NON È VULNERABILE A RACE CONDITION


Missing Validation for Subscription IDs: In HandleUnsubscribeForSharedData, HandleUnsubscribe, and HandleModify, the subscriptionId is taken from the path and passed to the processor without any validation or sanitization.
NUOVA CVE, NON VALIDA PARAMETRO subid, MOLTO BASSA, NESSUN IMPATTO
https://github.com/free5gc/free5gc/security/advisories/GHSA-f72w-jgfw-hhm9 
Improper Input Validation (CWE-20/209) — impatto nullosubscriptionId accettato dal path senza alcun controllo formale. 
---------------------------------------------------------------------------------------------------------



CVE SCOPERTE DOPO ESPERIMENTO LLM SENZA ANALISI STATICA DEL CODICE

UDR: 4 NUOVE CVE
PCF: 0 NUOVE CVE
AMF: 2 NUOVE CVE
UDM: 4 NUOVE CVE

TOTALE: 10 NUOVE CVE

CVE SCOPERTE DOPO ESPERIMENTO LLM + ANALISI STATICA DEL CODICE

UDR: 4 NUOVE CVE
PCF: 0 NUOVE CVE
AMF: 2 NUOVE CVE
UDM: 4 NUOVE CVE + 2 NUOVE CVE

TOTALE: 10+2 NUOVE CVE

COMMENTO RAGIONAMENTO:
Il test con sonarqube sicuro non peggiora i risultati, anzi trova due nuove cve sull’UDM e valida molto meglio le CVE che già avevamo. Di sicuro insieme possono essere più utili rispetto alla sola analisi statica del codice che non aveva prodotto risultati concreti.

Ho paura che però possa esserci un condizionamento dato dall’aumento delle rep che forse ha portato a nuove CVE e non dall’analisi statica del codice. Non so.

MATRICE CLASSE X NF


Classe di vulnerabilità
UDR
PCF
AMF
UDM
TOT
DoS
2
0
1
1
4
Improper input validation
3
0
0
1
4
Information Exposure
0
0
1
2
3
Logic Error
0
0
0
2
2
Totale
5
0
2
6
13




