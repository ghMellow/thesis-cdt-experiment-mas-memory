# Task 7 — 5G Security Code Review: UDR PolicyDataSubsToNotifyPost Handler

**ID:** task7_vuln_udr  
**Tipo:** security code review  
**Difficoltà:** alta  
**NF:** UDR (Unified Data Repository)

---

## Scenario

You are reviewing the HTTP handler for `PolicyDataSubsToNotifyPost` in the UDR SBI layer of a free5GC implementation. This endpoint allows NFs (e.g., PCF) to subscribe to policy data change notifications.

For reference, a working handler elsewhere in the same codebase uses a helper function:

```go
// Helper function used by other handlers
func getDataFromRequestBody(c *gin.Context, data interface{}) error {
    reqBody, err := c.GetRawData()
    if err != nil {
        pd := openapi.ProblemDetailsSystemFailure(err.Error())
        c.JSON(http.StatusInternalServerError, pd)
        return err
    }
    err = openapi.Deserialize(data, reqBody, "application/json")
    if err != nil {
        pd := util.ProblemDetailsMalformedReqSyntax(err.Error())
        c.JSON(http.StatusBadRequest, pd)
        return err
    }
    return err
}
```

The handler under review does NOT use this helper. Instead it is implemented inline:

```go
func (s *Server) HandlePolicyDataSubsToNotifyPost(c *gin.Context) {
    var policyDataSubscription models.PolicyDataSubscription

    reqBody, err := c.GetRawData()
    if err != nil {
        logger.DataRepoLog.Errorf("Get Request Body error: %+v", err)
        pd := openapi.ProblemDetailsSystemFailure(err.Error())
        c.Set(sbi.IN_PB_DETAILS_CTX_STR, pd.Cause)
        c.JSON(http.StatusInternalServerError, pd)
    }

    err = openapi.Deserialize(policyDataSubscription, reqBody, "application/json")
    if err != nil {
        logger.DataRepoLog.Errorf("Deserialize Request Body error: %+v", err)
        pd := util.ProblemDetailsMalformedReqSyntax(err.Error())
        c.Set(sbi.IN_PB_DETAILS_CTX_STR, pd.Cause)
        c.JSON(http.StatusBadRequest, pd)
    }

    logger.DataRepoLog.Tracef("Handle PolicyDataSubsToNotifyPost")

    s.Processor().PolicyDataSubsToNotifyPostProcedure(c, policyDataSubscription)
}
```

The signature of `openapi.Deserialize` is:
```go
func Deserialize(v interface{}, b []byte, contentType string) error
```

---

## Question

This handler contains at least two distinct bugs. Identify both of them:

1. Describe each bug precisely, referencing the specific line or expression where it occurs.
2. For each bug, explain the runtime consequence.
3. Propose a correct fix for each.

---

## Agent Instructions

Reply ONLY in JSON format:

```json
{
  "bugs": [
    {
      "bug_id": 1,
      "description": "...",
      "affected_expression": "...",
      "runtime_consequence": "...",
      "fix": "..."
    },
    {
      "bug_id": 2,
      "description": "...",
      "affected_expression": "...",
      "runtime_consequence": "...",
      "fix": "..."
    }
  ],
  "confidence": 0.0
}
```
