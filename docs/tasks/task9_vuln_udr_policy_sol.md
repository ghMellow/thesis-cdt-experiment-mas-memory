# Solution — Task 9 (Security Review: UDR Policy Data Subscription Handlers)

**ID:** task9_vuln_udr_policy_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent  
**CVE reference:** CWE-670 (Always-Incorrect Control Flow Implementation) — same class as GHSA missing-return family in UDR

---

## Ground Truth

```json
{
  "answer": "Both handlers are missing `return` statements after each `c.JSON(...)` error response. In Go/Gin, c.JSON() writes the HTTP response but does not stop execution. When GetRawData() fails, the handler continues to call openapi.Deserialize with a nil/empty body, and then calls the Processor regardless. When Deserialize fails, the handler calls the Processor with a zero-value struct. In both cases the error response and a processor invocation are both sent for the same request.",
  "type": "textual_security_review"
}
```

## GT Rationale

### Finding — Missing `return` after every `c.JSON()` error call (CWE-670)

Both `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut` share the same defective pattern. Neither error-handling block ends with `return`:

```go
if err != nil {
    ...
    c.JSON(http.StatusInternalServerError, pd)
    // ← no return
}
// execution continues here
```

**Consequence chain in `HandlePolicyDataSubsToNotifyPost`:**

1. If `c.GetRawData()` fails:
   - A 500 response is written to the client
   - `reqBody` is nil/empty
   - `openapi.Deserialize(policyDataSubscription, nil, ...)` is called — likely returns an error or populates a zero-value struct
   - The second `if err != nil` block fires, writing a **400 response** — the client now receives two HTTP responses on the same connection
   - `s.Processor().PolicyDataSubsToNotifyPostProcedure(c, policyDataSubscription)` is called with a zero-value subscription — may create an empty/invalid subscription record in the policy data store

2. If `openapi.Deserialize()` fails (body read succeeded but JSON is malformed):
   - A 400 response is written
   - `s.Processor().PolicyDataSubsToNotifyPostProcedure(c, policyDataSubscription)` is called with the zero-value `policyDataSubscription` — creates a bogus subscription
   - The processor call may also write another response, causing double-write

**Impact in 5G context:**
- Policy data subscriptions are used by the PCF to receive change notifications for UE policies. Creating bogus zero-value subscriptions could flood the notification system with empty subscribers, consuming UDR storage and triggering spurious notifications.
- Double HTTP writes cause connection-level issues that are hard to diagnose and may indicate to callers that the operation succeeded even when it failed.
- The reference implementation (`HandlePolicyDataBdtDataBdtReferenceIdPut`) uses the `getDataFromRequestBody` helper which correctly returns early on error — the two vulnerable handlers bypass this helper and replicate its logic incorrectly.

**Fix:**
```go
if err != nil {
    ...
    c.JSON(http.StatusInternalServerError, pd)
    return  // ← add this
}
// ...
if err != nil {
    ...
    c.JSON(http.StatusBadRequest, pd)
    return  // ← add this
}
```

Or, better: refactor to use `getDataFromRequestBody(c, &policyDataSubscription)` as shown in the reference handler, which handles both error cases and the `return` internally.

### Secondary finding — Pass by value instead of pointer in Deserialize

```go
err = openapi.Deserialize(policyDataSubscription, reqBody, "application/json")
```

`policyDataSubscription` is passed by value, not by pointer. `openapi.Deserialize` likely expects a pointer to populate the struct. This means deserialization either fails or writes to a copy that is immediately discarded. The processor then always receives a zero-value `policyDataSubscription` even when the body is valid. The correct call is:

```go
err = openapi.Deserialize(&policyDataSubscription, reqBody, "application/json")
```

This is not a security vulnerability per se but a correctness bug that means the subscription POST/PUT never persists the actual subscriber data.

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "missing_return_identified_score": {
      "max": 3,
      "criteri": {
        "3": "Correctly identifies that c.JSON() does not stop execution in Go, that both handlers are missing return after each error block, and explains that the processor is called despite errors — covers both handlers and both error sites",
        "2": "Identifies the missing return issue in at least one handler and one error site, explains the fall-through to processor",
        "1": "Mentions that returns are missing without explaining the Go/Gin control flow consequence",
        "0": "Does not identify the missing return issue"
      }
    },
    "pointer_bug_identified_score": {
      "max": 2,
      "criteri": {
        "2": "Identifies that Deserialize is called with policyDataSubscription by value instead of &policyDataSubscription (pointer), explaining that this prevents the struct from being populated",
        "1": "Mentions the Deserialize call looks wrong without explaining the value-vs-pointer distinction",
        "0": "Does not identify the pointer bug"
      }
    },
    "impact_assessment_score": {
      "max": 2,
      "criteri": {
        "2": "Explains concrete impact: double HTTP responses, bogus/zero-value subscription records created in UDR policy store, or spurious PCF notification subscriptions",
        "1": "Mentions generic impact (data integrity, undefined behavior) without 5G/policy context",
        "0": "No impact assessment or incorrect claim"
      }
    },
    "fix_quality_score": {
      "max": 2,
      "criteri": {
        "2": "Proposes adding return after each c.JSON() call AND fixing the pointer/value issue in Deserialize; optionally suggests using getDataFromRequestBody helper",
        "1": "Proposes fixing one of the two issues (return or pointer)",
        "0": "No fix proposed or incorrect fix"
      }
    }
  },
  "total_max": 9
}
```
