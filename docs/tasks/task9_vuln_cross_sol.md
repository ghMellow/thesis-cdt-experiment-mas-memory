# Solution — Task 9 (Cross-NF Security Review)

**ID:** task9_vuln_cross_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent  
**CVE references:** all 9 GHSA from Patch_Spiegazione.md (GHSA-98cp, GHSA-wrwh×6, GHSA-r99v, GHSA-585v)

---

## Ground Truth

```json
{
  "answer": "Cross-file: UDM validates SUPI in some handlers (HandleGetAmData, HandleUnsubscribe) but not in others (HandleGetSmfSelectData etc.); UDR never validates ueId format in any handler — this is a systemic inconsistency in the same codebase. Per-file: PCF has CORS misconfiguration (AllowAllOrigins+AllowCredentials); UDR has missing return after 404 in three handlers; AMF has missing default case in HTTPUEContextTransfer and wrong c.Set type in multiple handlers.",
  "type": "textual_security_review"
}
```

## GT Rationale

### Cross-file finding — Inconsistent UE identifier validation across UDM and UDR

This is the key systemic finding that only becomes visible with a multi-file view:

- **UDM (File 3)**: `HandleGetAmData` and `HandleUnsubscribe` call `validator.IsValidSupi()` / `validator.IsValidGpsi()` before passing the identifier to the processor. This is the correct 3GPP-compliant pattern (TS 29.503 §6.1.3.5.2).
- **UDM (File 3)**: `HandleGetSmfSelectData`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetSupi` — same file, same data type (`supi` path param), **no validation call**.
- **UDR (File 4)**: `HandleQueryAmfContext3gpp` and the majority of handlers only check `ueId == ""` — **no format validation at all**, across the entire file.

The cross-file insight: the UDM validator (`validator.IsValidSupi`) is available in the shared library and used correctly in some UDM handlers, yet the UDR — which stores the same SUPI-keyed subscription data — never uses it. This is a systemic omission, not a one-off mistake.

### Per-file findings (all also present in tasks 5–8)

| NF | Finding | Functions |
| --- | --- | --- |
| PCF | CORS: AllowAllOrigins + AllowCredentials | `setCorsHeader` |
| AMF | Missing default in Content-Type switch | `HTTPUEContextTransfer` |
| AMF | c.Set receives struct instead of string | `HTTPCreateUEContext`, `HTTPUEContextTransfer` |
| UDR | Missing return after 404 | `...SubsToNotifySubscriptionIdDelete/Get/Put` |
| UDR | Regex `\|.+` makes ueId validation trivial | `HandleCreateEeSubscriptions`, `HandleQueryeesubscriptions` |

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "cross_file_inconsistency_score": {
      "max": 4,
      "criteri": {
        "4": "Explicitly identifies the cross-file UE identifier validation gap: names UDM handlers that validate SUPI correctly (HandleGetAmData or HandleUnsubscribe) AND UDM handlers or UDR handlers that do not validate, explains this as a systemic inconsistency within the same codebase handling the same data type",
        "3": "Notes that SUPI/ueId validation is applied in some handlers but not others across the files, identifying at least one correct and one incorrect handler, even if not fully naming the systemic scope",
        "2": "Notes inconsistent input validation across the files in a general way without naming the specific handlers or the UDM/UDR contrast",
        "1": "Mentions input validation as a cross-file concern without specific evidence",
        "0": "Does not identify any cross-file inconsistency"
      }
    },
    "per_file_coverage_score": {
      "max": 3,
      "criteri": {
        "3": "Correctly identifies at least 3 of the 5 distinct per-file vulnerability classes: CORS misconfiguration (PCF), missing default case (AMF), wrong c.Set type (AMF), missing return after 404 (UDR), ineffective regex (UDR)",
        "2": "Identifies 2 per-file vulnerability classes correctly",
        "1": "Identifies 1 per-file vulnerability class correctly",
        "0": "Identifies no per-file vulnerabilities, or only identifies issues that do not exist"
      }
    },
    "impact_global_score": {
      "max": 2,
      "criteri": {
        "2": "Frames the findings in a 5G core security context: explains why identifier validation matters for SUPI-keyed data stores, or how CORS affects the OAM plane, or how the missing return creates an exploitable path in the SBI",
        "1": "Generic security impact description without 5G-specific framing",
        "0": "No impact assessment"
      }
    }
  },
  "total_max": 9
}
```
