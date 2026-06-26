# Task 7 — Security Code Review: UDR Regex Validation Bypass (5G)

**ID:** task7_vuln_udr
**Tipo:** security_code_review
**Difficoltà:** alta
**NF:** UDR (Unified Data Repository)

---

## Scenario

You are reviewing the Unified Data Repository (UDR) component of a free5GC 5G core network. The UDR stores subscription data for all UEs and is queried by multiple NFs (UDM, PCF, NEF).

The function below handles POST requests to create Event Exposure (EE) subscriptions for a given UE ID. The UE ID can be a SUPI (Subscription Permanent Identifier) or GPSI (Generic Public Subscription Identifier). Before processing, the handler validates the `ueId` parameter against a regex pattern.

---

## Code Snippet

```go
// HTTPCreateEeSubscriptions - Creates EE subscriptions of a UE
func (s *Server) HandleCreateEeSubscriptions(c *gin.Context) {
    var eeSubscription models.EeSubscription

    // ... request body parsing omitted for brevity ...

    logger.DataRepoLog.Tracef("Handle CreateEeSubscriptions")

    // String represents the SUPI or GPSI.
    // Pattern: "^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$".
    ueId := c.Params.ByName("ueId")
    if ueId == "" {
        util.EmptyUeIdProblemJson(c)
        return
    }
    match, err := regexp.MatchString(
        "^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$", ueId)
    if !match {
        problemDetail := models.ProblemDetails{
            Title:  "Invalid parameter",
            Status: http.StatusBadRequest,
            Detail: "Invalid ueId",
            Cause:  "INVALID_PARAMETER",
        }
        logger.DataRepoLog.Errorf("Invalid ueId: %s", ueId)
        c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)
        c.JSON(http.StatusBadRequest, problemDetail)
        return
    }
    if err != nil {
        logger.DataRepoLog.Errorf("Invalid regular expression: %s", err)
    }

    s.Processor().CreateEeSubscriptionsProcedure(c, ueId, eeSubscription)
}
```

The same pattern is used in `HandleQueryeesubscriptions` for GET requests.

The comment in the code references this intended pattern from 3GPP TS 29.571:

```
^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|supi-[^@]+)$
```

---

## Question

1. Identify the **security vulnerability** in the regex pattern used for `ueId` validation.
2. Explain the **concrete impact** of this vulnerability on the UDR.
3. Propose a **corrected regex pattern** and explain what it should enforce.

---

## Agent Instructions

Reply ONLY in JSON format:

```json
{
  "answer": {
    "vulnerability": "...",
    "impact": "...",
    "fix": "..."
  },
  "reasoning": "...",
  "confidence": 0.0
}
```
