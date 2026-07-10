# Validation Package — Task 5: PCF CORS Misconfiguration

## Source material

**File originale:** `File_Free5gc_Vulnerabili/PCF/api_oam.go` (65 righe)  
**Vulnerabilità di riferimento:** V1 — CORS Misconfiguration (GHSA-98cp-84m9-q3qp)  
**Task definition:** `docs/tasks/task5_vuln_pcf.md`  
**Rubric:** `docs/tasks/task5_vuln_pcf_sol.md`

Il task fornisce al modello lo snippet Go della funzione `setCorsHeader` del PCF OAM handler, senza indicazioni su dove cercare la vulnerabilità.

---

## Vulnerabilità target (GT)

`setCorsHeader` configura il middleware CORS con `AllowAllOrigins: true` e `AllowCredentials: true` simultaneamente. Per la CORS spec (Fetch Standard §3.2), questa combinazione è invalida: `Access-Control-Allow-Credentials: true` è incompatibile con `Access-Control-Allow-Origin: *`. Qualsiasi client non-browser può eseguire richieste cross-origin credenzializzate verso `/am-policy/:supi`.

**Fix corretto:** sostituire `AllowAllOrigins: true` con `AllowOrigins: []string{...}` (whitelist esplicita); rimuovere gli header manuali ridondanti.

---

## Rubrica (4 categorie, max 9 punti)

| Categoria | Max | Cosa valuta |
|---|---|---|
| `vulnerability_identified_score` | 3 | Identifica la combinazione AllowAllOrigins + AllowCredentials come violazione spec |
| `location_precision_score` | 2 | Cita `setCorsHeader` / il blocco `cors.Config` |
| `impact_assessment_score` | 2 | Impatto specifico 5G (accesso a dati policy SUPI-indexed) |
| `fix_quality_score` | 2 | Fix corretto: whitelist esplicita + rimozione header ridondanti |

Soglia "correct": normalized score ≥ 0.7 (≥ 6.3/9 punti).

---

## Risultati — Expert (rep1)

**File JSON:** `results/1A/expert/task5_vuln_pcf_rep1.json`  
**Verdict:** correct | **Attempts:** 1 | **Score:** 8/9 (0.889) | **Confidence:** 1.0

| Categoria | Score |
|---|---|
| `vulnerability_identified_score` | 2/3 |
| `location_precision_score` | 2/2 |
| `impact_assessment_score` | 2/2 |
| `fix_quality_score` | 2/2 |

**Answer:**
> The primary vulnerability is the dynamic and overly permissive application of CORS configuration within the request handler, which is inefficient and exposes the endpoint to overly broad cross-origin requests.

**Reasoning:**
> 1. Vulnerability Class: CORS Misconfiguration and Inefficient Middleware Application.
> 2. Location: The `setCorsHeader` function, specifically where `s.router.Use(cors.New(...))` is called inside the request handler flow, and the manual header setting.
> 3. Security Impact in 5G Context: In a 5G core environment, SBI endpoints handle sensitive network state and policy information. Allowing `AllowAllOrigins: true` and broad methods/headers significantly increases the attack surface. An attacker from any domain can potentially interact with these sensitive OAM functions, leading to unauthorized policy retrieval or manipulation if the downstream processor is not perfectly secured.
> 4. Proposed Fix: CORS middleware should be applied once globally to the router setup, not dynamically per request. The configuration should be reviewed to ensure only necessary origins and methods are allowed. The manual header setting in `setCorsHeader` should be removed if the middleware handles it correctly.
>
> Additionally, while not a direct injection vulnerability in this snippet, the lack of strict input validation on the extracted path parameter `supi` before passing it to the processor function (`s.Processor().HandleOAMGetAmPolicyRequest`) poses a risk of path traversal or logic bypass if the downstream logic is flawed. Input validation should be enforced immediately upon extraction.

**Dove manca 1 punto:** `vulnerability_identified_score = 2/3`. Il modello identifica `AllowAllOrigins` come problema e ne descrive l'impatto, ma non collega esplicitamente la combinazione `AllowAllOrigins + AllowCredentials` come violazione specifica della CORS spec. Descrive il rischio correttamente senza nominare l'incompatibilità tecnica.

**Feedback judge:**
> "The only minor point for improvement would be explicitly stating that the combination of AllowAllOrigins and AllowCredentials is the specific violation of the CORS specification, which would achieve the maximum score for vulnerability identification."

---

## Risultati — Beginner (rep1)

**File JSON:** `results/1A/beginner/task5_vuln_pcf_rep1.json`  
**Verdict:** correct | **Attempts:** 1 | **Score:** 9/9 (1.0) | **Confidence:** 1.0

