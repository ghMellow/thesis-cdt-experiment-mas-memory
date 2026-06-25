# Task 5 — Security Code Review: Missing Flow Control

**ID:** task5_vuln_missing_return
**Tipo:** textual
**Difficoltà:** bassa

---

## Scenario

You are a 5G security engineer reviewing the SBI (Service Based Interface) layer of a UDR (Unified Data Repository) network function before deployment. A colleague has flagged the following three handlers as potentially problematic.

The UDR exposes REST endpoints for managing application influence data subscriptions. Due to a routing conflict in the Gin framework, the path `/application-data/influenceData/:influenceId/:subscriptionId` is shared between the `subs-to-notify` resource and individual influence data items. The handlers below are responsible for routing correctly based on the value of `influenceId`.

**Handler 1 — DELETE**

```go
func (s *Server) HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete(c *gin.Context) {
    logger.DataRepoLog.Tracef("Handle ApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete")

    influenceId := c.Param("influenceId")
    if influenceId != "subs-to-notify" {
        c.String(http.StatusNotFound, "404 page not found")
    }

    subscriptionId := c.Params.ByName("subscriptionId")
    s.Processor().ApplicationDataInfluenceDataSubsToNotifySubscriptionIdDeleteProcedure(c, subscriptionId)
}
```

**Handler 2 — GET**

```go
func (s *Server) HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet(c *gin.Context) {
    logger.DataRepoLog.Tracef("Handle ApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet")

    influenceId := c.Param("influenceId")
    if influenceId != "subs-to-notify" {
        c.String(http.StatusNotFound, "404 page not found")
    }

    subscriptionId := c.Params.ByName("subscriptionId")
    s.Processor().ApplicationDataInfluenceDataSubsToNotifySubscriptionIdGetProcedure(c, subscriptionId)
}
```

**Handler 3 — PUT**

```go
func (s *Server) HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut(c *gin.Context) {
    influenceId := c.Param("influenceId")
    if influenceId != "subs-to-notify" {
        c.String(http.StatusNotFound, "404 page not found")
    }

    requestBody, err := c.GetRawData()
    if err != nil { /* ... error handling ... */ return }

    var trafficInfluSub models.TrafficInfluSub
    err = openapi.Deserialize(&trafficInfluSub, requestBody, "application/json")
    if err != nil { /* ... error handling ... */ return }

    subscriptionId := c.Params.ByName("subscriptionId")
    s.Processor().ApplicationDataInfluenceDataSubsToNotifySubscriptionIdPutProcedure(c, subscriptionId, &trafficInfluSub)
}
```

---

## Question

Identify any security weaknesses or implementation bugs present in the code above.

For each issue found, describe:
- what the problem is
- what an attacker or a misbehaving client could trigger as a consequence

---

## Agent Instructions

Reply ONLY in JSON format:

```json
{
  "answer": "description of the vulnerability or vulnerabilities found",
  "reasoning": "technical explanation of the issue and its consequences",
  "confidence": 0.0
}
```
