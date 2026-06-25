# Task 6 — 5G Security Code Review: AMF UEContextTransfer Missing Default Case

**ID:** task6_vuln_amf  
**Tipo:** security code review  
**Difficoltà:** media  
**NF:** AMF (Access and Mobility Management Function)

---

## Scenario

You are reviewing two HTTP handlers in the AMF SBI layer of a free5GC implementation. Both handle requests whose body may arrive as either `application/json` or `multipart/related`, and both share the same content-type dispatch pattern. Read them carefully:

**Handler A — HTTPCreateUEContext:**

```go
func (s *Server) HTTPCreateUEContext(c *gin.Context) {
    var createUeContextRequest models.CreateUeContextRequest
    createUeContextRequest.JsonData = new(models.UeContextCreateData)

    requestBody, err := c.GetRawData()
    if err != nil { /* ... 500 error and return ... */ }

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

    if err != nil { /* ... 400 error and return ... */ }
    s.Processor().HandleCreateUEContextRequest(c, createUeContextRequest)
}
```

**Handler B — HTTPUEContextTransfer:**

```go
func (s *Server) HTTPUEContextTransfer(c *gin.Context) {
    var ueContextTransferRequest models.UeContextTransferRequest
    ueContextTransferRequest.JsonData = new(models.UeContextTransferReqData)

    requestBody, err := c.GetRawData()
    if err != nil { /* ... 500 error and return ... */ }

    contentType := c.GetHeader("Content-Type")
    str := strings.Split(contentType, ";")
    switch str[0] {
    case applicationjson:
        err = openapi.Deserialize(ueContextTransferRequest.JsonData, requestBody, contentType)
    case multipartrelate:
        err = openapi.Deserialize(&ueContextTransferRequest, requestBody, contentType)
    }

    if err != nil { /* ... 400 error and return ... */ }
    s.Processor().HandleUEContextTransferRequest(c, ueContextTransferRequest)
}
```

---

## Question

Compare Handler A and Handler B carefully.

1. Identify any security-relevant difference between the two handlers.
2. What happens in Handler B if a caller sends a request with an unexpected or malformed `Content-Type` (e.g., `text/plain`, `application/xml`, or an empty string)?
3. What is the impact of this difference, and what is the correct fix?

---

## Agent Instructions

Reply ONLY in JSON format:

```json
{
  "vulnerability_found": true | false,
  "vulnerability_description": "...",
  "affected_handler": "...",
  "affected_line_or_pattern": "...",
  "impact": "...",
  "fix": "...",
  "confidence": 0.0
}
```
