# Task 8 — Security Code Review: UDM Subscriber Data Management Handler (Go)

**ID:** task8_vuln_udm  
**Tipo:** textual  
**Difficoltà:** media-alta

---

## Scenario

The following Go source file is the Subscriber Data Management SBI handler of the **Unified Data Management (UDM)** function in a free5GC 5G core implementation. The UDM stores and provides access to UE subscription data (mobility, session management, authentication) to other NFs. Each endpoint is keyed by a SUPI (Subscription Permanent Identifier) or GPSI.

Perform a **security code review** of the representative handler selection below. Focus on input validation consistency — pay attention to which handlers validate identifiers before use and which do not.

```go
package sbi

import (
	"net/http"
	"strings"
	"net/url"
	"encoding/json"

	"github.com/gin-gonic/gin"

	"github.com/free5gc/openapi"
	"github.com/free5gc/openapi/models"
	"github.com/free5gc/udm/internal/logger"
	"github.com/free5gc/util/metrics/sbi"
	"github.com/free5gc/util/validator"
)

// GetAmData - retrieve a UE's Access and Mobility Subscription Data
func (s *Server) HandleGetAmData(c *gin.Context) {
	query := url.Values{}
	query.Set("plmn-id", c.Query("plmn-id"))
	query.Set("supported-features", c.Query("supported-features"))

	supi := c.Params.ByName("supi")
	if !validator.IsValidSupi(supi) {
		problemDetail := models.ProblemDetails{
			Title:  "Malformed request syntax",
			Status: http.StatusBadRequest,
			Detail: "Supi is invalid",
			Cause:  "MANDATORY_IE_INCORRECT",
		}
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(problemDetail.Status)))
		c.JSON(int(problemDetail.Status), problemDetail)
		return
	}

	plmnIDStruct, problemDetails := s.getPlmnIDStruct(c.Request.URL.Query())
	if problemDetails != nil {
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetails.Cause)
		c.JSON(int(problemDetails.Status), problemDetails)
		return
	}
	var plmnID string
	if plmnIDStruct != nil {
		plmnID = plmnIDStruct.Mcc + plmnIDStruct.Mnc
	}
	supportedFeatures := query.Get("supported-features")
	s.Processor().GetAmDataProcedure(c, supi, plmnID, supportedFeatures)
}

// GetSmfSelectData - retrieve a UE's SMF Selection Subscription Data
func (s *Server) HandleGetSmfSelectData(c *gin.Context) {
	query := url.Values{}
	query.Set("plmn-id", c.Query("plmn-id"))
	query.Set("supported-features", c.Query("supported-features"))

	supi := c.Params.ByName("supi")
	plmnIDStruct, problemDetails := s.getPlmnIDStruct(c.Request.URL.Query())
	if problemDetails != nil {
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetails.Cause)
		c.JSON(int(problemDetails.Status), problemDetails)
		return
	}
	var plmnID string
	if plmnIDStruct != nil {
		plmnID = plmnIDStruct.Mcc + plmnIDStruct.Mnc
	}
	supportedFeatures := query.Get("supported-features")
	s.Processor().GetSmfSelectDataProcedure(c, supi, plmnID, supportedFeatures)
}

// GetNssai - retrieve a UE's subscribed NSSAI
func (s *Server) HandleGetNssai(c *gin.Context) {
	query := url.Values{}
	query.Set("plmn-id", c.Query("plmn-id"))
	query.Set("supported-features", c.Query("supported-features"))

	supi := c.Params.ByName("supi")
	plmnIDStruct, problemDetails := s.getPlmnIDStruct(c.Request.URL.Query())
	if problemDetails != nil {
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetails.Cause)
		c.JSON(int(problemDetails.Status), problemDetails)
		return
	}
	var plmnID string
	if plmnIDStruct != nil {
		plmnID = plmnIDStruct.Mcc + plmnIDStruct.Mnc
	}
	supportedFeatures := query.Get("supported-features")
	s.Processor().GetNssaiProcedure(c, supi, plmnID, supportedFeatures)
}

// GetSmData - retrieve a UE's Session Management Subscription Data
func (s *Server) HandleGetSmData(c *gin.Context) {
	query := url.Values{}
	query.Set("plmn-id", c.Query("plmn-id"))
	query.Set("dnn", c.Query("dnn"))
	query.Set("single-nssai", c.Query("single-nssai"))
	query.Set("supported-features", c.Query("supported-features"))

	supi := c.Params.ByName("supi")
	plmnIDStruct, problemDetails := s.getPlmnIDStruct(c.Request.URL.Query())
	if problemDetails != nil {
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetails.Cause)
		c.JSON(int(problemDetails.Status), problemDetails)
		return
	}
	var plmnID string
	if plmnIDStruct != nil {
		plmnID = plmnIDStruct.Mcc + plmnIDStruct.Mnc
	}
	Dnn := query.Get("dnn")
	Snssai := query.Get("single-nssai")
	supportedFeatures := query.Get("supported-features")
	s.Processor().GetSmDataProcedure(c, supi, plmnID, Dnn, Snssai, supportedFeatures)
}

// GetTraceData - retrieve a UE's Trace Configuration Data
func (s *Server) HandleGetTraceData(c *gin.Context) {
	supi := c.Params.ByName("supi")
	plmnID := c.Query("plmn-id")
	s.Processor().GetTraceDataProcedure(c, supi, plmnID)
}

// GetUeContextInSmfData - retrieve a UE's UE Context In SMF Data
func (s *Server) HandleGetUeContextInSmfData(c *gin.Context) {
	supi := c.Params.ByName("supi")
	supportedFeatures := c.Query("supported-features")
	s.Processor().GetUeContextInSmfDataProcedure(c, supi, supportedFeatures)
}

// GetSupi - retrieve multiple data sets
func (s *Server) HandleGetSupi(c *gin.Context) {
	query := url.Values{}
	query.Set("plmn-id", c.Query("plmn-id"))
	query.Set("dataset-names", c.Query("dataset-names"))
	query.Set("supported-features", c.Query("supported-features"))

	supi := c.Params.ByName("supi")
	plmnIDStruct, problemDetails := s.getPlmnIDStruct(c.Request.URL.Query())
	if problemDetails != nil {
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetails.Cause)
		c.JSON(int(problemDetails.Status), problemDetails)
		return
	}
	var plmnID string
	if plmnIDStruct != nil {
		plmnID = plmnIDStruct.Mcc + plmnIDStruct.Mnc
	}
	dataSetNames := strings.Split(query.Get("dataset-names"), ",")
	supportedFeatures := query.Get("supported-features")
	s.Processor().GetSupiProcedure(c, supi, plmnID, dataSetNames, supportedFeatures)
}

// Unsubscribe - unsubscribe from notifications
func (s *Server) HandleUnsubscribe(c *gin.Context) {
	// TS 29.503 6.1.3.4.2
	ueId := c.Params.ByName("ueId")
	valid := validator.IsValidGpsi(ueId) || validator.IsValidSupi(ueId)
	if !valid {
		problemDetail := models.ProblemDetails{
			Title:  "Malformed request syntax",
			Status: http.StatusBadRequest,
			Detail: "UE ID is invalid",
			Cause:  "MANDATORY_IE_INCORRECT",
		}
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(int(problemDetail.Status)))
		c.JSON(int(problemDetail.Status), problemDetail)
		return
	}
	subscriptionID := c.Params.ByName("subscriptionId")
	s.Processor().UnsubscribeProcedure(c, ueId, subscriptionID)
}
```

---

## Question

Identify all security vulnerabilities or logic errors present in this code. For each finding:

1. Name the vulnerability class or error type
2. Identify the exact function(s) and describe the specific code pattern that is problematic
3. Explain the security impact in the context of the UDM, which is the authoritative source of UE subscription data in the 5G core
4. Propose a correct fix

**Pay special attention to:**

- **Input validation consistency:** Compare how different handlers for the same NF treat the `supi` path parameter. Are all handlers equally defensive?
- **3GPP TS 29.503 requirement:** Section 6.1.3.5.2 requires that the SUPI format be validated at the SBI boundary. Which handlers comply with this requirement and which do not?
- **Impact of missing validation:** If a SUPI with malformed format reaches the UDM processor and then the UDR, what classes of downstream issues can arise?

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
