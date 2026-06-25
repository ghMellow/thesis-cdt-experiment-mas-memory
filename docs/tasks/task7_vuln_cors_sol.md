# Solution — Task 7 (security code review: CORS misconfiguration)

**ID:** task7_vuln_cors_sol
**Usage:** rubric for judge agent, GT not exposed to the tested agent

---

## Ground Truth

```json
{
  "answer": "Three issues. (1) DoS via middleware accumulation: s.router.Use() is called inside the request handler setCorsHeader, which means a new CORS middleware is appended to the Gin engine's global chain on every incoming request. The chain grows without bound, causing memory exhaustion under sustained traffic. (2) Invalid CORS policy: AllowAllOrigins (equivalent to Access-Control-Allow-Origin: *) is set together with AllowCredentials: true. The CORS spec forbids this combination; modern browsers will reject the response, making credentialed cross-origin requests permanently broken. (3) Duplicate and conflicting CORS configuration: CORS headers are set both by the cors.New() middleware and manually via c.Writer.Header().Set(), using different header lists. The two configurations can conflict, producing non-deterministic header values depending on middleware execution order.",
  "type": "textual_reasoning"
}
```

## GT Rationale

**Issue 1 — Middleware accumulation (DoS):**

`s.router.Use()` modifies the Gin engine's global handler chain. Calling it from within a per-request handler means each request permanently adds one more middleware layer to the chain. After N requests, every subsequent request executes N+1 CORS middleware instances. Memory and CPU grow monotonically until OOM crash. This is the root cause of the memory growth symptom.

**Issue 2 — AllowAllOrigins + AllowCredentials (CORS spec violation):**

Per the Fetch standard (WHATWG): if the `Access-Control-Allow-Credentials` response header is `true`, the `Access-Control-Allow-Origin` header MUST NOT be `*`. When both are present, compliant browsers (Chrome, Firefox, Safari) block the response entirely. The consequence is that no browser-based management tool can make credentialed cross-origin requests to this endpoint, even if it is on a trusted origin. Additionally, this configuration signals that the CORS policy was never tested — weakening confidence in the overall security posture.

**Issue 3 — Duplicate CORS headers (non-deterministic behavior):**

The `cors.New()` middleware and the manual `c.Writer.Header().Set()` calls both write CORS headers, but with different values:
- `cors.New()` uses `AllowHeaders` from the config struct
- Manual calls use a different, longer list including `Authorization`, `X-CSRF-Token`, etc.

HTTP headers can be set multiple times; the final value depends on execution order. If the middleware runs after the manual sets, it may overwrite them. If it runs before, the manual sets override. The result is that the actual CORS policy in effect at runtime differs from what either configuration specifies, making the behavior untestable and unpredictable.

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "dos_vulnerability_score": {
      "max": 4,
      "criteri": {
        "4": "Identifies that s.router.Use() inside a per-request handler permanently appends middleware to the global chain, explains that the chain grows with each request, and connects this to memory exhaustion (DoS)",
        "3": "Identifies that s.router.Use() is called per-request and is problematic, but does not fully explain the cumulative growth mechanism or the DoS impact",
        "2": "Notices that CORS setup is inside the handler rather than at startup, but frames it only as a performance issue rather than a DoS vulnerability",
        "1": "Mentions something wrong with setCorsHeader being called per-request without identifying the middleware accumulation mechanism",
        "0": "Does not identify this issue"
      }
    },
    "cors_spec_violation_score": {
      "max": 3,
      "criteri": {
        "3": "Identifies that AllowAllOrigins and AllowCredentials: true cannot coexist per the CORS spec, and explains that browsers will reject the response",
        "2": "Identifies that the combination is problematic (too permissive or broken), but without referencing the spec or explaining the browser rejection behavior",
        "1": "Flags AllowAllOrigins as overly permissive without identifying the credentials conflict",
        "0": "Does not identify this issue"
      }
    },
    "duplicate_config_score": {
      "max": 2,
      "criteri": {
        "2": "Identifies that CORS headers are set twice (via middleware and manually) with differing values, and explains that the resulting behavior is non-deterministic",
        "1": "Notices redundancy between the two CORS configurations without explaining the conflict or non-determinism",
        "0": "Does not identify this issue"
      }
    },
    "clarity_score": {
      "max": 1,
      "criteri": {
        "1": "Clear response, valid JSON, issues described separately and with distinct root causes",
        "0": "Malformed JSON or issues conflated without distinction"
      }
    }
  },
  "total_max": 10
}
```
