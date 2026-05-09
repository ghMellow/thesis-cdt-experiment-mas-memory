# Task 9 — Security Code Review: Cross-NF Analysis (PCF / AMF / UDM / UDR)

**ID:** task9_vuln_cross  
**Tipo:** textual  
**Difficoltà:** alta

---

## Scenario

The following excerpts come from **four different Go source files**, each belonging to a different 5G core Network Function (NF) in a free5GC implementation. All files are SBI (Service-Based Interface) HTTP handlers using the Gin framework, communicating over the 5G Service-Based Architecture.

Perform a **security code review across all four files simultaneously**. In addition to per-file vulnerabilities, look for **cross-file inconsistencies**: cases where one NF applies a security control correctly while another NF handling the same data type omits it.

---

### File 1 — PCF: `api_oam.go`

```go
func (s *Server) setCorsHeader(c *gin.Context) {
    s.router.Use(cors.New(cors.Config{
        AllowMethods:     []string{"GET", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"},
        AllowHeaders:     []string{"Origin", "Content-Length", "Content-Type", "User-Agent",
                                   "Referrer", "Host", "Token", "X-Requested-With"},
        ExposeHeaders:    []string{"Content-Length"},
        AllowCredentials: true,
        AllowAllOrigins:  true,
        MaxAge:           86400,
    }))
    c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
    c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
    c.Writer.Header().Set("Access-Control-Allow-Headers",
        "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, "+
        "accept, origin, Cache-Control, X-Requested-With")
    c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT, PATCH, DELETE")
}

func (s *Server) HTTPOAMGetAmPolicy(c *gin.Context) {
    s.setCorsHeader(c)
    supi := c.Params.ByName("supi")
    if supi == "" {
        problemDetails := &models.ProblemDetails{
            Title:  util.ERROR_INITIAL_PARAMETERS,
            Status: http.StatusBadRequest,
        }
        c.JSON(int(problemDetails.Status), problemDetails)
        return
    }
    s.Processor().HandleOAMGetAmPolicyRequest(c, supi)
}
```

---

### File 2 — AMF: `api_communication.go` (selected handlers)

```go
// HTTPCreateUEContext — has default case in switch
func (s *Server) HTTPCreateUEContext(c *gin.Context) {
    var createUeContextRequest models.CreateUeContextRequest
    createUeContextRequest.JsonData = new(models.UeContextCreateData)
    requestBody, err := c.GetRawData()
    if err != nil {
        problemDetail := models.ProblemDetails{Title: "System failure",
            Status: http.StatusInternalServerError, Detail: err.Error(), Cause: "SYSTEM_FAILURE"}
        c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)   // note: struct, not string
        c.JSON(http.StatusInternalServerError, problemDetail)
        return
    }
    switch strings.Split(c.GetHeader("Content-Type"), ";")[0] {
    case applicationjson:
        err = openapi.Deserialize(createUeContextRequest.JsonData, requestBody, c.GetHeader("Content-Type"))
    case multipartrelate:
        err = openapi.Deserialize(&createUeContextRequest, requestBody, c.GetHeader("Content-Type"))
    default:
        err = fmt.Errorf("wrong content type")
    }
    if err != nil { /* ... return 400 ... */ }
    s.Processor().HandleCreateUEContextRequest(c, createUeContextRequest)
}

// HTTPUEContextTransfer — missing default case
func (s *Server) HTTPUEContextTransfer(c *gin.Context) {
    var ueContextTransferRequest models.UeContextTransferRequest
    ueContextTransferRequest.JsonData = new(models.UeContextTransferReqData)
    requestBody, err := c.GetRawData()
    if err != nil {
        problemDetail := models.ProblemDetails{Title: "System failure",
            Status: http.StatusInternalServerError, Detail: err.Error(), Cause: "SYSTEM_FAILURE"}
        c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)   // note: struct, not string
        c.JSON(http.StatusInternalServerError, problemDetail)
        return
    }
    switch strings.Split(c.GetHeader("Content-Type"), ";")[0] {
    case applicationjson:
        err = openapi.Deserialize(ueContextTransferRequest.JsonData, requestBody, c.GetHeader("Content-Type"))
    case multipartrelate:
        err = openapi.Deserialize(&ueContextTransferRequest, requestBody, c.GetHeader("Content-Type"))
    // no default
    }
    if err != nil { /* ... return 400 ... */ }
    s.Processor().HandleUEContextTransferRequest(c, ueContextTransferRequest)
}

// HTTPAMFStatusChangeSubscribeModify — correct c.Set usage
func (s *Server) HTTPAMFStatusChangeSubscribeModify(c *gin.Context) {
    requestBody, err := c.GetRawData()
    if err != nil {
        problemDetail := models.ProblemDetails{Title: "System failure",
            Status: http.StatusInternalServerError, Detail: err.Error(), Cause: "SYSTEM_FAILURE"}
        c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)  // correct: string
        c.JSON(http.StatusInternalServerError, problemDetail)
        return
    }
    // ...
}
```

---

### File 3 — UDM: `api_subscriberdatamanagement.go` (selected handlers)

