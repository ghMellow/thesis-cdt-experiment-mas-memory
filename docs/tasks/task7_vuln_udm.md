# Task 7 — 5G Code Vulnerability Detection (UDM)

**ID:** task7_vuln_udm  
**Tipo:** textual  
**Difficoltà:** media-alta

---

## Scenario

The following handlers are taken from the **UDM** (Unified Data Management)
function of free5gc, in the `Nudm_SubscriberDataManagement` SBI. They all read a
`supi` (Subscription Permanent Identifier) from the URL path and forward it to
the data layer.

```go
// GetAmData - retrieve a UE's Access and Mobility Subscription Data
func (s *Server) HandleGetAmData(c *gin.Context) {
	query := url.Values{}
	query.Set("plmn-id", c.Query("plmn-id"))
	query.Set("supported-features", c.Query("supported-features"))

	logger.SdmLog.Infof("Handle GetAmData")

	// TS 29.503 6.1.3.5.2 — Validate SUPI format
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

// GetSmfSelectData - retrieve a UE's SMF Selection Subscription Data
func (s *Server) HandleGetSmfSelectData(c *gin.Context) {
	query := url.Values{}
	query.Set("plmn-id", c.Query("plmn-id"))
	query.Set("supported-features", c.Query("supported-features"))

	logger.SdmLog.Infof("Handle GetSmfSelectData")

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

// GetSmData - retrieve a UE's Session Management Subscription Data
func (s *Server) HandleGetSmData(c *gin.Context) {
	query := url.Values{}
	query.Set("plmn-id", c.Query("plmn-id"))
	query.Set("dnn", c.Query("dnn"))
	query.Set("single-nssai", c.Query("single-nssai"))
	query.Set("supported-features", c.Query("supported-features"))

	logger.SdmLog.Infof("Handle GetSmData")

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
