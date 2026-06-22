# Task 8 — 5G Code Vulnerability Detection (UDR)

**ID:** task8_vuln_udr  
**Tipo:** textual  
**Difficoltà:** alta

---

## Scenario

The following handlers are taken from the **UDR** (Unified Data Repository) of
free5gc, in the `Nudr_DataRepository` SBI. They handle the
`application-data/influenceData/subs-to-notify` resources. Because of a Gin
wildcard limitation, the `:influenceId` path segment is expected to carry the
literal value `"subs-to-notify"`, and each handler checks it before proceeding.

```go
func (s *Server) HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete(c *gin.Context) {
	logger.DataRepoLog.Tracef("Handle ...SubscriptionIdDelete")

	influenceId := c.Param("influenceId")
	if influenceId != "subs-to-notify" {
		c.String(http.StatusNotFound, "404 page not found")
	}

	subscriptionId := c.Params.ByName("subscriptionId")

	s.Processor().ApplicationDataInfluenceDataSubsToNotifySubscriptionIdDeleteProcedure(c, subscriptionId)
}

func (s *Server) HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet(c *gin.Context) {
	logger.DataRepoLog.Tracef("Handle ...SubscriptionIdGet")

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

	requestBody, err := c.GetRawData()
	if err != nil {
		// ... return 500 ProblemDetails ...
		return
	}

	var trafficInfluSub models.TrafficInfluSub
	err = openapi.Deserialize(&trafficInfluSub, requestBody, "application/json")
	if err != nil {
		// ... return 400 Malformed request syntax ...
		return
	}

	subscriptionId := c.Params.ByName("subscriptionId")

	s.Processor().ApplicationDataInfluenceDataSubsToNotifySubscriptionIdPutProcedure(c, subscriptionId, &trafficInfluSub)
}
```

---

## Question

Analyze the code and identify the **security vulnerability** it contains.
Explain the mechanism that triggers it and its impact, and point to the
function(s) and line(s) responsible.

---

## Agent Instructions

Reply ONLY in JSON format:

```json
{
  "answer": {
    "vulnerabilities": [
      {
        "type": "short vulnerability class (e.g. DoS, injection, ...)",
        "location": "function and/or line reference",
        "severity": "low | medium | high | critical",
        "description": "what is wrong and why"
      }
    ]
  },
  "reasoning": "...",
  "confidence": 0.0
}
```
