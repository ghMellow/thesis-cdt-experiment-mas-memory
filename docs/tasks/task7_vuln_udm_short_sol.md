# Solution — Task 7a (UDM missing SUPI validation — short)

**ID:** task7_vuln_udm_short_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent

---

## Ground Truth

```json
{
  "answer": {
    "vulnerability_type": "Missing input validation — SUPI format not validated before passing to processor",
    "location": "HandleGetSmfSelectData — supi extracted from path parameters but validator.IsValidSupi() never called",
    "impact": "An arbitrary or malformed SUPI string is forwarded to the data layer without format checking, potentially triggering unexpected behavior in downstream processing or database queries, in violation of 3GPP TS 29.503"
  },
  "type": "textual_security"
}
```

## GT Rationale

- `HandleGetAmData` correctly calls `validator.IsValidSupi(supi)` per TS 29.503 §6.1.3.5.2 and returns HTTP 400 if invalid
- `HandleGetSmfSelectData` extracts the same `supi` path parameter but passes it directly to `GetSmfSelectDataProcedure` with no format check
- Both handlers serve the same UE identifier from the same URL path segment — the validation gap is inconsistent and constitutes a missing security control
- A malformed or injected SUPI string could reach the database/processor layer unfiltered

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "identification_score": {
      "max": 3,
      "criteri": {
        "3": "Correctly identifies that HandleGetSmfSelectData lacks the validator.IsValidSupi() check present in HandleGetAmData",
        "2": "Identifies missing input validation on supi in the second handler but does not reference the comparison with the first handler",
        "1": "Notes a generic input validation gap without identifying the SUPI validator specifically",
        "0": "Does not identify the vulnerability or confuses which handler is vulnerable"
      }
    },
    "location_score": {
      "max": 2,
      "criteri": {
        "2": "Correctly names HandleGetSmfSelectData and the absent IsValidSupi call after supi extraction",
        "1": "Points to the second handler generally without the specific missing call",
        "0": "Incorrect or missing location"
      }
    },
    "impact_score": {
      "max": 2,
      "criteri": {
        "2": "Explains that an unvalidated SUPI reaches the processor/data layer, potentially causing unexpected behavior or violating 3GPP spec requirements",
        "1": "Mentions that invalid input can reach the backend without explaining the specific risk",
        "0": "No impact described or impact is incorrect"
      }
    },
    "clarity_score": {
      "max": 1,
      "criteri": {
        "1": "Response is valid JSON with all required fields populated",
        "0": "Malformed JSON or missing required fields"
      }
    }
  },
  "total_max": 8
}
```
