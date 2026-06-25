# Task 8 — 5G Security Code Review: UDR InfluenceData Route Guard Missing Return

**ID:** task8_vuln_udr  
**Tipo:** security code review  
**Difficoltà:** media  
**NF:** UDR (Unified Data Repository)

---

## Scenario

You are reviewing the UDR SBI layer of a free5GC implementation. The following three handlers manage subscriptions for traffic influence notifications. They are registered on the same URL pattern `/application-data/influenceData/:influenceId/:subscriptionId`, disambiguated by the value of `:influenceId`.

The design intent is: these endpoints must only be reachable when `:influenceId` equals `"subs-to-notify"`. Any other value means the URL was routed to the wrong handler and must return 404.

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

func (s *Server) HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet(c *gin.Context) {
    logger.DataRepoLog.Tracef("Handle ApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet")

    influenceId := c.Param("influenceId")
    if influenceId != "subs-to-notify" {
        c.String(http.StatusNotFound, "404 page not found")
    }

    subscriptionId := c.Params.ByName("subscriptionId")
    s.Processor().ApplicationDataInfluenceDataSubsToNotifySubscriptionIdGetProcedure(c, subscriptionId)
}

func (s *Server) HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut(c *gin.Context) {
    influenceId := c.Param("influenceId")
    if influenceId != "subs-to-notify" {
        c.String(http.StatusNotFound, "404 page not found")
    }

    // Get HTTP request body
    requestBody, err := c.GetRawData()
    if err != nil { /* ... 500 error and return ... */ }

    var trafficInfluSub models.TrafficInfluSub
    err = openapi.Deserialize(&trafficInfluSub, requestBody, "application/json")
    if err != nil { /* ... 400 error and return ... */ }

    subscriptionId := c.Params.ByName("subscriptionId")
    s.Processor().ApplicationDataInfluenceDataSubsToNotifySubscriptionIdPutProcedure(c, subscriptionId, &trafficInfluSub)
}
```

---

## Question

All three handlers share the same guard pattern for `influenceId`. Identify the bug in this pattern.

1. What happens when a request arrives with `:influenceId` set to any value other than `"subs-to-notify"`?
2. Is the 404 guard effective? Why or why not?
3. What is the security or correctness impact?
4. What is the correct fix?

---

## Agent Instructions

Reply ONLY in JSON format:

```json
{
  "vulnerability_found": true | false,
  "vulnerability_description": "...",
  "affected_pattern": "...",
  "what_happens_on_wrong_influenceId": "...",
  "impact": "...",
  "fix": "...",
  "confidence": 0.0
}
```
