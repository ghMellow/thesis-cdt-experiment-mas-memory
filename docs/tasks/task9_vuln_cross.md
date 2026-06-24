# Task 9 — 5G Core Security Review: Cross-NF Vulnerability Identification

**ID:** task9_vuln_cross  
**Tipo:** textual  
**Difficoltà:** alta

---

## Scenario

You are performing a security audit across multiple network functions of a 5G core implementation. Three code snippets are provided below, each from a different NF (Network Function) in the SBI (Service Based Interface) layer. Each snippet contains a distinct security vulnerability.

---

### Snippet 1 — AMF (Access and Mobility Management Function)

`api_communication.go` — UE context transfer handler

```go
func (s *Server) HTTPUEContextTransfer(c *gin.Context) {
    // request body reading omitted for brevity

    contentType := c.GetHeader("Content-Type")
    str := strings.Split(contentType, ";")
    switch str[0] {
    case applicationjson:
        err = openapi.Deserialize(ueContextTransferRequest.JsonData, requestBody, contentType)
    case multipartrelate:
        err = openapi.Deserialize(&ueContextTransferRequest, requestBody, contentType)
    }

    if err != nil {
        rsp := models.ProblemDetails{Status: http.StatusBadRequest}
        c.JSON(http.StatusBadRequest, rsp)
        return
    }
    s.Processor().HandleUEContextTransferRequest(c, ueContextTransferRequest)
}
```

---

### Snippet 2 — UDM (Unified Data Management)

`api_subscriberdatamanagement.go` — SMF selection data handler

```go
func (s *Server) HandleGetSmfSelectData(c *gin.Context) {
    supi := c.Params.ByName("supi")

    plmnIDStruct, problemDetails := s.getPlmnIDStruct(c.Request.URL.Query())
    if problemDetails != nil {
        c.JSON(int(problemDetails.Status), problemDetails)
        return
    }
    var plmnID string
    if plmnIDStruct != nil {
        plmnID = plmnIDStruct.Mcc + plmnIDStruct.Mnc
    }
    supportedFeatures := c.Query("supported-features")
    s.Processor().GetSmfSelectDataProcedure(c, supi, plmnID, supportedFeatures)
}
```

---

### Snippet 3 — UDR (Unified Data Repository)

`api_datarepository.go` — policy data subscription handler

```go
func (s *Server) HandlePolicyDataSubsToNotifyPost(c *gin.Context) {
    var policyDataSubscription models.PolicyDataSubscription

    reqBody, err := c.GetRawData()
    if err != nil {
        pd := openapi.ProblemDetailsSystemFailure(err.Error())
        c.JSON(http.StatusInternalServerError, pd)
    }

    err = openapi.Deserialize(policyDataSubscription, reqBody, "application/json")
    if err != nil {
        pd := util.ProblemDetailsMalformedReqSyntax(err.Error())
        c.JSON(http.StatusBadRequest, pd)
    }

    s.Processor().PolicyDataSubsToNotifyPostProcedure(c, policyDataSubscription)
}
```

---

## Question

For each of the three snippets, identify the security vulnerability present. Specify the NF, the vulnerability type, the exact location in the code, and the potential impact.

---

## Agent Instructions

Reply ONLY in JSON format. The `answer` field must contain exactly one entry per snippet:

```json
{
  "answer": [
    {
      "nf": "AMF",
      "vulnerability_type": "...",
      "location": "...",
      "impact": "..."
    },
    {
      "nf": "UDM",
      "vulnerability_type": "...",
      "location": "...",
      "impact": "..."
    },
    {
      "nf": "UDR",
      "vulnerability_type": "...",
      "location": "...",
      "impact": "..."
    }
  ],
  "reasoning": "...",
  "confidence": 0.0
}
```
