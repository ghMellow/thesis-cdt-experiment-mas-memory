# Solution — Task 8 (Security Review: UDM Subscriber Data Management Handler)

**ID:** task8_vuln_udm_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent  
**CVE reference:** GHSA-585v-hcgf-jhfr

---

## Ground Truth

```json
{
  "answer": "Inconsistent SUPI validation: HandleGetAmData and HandleUnsubscribe correctly validate the SUPI/GPSI format using validator functions, but HandleGetSmfSelectData, HandleGetNssai, HandleGetSmData, HandleGetTraceData, HandleGetUeContextInSmfData, and HandleGetSupi pass the raw supi path parameter directly to the processor without any format validation, violating TS 29.503 §6.1.3.5.2",
  "type": "textual_security_review"
}
```

## GT Rationale

### Core finding — Missing SUPI validation in 6 of 8 handlers (CWE-20 / GHSA-585v-hcgf-jhfr)

`HandleGetAmData` (lines 30–68) is the reference implementation: it calls `validator.IsValidSupi(supi)` before passing the value downstream. `HandleUnsubscribe` similarly calls `validator.IsValidGpsi(ueId) || validator.IsValidSupi(ueId)`.

However, six other handlers that also receive a SUPI-keyed path parameter perform no format validation whatsoever:

| Handler | Data returned |
|---|---|
| `HandleGetSmfSelectData` | SMF Selection Subscription Data |
| `HandleGetNssai` | Subscribed Network Slice Selection Assistance Info |
| `HandleGetSmData` | Session Management Subscription Data |
| `HandleGetTraceData` | Trace Configuration Data |
| `HandleGetUeContextInSmfData` | UE Context in SMF Data |
| `HandleGetSupi` | Multiple data sets (bulk endpoint) |

Each of these calls `s.Processor().Get*Procedure(c, supi, ...)` with an unvalidated `supi`. The SUPI then propagates to the UDR via the processor, where it is used as a MongoDB document key.

**Impact in 5G context:**
1. **Spec violation**: TS 29.503 §6.1.3.5.2 mandates SUPI format validation at the SBI layer. A SUPI that does not match `^(imsi-[0-9]{5,15}|nai-.+|...)$` should never reach the UDR.
2. **Data exposure**: A caller can probe for subscription data using arbitrary strings as SUPI keys, including empty-prefix strings or encoding variants, potentially hitting documents that should not be accessible.
3. **Downstream surface**: Malformed SUPI values could interfere with collection indexes or trigger unexpected behavior in the UDR's BSON filter construction.
4. **Cross-NF inconsistency**: The same subscription data accessible via the validated `HandleGetAmData` path is also accessible via the unvalidated `HandleGetSmfSelectData` or `HandleGetNssai` path — bypassing the intended validation gate.

**Fix:** Add `if !validator.IsValidSupi(supi) { ... return }` (identical to `HandleGetAmData`) at the top of each of the six vulnerable handlers, before any query parameter parsing.

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "inconsistency_identified_score": {
      "max": 3,
      "criteri": {
        "3": "Correctly identifies that HandleGetAmData validates SUPI but at least 3 of the 6 other handlers do not, names the specific handlers, and characterizes this as an inconsistency in the same NF codebase",
        "2": "Identifies the validation inconsistency and names at least one vulnerable handler by name (beyond HandleGetAmData as reference)",
        "1": "Mentions that some handlers lack validation in general terms without identifying specific functions",
        "0": "Does not identify any validation inconsistency, or incorrectly asserts all handlers validate correctly"
      }
    },
    "spec_reference_score": {
      "max": 2,
      "criteri": {
        "2": "References 3GPP TS 29.503 or the SUPI format requirement as the relevant standard, or correctly describes what a valid SUPI looks like (imsi-/nai-/etc. prefix)",
        "1": "Mentions that there is a standardized format for SUPI without citing the spec",
        "0": "No reference to 3GPP requirements or SUPI format definition"
      }
    },
    "impact_assessment_score": {
      "max": 2,
      "criteri": {
        "2": "Explains concrete downstream impact: arbitrary SUPI values reaching UDR, potential for data probing across subscription collections, cross-NF bypass of validation gate",
        "1": "Mentions generic impact (unauthorized data access) without 5G-specific detail",
        "0": "No impact assessment or incorrect claim"
      }
    },
    "fix_quality_score": {
      "max": 2,
      "criteri": {
        "2": "Proposes adding validator.IsValidSupi() (or equivalent) to the unvalidated handlers, correctly identifying it as the same control already used in HandleGetAmData",
        "1": "Suggests adding input validation without specifying the correct validator function or pattern",
        "0": "No fix proposed or fix is incorrect"
      }
    }
  },
  "total_max": 9
}
```
