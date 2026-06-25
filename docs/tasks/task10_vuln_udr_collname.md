# Task 10 — Security Code Review: UDR SDM Subscription Handler — Wrong Collection Name (Go)

**ID:** task10_vuln_udr_collname  
**Tipo:** textual  
**Difficoltà:** alta

---

## Scenario

The following Go source file excerpt is from the **Unified Data Repository (UDR)** SBI handler in a free5GC 5G core implementation. The UDR stores multiple categories of UE data in distinct MongoDB collections, identified by the `collName` variable passed to the processor.

SDM (Subscriber Data Management) subscriptions allow NFs such as the UDM to subscribe to change notifications for specific UE subscription data. They are stored in a dedicated collection separate from the AMF non-3GPP access context data.

Perform a **security code review** of the handler below. Pay close attention to the collection name used and compare it against the surrounding handlers.

```go
package sbi

import (
	"net/http"

	"github.com/gin-gonic/gin"

	"github.com/free5gc/openapi"
	"github.com/free5gc/openapi/models"
	"github.com/free5gc/udr/internal/logger"
	"github.com/free5gc/udr/internal/util"
	"github.com/free5gc/util/metrics/sbi"
)

// HTTPCreateSdmSubscriptions - Create individual sdm subscription
// POST /subscription-data/:ueId/:servingPlmnId/sdm-subscriptions
func (s *Server) HandleCreateSdmSubscriptions(c *gin.Context) {
	var sdmSubscription models.SdmSubscription

	requestBody, err := c.GetRawData()
	if err != nil {
		problemDetail := models.ProblemDetails{
			Title:  "System failure",
			Status: http.StatusInternalServerError,
			Detail: err.Error(),
			Cause:  "SYSTEM_FAILURE",
		}
		logger.DataRepoLog.Errorf("Get Request Body error: %+v", err)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)
		c.JSON(http.StatusInternalServerError, problemDetail)
		return
	}

	err = openapi.Deserialize(&sdmSubscription, requestBody, "application/json")
	if err != nil {
		problemDetail := "[Request Body] " + err.Error()
		rsp := models.ProblemDetails{
			Title:  "Malformed request syntax",
			Status: http.StatusBadRequest,
			Detail: problemDetail,
		}
		logger.DataRepoLog.Errorln(problemDetail)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(rsp.Status)))
		c.JSON(http.StatusBadRequest, rsp)
		return
	}

	logger.DataRepoLog.Tracef("Handle CreateSdmSubscriptions")

	collName := "subscriptionData.contextData.amfNon3gppAccess"
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}

	s.Processor().CreateSdmSubscriptionsProcedure(c, sdmSubscription, collName, ueId)
}

// HTTPQuerysdmsubscriptions - Retrieves the sdm subscriptions of a UE
// GET /subscription-data/:ueId/:servingPlmnId/sdm-subscriptions
func (s *Server) HandleQuerysdmsubscriptions(c *gin.Context) {
	logger.DataRepoLog.Tracef("Handle Querysdmsubscriptions")

	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}

	s.Processor().QuerysdmsubscriptionsProcedure(c, ueId)
}

// HTTPCreateAmfContextNon3gpp - To store the AMF context data of a UE using non-3gpp access in the UDR
// PUT /subscription-data/:ueId/:servingPlmnId/amf-non-3gpp-access
func (s *Server) HandleCreateAmfContextNon3gpp(c *gin.Context) {
	var amfNon3GppAccessRegistration models.AmfNon3GppAccessRegistration

	requestBody, err := c.GetRawData()
	if err != nil {
		problemDetail := models.ProblemDetails{
			Title:  "System failure",
			Status: http.StatusInternalServerError,
			Detail: err.Error(),
			Cause:  "SYSTEM_FAILURE",
		}
		logger.DataRepoLog.Errorf("Get Request Body error: %+v", err)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)
		c.JSON(http.StatusInternalServerError, problemDetail)
		return
	}

	err = openapi.Deserialize(&amfNon3GppAccessRegistration, requestBody, "application/json")
	if err != nil {
		problemDetail := "[Request Body] " + err.Error()
		rsp := models.ProblemDetails{
			Title:  "Malformed request syntax",
			Status: http.StatusBadRequest,
			Detail: problemDetail,
		}
		logger.DataRepoLog.Errorln(problemDetail)
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(rsp.Status)))
		c.JSON(http.StatusBadRequest, rsp)
		return
	}

	logger.DataRepoLog.Tracef("Handle CreateAmfContextNon3gpp")
	ueId := c.Params.ByName("ueId")
	if ueId == "" {
		util.EmptyUeIdProblemJson(c)
		return
	}

	s.Processor().CreateAmfContextNon3gppProcedure(
		c, amfNon3GppAccessRegistration, "subscriptionData.contextData.amfNon3gppAccess", ueId)
}
```

For additional context, other SDM-related collection names in the same file include:
- `"subscriptionData.contextData.sdmSubscriptions"` — used in the SMF context handler

---

## Question

Identify the security or correctness vulnerability present in `HandleCreateSdmSubscriptions`. For your finding:

1. Name the vulnerability class or error type
2. Describe precisely what is wrong — compare the `collName` used against what it should be
3. Explain what happens at runtime: where does the SDM subscription document end up, what gets overwritten or mixed up, and what is the security/availability impact in the 5G core
4. Propose the correct fix

---

## Agent Instructions

Reply ONLY in Markdown using this template:

```md
### Reasoning
Detailed analysis: what is wrong, why, what happens at runtime, impact, fix

### Answer
Brief summary of the vulnerability found (1-2 sentences)

### Confidence
0.0
```
