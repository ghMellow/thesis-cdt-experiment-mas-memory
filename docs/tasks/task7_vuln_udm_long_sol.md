# Solution — Task 7b (UDM missing SUPI validation — full file)

**ID:** task7_vuln_udm_long_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent

---

## Ground Truth

```json
{
  "answer": [
    {
      "vulnerability_type": "Missing SUPI input validation",
      "location": "HandleGetSmfSelectData — supi extracted from path but IsValidSupi() not called",
      "impact": "Arbitrary or malformed SUPI values forwarded to processor and data layer"
    },
    {
      "vulnerability_type": "Missing SUPI input validation",
      "location": "HandleGetSupi — supi extracted but no IsValidSupi() check",
      "impact": "Arbitrary SUPI reaches GetSupiProcedure unvalidated"
    },
    {
      "vulnerability_type": "Missing SUPI input validation",
      "location": "HandleGetNssai — supi extracted but no IsValidSupi() check",
      "impact": "Arbitrary SUPI reaches GetNssaiProcedure unvalidated"
    },
    {
      "vulnerability_type": "Missing SUPI input validation",
      "location": "HandleGetSmData — supi extracted but no IsValidSupi() check",
      "impact": "Arbitrary SUPI reaches GetSmDataProcedure unvalidated"
    },
    {
      "vulnerability_type": "Missing SUPI input validation",
      "location": "HandleGetTraceData — supi extracted but no IsValidSupi() check",
      "impact": "Arbitrary SUPI reaches GetTraceDataProcedure unvalidated"
    },
    {
      "vulnerability_type": "Missing SUPI input validation",
      "location": "HandleGetUeContextInSmfData — supi extracted but no IsValidSupi() check",
      "impact": "Arbitrary SUPI reaches GetUeContextInSmfDataProcedure unvalidated"
    },
    {
      "vulnerability_type": "Missing SUPI input validation",
      "location": "HandleSubscribe — supi extracted after deserialization but no IsValidSupi() check",
      "impact": "Arbitrary SUPI reaches SubscribeProcedure unvalidated"
    },
    {
      "vulnerability_type": "Missing SUPI input validation",
      "location": "HandleModifyForSharedData — supi extracted but no IsValidSupi() check",
      "impact": "Arbitrary SUPI reaches ModifyForSharedDataProcedure unvalidated"
    }
  ],
  "type": "textual_security"
}
```

## GT Rationale

- `HandleGetAmData` correctly calls `validator.IsValidSupi(supi)` per TS 29.503 §6.1.3.5.2
- `HandleUnsubscribe`, `HandleModify`, `HandleGetIdTranslationResult` correctly validate via `IsValidGpsi || IsValidSupi`
- All remaining handlers that extract a `supi` or `ueId` path parameter and pass it to a processor do so without format validation
- The 8 handlers listed above are the complete set of unprotected endpoints in the file

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "completeness_score": {
      "max": 3,
      "criteri": {
        "3": "Identifies 5 or more handlers with missing SUPI validation, correctly distinguishing them from the handlers that do validate",
        "2": "Identifies 3-4 handlers with missing SUPI validation",
        "1": "Identifies 1-2 handlers with missing SUPI validation, or correctly identifies the pattern but names only one concrete handler",
        "0": "Does not identify the SUPI validation gap or only reports false positives on correctly validated handlers"
      }
    },
    "accuracy_score": {
      "max": 3,
      "criteri": {
        "3": "All reported handlers genuinely lack IsValidSupi(); does not flag HandleGetAmData, HandleUnsubscribe, HandleModify, or HandleGetIdTranslationResult as vulnerable",
        "2": "Mostly correct but includes one or two false positives on handlers that do validate",
        "1": "At least one correctly identified handler but also significant false positives",
        "0": "No correct handler identified, or only false positives"
      }
    },
    "impact_score": {
      "max": 2,
      "criteri": {
        "2": "Explains that unvalidated SUPI values reach the data/processor layer, violating 3GPP TS 29.503 and potentially enabling unexpected database access patterns",
        "1": "Mentions missing validation without connecting to downstream impact",
        "0": "No impact described or impact is incorrect"
      }
    },
    "clarity_score": {
      "max": 1,
      "criteri": {
        "1": "Response is valid JSON; answer is a list with at least one entry containing required fields",
        "0": "Malformed JSON or answer is not a list"
      }
    }
  },
  "total_max": 9
}
```
