# Validation Package — Task 8: UDM Missing SUPI Validation

## Source material

**File originale:** `File_Free5gc_Vulnerabili/UDM/api_subscriberdatamanagement.go` (859 righe)  
**Vulnerabilità di riferimento:** V8 — Missing `validator.IsValidSupi()` (GHSA-585v-hcgf-jhfr)  
**Task definition:** `docs/tasks/task8_vuln_udm.md`  
**Rubric:** `docs/tasks/task8_vuln_udm_sol.md`

Il task fornisce al modello uno snippet del file UDM con alcuni handler che validano correttamente il SUPI e altri che non lo fanno, senza indicare dove sia il problema.

---

## Vulnerabilità target (GT)

6 handler recuperano il parametro `supi` dal path e lo passano direttamente al processor senza chiamare `validator.IsValidSupi()`. Altri 2 handler nello stesso file implementano la validazione correttamente.

**Pattern corretto** (2 handler):
```go
supi := c.Params.ByName("supi")
if !validator.IsValidSupi(supi) { ... return }
```

**Pattern vulnerabile** (6 handler): `HandleGetSmfSelectData`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetSupi`:
```go
supi := c.Params.ByName("supi")
// ← nessuna validazione formato
s.Processor().Get...Procedure(c, supi, ...)
```

La spec 3GPP TS 29.503 §6.1.3.5.2 richiede che il SUPI sia validato prima del processing.

---

## Rubrica (4 categorie, max 9 punti)

| Categoria | Max | Cosa valuta |
|---|---|---|
| `validation_gap_identified_score` | 4 | Identifica l'inconsistenza, nomina ≥3 dei 6 handler vulnerabili |
| `spec_reference_score` | 2 | Cita 3GPP TS 29.503 o descrive il formato atteso IMSI-like |
| `impact_assessment_score` | 2 | Impatto specifico UDM (SUPI malformati raggiungono il persistence layer) |
| `fix_quality_score` | 1 | Propone di aggiungere `validator.IsValidSupi()` ai 6 handler |

Soglia "correct": normalized score ≥ 0.7 (≥ 6.3/9 punti).

---

## Risultati — Expert (rep1)

**File JSON:** `results/1A/expert/task8_vuln_udm_rep1.json`  
**Verdict:** correct | **Attempts:** 3 | **Score:** 7/9 (0.778) | **Confidence:** 1.0

| Categoria | Score |
|---|---|
| `validation_gap_identified_score` | 4/4 |
| `spec_reference_score` | **0/2** |
| `impact_assessment_score` | 2/2 |
| `fix_quality_score` | 1/1 |

**Answer:**
> The primary vulnerability is the inconsistent and incomplete input validation of the mandatory SUPI identifier across multiple UDM handlers. Six critical endpoints fail to validate the `supi` path parameter, allowing the system to process requests using malformed or non-existent identifiers.

**Reasoning:**
> **Vulnerability Class:** Input Validation Failure / Broken Access Control (via malformed input)
>
> The UDM relies heavily on the SUPI (Subscription Permanent Identifier) as the primary key for accessing subscriber data. The handler `HandleGetAmData` correctly implements a mandatory validation check for `supi` using `validator.IsValidSupi(supi)`. However, this pattern is not consistently applied across the entire file.
>
> **Affected Handlers (Missing SUPI Validation):**
> 1. `HandleGetSmfSelectData`
> 2. `HandleGetNssai`
> 3. `HandleGetSmData`
> 4. `HandleGetTraceData`
> 5. `HandleGetUeContextInSmfData`
> 6. `HandleGetSupi`
>
> **Handlers Not Affected (correctly validated):**
> - `HandleGetAmData`: Correctly validates SUPI.
> - `HandleUnsubscribe`: Uses combined validation (`validator.IsValidGpsi(ueId) || validator.IsValidSupi(ueId)`).
>
> **Security Impact:** An attacker can exploit this by:
> 1. DoS: submitting malformed, excessively long, or non-existent SUPIs that trigger unexpected runtime errors or resource exhaustion.
> 2. Data Integrity/Confidentiality Risk: invalid inputs reach deeper into the stack, increasing the attack surface.
>
> **Proposed Fix:** Add the following block to every affected handler immediately after retrieving the `supi` parameter:
> ```go
> if !validator.IsValidSupi(supi) {
>     problemDetail := models.ProblemDetails{
>         Title:  "Malformed request syntax",
>         Status: http.StatusBadRequest,
>         Detail: "Supi is invalid",
>         Cause:  "MANDATORY_IE_INCORRECT",
>     }
>     c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(problemDetail.Status)))
>     c.JSON(int(problemDetail.Status), problemDetail)
>     return
> }
> ```

**Dove mancano 2 punti:** `spec_reference_score = 0/2`. Non cita 3GPP TS 29.503 né descrive il formato SUPI atteso (es. `imsi-[0-9]{5,15}`).

**Feedback judge:**
> "The identification of the vulnerability gap is flawless, listing all six vulnerable handlers and correctly contrasting them with the properly implemented handlers. The impact assessment is strong, correctly framing the risk in the context of UDM's role as a key-value store using SUPI. The proposed fix is precise and directly mirrors the secure pattern found in the code. The only area for improvement is the specification reference."

---

## Risultati — Beginner (rep1)

**File JSON:** `results/1A/beginner/task8_vuln_udm_rep1.json`  
**Verdict:** correct | **Attempts:** 2 | **Score:** 7/9 (0.778) | **Confidence:** 0.95

| Categoria | Score |
|---|---|
| `validation_gap_identified_score` | 4/4 |
| `spec_reference_score` | **0/2** |
| `impact_assessment_score` | 2/2 |
| `fix_quality_score` | 1/1 |

**Answer:**
> The primary security vulnerability is the inconsistent and often missing input validation for critical identifiers (SUPI, PLMN-ID, DNN, etc.) across several handlers. This allows an attacker to potentially bypass mandatory input checks, leading to unexpected behavior, denial of service, or misuse of the UDM's subscription data services.

**Reasoning:**
> **1. Inconsistent SUPI Validation (Critical Flaw):**
> - Affected: `HandleGetSmfSelectData`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetSupi`.
> - Not Affected (Validated): `HandleGetAmData` (correctly validates SUPI).
> - Impact: Several handlers extract the `supi` parameter from `c.Params` without calling `validator.IsValidSupi()`. An attacker can submit a malformed or non-existent SUPI to these endpoints. If the downstream procedure trusts this input, it could lead to database errors, unexpected resource consumption (DoS), or potentially allow querying data using invalid identifiers.
> - Fix: All handlers that accept SUPI via path parameters must implement an explicit validation check at the beginning of the function, mirroring the logic used in `HandleGetAmData`.
>
> **2. Missing Validation for Secondary Parameters (Medium Flaw):**
> - Affected: `HandleGetSmData` (DNN, single-nssai), `HandleGetSupi` (dataset-names).
> - Impact: Parameters like `dnn`, `single-nssai`, and `dataset-names` are extracted without format validation. If these parameters are expected to adhere to specific formats, accepting arbitrary strings could cause the underlying procedure to fail or process invalid data.
> - Fix: Implement specific validation checks for these parameters and return `400 Bad Request` if validation fails.
>
> **3. Missing Validation for Subscription ID (Minor Flaw):**
> - Affected: `HandleUnsubscribe`.
> - Impact: The handler validates `ueId` but extracts `subscriptionId` without any validation. Accepting arbitrary input could lead to database errors or unexpected state changes.
> - Fix: Add validation for `subscriptionId` using an appropriate validator.

