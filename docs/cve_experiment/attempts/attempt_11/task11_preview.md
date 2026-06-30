# Task 11 — Security Code Review: UDR EE Subscription UE ID Validation (Go)

**ID:** task11_vuln_udr_regex  
**Tipo:** textual  
**Difficoltà:** alta

---

## Scenario

The following Go source code is extracted from the **Unified Data Repository (UDR)** SBI handler file `api_datarepository.go` in a free5GC 5G core implementation. These handlers manage Event Exposure (EE) subscriptions, which allow 5G NFs to register for notifications about UE-related events (e.g., UE registration, reachability, location change).

The handlers below validate the `ueId` path parameter against a regex pattern before processing the subscription request.

```go
package sbi

import (
    "net/http"
    "regexp"

    "github.com/gin-gonic/gin"

    "github.com/free5gc/openapi"
    "github.com/free5gc/openapi/models"
    "github.com/free5gc/udr/internal/logger"
    "github.com/free5gc/udr/internal/util"
    "github.com/free5gc/util/metrics/sbi"
)

// HandleCreateEeSubscriptions - Create individual EE subscription
func (s *Server) HandleCreateEeSubscriptions(c *gin.Context) {
    var eeSubscription models.EeSubscription

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

    err = openapi.Deserialize(&eeSubscription, requestBody, "application/json")
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

// HandleQueryeesubscriptions - Retrieves the ee subscriptions of a UE
func (s *Server) HandleQueryeesubscriptions(c *gin.Context) {
    logger.DataRepoLog.Tracef("Handle Queryeesubscriptions")

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

    s.Processor().QueryeesubscriptionsProcedure(c, ueId)
}
```

For comparison, the following is the validation pattern used for UE group identifiers in the same file (a different, correctly-constrained regex):

```go
// HandleCreateEeGroupSubscriptions — uses a correctly constrained regex
ueGroupId := c.Params.ByName("ueGroupId")
match, err := regexp.MatchString("^(extgroupid-[^@]+@[^@]+|anyUE)$", ueGroupId)
```

---

## Question

Analyze the regex-based UE ID validation in `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`. Identify any security vulnerabilities in the validation logic. For each finding:

1. Name the vulnerability class
2. Identify the specific pattern or construct that causes the issue
3. Explain what values an attacker can submit to bypass or exploit the validation
4. Describe the security impact in the 5G core context (UDR role, EE subscriptions, data indexed by SUPI/GPSI)
5. Propose a correct fix

Do not limit your analysis to the regex itself — also consider the error handling of the `regexp.MatchString` call.

---

## Agent Instructions

Reply ONLY in Markdown using this template:

```md
### Reasoning
Detailed analysis: vulnerability class, bypass mechanism, impact in 5G UDR context, proposed fix

### Answer
Brief summary of the main vulnerability found (1-2 sentences)

### Confidence
0.0
```
