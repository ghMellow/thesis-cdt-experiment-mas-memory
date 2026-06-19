# Task 7 — 5G Code Security Review: UDR Input Validation (ueId)

**ID:** task7_vuln_udr_regex  
**Tipo:** textual  
**Difficoltà:** alta

---

## Scenario

The following Go code is part of the **UDR (Unified Data Repository)**. It implements SBI HTTP handlers (Gin framework) that read a path parameter `ueId` (a SUPI or GPSI per 3GPP TS 29.505) and use it to build a MongoDB query filter.

File: `UDR/api_datarepository.go`

**Snippet A — `HandleCreateEeSubscriptions` (and identically in `HandleQueryeesubscriptions`):**

```go
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
```

**Snippet B — `HandleCreateAmfContext3gpp`, `HandleQueryAmfContext3gpp`, and many other `Handle*` functions in the same file (this is the dominant pattern across dozens of handlers):**

```go
ueId := c.Params.ByName("ueId")
if ueId == "" {
	util.EmptyUeIdProblemJson(c)
	return
}
filter := bson.M{"ueId": ueId}
s.Processor().CreateAmfContext3gppProcedure(c, collName, ueId, amf3GppAccessRegistration)
```

**For comparison, the UDM (Unified Data Management) NF in the same codebase validates the equivalent `supi` path parameter like this:**

```go
// UDM/api_subscriberdatamanagement.go — HandleGetAmData
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
```

---

## Question

1. Identify the security vulnerability/vulnerabilities in this code (cite the relevant lines/patterns). Consider both Snippet A and Snippet B, and the comparison with UDM.
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
