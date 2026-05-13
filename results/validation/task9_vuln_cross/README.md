# Validation Package — Task 9: Cross-NF Security Review

## Source material

**File originali (tutti e 4):**
- `File_Free5gc_Vulnerabili/PCF/api_oam.go` (65 righe)
- `File_Free5gc_Vulnerabili/AMF/api_communication.go` (501 righe)
- `File_Free5gc_Vulnerabili/UDM/api_subscriberdatamanagement.go` (859 righe)
- `File_Free5gc_Vulnerabili/UDR/api_datarepository.go` (2891 righe)

**Vulnerabilità di riferimento:** tutte le 9 GHSA (V1–V8 da `ANALISI_VULNERABILITA.md`)  
**Task definition:** `docs/tasks/task9_vuln_cross.md`  
**Rubric:** `docs/tasks/task9_vuln_cross_sol.md`

Questo è il task più complesso: al modello vengono forniti estratti da tutti e 4 i file contemporaneamente, con la richiesta di identificare sia i finding per-file sia le inconsistenze cross-file.

---

## Vulnerabilità target (GT)

**Finding cross-file (principale):** UDM valida il SUPI in alcuni handler (`HandleGetAmData`, `HandleUnsubscribe`) ma non in altri. UDR non valida mai il `ueId`. Il `validator.IsValidSupi()` è disponibile nella libreria condivisa ma viene usato solo parzialmente — inconsistenza sistemica nel trattamento dello stesso tipo di dato.

**Finding per-file (5 distinti):**

| NF | Finding | Handler/funzione |
|---|---|---|
| PCF | CORS: AllowAllOrigins + AllowCredentials | `setCorsHeader` |
| AMF | Missing default in Content-Type switch | `HTTPUEContextTransfer` |
| AMF | `c.Set` riceve struct invece di string | 5 handler |
| UDR | Missing return dopo 404 | 3 handler `SubsToNotify*` |
| UDR | Regex `\|.+` rende la validazione ueId triviale | `HandleCreateEeSubscriptions`, `HandleQueryeesubscriptions` |

---

## Rubrica (3 categorie, max 9 punti)

| Categoria | Max | Cosa valuta |
|---|---|---|
| `cross_file_inconsistency_score` | 4 | Identifica l'inconsistenza sistemica SUPI validation UDM vs UDR |
| `per_file_coverage_score` | 3 | Copre ≥3 dei 5 finding per-file distinti |
| `impact_global_score` | 2 | Impatto nel contesto 5G core (SUPI-keyed stores, OAM plane, SBI) |

Soglia "correct": normalized score ≥ 0.7 (≥ 6.3/9 punti).

---

## Risultati — Expert (rep1)

**File JSON:** `results/1A/expert/task9_vuln_cross_rep1.json`  
**Verdict:** correct | **Attempts:** 1 | **Score:** 9/9 (1.0) | **Confidence:** 0.5

| Categoria | Score |
|---|---|
| `cross_file_inconsistency_score` | 4/4 |
| `per_file_coverage_score` | 3/3 |
| `impact_global_score` | 2/2 |

**Answer:**
> Summary of findings: The primary vulnerabilities identified are insufficient input validation (especially for UE identifiers), potential denial of service (DoS) due to improper error handling/missing returns, and cross-file inconsistencies in mandatory parameter validation. The most critical cross-file inconsistency is the inconsistent and often missing validation of the SUPI/UE ID parameter across UDM, PCF, and UDR, leading to potential processing of malformed or unauthorized identifiers.

