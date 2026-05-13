# Task 6 — Security Code Review: UDR Data Repository Handler (Go)

**ID:** task6_vuln_udr  
**Tipo:** textual  
**Difficoltà:** alta

---

## Scenario

The following Go source file is part of the **Unified Data Repository (UDR)** SBI handler in a free5GC 5G core implementation. The UDR stores subscription data for all UEs and is accessed by other NFs (AMF, SMF, PCF) via REST APIs.

Perform a **security code review** of the excerpts below, taken from `api_datarepository.go`. Focus on logic errors, missing control flow statements, and input validation issues that could allow unauthorized data access or unintended backend operations.

```go
package sbi

import (
	"encoding/json"
	"net/http"
	"regexp"
	"strings"

	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/bson"

	"github.com/free5gc/openapi"
	"github.com/free5gc/openapi/models"
	udr_context "github.com/free5gc/udr/internal/context"
	"github.com/free5gc/udr/internal/logger"
	"github.com/free5gc/udr/internal/util"
	"github.com/free5gc/util/metrics/sbi"
)

// --- Section A: Influence Data handlers ---

// HTTPApplicationDataInfluenceDataGet handles GET /application-data/influenceData
func (s *Server) HandleApplicationDataInfluenceDataGet(c *gin.Context) {
	var filter []bson.M
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
			{"interGroupId": bson.M{"$in": internalGroupIds}},
			{"interGroupId": "AnyUE"},
		}
		filter = append(filter, bson.M{"$or": withAnyUeIndFilter})
	} else if len(supisParam) != 0 {
		supis := strings.Split(supisParam[0], ",")
		withAnyUeIndFilter := []bson.M{
			{"supi": bson.M{"$in": supis}},
			{"interGroupId": "AnyUE"},
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

/*
 * GIN wildcard issue:
 * '/application-data/influenceData/:influenceId' and
 * '/application-data/influenceData/subs-to-notify' patterns will be conflicted.
 * Only can use '/application-data/influenceData/:influenceId' pattern.
 * Here ":influenceId" value should be "subs-to-notify".
 */

// HTTPApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete
func (s *Server) HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete(c *gin.Context) {
	influenceId := c.Param("influenceId")
	if influenceId != "subs-to-notify" {
		c.String(http.StatusNotFound, "404 page not found")
	}

	subscriptionId := c.Params.ByName("subscriptionId")
	s.Processor().ApplicationDataInfluenceDataSubsToNotifySubscriptionIdDeleteProcedure(c, subscriptionId)
}

// HTTPApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet
func (s *Server) HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet(c *gin.Context) {
	influenceId := c.Param("influenceId")
	if influenceId != "subs-to-notify" {
		c.String(http.StatusNotFound, "404 page not found")
	}

	subscriptionId := c.Params.ByName("subscriptionId")
	s.Processor().ApplicationDataInfluenceDataSubsToNotifySubscriptionIdGetProcedure(c, subscriptionId)
}

// HTTPApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut
func (s *Server) HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut(c *gin.Context) {
	influenceId := c.Param("influenceId")
	if influenceId != "subs-to-notify" {
		c.String(http.StatusNotFound, "404 page not found")
	}

	requestBody, err := c.GetRawData()
	if err != nil {
		problemDetail := models.ProblemDetails{
			Title:  "System failure",
			Status: http.StatusInternalServerError,
			Detail: err.Error(),
			Cause:  "SYSTEM_FAILURE",
		}
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)
		c.JSON(http.StatusInternalServerError, problemDetail)
		return
	}
	// ... (deserialization and processor call follow)
	s.Processor().ApplicationDataInfluenceDataSubsToNotifySubscriptionIdPutProcedure(c, subscriptionId)
}

// --- Section B: EE Subscriptions with regex validation ---

// HTTPCreateEeGroupSubscriptions - Create a group EE subscription
func (s *Server) HandleCreateEeGroupSubscriptions(c *gin.Context) {
	// ... (request body parsing omitted)

	// pattern: '^(extgroupid-[^@]+@[^@]+|anyUE)$' -- 3GPP 29.505 5.2.29.2
	ueGroupId := c.Params.ByName("ueGroupId")

	match, err := regexp.MatchString("^(extgroupid-[^@]+@[^@]+|anyUE)$", ueGroupId)
	if !match {
		problemDetail := models.ProblemDetails{
			Title:  "Invalid parameter",
			Status: http.StatusBadRequest,
			Detail: "Invalid ueGroupId",
			Cause:  "INVALID_PARAMETER",
		}
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)
		c.JSON(http.StatusBadRequest, problemDetail)
		return
	}
	if err != nil {
		logger.DataRepoLog.Errorf("Invalid regular expression: %s", err)
	}

	s.Processor().CreateEeGroupSubscriptionsProcedure(c, ueGroupId, eeSubscription)
}

// HTTPCreateEeSubscriptions - Create individual EE subscription
func (s *Server) HandleCreateEeSubscriptions(c *gin.Context) {
	// ... (request body parsing omitted)

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
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)
		c.JSON(http.StatusBadRequest, problemDetail)
		return
	}
	if err != nil {
		logger.DataRepoLog.Errorf("Invalid regular expression: %s", err)
	}

	s.Processor().CreateEeSubscriptionsProcedure(c, ueId, eeSubscription)
}

// HTTPQueryeesubscriptions - Retrieves the ee subscriptions of a UE
func (s *Server) HandleQueryeesubscriptions(c *gin.Context) {
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
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)
		c.JSON(http.StatusBadRequest, problemDetail)
		return
	}
	if err != nil {
		logger.DataRepoLog.Errorf("Invalid regular expression: %s", err)
	}

	s.Processor().QueryeesubscriptionsProcedure(c, ueId)
}

// --- Section C: subscription-data handlers (representative sample) ---

// HTTPQueryAmfContext3gpp - Retrieves the AMF context data of a UE using 3gpp access
func (s *Server) HandleQueryAmfContext3gpp(c *gin.Context) {
	ueId := c.Params.ByName("ueId")
	collName := "subscriptionData.contextData.amf3gppAccess"

	if ueId == "" {
		problemDetail := &models.ProblemDetails{
			Title:  util.MALFORMED_REQUEST,
			Status: http.StatusBadRequest,
			Detail: "ueId is required",
		}
		util.GinProblemJson(c, problemDetail)
		return
	}

	s.Processor().QueryAmfContext3gppProcedure(c, collName, ueId)
}

func (s *Server) HandleAmfContext3gpp(c *gin.Context) {
	var patchItemArray []models.PatchItem
	requestBody, err := c.GetRawData()
	if err != nil {
		problemDetail := models.ProblemDetails{
			Title:  "System failure",
			Status: http.StatusInternalServerError,
			Detail: err.Error(),
			Cause:  "SYSTEM_FAILURE",
		}
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)
		c.JSON(http.StatusInternalServerError, problemDetail)
		return
	}
	err = openapi.Deserialize(&patchItemArray, requestBody, "application/json")
	if err != nil {
		problemDetail := "[Request Body] " + err.Error()
		rsp := models.ProblemDetails{
			Title:  "Malformed request syntax",
			Status: http.StatusBadRequest,
			Detail: problemDetail,
		}
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(rsp.Status)))
		c.JSON(http.StatusBadRequest, rsp)
		return
	}
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	filter := bson.M{"ueId": ueId}
	s.Processor().AmfContext3gppProcedure(c, collName, ueId, patchItemArray, filter)
}

// HTTPPolicyDataUesUeIdSmDataGet
func (s *Server) HandlePolicyDataUesUeIdSmDataGet(c *gin.Context) {
	collName := "policyData.ues.smData"
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}
	sNssai := models.Snssai{}
	sNssaiQuery := c.Request.URL.Query().Get("snssai")
	dnn := c.Request.URL.Query().Get("dnn")

	err := json.Unmarshal([]byte(sNssaiQuery), &sNssai)
	if err != nil {
		logger.DataRepoLog.Warnln(err)
	}
	s.Processor().PolicyDataUesUeIdSmDataGetProcedure(c, collName, ueId, sNssai, dnn)
}
```

