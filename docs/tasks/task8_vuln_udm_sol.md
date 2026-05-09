# Solution — Task 8 (Security Review: UDM Subscriber Data Management Handler)

**ID:** task8_vuln_udm_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent  
**CVE reference:** GHSA-585v-hcgf-jhfr

---

## Ground Truth

```json
{
  "answer": "Multiple UDM handlers retrieve the SUPI path parameter and pass it directly to the processor without calling validator.IsValidSupi(), while other handlers in the same file correctly validate it. The affected handlers are HandleGetSmfSelectData, HandleGetNssai, HandleGetSmData, HandleGetTraceData, HandleGetUeContextInSmfData, and HandleGetSupi.",
  "type": "textual_security_review"
}
```

## GT Rationale

### Primary finding — Missing SUPI format validation in 6 handlers

The file shows two distinct patterns for the same `supi` path parameter:

**Correct pattern** (2 handlers implement it):
```go
// HandleGetAmData:
supi := c.Params.ByName("supi")
if !validator.IsValidSupi(supi) { ... return }

// HandleUnsubscribe:
valid := validator.IsValidGpsi(ueId) || validator.IsValidSupi(ueId)
if !valid { ... return }
```

**Vulnerable pattern** (6 handlers):
```go
// HandleGetSmfSelectData, HandleGetNssai, HandleGetSmData,
// HandleGetTraceData, HandleGetUeContextInSmfData, HandleGetSupi:
supi := c.Params.ByName("supi")
// ← no format validation — passed directly to processor
s.Processor().Get...Procedure(c, supi, ...)
```

3GPP TS 29.503 §6.1.3.5.2 mandates SUPI validation before processing. A SUPI must match `imsi-[0-9]{5,15}` or other defined formats. Without validation:
- Arbitrary strings (including special characters, MongoDB operators embedded in JSON-style paths, or excessively long strings) reach the UDM processor and downstream persistence layer
- An attacker with access to the 5G SBI network can query subscription data using malformed SUPI values, potentially triggering unexpected behavior in the processor or underlying data store
- The inconsistency within the same file suggests a systematic omission rather than an intentional design choice

**Fix**: add `if !validator.IsValidSupi(supi) { ... return }` at the start of each affected handler, mirroring the pattern in `HandleGetAmData`.

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "validation_gap_identified_score": {
      "max": 4,
      "criteri": {
        "4": "Identifies the inconsistency: some handlers call validator.IsValidSupi() while others do not, names at least 3 of the 6 vulnerable handlers specifically (HandleGetSmfSelectData, HandleGetNssai, HandleGetSmData, HandleGetTraceData, HandleGetUeContextInSmfData, HandleGetSupi), and identifies which handlers are correctly implemented as a contrast",
        "3": "Identifies that SUPI validation is missing in multiple handlers and names at least 1-2 specific vulnerable handlers, but does not fully enumerate the affected set",
        "2": "Notes that SUPI validation is inconsistent or missing in some handlers without naming the specific functions",
        "1": "Mentions input validation as a general concern without connecting it to SUPI specifically",
        "0": "Does not identify the missing SUPI validation issue"
      }
    },
    "spec_reference_score": {
      "max": 2,
      "criteri": {
        "2": "References 3GPP TS 29.503 or describes the expected SUPI format (imsi-[0-9]{5,15} or similar) as the required validation standard",
        "1": "Notes that identifiers in 5G core must follow a specific format without citing the standard",
        "0": "No reference to 5G specification or identifier format requirements"
      }
    },
    "impact_assessment_score": {
      "max": 2,
      "criteri": {
        "2": "Correctly explains impact in UDM context: malformed or malicious SUPI values reaching the processor and persistence layer, potential data enumeration or unexpected behavior on subscription data keyed by SUPI",
        "1": "Generic input validation impact without UDM-specific context",
        "0": "No impact assessment"
      }
    },
    "fix_quality_score": {
      "max": 1,
      "criteri": {
        "1": "Proposes adding validator.IsValidSupi() (or equivalent) to the affected handlers, consistent with the pattern in HandleGetAmData",
        "0": "No fix proposed or fix is incorrect"
      }
    }
  },
  "total_max": 9
}
```
