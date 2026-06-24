# Task 7a — 5G Core Security Review: UDM Subscriber Data Handler (Short)

**ID:** task7_vuln_udm_short  
**Tipo:** textual  
**Difficoltà:** media

---

## Scenario

You are reviewing two handler functions from the **UDM (Unified Data Management)** SBI layer of a 5G core network. Both handlers retrieve subscription data for a specific UE identified by a SUPI (Subscription Permanent Identifier) extracted from the HTTP path.

```go
// HandleGetAmData - retrieve a UE's Access and Mobility Subscription Data
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

// HandleGetSmfSelectData - retrieve a UE's SMF Selection Subscription Data
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
```

---

## Question

Compare the two handler functions. Identify the security vulnerability present in the second handler (`HandleGetSmfSelectData`) that is absent in the first, and explain the potential impact.

---

## Agent Instructions

Reply ONLY in JSON format:

```json
{
  "answer": {
    "vulnerability_type": "...",
    "location": "...",
    "impact": "..."
  },
  "reasoning": "...",
  "confidence": 0.0
}
```
