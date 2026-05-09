# Solution — Task 7 (Security Review: AMF Communication Handler)

**ID:** task7_vuln_amf_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent  
**CVE references:** GHSA-r99v-75p9-xqm5 (AMF missing default case)

---

## Ground Truth

```json
{
  "answer": "HTTPUEContextTransfer is missing a default case in the Content-Type switch, so an arbitrary Content-Type bypasses deserialization and calls the processor with uninitialized data. Additionally, five handlers (HTTPCreateUEContext, HTTPEBIAssignment, HTTPRegistrationStatusUpdate, HTTPReleaseUEContext, HTTPN1N2MessageTransfer) pass the full ProblemDetails struct to c.Set instead of the string Cause field.",
  "type": "textual_security_review"
}
```

## GT Rationale

### Primary finding — Missing `default` case in Content-Type switch (`HTTPUEContextTransfer`)

`HTTPUEContextTransfer` has a switch on `str[0]` (Content-Type) with only two cases and **no `default`**:

```go
switch str[0] {
case applicationjson:
    err = openapi.Deserialize(ueContextTransferRequest.JsonData, requestBody, contentType)
case multipartrelate:
    err = openapi.Deserialize(&ueContextTransferRequest, requestBody, contentType)
// no default
}
```

With any other Content-Type (e.g., `text/plain`, `application/xml`, or a crafted value), `err` remains `nil` and the `if err != nil` block is skipped. The processor receives a `ueContextTransferRequest` where `JsonData` is an empty allocated struct (`new(models.UeContextTransferReqData)`) but has never been populated from the request body. This can cause:
- Panic or nil-dereference in the processor
- Processing of an empty/default UE context transfer (invalid operation on AMF state)
- Potential DoS if repeated

Compare with `HTTPCreateUEContext` (same file) which has `default: err = fmt.Errorf("wrong content type")` — the correct pattern.

**Fix**: add `default: err = fmt.Errorf("wrong content type")` to `HTTPUEContextTransfer`'s switch.

### Secondary finding — Wrong type passed to `c.Set` (5 handlers, information exposure)

Five handlers pass the entire `models.ProblemDetails` struct to `c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)` instead of the string value:

```go
// Wrong (5 handlers):
c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)      // struct

// Correct (HTTPAMFStatusChangeSubscribeModify and others):
c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause) // string
```

`IN_PB_DETAILS_CTX_STR` is consumed by the SBI metrics middleware which expects a string. Passing the struct:
- May cause runtime type-assertion panics in the middleware
- Exposes `err.Error()` (the raw Go error message, potentially containing internal paths, stack info, or configuration details) to the metrics/logging layer beyond its intended scope

**Fix**: replace `c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)` with `c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)` in all five affected handlers.

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "missing_default_score": {
      "max": 4,
      "criteri": {
        "4": "Identifies that HTTPUEContextTransfer is missing a default case in the Content-Type switch, explains that err remains nil for unknown Content-Types, and describes the consequence (processor called with uninitialized request data). Optionally notes the contrast with HTTPCreateUEContext which has the correct default.",
        "3": "Identifies the missing default case and that arbitrary Content-Types bypass deserialization, but does not fully explain the impact",
        "2": "Notes that the switch lacks a default or that error handling is incomplete in HTTPUEContextTransfer",
        "1": "Mentions Content-Type handling as a concern without identifying the missing default specifically",
        "0": "Does not identify the missing default issue"
      }
    },
    "inconsistent_context_set_score": {
      "max": 3,
      "criteri": {
        "3": "Identifies that multiple handlers pass the full ProblemDetails struct to c.Set instead of a string, explains the inconsistency with handlers that pass .Cause, and notes the risk of type mismatch in the metrics middleware",
        "2": "Notes that c.Set is used inconsistently or incorrectly in some handlers without fully explaining the impact",
        "1": "Mentions error handling inconsistency in a generic way",
        "0": "Does not identify the c.Set inconsistency"
      }
    },
    "impact_assessment_score": {
      "max": 2,
      "criteri": {
        "2": "Correctly explains impact in AMF context: potential DoS via uninitialized UE context transfer, panic in processor, or internal error info reaching the metrics layer",
        "1": "Generic impact description (undefined behavior, information exposure) without AMF-specific context",
        "0": "No impact assessment"
      }
    }
  },
  "total_max": 9
}
```
