# Solution — Task 9 (Cross-NF vulnerability identification)

**ID:** task9_vuln_cross_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent

---

## Ground Truth

```json
{
  "answer": [
    {
      "nf": "AMF",
      "vulnerability_type": "Missing default case in Content-Type switch — processor called with zero-value request data",
      "location": "HTTPUEContextTransfer — switch on str[0] has no default branch",
      "impact": "Unrecognized Content-Type leaves err nil; AMF processor receives uninitialized UE context transfer data"
    },
    {
      "nf": "UDM",
      "vulnerability_type": "Missing SUPI input validation — unvalidated identifier forwarded to data layer",
      "location": "HandleGetSmfSelectData — supi extracted from path but IsValidSupi() never called",
      "impact": "Arbitrary or malformed SUPI values reach the processor and potentially the subscription database"
    },
    {
      "nf": "UDR",
      "vulnerability_type": "Missing return after error response and Deserialize called without pointer",
      "location": "HandlePolicyDataSubsToNotifyPost — error blocks lack return; Deserialize(policyDataSubscription, ...) should use &policyDataSubscription",
      "impact": "Execution continues after error responses; processor always receives zero-value subscription data regardless of request content"
    }
  ],
  "type": "textual_security"
}
```

## GT Rationale

- **AMF**: The switch on `str[0]` covers only `applicationjson` and `multipartrelate`. A third Content-Type value leaves `err` as nil and the function calls the processor with default-initialized fields.
- **UDM**: `HandleGetAmData` in the same codebase validates SUPI via `validator.IsValidSupi()` per TS 29.503. `HandleGetSmfSelectData` accesses the same path parameter without validation — an inconsistency that bypasses the required format check.
- **UDR**: Two distinct bugs in the same function: (1) `c.JSON()` is called on errors but without `return`, so the processor is always reached; (2) `Deserialize` receives a value copy, not a pointer, so deserialized data is never written to the local variable.

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "completeness_score": {
      "max": 3,
      "criteri": {
        "3": "Correctly identifies a distinct vulnerability for all three NFs (AMF, UDM, UDR)",
        "2": "Correctly identifies vulnerabilities in exactly two of the three NFs",
        "1": "Correctly identifies a vulnerability in exactly one NF",
        "0": "No NF vulnerability correctly identified"
      }
    },
    "accuracy_score": {
      "max": 3,
      "criteri": {
        "3": "All identified vulnerabilities are technically accurate — correct mechanism described for each NF, no significant false positives",
        "2": "Identified vulnerabilities are mostly accurate with minor description errors",
        "1": "At least one vulnerability is accurately described; others are vague or partially incorrect",
        "0": "No vulnerability correctly described or only false positives"
      }
    },
    "impact_score": {
      "max": 2,
      "criteri": {
        "2": "Explains the real-world impact for at least two NFs: what downstream component is affected and how",
        "1": "Mentions impact for one NF or gives generic impact descriptions",
        "0": "No impact described or impacts are all incorrect"
      }
    },
    "clarity_score": {
      "max": 1,
      "criteri": {
        "1": "Response is valid JSON; answer is a list with exactly three entries each containing nf, vulnerability_type, location, and impact fields",
        "0": "Malformed JSON, missing entries, or missing required fields"
      }
    }
  },
  "total_max": 9
}
```
