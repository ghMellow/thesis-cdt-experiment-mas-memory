# Solution — Task 10 (UDM: inconsistent SUPI validation across SDM handlers)

**ID:** task10_vuln_udm_validator_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent

---

## Ground Truth

```json
{
  "answer": {
    "vulnerability": "CWE-20 (Improper Input Validation, GHSA-585v-hcgf-jhfr): HandleGetAmData (Snippet A) validates the 'supi' path parameter with validator.IsValidSupi(supi) per TS 29.503 6.1.3.5.2 before use, but several other Nudm_SDM handlers in the same file -- HandleGetSmfSelectData, HandleGetTraceData, HandleGetUeContextInSmfData, HandleGetNssai, HandleGetSmData, HandleGetSupi (Snippet B) -- read the same 'supi' path parameter and pass it directly to the corresponding Processor procedure with no format check at all.",
    "impact": "An attacker can call HandleGetSmfSelectData, HandleGetTraceData, HandleGetUeContextInSmfData, HandleGetNssai, HandleGetSmData or HandleGetSupi with a 'supi' value that does not conform to the 3GPP SUPI format (TS 23.003 / TS 29.503), and it reaches the processor/persistence layer unfiltered -- the same class of risk that HandleGetAmData explicitly guards against. This inconsistency means the format-validation control is not enforced uniformly across UDM's SDM API surface.",
    "fix": "Add the same check used in HandleGetAmData -- 'if !validator.IsValidSupi(supi) { ... return 400 Malformed request syntax / MANDATORY_IE_INCORRECT }' -- at the start of HandleGetSmfSelectData, HandleGetTraceData, HandleGetUeContextInSmfData, HandleGetNssai, HandleGetSmData, HandleGetSupi, and any other Nudm_SDM handler that reads 'supi' from the path without validating it."
  },
  "type": "textual_vuln_analysis"
}
```

## GT Rationale

- `HandleGetAmData` explicitly comments "TS 29.503 6.1.3.5.2 / Validate SUPI format" and rejects the request with `400 Bad Request` / `MANDATORY_IE_INCORRECT` if `validator.IsValidSupi(supi)` is false.
- `HandleGetSmfSelectData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetSupi` read `supi := c.Params.ByName("supi")` from the identical route pattern (`/:supi/...`) but skip this check entirely before calling their respective `*Procedure`.
- Since all these handlers are part of the same `Nudm_SDM` service and read the same path parameter, the validation should be applied uniformly; its absence in most handlers is an inconsistency, not an intentional relaxation — this is GHSA-585v-hcgf-jhfr.
- The fix is mechanical and low-risk: copy the existing validation block from `HandleGetAmData` into each of the unvalidated handlers.

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "vuln_identified_score": {
      "max": 3,
      "criteri": {
        "3": "Identifies that Snippet B's handlers (at least 2 of: HandleGetSmfSelectData, HandleGetTraceData, HandleGetUeContextInSmfData, HandleGetNssai, HandleGetSmData, HandleGetSupi) skip the validator.IsValidSupi check that HandleGetAmData performs on the same 'supi' parameter, framing it as an inconsistent/missing input validation",
        "2": "Identifies that some handlers lack SUPI validation compared to HandleGetAmData, but names only one affected handler or is vague about which ones",
        "1": "Notes generically that 'supi is not validated' in some handler without the comparison to HandleGetAmData's validator.IsValidSupi",
        "0": "Does not identify the missing/inconsistent SUPI validation"
      }
    },
    "impact_assessment_score": {
      "max": 2,
      "criteri": {
        "0": "No impact assessment, or generic 'security risk'",
        "1": "Generic impact (e.g. 'invalid input could cause errors') without referencing the 3GPP SUPI format requirement or the inconsistency with HandleGetAmData",
        "2": "Impact specific to context: malformed-format supi values reach the processor/persistence layer in the unvalidated handlers, violating TS 23.003/29.503 and inconsistent with the control already implemented in HandleGetAmData"
      }
    },
    "fix_proposed_score": {
      "max": 2,
      "criteri": {
        "0": "No fix proposed, or incorrect fix",
        "1": "Generic fix (e.g. 'validate supi') without naming validator.IsValidSupi or the HandleGetAmData pattern to replicate",
        "2": "Specific correct fix: add the validator.IsValidSupi(supi) check (mirroring HandleGetAmData, returning 400/MANDATORY_IE_INCORRECT) to each of the unvalidated handlers"
      }
    },
    "false_positives_score": {
      "max": 1,
      "criteri": {
        "1": "No misleading or unrelated vulnerabilities reported as the primary finding",
        "0": "Reports unrelated/incorrect vulnerabilities as the main finding, obscuring or replacing the missing-validator inconsistency"
      }
    },
    "clarity_score": {
      "max": 1,
      "criteri": {
        "1": "Clear, structured response, valid JSON",
        "0": "Malformed JSON or confused response"
      }
    },
    "confidence_calibration_score": {
      "max": 1,
      "criteri": {
        "1": "Confidence >= 0.7 if the missing-validator inconsistency is correctly identified, or low confidence if it is missed",
        "0": "High confidence despite missing the issue, or inexplicably low confidence on a correct finding"
      }
    }
  },
  "total_max": 10
}
```
