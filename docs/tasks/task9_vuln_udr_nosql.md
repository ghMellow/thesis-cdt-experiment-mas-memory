# Task 9 — 5G Code Security Review: UDR Application Data Influence Query

**ID:** task9_vuln_udr_nosql  
**Tipo:** textual  
**Difficoltà:** media

---

## Scenario

The following Go code is part of the **UDR (Unified Data Repository)**. It implements the SBI HTTP handler (Gin framework) for `GET /application-data/influenceData`, which returns "Application Data Influence Data" entries, optionally filtered by query parameters.

File: `UDR/api_datarepository.go`

```go
// HTTPApplicationDataInfluenceDataGet -
func (s *Server) HandleApplicationDataInfluenceDataGet(c *gin.Context) {
	var filter []bson.M
	logger.DataRepoLog.Tracef("Handle ApplicationDataInfluenceDataGet")
	collName := "applicationData.influenceData"

	influenceIdsParam := c.QueryArray("influence-Ids")
	dnnsParam := c.QueryArray("dnns")
	internalGroupIdsParam := c.QueryArray("internal-Group-Id")
	supisParam := c.QueryArray("supis")
	snssaisParam := c.QueryArray("snssais")
	if len(influenceIdsParam) != 0 {
		influenceIds := strings.Split(influenceIdsParam[0], ",")
		filter = append(filter, bson.M{"influenceId": bson.M{"$in": influenceIds}})
	}
	if len(dnnsParam) != 0 {
		dnns := strings.Split(dnnsParam[0], ",")
		filter = append(filter, bson.M{"dnn": bson.M{"$in": dnns}})
	}
	if len(internalGroupIdsParam) != 0 {
		internalGroupIds := strings.Split(internalGroupIdsParam[0], ",")
		withAnyUeIndFilter := []bson.M{
			{
				"interGroupId": bson.M{"$in": internalGroupIds},
			},
			{
				"interGroupId": "AnyUE",
			},
		}
		filter = append(filter, bson.M{"$or": withAnyUeIndFilter})
	} else if len(supisParam) != 0 {
		supis := strings.Split(supisParam[0], ",")
		withAnyUeIndFilter := []bson.M{
			{
				"supi": bson.M{"$in": supis},
			},
			{
				"interGroupId": "AnyUE",
			},
		}
		filter = append(filter, bson.M{"$or": withAnyUeIndFilter})
	}
	if len(snssaisParam) != 0 {
		snssais := s.Processor().ParseSnssaisFromQueryParam(snssaisParam[0])
		matchList := s.Processor().BuildSnssaiMatchList(snssais)
		filter = append(filter, bson.M{"$or": matchList})
	}
	s.Processor().ApplicationDataInfluenceDataGetProcedure(c, collName, filter)
}
```

Note: none of `influence-Ids`, `dnns`, `internal-Group-Id`, `supis`, `snssais` are validated for format or cardinality before being split on `,` and inserted into the BSON filter.

---

## Question

1. Identify any security vulnerability in this code (cite the relevant query parameter(s) and lines).
2. Assess the concrete impact in the context of a 5G core deployment.
3. Propose a specific fix.

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
