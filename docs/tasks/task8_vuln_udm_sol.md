# Solution — Task 8 (UDM: Missing SUPI validation in SDM handlers)

**ID:** task8_vuln_udm_sol  
**Usage:** rubric for judge agent — GT not exposed to the tested agent

---

## Ground Truth

```json
{
  "non_compliant_handlers": [
    "HandleGetSmfSelectData",
    "HandleGetSupi",
    "HandleGetNssai",
    "HandleGetTraceData",
    "HandleGetUeContextInSmfData"
  ],
  "compliant_handlers_in_file": [
    "HandleGetAmData",
    "HandleUnsubscribe",
    "HandleModify",
    "HandleGetIdTranslationResult"
  ]
}
```

Note: `HandleGetUeContextInSmfData` is also non-compliant (passes `supi` directly to processor without validation) but is not shown in the snippet. The four shown non-compliant handlers (B, C, D, E) are sufficient for full scoring.

## GT Rationale

### Non-compliant handlers (shown in snippet)

- **HandleGetSmfSelectData** (B): reads `supi`, skips validation, passes directly to `GetSmfSelectDataProcedure`
- **HandleGetSupi** (C): reads `supi`, skips validation, passes to `GetSupiProcedure` which retrieves multiple data sets
- **HandleGetNssai** (D): reads `supi`, skips validation, passes to `GetNssaiProcedure`
- **HandleGetTraceData** (E): reads `supi`, skips validation, passes to `GetTraceDataProcedure`

### Attack vectors

**1. NoSQL Injection (MongoDB operator injection)**

In free5GC, the UDM processor passes the SUPI string as a MongoDB filter field. If the SUPI is used in a query like `bson.M{"supi": supi}` and `supi` contains a MongoDB operator (e.g., `{"$gt": ""}`) — possible if the SUPI is later parsed as a BSON document rather than a literal string — it can match all documents in the collection. More practically, without format validation, a SUPI like `imsi-` + long padding or special characters can cause the MongoDB query to behave unexpectedly or to scan the entire collection (performance DoS).

**2. Enumeration / Data exfiltration**

Without format validation, an attacker can probe the UDM with arbitrary strings as SUPI. This allows:
- Systematic enumeration of subscriber records by trying different SUPI values
- Probing internal collection names or field patterns through error messages returned by the processor
- Bypassing access control checks that might rely on SUPI format (e.g., a check that `supi` starts with `imsi-` to determine which collection to query)

**3. Denial of Service via malformed input**

A very long SUPI, a SUPI with null bytes, or a SUPI triggering a regex catastrophic backtracking in downstream code can cause CPU spikes or panics in the UDM processor layer. Without input validation at the handler boundary, these inputs reach deep into the business logic.

**4. 3GPP Compliance violation**

TS 29.503 §6.1.3.5.2 requires 400 Bad Request with cause `MANDATORY_IE_INCORRECT` for invalid SUPI. Without validation, the UDM returns 200 OK or a database-level error for malformed SUPIs, violating the specification and potentially confusing NF consumers about the validity of their requests.

### Inconsistency analysis

The partial application of the fix (only `HandleGetAmData` was patched while sibling handlers were not) is a textbook example of an incomplete security patch. The risks are:

- **Attack surface remains open**: An attacker who knows about the SUPI validation requirement will try all SDM endpoints, not just `/am-data`. The unpatched endpoints (`/smf-select-data`, `/nssai`, `/sm-data`, `/trace-data`) remain exploitable.
- **False sense of security**: The patch in Handler A may give reviewers the impression that SUPI validation is "done," leading future developers to skip validation in new handlers following Handler B as a template rather than Handler A.
- **Differential security**: Data accessible via Handler B (SMF selection data — which SMF to use) and Handler D (NSSAI — which network slices a UE is subscribed to) is equally sensitive to data in Handler A. The inconsistency has no security justification.

### Minimal fix for Handler B

```go
func (s *Server) HandleGetSmfSelectData(c *gin.Context) {
    query := url.Values{}
    query.Set("plmn-id", c.Query("plmn-id"))
    query.Set("supported-features", c.Query("supported-features"))

    logger.SdmLog.Infof("Handle GetSmfSelectData")

    // TS 29.503 6.1.3.5.2 — Validate SUPI format
    supi := c.Params.ByName("supi")
    if !validator.IsValidSupi(supi) {
        problemDetail := models.ProblemDetails{
            Title:  "Malformed request syntax",
            Status: http.StatusBadRequest,
            Detail: "Supi is invalid",
            Cause:  "MANDATORY_IE_INCORRECT",
        }
        logger.SdmLog.Warnln("Supi is invalid")
        c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(problemDetail.Status)))
        c.JSON(int(problemDetail.Status), problemDetail)
        return
    }

    plmnIDStruct, problemDetails := s.getPlmnIDStruct(c.Request.URL.Query())
    if problemDetails != nil {
        c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetails.Cause)
        c.JSON(int(problemDetails.Status), problemDetails)
        return
    }
    var plmnID string
    if plmnIDStruct != nil {
        plmnID = plmnIDStruct.Mcc + plmnIDStruct.Mnc
    }
    supportedFeatures := query.Get("supported-features")
    s.Processor().GetSmfSelectDataProcedure(c, supi, plmnID, supportedFeatures)
}
```

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + task scenario + this rubric.

```json
{
  "rubrica": {
    "non_compliant_identification": {
      "max": 3,
      "criteri": {
        "3": "Correctly identifies all four shown non-compliant handlers (HandleGetSmfSelectData, HandleGetSupi, HandleGetNssai, HandleGetTraceData) and correctly identifies HandleGetAmData as compliant",
        "2": "Identifies 3 of the 4 non-compliant handlers correctly",
        "1": "Identifies at least 1 non-compliant handler and correctly explains why (missing validator.IsValidSupi call)",
        "0": "Cannot identify non-compliant handlers or identifies them incorrectly"
      }
    },
    "attack_vectors": {
      "max": 3,
      "criteri": {
        "3": "Describes at least two distinct attack vectors, at least one of which is specific to the UDM/MongoDB context (NoSQL injection OR SUPI enumeration), with technical explanation",
        "2": "Describes two attack vectors but without MongoDB/UDM-specific framing, OR describes one highly specific vector",
        "1": "Mentions input validation bypass generically without specific attack mechanism",
        "0": "No attack vector analysis or incorrect analysis"
      }
    },
    "inconsistency_analysis": {
      "max": 2,
      "criteri": {
        "2": "Identifies the partial fix pattern (only some handlers patched), explains the risk of remaining attack surface AND the template effect on future code, with reference to the specific handlers",
        "1": "Notes that the fix is incomplete or that other handlers are also affected, without deeper analysis",
        "0": "Does not address the inconsistency question"
      }
    },
    "fix_correctness": {
      "max": 1,
      "criteri": {
        "1": "Fix adds `validator.IsValidSupi(supi)` check with correct 400 response and return before the processor call, matching the Handler A pattern",
        "0": "Fix is absent, syntactically incorrect, or does not include the return statement"
      }
    },
    "clarity_score": {
      "max": 1,
      "criteri": {
        "1": "Valid JSON, non_compliant_handlers is an array of strings, fix is a code snippet",
        "0": "Malformed JSON or response structure does not match requested format"
      }
    }
  },
  "total_max": 10
}
```
