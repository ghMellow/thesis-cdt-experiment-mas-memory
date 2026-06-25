# Task 7 — AMF: Missing Default Case in Content-Type Switch (Silent Data Corruption)

**ID:** task7_vuln_amf  
**Tipo:** security_code_review  
**Difficoltà:** media  
**NF:** AMF (Access and Mobility Management Function)  
**CVE reference:** GHSA-r99v-75p9-xqm5

---

## Scenario

You are reviewing the AMF (Access and Mobility Management Function) SBI communication handler in a free5GC 5G core deployment. The AMF is responsible for UE registration, authentication, and mobility management — it is the first NF that UE signaling passes through.

Two handlers in `AMF/api_communication.go` process UE context operations using a `switch` statement on the `Content-Type` header. Compare them carefully.

---

## Code Snippet

```go
// File: AMF/api_communication.go

// Handler A — HTTPCreateUEContext
func (s *Server) HTTPCreateUEContext(c *gin.Context) {
    var createUeContextRequest models.CreateUeContextRequest
    createUeContextRequest.JsonData = new(models.UeContextCreateData)

    requestBody, err := c.GetRawData()
    if err != nil {
        logger.CommLog.Errorf("Get Request Body error: %+v", err)
        problemDetail := models.ProblemDetails{
            Title:  "System failure",
            Status: http.StatusInternalServerError,
            Detail: err.Error(),
            Cause:  "SYSTEM_FAILURE",
        }
        c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)
        c.JSON(http.StatusInternalServerError, problemDetail)
        return
    }

    contentType := c.GetHeader("Content-Type")
    str := strings.Split(contentType, ";")
    switch str[0] {
    case applicationjson:
        err = openapi.Deserialize(createUeContextRequest.JsonData, requestBody, contentType)
    case multipartrelate:
        err = openapi.Deserialize(&createUeContextRequest, requestBody, contentType)
    default:
        err = fmt.Errorf("wrong content type")
    }

    if err != nil {
        problemDetail := reqbody + err.Error()
        rsp := models.ProblemDetails{
            Title:  "Malformed request syntax",
            Status: http.StatusBadRequest,
            Detail: problemDetail,
        }
        logger.CommLog.Errorln(problemDetail)
        c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText((http.StatusBadRequest)))
        c.JSON(http.StatusBadRequest, rsp)
        return
    }
    s.Processor().HandleCreateUEContextRequest(c, createUeContextRequest)
}

// Handler B — HTTPUEContextTransfer
func (s *Server) HTTPUEContextTransfer(c *gin.Context) {
    var ueContextTransferRequest models.UeContextTransferRequest
    ueContextTransferRequest.JsonData = new(models.UeContextTransferReqData)

    requestBody, err := c.GetRawData()
    if err != nil {
        logger.CommLog.Errorf("Get Request Body error: %+v", err)
        problemDetail := models.ProblemDetails{
            Title:  "System failure",
            Status: http.StatusInternalServerError,
            Detail: err.Error(),
            Cause:  "SYSTEM_FAILURE",
        }
        c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)
        c.JSON(http.StatusInternalServerError, problemDetail)
        return
    }

    contentType := c.GetHeader("Content-Type")
    str := strings.Split(contentType, ";")
    switch str[0] {
    case applicationjson:
        err = openapi.Deserialize(ueContextTransferRequest.JsonData, requestBody, contentType)
    case multipartrelate:
        err = openapi.Deserialize(&ueContextTransferRequest, requestBody, contentType)
    }
    // ← no default case

    if err != nil {
        problemDetail := reqbody + err.Error()
        rsp := models.ProblemDetails{
            Title:  "Malformed request syntax",
            Status: http.StatusBadRequest,
            Detail: problemDetail,
        }
        logger.CommLog.Errorln(problemDetail)
        c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(http.StatusBadRequest))
        c.JSON(http.StatusBadRequest, rsp)
        return
    }
    s.Processor().HandleUEContextTransferRequest(c, ueContextTransferRequest)
}
```

The constants are defined as:
```go
const (
    applicationjson  = "application/json"
    multipartrelate  = "multipart/related"
    reqbody          = "[Request Body] "
)
```

---

## Question

You are a 5G core security analyst. Compare `HTTPCreateUEContext` (Handler A) and `HTTPUEContextTransfer` (Handler B) carefully, then answer:

1. **What is the structural difference** between the two `switch` statements?
2. **What security consequence** does this difference have in Handler B? Describe the concrete execution path when an attacker sends a request with an unexpected `Content-Type` (e.g., `text/xml` or an empty header).
3. **What is the impact** in the context of a 5G AMF? Consider that `HandleUEContextTransferRequest` processes the transfer of a UE context between AMFs during handover.
4. **Why is this also a problem** when `Content-Type` is simply missing or empty?
5. **Propose the minimal fix** for Handler B.

---

## Agent Instructions

Reply ONLY in JSON format:

```json
{
  "structural_difference": "description of what Handler A has that Handler B lacks",
  "attack_path": "step-by-step execution trace with unexpected Content-Type in Handler B",
  "impact_5g": "impact in AMF/5G handover context",
  "empty_content_type_issue": "explanation of the empty/missing Content-Type edge case",
  "fix": "corrected switch statement for Handler B",
  "reasoning": "analysis steps",
  "confidence": 0.0
}
```