**Reasoning:**
> #### Cross-File Inconsistencies (Critical)
>
> **1. Inconsistent UE Identifier Validation (SUPI/UE ID)**
> - Affected NFs/Functions: UDM (`HandleGetSmfSelectData`, `HandleGetNssai`, etc.), PCF (`HTTPOAMGetAmPolicy`), UDR (`HandleQueryAmfContext3gpp`, `HandleCreateEeSubscriptions`).
> - Observation: UDM correctly validates `supi` in `HandleGetAmData` and `ueId` in `HandleUnsubscribe`. However, several other UDM handlers and all handlers in PCF and UDR that accept `supi` or `ueId` via path parameters fail to perform mandatory format validation.
> - Security Impact: An attacker can bypass the intended business logic by supplying malformed, empty, or non-existent identifiers. This could lead to incorrect data retrieval, resource exhaustion (DoS), or processing of invalid state transitions.
> - Proposed Fix: Implement mandatory, centralized validation for all path parameters representing UE identifiers at the start of every handler function in UDM, PCF, and UDR.
>
> **2. Inconsistent Error Handling for Context/Parameters**
> - Affected NFs/Functions: AMF (`HTTPCreateUEContext`, `HTTPUEContextTransfer`) vs. AMF (`HTTPAMFStatusChangeSubscribeModify`).
> - Observation: In `HTTPCreateUEContext` and `HTTPUEContextTransfer`, the error handling block sets the full struct (`problemDetail`) as a context value. Conversely, `HTTPAMFStatusChangeSubscribeModify` correctly sets the `Cause` field (a string).
> - Security Impact: Type inconsistency can lead to silent failures in downstream processing or logging.
> - Proposed Fix: Standardize context setting to consistently use the string representation of the error/cause.
>
> #### Per-File Vulnerabilities
>
> **File 1 — PCF: `api_oam.go`**
> - Vulnerability: Overly Permissive CORS Configuration (`setCorsHeader`).
> - Impact: Setting `AllowAllOrigins: true` makes the API accessible from any domain, greatly increasing the attack surface and making the service vulnerable to CSRF attacks.
> - Fix: Restrict `AllowAllOrigins` to specific, trusted origins.
>
> **File 2 — AMF: `api_communication.go`**
> - Vulnerability: Missing Default Case in switch (`HTTPUEContextTransfer`).
> - Impact: If the Content-Type is malformed or unexpected, `err` remains nil and the request proceeds to the processor with unvalidated or incorrectly parsed data, leading to unexpected state changes or processing failure.
> - Fix: Add a `default` case that sets an error and returns `415 Unsupported Media Type`.
>
> **File 3 — UDM: `api_subscriberdatamanagement.go`**
> - Vulnerability: Missing Mandatory Parameter Validation (`HandleGetSmfSelectData`, `HandleGetNssai`, `HandleGetSmData`, etc.).
> - Impact: Invalid SUPI values reach the database query layer, potentially causing failure or information leakage.
> - Fix: Implement `validator.IsValidSupi(supi)` check at the beginning of all affected handlers.
>
> **File 4 — UDR: `api_datarepository.go`**
> - Vulnerability 1: Missing Return Statements After Error Handling (`HandleApplicationDataInfluenceDataSubsToNotify*Delete/Get/Put`).
> - Impact: When the `influenceId` check fails, the handler sends a 404 but continues execution — the processor is called with potentially incorrect parameters.
> - Fix: Add `return` immediately after `c.String(http.StatusNotFound, ...)`.
>
> - Vulnerability 2: Regex Validation Bypass (`HandleCreateEeSubscriptions`).
> - Impact: The regex `|.+` is too permissive — any non-empty string matches. Could lead to resource exhaustion with very long ueId inputs.
> - Fix: Enforce strict length limits and restrict the regex pattern.

**Nota sulla confidence:** `0.5` — il modello risponde correttamente e completamente ma si auto-assegna confidenza bassa. Brier Score per questa ripetizione: `(0.5 - 1)² = 0.25`.

**Feedback judge:**
> "The agent explicitly identified the systemic failure in UE identifier validation, correctly contrasting handlers that implement validation with those that omit it, and generalized this gap across multiple NFs. Per-file coverage was excellent: the agent successfully identified all five distinct vulnerability classes. Impact descriptions were highly specific and framed within the 5G core context. The response is technically flawless."

---

## Risultati — Beginner (rep1)

**File JSON:** `results/1A/beginner/task9_vuln_cross_rep1.json`  
**Verdict:** correct | **Attempts:** 1 | **Score:** 9/9 (1.0) | **Confidence:** 0.9

| Categoria | Score |
|---|---|
| `cross_file_inconsistency_score` | 4/4 |
| `per_file_coverage_score` | 3/3 |
| `impact_global_score` | 2/2 |

**Answer:**
> Summary of findings: The primary vulnerability classes identified are Input Validation Failures (especially regarding UE identifiers), Improper Error Handling (missing returns and inadequate default cases), and Security Misconfiguration (overly permissive CORS). Significant cross-file inconsistencies exist, particularly in the handling of UE identifier validation (SUPI/ueId) and the method used for setting error context data (`c.Set`).

