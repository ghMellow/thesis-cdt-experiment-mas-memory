# Task 10 — 5G Code Security Review: UDM Subscriber Data Management Handlers

**ID:** task10_vuln_udm_validator  
**Tipo:** textual  
**Difficoltà:** media

---

## Scenario

The following Go code is part of the **UDM (Unified Data Management)**. It implements SBI HTTP handlers (Gin framework) for `Nudm_SDM` (Subscriber Data Management) operations, which read a path parameter `supi` (Subscription Permanent Identifier, 3GPP TS 23.003) and pass it to the processor layer.

File: `UDM/api_subscriberdatamanagement.go`

**Snippet A — `HandleGetAmData` (validates the SUPI):**

```go
func (s *Server) HandleGetAmData(c *gin.Context) {
	query := url.Values{}
	query.Set("plmn-id", c.Query("plmn-id"))
	query.Set("supported-features", c.Query("supported-features"))

	logger.SdmLog.Infof("Handle GetAmData")

	// TS 29.503 6.1.3.5.2
	// Validate SUPI format
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
```

**Snippet B — `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData` (same file, same SUPI parameter, no validation):**

```go
func (s *Server) HandleGetSmfSelectData(c *gin.Context) {
	query := url.Values{}
	query.Set("plmn-id", c.Query("plmn-id"))
	query.Set("supported-features", c.Query("supported-features"))

	logger.SdmLog.Infof("Handle GetSmfSelectData")

	supi := c.Params.ByName("supi")
	// use c.Request.URL.Query() only for getPlmnIDStruct
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

// GetTraceData - retrieve a UE's Trace Configuration Data
func (s *Server) HandleGetTraceData(c *gin.Context) {
	logger.SdmLog.Infof("Handle GetTraceData")

	supi := c.Params.ByName("supi")
	plmnID := c.Query("plmn-id")

	s.Processor().GetTraceDataProcedure(c, supi, plmnID)
}

// GetUeContextInSmfData - retrieve a UE's UE Context In SMF Data
func (s *Server) HandleGetUeContextInSmfData(c *gin.Context) {
	logger.SdmLog.Infof("Handle GetUeContextInSmfData")

	supi := c.Params.ByName("supi")
	supportedFeatures := c.Query("supported-features")

	s.Processor().GetUeContextInSmfDataProcedure(c, supi, supportedFeatures)
}
```

---

## Question

1. Identify the security vulnerability in this code (cite the relevant handlers and lines).
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