| Categoria | Score |
|---|---|
| `vulnerability_identified_score` | 3/3 |
| `location_precision_score` | 2/2 |
| `impact_assessment_score` | 2/2 |
| `fix_quality_score` | 2/2 |

**Answer:**
> The code exhibits severe CORS misconfiguration by allowing all origins and relies on manual header setting, and it lacks robust input validation for path parameters.

**Reasoning:**
> 1. Vulnerability Class: CORS Misconfiguration and Insecure Configuration.
>    Location: `setCorsHeader` function.
>    Impact in 5G Context: Setting `AllowAllOrigins: true` and allowing credentials (`AllowCredentials: true`) means any external client (or internal component with access to the network) can make cross-origin requests to this SBI endpoint. If this endpoint handles sensitive policy information (AmPolicy), this could lead to unauthorized data exposure or denial of service if not properly authenticated.
>    Proposed Fix: Restrict `AllowAllOrigins` to specific, known origins (e.g., the trusted NRF/SMF components) and remove the manual header setting, relying solely on the configured middleware, or ensure the middleware is correctly applied globally.
>
> 2. Vulnerability Class: Potential Input Validation/Injection (Path Parameter Handling).
>    Location: `HTTPOAMGetAmPolicy` function, specifically extracting `supi`.
>    Impact in 5G Context: The `supi` parameter is directly passed to the internal processor (`s.Processor().HandleOAMGetAmPolicyRequest`). If this parameter is not strictly validated, an attacker could attempt to probe for valid or invalid SUPIs, potentially leading to information disclosure or denial of service against the PCF.
>    Proposed Fix: Implement strict validation for the `supi` parameter immediately upon extraction. Ensure that the value is checked against expected formats and that the requested policy ID actually exists before processing.
>
> 3. Code Smell/Misconfiguration: Poor Middleware Implementation.
>    Location: `setCorsHeader` function, where `s.router.Use(...)` is called inside a request-handling context.
>    Impact: Calling `Use` inside a function meant to handle a specific request is incorrect — it registers middleware globally each time a request is received. This suggests a misunderstanding of how Gin middleware should be applied, potentially leading to inconsistent security policy enforcement.
>    Proposed Fix: The CORS middleware configuration should be applied once when the router is initialized, not dynamically within a request handler function.

**Dove prende il punto in più:** nomina esplicitamente la coppia `AllowAllOrigins: true` + `AllowCredentials: true` come la configurazione problematica, raggiungendo il criterio massimo della rubrica.

**Feedback judge:**
> "The agent correctly identified the critical CORS misconfiguration, specifically noting the dangerous combination of `AllowAllOrigins: true` and `AllowCredentials: true`, which violates CORS specifications. The analysis was highly precise, pointing directly to the `setCorsHeader` function and the middleware configuration. Furthermore, the agent provided a strong, context-aware impact assessment by relating the vulnerability to unauthorized access of sensitive UE policy data (AmPolicy) within the 5G core."

---

## Valutazione del sistema (Nicolò)

**Risultato:** entrambi i ruoli trovano la vulnerabilità al primo tentativo, nessun retry.

**Anomalia minore:** beginner (9/9) supera expert (8/9). Il prompt expert produce un'analisi architetturale più ampia (nota anche l'abuso del middleware dinamico per-request), ma questo la allontana dal criterio esatto della rubrica. Il prompt beginner produce un'analisi più focalizzata che centra il punto preciso (la coppia AllowAllOrigins + AllowCredentials).

**Affidabilità della rubrica:** il criterio `vulnerability_identified_score` discrimina correttamente i due livelli di risposta. Il delta 2 vs 3 cattura una differenza reale nella precisione tecnica.

---

## Domande per il validatore

1. **Correttezza del finding:** la vulnerabilità identificata (CORS AllowAllOrigins + AllowCredentials) corrisponde a quanto identificato manualmente in `api_oam.go`?
2. **Qualità ragionamento expert:** la risposta expert descrive correttamente il rischio anche senza nominare esplicitamente la violazione spec — è una risposta "quasi corretta" o manca qualcosa di sostanziale?
3. **Criterio rubrica:** il criterio `vulnerability_identified_score=3` richiede di nominare la coppia come violazione spec — ti sembra un requisito ragionevole per un analista di sicurezza, o è troppo accademico?
4. **False positives:** entrambi i ruoli aggiungono osservazioni su "input validation for path parameters (`supi`)" e "poor middleware lifecycle" — questi sono finding validi o falsi positivi per questo file?
