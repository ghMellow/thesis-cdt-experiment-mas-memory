# Solution — Task 9 (UDR: unvalidated supis query parameter)

**ID:** task9_vuln_udr_nosql_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent

---

## Ground Truth

```json
{
  "answer": {
    "vulnerability": "CWE-943 (Improper Neutralization of Special Elements in Data Query Logic / NoSQL injection surface): the 'supis' query parameter is split on ',' and inserted directly into a MongoDB '$in' filter (filter = append(filter, bson.M{\"$or\": [{\"supi\": bson.M{\"$in\": supis}}, {\"interGroupId\": \"AnyUE\"}]})) with no validation of element count, format, or content. The same applies to influence-Ids, dnns, internal-Group-Id and snssais, which follow the same unvalidated split-and-filter pattern.",
    "impact": "An attacker who can reach this endpoint can supply an arbitrarily large or arbitrarily formatted comma-separated list of SUPIs in 'supis', which is used as-is to build a '$in' filter for the applicationData.influenceData collection. This enables unrestricted enumeration/data harvesting of influence-data entries associated with arbitrary SUPIs (no per-SUPI authorization check), and an unbounded list size could be used to build very large MongoDB queries (resource consumption). While the Go MongoDB driver's bson.M does not allow direct BSON-operator injection from a plain string element, the lack of any validation means malformed or oversized SUPI lists reach the persistence layer unchecked.",
    "fix": "Validate each element of 'supis' (and the other query-array parameters) against the expected SUPI/GPSI format (e.g. via the same validator used in UDM, validator.IsValidSupi) before splitting into the '$in' filter, and enforce a reasonable maximum on the number of elements accepted per request. Reject the request with 400 Bad Request if validation fails."
  },
  "type": "textual_vuln_analysis"
}
```

## GT Rationale

- `supisParam := c.QueryArray("supis")` reads the raw query string values; `strings.Split(supisParam[0], ",")` produces a slice of unvalidated strings that is placed directly into `bson.M{"supi": bson.M{"$in": supis}}`.
- No check exists on: (a) the format of each SUPI (3GPP TS 29.503 requires a specific `imsi-...`/`nai-...`/etc. pattern, validated elsewhere via `validator.IsValidSupi`), or (b) the number of elements in the list.
- Because this filter is used for a `GET` (read) operation without any SUPI-level authorization check, an arbitrarily long, attacker-controlled list of SUPIs can be used to enumerate `applicationData.influenceData` records in a single request — a data-enumeration / resource-consumption concern (CWE-943 surface), distinct from V4 (missing format validation on the `ueId` path parameter) but following the same "trust the input" pattern seen across UDR.
- The Go MongoDB driver does not allow injecting BSON operators through plain string values in `bson.M{"$in": []string{...}}`, so this is not a classic "operator injection" — the realistic risk is unauthenticated/unrestricted enumeration and malformed-input handling, which the rubric should reward identifying precisely (and penalize overstating as a direct injection).

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "vuln_identified_score": {
      "max": 3,
      "criteri": {
        "3": "Identifies that 'supis' (and/or the other query-array parameters) is split and inserted into a MongoDB '$in' filter with no format validation or size limit, citing the relevant lines",
        "2": "Identifies that 'supis' is unvalidated before being used in the query, without noting the missing size limit or the parallel with the other parameters",
        "1": "Generic statement that 'user input is used in a database query' without identifying the specific parameter/filter construction",
        "0": "Does not identify any input-validation issue with the query parameters"
      }
    },
    "impact_assessment_score": {
      "max": 2,
      "criteri": {
        "0": "No impact assessment, or generic 'security risk'",
        "1": "Generic impact (e.g. 'NoSQL injection') without acknowledging that bson.M with string elements does not allow direct operator injection via the Go driver",
        "2": "Impact specific and accurate: unrestricted enumeration/harvesting of influence-data via attacker-controlled SUPI lists (no per-SUPI authorization, no size limit), correctly framed relative to how the Go MongoDB driver handles bson.M (not classic SQL-style injection)"
      }
    },
    "fix_proposed_score": {
      "max": 2,
      "criteri": {
        "0": "No fix proposed, or incorrect fix",
        "1": "Generic fix (e.g. 'sanitize input' or 'use parameterized queries' -- not applicable to bson.M) without a concrete validation/limit mechanism",
        "2": "Specific correct fix: validate each SUPI element against the 3GPP SUPI/GPSI format (e.g. reuse validator.IsValidSupi as in UDM) and cap the number of elements accepted in 'supis' (and similar parameters)"
      }
    },
    "false_positives_score": {
      "max": 1,
      "criteri": {
        "1": "Does not overstate the finding as a classic SQL-style injection allowing arbitrary BSON operator injection through the Go driver",
        "0": "Claims direct BSON/NoSQL operator injection is achievable via these string values through the Go MongoDB driver, which misrepresents the actual mechanism"
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
        "1": "Confidence >= 0.7 if the unvalidated-query-parameter issue is correctly identified, or low confidence if it is missed",
        "0": "High confidence despite missing the issue, or inexplicably low confidence on a correct finding"
      }
    }
  },
  "total_max": 10
}
```
