# Solution — Task 7 (UDM vulnerability detection)

**ID:** task7_vuln_udm_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent  
**Reference:** free5gc advisory GHSA-585v-hcgf-jhfr (missing validator.IsValidSupi)

---

## Ground Truth

```json
{
  "answer": {
    "vulnerability": "Missing SUPI format validation in HandleGetSmfSelectData and HandleGetSmData",
    "location": "HandleGetSmfSelectData, HandleGetSmData",
    "severity": "high",
    "mechanism": "HandleGetAmData validates the path parameter with validator.IsValidSupi(supi) before using it, but HandleGetSmfSelectData and HandleGetSmData forward the raw supi straight to the processor with no validation. An attacker can supply a malformed or crafted supi (e.g. unexpected characters or query-operator-like content) that reaches the backend data query, enabling unvalidated data access / injection and unexpected behaviour."
  },
  "type": "textual_security"
}
```

## GT Rationale

- `HandleGetAmData` correctly calls `validator.IsValidSupi(supi)` and rejects
  invalid identifiers (TS 29.503 6.1.3.5.2).
- `HandleGetSmfSelectData` and `HandleGetSmData` omit that check entirely: the
  `supi` from the path is passed unvalidated to `GetSmfSelectDataProcedure` /
  `GetSmDataProcedure`. The inconsistency between sibling handlers is the signal.
- Impact: a malformed/crafted `supi` reaches the data layer (MongoDB), enabling
  injection / unauthorized or unexpected data access depending on how the
  processor builds the query.

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "detection_score": {
      "max": 3,
      "criteri": {
        "3": "Identifies that HandleGetSmfSelectData and/or HandleGetSmData forward the supi without the validator.IsValidSupi() check that HandleGetAmData performs",
        "2": "Notices that the supi is used without validation but does not contrast it with the validating handler, or names only one of the two affected handlers",
        "1": "Flags a generic input-validation concern without pinpointing the missing SUPI validation",
        "0": "Does not identify any real vulnerability in the code"
      }
    },
    "impact_score": {
      "max": 2,
      "criteri": {
        "2": "Explains that the unvalidated supi reaches the data layer, enabling injection / unauthorized or unexpected data access",
        "1": "States the impact or the mechanism but not both",
        "0": "No correct explanation of mechanism or impact"
      }
    },
    "localization_score": {
      "max": 1,
      "criteri": {
        "1": "Points to HandleGetSmfSelectData / HandleGetSmData and contrasts with HandleGetAmData",
        "0": "Wrong or missing location"
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
        "1": "Confidence >= 0.7 if detection is correct, or low confidence if detection is wrong",
        "0": "High confidence on wrong detection, or inexplicably low confidence on correct detection"
      }
    }
  },
  "total_max": 8
}
```
