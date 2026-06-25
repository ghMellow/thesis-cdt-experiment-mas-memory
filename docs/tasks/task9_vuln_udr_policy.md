# Task 9 — Security Code Review: UDR Policy Data Subscription Handlers (Go)

**ID:** task9_vuln_udr_policy  
**Tipo:** textual  
**Difficoltà:** media

---

## Scenario

The following Go source file excerpts are from the **Unified Data Repository (UDR)** SBI handler in a free5GC 5G core implementation. These handlers manage policy data subscriptions: external NFs (e.g., PCF) POST subscriptions to receive notifications when UE policy data changes, and can update existing subscriptions via PUT.

Perform a **security code review** of the two handlers below. Focus on control flow correctness after error conditions.

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

// HandlePolicyDataSubsToNotifyPost - Create a new policy data subscription
// POST /policy-data/subs-to-notify
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

// HandlePolicyDataSubsToNotifySubsIdPut - Update an existing policy data subscription
// PUT /policy-data/subs-to-notify/:subsId
func (s *Server) HandlePolicyDataSubsToNotifySubsIdPut(c *gin.Context) {
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

	logger.DataRepoLog.Tracef("Handle PolicyDataSubsToNotifySubsIdPut")

	subsId := c.Params.ByName("subsId")
	s.Processor().PolicyDataSubsToNotifySubsIdPutProcedure(c, subsId, policyDataSubscription)
}
```

For reference, here is a correctly implemented handler from the same file that manages the same kind of data (policy data BDT):

```go
// HandlePolicyDataBdtDataBdtReferenceIdPut - correctly implemented
func (s *Server) HandlePolicyDataBdtDataBdtReferenceIdPut(c *gin.Context) {
	var bdtData models.BdtData

	if err := getDataFromRequestBody(c, &bdtData); err != nil {
		return
	}
	logger.DataRepoLog.Tracef("Handle PolicyDataBdtDataBdtReferenceIdPut")

	collName := "policyData.bdtData"
	bdtReferenceId := c.Params.ByName("bdtReferenceId")
	s.Processor().PolicyDataBdtDataBdtReferenceIdPutProcedure(c, collName, bdtReferenceId, bdtData)
}
```

---

## Question

Identify all security vulnerabilities or logic errors present in the two handlers shown above. For each finding:

1. Name the vulnerability class or error type
2. Identify the exact location(s) within each handler where the issue occurs
3. Explain the security or reliability impact in the context of a 5G UDR storing policy data subscriptions
4. Propose a correct fix, using the reference handler as a guide if helpful

**Hint:** Pay close attention to what happens in Go after calling `c.JSON(...)` without a subsequent `return` statement.

---

## Agent Instructions

Reply ONLY in Markdown using this template:

```md
### Reasoning
Detailed analysis for each finding: class, location, impact, fix

### Answer
Brief summary of the main vulnerability found (1-2 sentences)

### Confidence
0.0
```
