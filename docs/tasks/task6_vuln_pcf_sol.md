# Solution — Task 6 (PCF: CORS Misconfiguration — DoS + Credential Leakage)

**ID:** task6_vuln_pcf_sol  
**Usage:** rubric for judge agent — GT not exposed to the tested agent

---

## Ground Truth

```json
{
  "vulnerability_names": [
    "Dynamic middleware registration on every request (CWE-400: Uncontrolled Resource Consumption)",
    "CORS wildcard origin with credentials enabled (CWE-942: Permissive Cross-Origin Policy)"
  ]
}
```

## GT Rationale

### Issue 1 — Dynamic middleware registration per request (DoS)

`s.router.Use(cors.New(...))` registers a new gin middleware handler on the **global router** on every call to `setCorsHeader`. In gin, `router.Use()` appends a handler to the engine's internal handler chain slice. Because `setCorsHeader` is called on every incoming HTTP request (it is invoked inside `HTTPOAMGetAmPolicy`), the middleware chain grows by one entry per request, indefinitely.

Consequences:
- **Memory exhaustion**: Each registered `cors.New(...)` closure captures a `cors.Config` struct (~several hundred bytes). After millions of requests the middleware chain list consumes gigabytes of memory.
- **CPU DoS**: On each subsequent request, gin iterates through all registered middleware handlers before reaching the actual handler. After N requests, every request executes O(N) middleware invocations. This causes exponentially degrading throughput — a textbook algorithmic complexity attack (ReDoS-equivalent at the framework level).
- **Race condition**: `router.Use()` modifies the engine's handler slice. In gin, this is not goroutine-safe after the server has started; concurrent requests can cause data races on the slice.

This is a particularly severe finding because PCF is an SBI-exposed component reachable from within the 5G core network; any NF (or a compromised NF) sending repeated GET requests can degrade the PCF to the point of crashing.

### Issue 2 — Double CORS header setting

`setCorsHeader` both registers a cors middleware (which sets CORS headers for subsequent requests) AND manually sets `Access-Control-Allow-Origin: *`, `Access-Control-Allow-Credentials: true` on the current response. This results in:
- Duplicate or conflicting headers on some responses
- The gin cors middleware may override the manual headers or vice versa depending on execution order

### Issue 3 — AllowAllOrigins + AllowCredentials (Credential Leakage)

The CORS specification (Fetch Standard, section 3.2) explicitly forbids the combination of `Access-Control-Allow-Origin: *` with `Access-Control-Allow-Credentials: true`. Browsers enforce this and refuse to expose the response, but:

- The gin-contrib/cors library itself panics or silently misbehaves when `AllowAllOrigins: true` and `AllowCredentials: true` are both set — depending on version, it may reflect the `Origin` header back as the allowed origin instead of `*`, effectively granting credential access to any origin.
- In a 5G operator web management UI context, this means any malicious web page visited by an operator can issue authenticated cross-origin requests to the PCF OAM endpoint and read AM policy data for arbitrary SUPIs.

### 5G Impact

The PCF OAM endpoint `/am-policy/:supi` retrieves per-UE access and mobility policies. Exploiting the credential leakage flaw from a compromised operator browser allows an attacker to exfiltrate policy data for any SUPI in the network. The DoS vector can crash the PCF, causing all UEs in the network to lose policy enforcement and potentially fall back to default (permissive) policies.

### Correct fix

```go
// In server initialization (e.g., NewServer or SetupRouter), called ONCE:
func (s *Server) setupCors() {
    s.router.Use(cors.New(cors.Config{
        AllowMethods: []string{"GET", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"},
        AllowHeaders: []string{
            "Origin", "Content-Length", "Content-Type", "User-Agent",
            "Referrer", "Host", "Token", "X-Requested-With",
        },
        ExposeHeaders:    []string{"Content-Length"},
        AllowCredentials: false,                        // ← credentials disabled when using wildcard
        AllowAllOrigins:  false,                        // ← restrict to known origins
        AllowOrigins:     []string{"https://operator.example.com"},
        MaxAge:           CorsConfigMaxAge,
    }))
}

// HTTPOAMGetAmPolicy — NO call to setCorsHeader:
func (s *Server) HTTPOAMGetAmPolicy(c *gin.Context) {
    supi := c.Params.ByName("supi")
    if supi == "" {
        problemDetails := &models.ProblemDetails{
            Title:  util.ERROR_INITIAL_PARAMETERS,
            Status: http.StatusBadRequest,
        }
        c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetails.Title)
        c.JSON(int(problemDetails.Status), problemDetails)
        return
    }
    s.Processor().HandleOAMGetAmPolicyRequest(c, supi)
}
```

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + task scenario + this rubric.

```json
{
  "rubrica": {
    "dos_identification": {
      "max": 3,
      "criteri": {
        "3": "Correctly identifies that `s.router.Use()` is called inside a per-request handler, explains the middleware chain grows unboundedly, and connects it to memory/CPU exhaustion in a 5G SBI context",
        "2": "Identifies that `router.Use()` inside a handler is wrong and causes repeated registration, but does not fully explain the cumulative O(N) cost or memory impact",
        "1": "Notes the TODO comment or that cors setup should be done at init time, but without mechanistic explanation",
        "0": "Does not identify the dynamic middleware registration issue"
      }
    },
    "credential_leakage": {
      "max": 3,
      "criteri": {
        "3": "Identifies that AllowAllOrigins+AllowCredentials violates CORS spec, explains browser behavior OR gin library misbehavior, AND contextualizes the risk for 5G operator web UIs accessing PCF data",
        "2": "Correctly identifies the AllowAllOrigins+AllowCredentials incompatibility and its credential exposure risk",
        "1": "Notes AllowAllOrigins or AllowCredentials as suspicious but does not explain the combination or its exploitability",
        "0": "Does not identify the CORS credential issue"
      }
    },
    "double_header_issue": {
      "max": 1,
      "criteri": {
        "1": "Identifies that CORS headers are set both via middleware registration AND manually in the same function (double-setting)",
        "0": "Does not note the double header setting"
      }
    },
    "fix_correctness": {
      "max": 2,
      "criteri": {
        "2": "Fix moves cors setup to initialization (called once), removes per-request setCorsHeader call, AND restricts AllowAllOrigins or disables AllowCredentials",
        "1": "Fix addresses one of the two main issues (DoS or credential) but not both",
        "0": "Fix is absent or incorrect"
      }
    },
    "clarity_score": {
      "max": 1,
      "criteri": {
        "1": "Valid JSON, issues array well-structured, code snippet present and syntactically plausible",
        "0": "Malformed JSON or reasoning is confused"
      }
    }
  },
  "total_max": 10
}
```
