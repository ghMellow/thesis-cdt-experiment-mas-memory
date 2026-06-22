# Task 6 — 5G Code Vulnerability Detection (AMF)

**ID:** task6_vuln_amf  
**Tipo:** textual  
**Difficoltà:** media-alta

---

## Scenario

The following two handlers are taken from the **AMF** (Access and Mobility
Management Function) of free5gc, in the `Namf_Communication` SBI. Both parse a
request body whose format depends on the `Content-Type` header.

```go
func (s *Server) HTTPCreateUEContext(c *gin.Context) {
	var createUeContextRequest models.CreateUeContextRequest
	createUeContextRequest.JsonData = new(models.UeContextCreateData)

	requestBody, err := c.GetRawData()
	if err != nil {
		// ... return 500 ProblemDetails ...
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
		// ... return 400 Malformed request syntax ...
		return
	}
	s.Processor().HandleCreateUEContextRequest(c, createUeContextRequest)
}

func (s *Server) HTTPUEContextTransfer(c *gin.Context) {
	var ueContextTransferRequest models.UeContextTransferRequest
	ueContextTransferRequest.JsonData = new(models.UeContextTransferReqData)

	requestBody, err := c.GetRawData()
	if err != nil {
		// ... return 500 ProblemDetails ...
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

	if err != nil {
		// ... return 400 Malformed request syntax ...
		return
	}
	s.Processor().HandleUEContextTransferRequest(c, ueContextTransferRequest)
}
```

---

## Question

Analyze the code and identify the **security vulnerability** it contains.
Explain the mechanism that triggers it and its impact, and point to the
function and line(s) responsible.

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