---

## Question

Identify all security vulnerabilities or logic errors present in this code. For each finding:

1. Name the vulnerability class or error type
2. Identify the exact function(s) and the specific lines or patterns where the issue occurs
3. Explain the security impact in the context of a 5G UDR that stores UE subscription data
4. Propose a correct fix

**Pay special attention to:**

- **Control flow in Gin handlers:** When a Gin context method (e.g., `c.String()`, `c.JSON()`) writes an HTTP response, does execution halt in Go, or does the handler continue running? Examine the three `subs-to-notify` handlers (Section A) to see if the absence of `return` after `c.String(http.StatusNotFound, ...)` allows code to proceed to the processor call.
- **Regex validation patterns:** Analyze the regex patterns used for `ueId` validation in Section B. Specifically, look at the final alternative in the pattern. Does a catch-all branch like `|.+` undermine the entire regex logic?
- **UDR-specific impact:** Explain how vulnerabilities affect UDR operations on subscription collections (e.g., unauthorized DELETE/GET/PUT on `influenceData.subs-to-notify` subscriptions, or arbitrary `ueId` values reaching the MongoDB persistence layer).

---

## Agent Instructions

Reply ONLY in Markdown using this template:

```md
### Answer
Brief summary listing the main vulnerability types found (1-3 sentences)

### Reasoning
Detailed analysis for each finding: class, location, impact, fix

### Confidence
0.0
```
