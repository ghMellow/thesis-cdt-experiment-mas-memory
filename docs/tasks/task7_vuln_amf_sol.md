# Solution — Task 7 (Security Review: AMF Communication Handler)

**ID:** task7_vuln_amf_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent  
**CVE references:** V6 (CWE-209, information exposure via c.Set struct); V7 (CWE-392, missing default in HTTPUEContextTransfer); GHSA-r99v-75p9-xqm5 (N1N2MessageTransfer logic error)

---

## Ground Truth

```json
{
  "answer": "Three distinct issues: (1) five handlers pass the full ProblemDetails struct to c.Set(IN_PB_DETAILS_CTX_STR) instead of the expected string field (information exposure / type inconsistency); (2) HTTPUEContextTransfer has no default case in its Content-Type switch, causing the processor to be called with an undeserialized struct when Content-Type is unrecognized; (3) HTTPN1N2MessageTransfer unconditionally sets an error when Content-Type is application/json, making it impossible to call that endpoint with JSON",
  "type": "textual_security_review"
}
```

## GT Rationale

### Finding 1 — c.Set with full struct instead of string (CWE-209)

Five handlers (`HTTPCreateUEContext`, `HTTPEBIAssignment`, `HTTPRegistrationStatusUpdate`, `HTTPReleaseUEContext`, `HTTPN1N2MessageTransfer`) call:

```go
c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)  // struct
```

The correct pattern (used in `HTTPAMFStatusChangeSubscribeModify` and others) is:

```go
c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)  // string
```

`IN_PB_DETAILS_CTX_STR` is read by the SBI metrics middleware, which expects a string. Passing the full struct:
1. Breaks the type contract expected by the middleware (runtime type assertion will fail silently or panic depending on implementation)
2. The struct contains `Detail: err.Error()`, which may include internal system errors, file paths, or stack details — exposing this to the metrics/logging pipeline violates CWE-209 (generation of error messages containing sensitive information)

**Fix:** Replace `c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail)` with `c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetail.Cause)` in all five handlers.

### Finding 2 — Missing default case in HTTPUEContextTransfer (CWE-392)

```go
switch str[0] {
case applicationjson:
    err = openapi.Deserialize(...)
case multipartrelate:
    err = openapi.Deserialize(...)
// no default: err remains nil for any other Content-Type
}

if err != nil { ... return }
s.Processor().HandleUEContextTransferRequest(c, ueContextTransferRequest)
```

If `Content-Type` is anything other than the two known values (e.g., `text/plain`, an attacker-controlled value), `err` remains `nil`, no deserialization occurs, and the processor is called with a partially-initialized `ueContextTransferRequest` (only `JsonData` is non-nil, pointing to an empty `UeContextTransferReqData`). This can cause undefined behavior, nil pointer dereferences, or silent data corruption in the UE context transfer procedure.

Compare with `HTTPCreateUEContext` in the same file: identical structure but has `default:` (empty but present, and the comment-absent default means err stays nil there too — both are problematic, but `HTTPUEContextTransfer` is worse for lacking the case entirely).

**Fix:** Add `default: err = fmt.Errorf("wrong content type")` to the switch in `HTTPUEContextTransfer`, mirroring `HTTPN1N2MessageTransfer`.

### Finding 3 — N1N2MessageTransfer rejects application/json (logic error)

```go
switch str[0] {
case applicationjson:
    err = fmt.Errorf("N1 and N2 datas are both Empty in N1N2MessgeTransfer")
// ...
```

The `applicationjson` case unconditionally sets an error. This means any N1N2 message transfer request with Content-Type `application/json` is always rejected with status 400, regardless of the body content. The N1/N2 transfer endpoint only works with multipart/related. While this may reflect an intentional restriction (N1N2 messages require binary N2 data that cannot be conveyed as plain JSON), the error message is misleading and this case should either be documented as intentionally unsupported or handled gracefully by returning a 415 Unsupported Media Type rather than a 400 Malformed Request Syntax.

**Fix:** Replace the `applicationjson` case with `return c.JSON(http.StatusUnsupportedMediaType, ...)` with a clear message, or remove the case and let the `default` handle unsupported types.

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "struct_set_issue_score": {
      "max": 3,
      "criteri": {
        "3": "Identifies that c.Set(IN_PB_DETAILS_CTX_STR, problemDetail) passes a struct where a string is expected, names at least 3 of the 5 affected handlers, and explains the information exposure or type mismatch consequence",
        "2": "Identifies the struct vs string inconsistency and at least one affected handler, with some explanation of impact",
        "1": "Mentions inconsistency in error handling across handlers without identifying the specific c.Set type issue",
        "0": "Does not identify this issue"
      }
    },
    "missing_default_score": {
      "max": 3,
      "criteri": {
        "3": "Identifies that HTTPUEContextTransfer has no default case in its switch, explains that unknown Content-Type causes processor to be called with undeserialized struct, and contrasts with HTTPCreateUEContext or HTTPN1N2MessageTransfer",
        "2": "Identifies the missing default case in HTTPUEContextTransfer and explains the behavioral consequence",
        "1": "Mentions the switch issue without explaining what happens with unrecognized Content-Type",
        "0": "Does not identify this issue"
      }
    },
    "n1n2_logic_score": {
      "max": 2,
      "criteri": {
        "2": "Identifies that the applicationjson case unconditionally produces an error, making JSON-type N1N2 requests always fail, and notes this is a logic error (not a security hardening measure)",
        "1": "Notices the applicationjson case behavior without fully explaining the semantic impact",
        "0": "Does not identify this issue or marks it as correct behavior without qualification"
      }
    },
    "fix_quality_score": {
      "max": 2,
      "criteri": {
        "2": "Proposes correct fixes for at least two of the three issues: string vs struct in c.Set; add default case; fix N1N2 applicationjson handling",
        "1": "Proposes a fix direction for one issue",
        "0": "No fix proposed or all fixes are incorrect"
      }
    }
  },
  "total_max": 10
}
```