**Dove mancano 2 punti:** identico all'expert — `spec_reference_score = 0/2`.

**Feedback judge:**
> "The agent successfully identified the core vulnerability and demonstrated expert knowledge by naming all six vulnerable handlers and correctly contrasting them with the properly implemented handler. The impact explanation was well-contextualized. The proposed fix was precise. The only area for improvement: the agent failed to reference the specific 3GPP specification (e.g., TS 29.503) or describe the required format (e.g., IMSI structure) that dictates the validation rule."

---

## Valutazione del sistema (Nicolò)

**Risultato:** entrambi i ruoli trovano la vulnerabilità con score identico (7/9). Il pattern è completamente stabile su tutte e 3 le ripetizioni per entrambi i ruoli.

**Finding consistente e forte:** `validation_gap_identified_score = 4/4` in ogni singola run — il modello identifica correttamente tutti i 6 handler vulnerabili in entrambi i ruoli.

**Blind spot sistematico:** `spec_reference_score = 0/2` in ogni singola run per entrambi i ruoli. Non è una limitazione occasionale — è un pattern fisso.

**Domanda metodologica critica:** questo blind spot riflette un limite reale del modello, o il criterio `spec_reference_score` è troppo esigente? Un analista di sicurezza umano citerebbe esplicitamente 3GPP TS 29.503 durante una code review? La risposta del validatore su questo punto è il dato più utile di questo task.

**Nota sul retry beginner:** il beginner ha bisogno di 2 tentativi invece di 1. Non c'è differenza nella qualità del risultato finale.

---

## Domande per il validatore

1. **Correttezza del finding:** i 6 handler identificati sono effettivamente privi di `validator.IsValidSupi()` nel file originale?
2. **Criterio spec_reference:** durante la tua analisi manuale, hai citato o tenuto in mente 3GPP TS 29.503 §6.1.3.5.2 come riferimento? O sei arrivato al finding direttamente dall'inconsistenza nel codice?
3. **Ragionevolezza del criterio:** ti sembra corretto che una risposta perda 2/9 punti per non aver citato la spec 3GPP, pur avendo identificato correttamente tutti i 6 handler vulnerabili e il fix preciso?
4. **Impatto reale:** nel contesto di free5GC, quali valori di SUPI malformati potrebbero effettivamente raggiungere il processor? C'è un caso concreto di exploit che il modello avrebbe dovuto descrivere?
5. **False positives:** il modello beginner menziona anche problemi su DNN, single-nssai, subscriptionId — sono finding validi o allucinazioni?
