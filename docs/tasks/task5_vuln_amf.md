# Task 5 — 5G Security Code Review: AMF N1N2MessageTransfer Handler

**ID:** task5_vuln_amf  
**Tipo:** security code review  
**Difficoltà:** media  
**NF:** AMF (Access and Mobility Management Function)

---

## Scenario

You are performing a security and correctness review of the AMF SBI (Service-Based Interface) layer in a free5GC implementation. The following Go code is the HTTP handler for the N1N2MessageTransfer operation, which transfers NAS (N1) and/or N2 messages between AMF and external NFs such as SMF or NEF.

```go
func (s *Server) HTTPN1N2MessageTransfer(c *gin.Context) {
    var n1n2MessageTransferRequest models.N1N2MessageTransferRequest
    n1n2MessageTransferRequest.JsonData = new(models.N1N2MessageTransferReqData)

    requestBody, err := c.GetRawData()
    if err != nil {
        problemDetail := models.ProblemDetails{
            Title:  "System failure",
            Status: http.StatusInternalServerError,
            Detail: err.Error(),
            Cause:  "SYSTEM_FAILURE",
        }
        logger.CommLog.Errorf("Get Request Body error: %+v", err)
        c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)
        c.JSON(http.StatusInternalServerError, problemDetail)
        return
    }

    contentType := c.GetHeader("Content-Type")
    str := strings.Split(contentType, ";")
    switch str[0] {
    case applicationjson:
        err = fmt.Errorf("N1 and N2 datas are both Empty in N1N2MessgeTransfer")
    case multipartrelate:
        err = openapi.Deserialize(&n1n2MessageTransferRequest, requestBody, contentType)
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
        c.Set(sbi.IN_PB_DETAILS_CTX_STR, http.StatusText(http.StatusBadRequest))
        c.JSON(http.StatusBadRequest, rsp)
        return
    }
    s.Processor().HandleN1N2MessageTransferRequest(c, n1n2MessageTransferRequest)
}
```

**Context:** In 3GPP TS 29.518, the N1N2MessageTransfer operation may carry:
- Multipart (`multipart/related`): both N1 (NAS) and N2 (NGAP) message parts
- JSON only (`application/json`): only N2 data (e.g., paging, handover command) without an N1 NAS payload

---

## Question

Review the handler above. Identify any logic error or security issue in how it handles different `Content-Type` values. Specifically:

1. What happens when a caller sends a valid `application/json` request with only N2 data (a legitimate use case per 3GPP spec)?
2. Is the behavior correct? If not, describe the impact.
3. What is the correct fix?

---

## Agent Instructions

Reply ONLY in JSON format:

```json
{
  "vulnerability_found": true | false,
  "vulnerability_description": "...",
  "affected_line_or_pattern": "...",
  "impact": "...",
  "fix": "...",
  "confidence": 0.0
}
```