```go
// HandleGetAmData — validates SUPI format
func (s *Server) HandleGetAmData(c *gin.Context) {
    supi := c.Params.ByName("supi")
    if !validator.IsValidSupi(supi) {
        problemDetail := models.ProblemDetails{Title: "Malformed request syntax",
            Status: http.StatusBadRequest, Detail: "Supi is invalid", Cause: "MANDATORY_IE_INCORRECT"}
        c.JSON(int(problemDetail.Status), problemDetail)
        return
    }
    // ... calls GetAmDataProcedure
}

// HandleUnsubscribe — validates UE ID format
func (s *Server) HandleUnsubscribe(c *gin.Context) {
    ueId := c.Params.ByName("ueId")
    valid := validator.IsValidGpsi(ueId) || validator.IsValidSupi(ueId)
    if !valid {
        problemDetail := models.ProblemDetails{Title: "Malformed request syntax",
            Status: http.StatusBadRequest, Detail: "UE ID is invalid", Cause: "MANDATORY_IE_INCORRECT"}
        c.JSON(int(problemDetail.Status), problemDetail)
        return
    }
    s.Processor().UnsubscribeProcedure(c, ueId, c.Params.ByName("subscriptionId"))
}

// HandleGetSmfSelectData — no SUPI validation
func (s *Server) HandleGetSmfSelectData(c *gin.Context) {
    supi := c.Params.ByName("supi")
    // no validator.IsValidSupi() call
    plmnIDStruct, problemDetails := s.getPlmnIDStruct(c.Request.URL.Query())
    if problemDetails != nil { /* ... */ return }
    s.Processor().GetSmfSelectDataProcedure(c, supi, plmnIDStruct.Mcc+plmnIDStruct.Mnc, "")
}

// HandleGetNssai, HandleGetSmData, HandleGetTraceData, HandleGetUeContextInSmfData,
// HandleGetSupi — all follow the same pattern as HandleGetSmfSelectData (no SUPI validation)
```

---

### File 4 — UDR: `api_datarepository.go` (selected handlers)

```go
// HandleQueryAmfContext3gpp — only empty check, no format validation
func (s *Server) HandleQueryAmfContext3gpp(c *gin.Context) {
    ueId := c.Params.ByName("ueId")
    if ueId == "" {
        util.EmptyUeIdProblemJson(c)
        return
    }
    // ueId passed directly to processor and MongoDB filter
    s.Processor().QueryAmfContext3gppProcedure(c, "subscriptionData.contextData.amf3gppAccess", ueId)
}

// HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete — missing return after 404
func (s *Server) HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete(c *gin.Context) {
    influenceId := c.Param("influenceId")
    if influenceId != "subs-to-notify" {
        c.String(http.StatusNotFound, "404 page not found")
        // missing return — execution continues
    }
    subscriptionId := c.Params.ByName("subscriptionId")
    s.Processor().ApplicationDataInfluenceDataSubsToNotifySubscriptionIdDeleteProcedure(c, subscriptionId)
}

// HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet — same pattern
func (s *Server) HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet(c *gin.Context) {
    influenceId := c.Param("influenceId")
    if influenceId != "subs-to-notify" {
        c.String(http.StatusNotFound, "404 page not found")
        // missing return
    }
    subscriptionId := c.Params.ByName("subscriptionId")
    s.Processor().ApplicationDataInfluenceDataSubsToNotifySubscriptionIdGetProcedure(c, subscriptionId)
}

// HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut — same pattern
func (s *Server) HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut(c *gin.Context) {
    influenceId := c.Param("influenceId")
    if influenceId != "subs-to-notify" {
        c.String(http.StatusNotFound, "404 page not found")
        // missing return
    }
    // ... (reads body, calls processor)
}

// HandleCreateEeSubscriptions — regex validation with trivial bypass
func (s *Server) HandleCreateEeSubscriptions(c *gin.Context) {
    ueId := c.Params.ByName("ueId")
    if ueId == "" { util.EmptyUeIdProblemJson(c); return }
    match, err := regexp.MatchString(
        "^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$", ueId)
    if !match { /* return 400 */ return }
    if err != nil { logger.DataRepoLog.Errorf("Invalid regular expression: %s", err) }
    s.Processor().CreateEeSubscriptionsProcedure(c, ueId, eeSubscription)
}
```

---

## Question

Analyze all four files together and identify:

1. **Per-file vulnerabilities**: security issues within each individual NF handler
2. **Cross-file inconsistencies**: cases where one NF applies a security control correctly while another NF omits it for the same type of data or operation
3. For each finding: name the vulnerability class, identify the affected function(s) and NF, explain the security impact in the 5G core context, propose a fix

Pay special attention to how the four NFs handle **UE identifier validation** (SUPI, ueId, supi path parameters) — this is the most informative cross-file comparison.

---

## Agent Instructions

Reply ONLY in JSON format:

```json
{
  "answer": "Summary of findings: list the main vulnerability classes found and note whether any cross-file inconsistencies were identified (1-3 sentences)",
  "reasoning": "Full analysis organized by finding type. For cross-file issues: explicitly name both the NF that applies the control correctly and the NF that omits it. For per-file issues: specify NF, function, impact, fix.",
  "confidence": 0.0
}
```
