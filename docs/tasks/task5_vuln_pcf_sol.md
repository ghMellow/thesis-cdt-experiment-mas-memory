# Solution — Task 5 (PCF OAM CORS DoS)

**ID:** task5_vuln_pcf_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent

---

## Ground Truth

```json
{
  "answer": {
    "vulnerability_type": "Resource exhaustion / DoS via middleware registration in request handler",
    "location": "setCorsHeader function — s.router.Use(cors.New(...)) called inside a per-request handler",
    "impact": "Each HTTP request permanently appends a new CORS middleware to the Gin router chain, causing unbounded memory and CPU growth that leads to denial of service"
  },
  "type": "textual_security"
}
```

## GT Rationale

- `s.router.Use(cors.New(...))` is called inside `setCorsHeader`, which is invoked on every GET request to `/am-policy/:supi`
- In Gin, `router.Use()` is an initialisation-time operation; calling it at request time permanently adds a middleware to the chain
- Each request appends one more middleware entry: after N requests, the chain processes N redundant CORS middlewares
- This is a confirmed resource leak that degrades performance and eventually causes OOM/DoS
- Secondary issue: `AllowAllOrigins: true` combined with `AllowCredentials: true` is a CORS misconfiguration (browsers reject it per spec, but the server still exposes credentials headers to any origin)

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "identification_score": {
      "max": 3,
      "criteri": {
        "3": "Correctly identifies that s.router.Use() is called inside a request handler, causing middleware accumulation on every request",
        "2": "Identifies a CORS-related issue or resource leak but without explaining the router.Use() accumulation mechanism",
        "1": "Mentions CORS misconfiguration (AllowAllOrigins + AllowCredentials) as the primary issue without noticing the middleware accumulation",
        "0": "Does not identify a meaningful vulnerability, or identifies only unrelated issues"
      }
    },
    "location_score": {
      "max": 2,
      "criteri": {
        "2": "Correctly names setCorsHeader and the s.router.Use() call as the vulnerable location",
        "1": "Points to setCorsHeader or HTTPOAMGetAmPolicy generically without the specific call",
        "0": "Incorrect or missing location"
      }
    },
    "impact_score": {
      "max": 2,
      "criteri": {
        "2": "Explains that repeated middleware registration causes memory growth and can lead to DoS of the PCF node",
        "1": "Mentions performance degradation or resource issue without connecting it to request-level accumulation",
        "0": "No impact described, or impact is incorrect"
      }
    },
    "clarity_score": {
      "max": 1,
      "criteri": {
        "1": "Response is valid JSON with all required fields populated",
        "0": "Malformed JSON or missing required fields"
      }
    }
  },
  "total_max": 8
}
```
