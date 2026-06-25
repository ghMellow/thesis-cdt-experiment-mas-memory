# Task 8 — UDM: Missing SUPI Validation in SDM Handlers (Input Validation Bypass)

**ID:** task8_vuln_udm  
**Tipo:** security_code_review  
**Difficoltà:** alta  
**NF:** UDM (Unified Data Management)  
**CVE reference:** GHSA-585v-hcgf-jhfr

---

## Scenario

You are auditing the UDM (Unified Data Management) subscriber data management (SDM) SBI handler in a free5GC 5G core deployment. The UDM stores and serves subscriber credentials, NSSAI (network slice configuration), SM (session management) subscription data, and trace configuration.

The file `UDM/api_subscriberdatamanagement.go` contains multiple GET handlers that take a SUPI (Subscription Permanent Identifier, format `imsi-<15 digits>`) as a path parameter. The 3GPP specification TS 29.503 §6.1.3.5.2 requires servers to validate the SUPI format before processing the request.

Study the following handlers and identify which ones comply with the specification requirement and which do not.

---

## Code Snippet

```go
// File: UDM/api_subscriberdatamanagement.go

// HANDLER A — GetAmData (compliant)
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

// HANDLER B — GetSmfSelectData
func (s *Server) HandleGetSmfSelectData(c *gin.Context) {
    query := url.Values{}
    query.Set("plmn-id", c.Query("plmn-id"))
    query.Set("supported-features", c.Query("supported-features"))

    logger.SdmLog.Infof("Handle GetSmfSelectData")

    supi := c.Params.ByName("supi")
    // ← no SUPI validation
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

// HANDLER C — GetSupi (retrieve multiple data sets)
func (s *Server) HandleGetSupi(c *gin.Context) {
    query := url.Values{}
    query.Set("plmn-id", c.Query("plmn-id"))
    query.Set("dataset-names", c.Query("dataset-names"))
    query.Set("supported-features", c.Query("supported-features"))

    logger.SdmLog.Infof("Handle GetSupiRequest")

    supi := c.Params.ByName("supi")
    // ← no SUPI validation
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

// HANDLER D — GetNssai (retrieve subscribed NSSAI)
func (s *Server) HandleGetNssai(c *gin.Context) {
    query := url.Values{}
    query.Set("plmn-id", c.Query("plmn-id"))
    query.Set("supported-features", c.Query("supported-features"))

    logger.SdmLog.Infof("Handle GetNssai")

    supi := c.Params.ByName("supi")
    // ← no SUPI validation
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

// HANDLER E — GetTraceData
func (s *Server) HandleGetTraceData(c *gin.Context) {
    logger.SdmLog.Infof("Handle GetTraceData")

    supi := c.Params.ByName("supi")
    // ← no SUPI validation
    plmnID := c.Query("plmn-id")
    s.Processor().GetTraceDataProcedure(c, supi, plmnID)
}
```

Additionally, the `validator` package provides:

```go
// validator package (for reference — not part of the vulnerable file)
func IsValidSupi(supi string) bool {
    // Accepts: "imsi-<15 digits>" or "nai-<...>"
    // Rejects: empty strings, SQL/NoSQL injection patterns, arbitrary strings
}
```

---

## Question

You are a 5G core security analyst. Analyze the five handlers above and answer:

1. **Which handlers are non-compliant** with TS 29.503 §6.1.3.5.2? List them by name.
2. **What is the security risk** of accepting an unvalidated SUPI? Consider that the SUPI is used as a query key into the UDM's subscriber database (MongoDB in free5GC). Describe at least two distinct attack vectors.
3. **Handler A validates SUPI but Handler B does not**, yet they serve related data (AM data vs SMF selection data). What does this inconsistency suggest about how the fix was applied — and what is the risk of such inconsistent patching?
4. **Propose the minimal fix** for Handler B (HandleGetSmfSelectData) that brings it into compliance, matching the pattern established by Handler A.

---

## Agent Instructions

Reply ONLY in JSON format:

```json
{
  "non_compliant_handlers": ["list of handler names"],
  "attack_vectors": [
    {
      "name": "attack vector name",
      "description": "technical explanation"
    }
  ],
  "inconsistency_analysis": "explanation of partial fix risk and what it implies about the patch process",
  "fix": "corrected HandleGetSmfSelectData code snippet",
  "reasoning": "step-by-step analysis",
  "confidence": 0.0
}
```