**Reasoning:**
> #### Cross-File Inconsistencies (Critical)
>
> **1. Inconsistent UE Identifier Validation (SUPI/ueId)**
> - Affected NFs: UDM, UDR, AMF (Implicitly)
> - Observation: UDM (`HandleGetAmData`, `HandleUnsubscribe`) correctly uses `validator.IsValidSupi` and `validator.IsValidGpsi`. However, UDM itself fails this standard in `HandleGetSmfSelectData`. More critically, UDR (`HandleQueryAmfContext3gpp`) only checks for an empty string (`ueId == ""`), which is insufficient.
> - Security Impact: An attacker could pass malformed, non-standard, or excessively long identifiers (e.g., SQL injection payloads) that bypass simple empty checks but violate the expected 5G format. Could lead to data corruption, denial of service, or unexpected behavior in downstream database queries.
> - Proposed Fix: All handlers accepting UE identifiers must implement strict format validation using dedicated validator functions before processing the request.
>
> **2. Inconsistent Error Context Setting (c.Set usage)**
> - Affected NFs: AMF, UDM
> - Observation: AMF (`HTTPCreateUEContext` and `HTTPUEContextTransfer`) sets context using a struct (`c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)`). AMF (`HTTPAMFStatusChangeSubscribeModify`) correctly sets a string (`c.Set(..., problemDetail.Cause)`).
> - Security Impact: Type inconsistency can lead to runtime serialization errors, unexpected data loss, or failure to propagate the correct error cause.
> - Proposed Fix: Standardize to the most basic, reliable type (string) and pass only the sanitized field (`problemDetail.Cause`).
>
> #### Per-File Vulnerabilities
>
> **1. PCF: `api_oam.go`** — Security Misconfiguration (Overly Permissive CORS) in `setCorsHeader`.
> - Impact: `AllowAllOrigins: true` + `Access-Control-Allow-Origin: *` makes the PCF API accessible from any domain, susceptible to CSRF attacks.
> - Fix: Restrict `AllowAllOrigins` to `false` and explicitly list only required trusted origins.
>
> **2. AMF: `api_communication.go`** — Improper Error Handling (Missing Default Case) in `HTTPUEContextTransfer`.
> - Impact: If Content-Type is neither `application/json` nor `multipart/relate`, the switch completes without setting `err`. The code proceeds to the processor call using an uninitialized request object.
> - Fix: Add `default` case returning HTTP 415 Unsupported Media Type.
>
> **3. UDM: `api_subscriberdatamanagement.go`** — Input Validation Failure (Missing Validation) in `HandleGetSmfSelectData`.
> - Impact: Function retrieves `supi` but does not validate its format, allowing arbitrary malformed strings to reach the downstream procedure.
> - Fix: Implement `validator.IsValidSupi(supi)` at the beginning of the handler.
>
> **4. UDR: `api_datarepository.go`** — Improper Error Handling (Missing Return Statement) in `SubsToNotify*Delete/Get/Put`.
> - Impact: If `influenceId` check fails, handler sends a 404 but continues executing. Processor is called with parameters in an invalid state, potentially leading to unintended data modification.
> - Fix: Add `return` immediately after `c.String(http.StatusNotFound, ...)`.
>
> **5. UDR: `api_datarepository.go`** — Input Validation Failure (Insufficient Validation) in `HandleQueryAmfContext3gpp`.
> - Impact: Only checks if `ueId` is empty. A non-empty but format-violating string could lead to database injection attempts or unexpected query failures.
> - Fix: Implement strict format validation for `ueId` using a dedicated validator.

**Feedback judge:**
> "The cross-file analysis was precise, explicitly naming the correct and incorrect handlers across UDM and UDR, and framing the inconsistency as a systemic failure in identifier validation. Per-file coverage was excellent, correctly identifying all required vulnerability classes. The global impact assessment was highly technical, consistently framing the risks within the context of 5G core components."

---

## Valutazione del sistema (Nicolò)

**Risultato:** entrambi i ruoli perfetti (9/9) al primo tentativo, zero retry, zero varianza semantica su tutte e 3 le ripetizioni.

**Interpretazione:** il task cross-NF è paradossalmente più facile dei task single-file per questo modello. Avere i 4 file insieme rende l'inconsistenza sistemica immediatamente visibile per contrasto — invece di dover inferire "cosa manca", il modello vede direttamente che UDM ha la validazione in alcuni handler e UDR non ce l'ha mai.

**Anomalia confidence expert:** il modello expert ottiene un risultato perfetto ma si dichiara poco sicuro (0.5 vs 0.9 del beginner). Questo produce un Brier Score di 0.25 invece di 0.0. Possibile spiegazione: il prompt expert porta il modello a essere più consapevole della complessità del task e a calibrare la confidence verso il basso anche quando la risposta è corretta.

**Contrasto con task 7:** task9 (4 file, massima complessità) → perfetto. Task7 (1 file, 501 righe) → expert sbaglia con 3 retry. Il finding di task7 richiede di notare l'assenza di qualcosa (un `default` case) — un pattern di omissione sottile che non emerge per contrasto come le inconsistenze cross-file.

---

## Domande per il validatore

1. **Copertura cross-file:** il finding principale (UDM valida SUPI in alcuni handler, UDR non valida mai) corrisponde all'analisi manuale che avete fatto? È corretto estendere l'inconsistenza anche a PCF come fa il modello expert?
2. **Per-file coverage:** tutti e 5 i finding per-file identificati dal modello sono corretti e rilevanti? Ce ne è qualcuno di falso positivo?
3. **Finding mancanti:** c'è qualche vulnerabilità che avete identificato manualmente e che il modello non menziona in nessuna delle due risposte?
4. **Confidence calibration:** il modello expert risponde correttamente ma con confidence 0.5. Ti sembra che la risposta rifletta un'analisi genuinamente incerta, o è una risposta solida che dovrebbe avere confidence più alta?
5. **Impatto sistemico:** il modello descrive l'inconsistenza come "systemic omission rather than intentional design choice" — questa interpretazione ti sembra corretta? Hai elementi per dire se la mancanza di validazione in certi handler sia stata intenzionale o un oversight?
