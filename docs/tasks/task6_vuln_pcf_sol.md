# Solution — Task 6 (PCF: insecure CORS configuration)

**ID:** task6_vuln_pcf_sol
**Usage:** rubric for judge agent, GT not exposed to the tested agent
**CVE reference:** GHSA-98cp-84m9-q3qp (free5GC PCF)

---

## Ground Truth

```json
{
  "answer": {
    "vulnerabilities": [
      "AllowAllOrigins: true combined with AllowCredentials: true is forbidden by the CORS spec (W3C) and most browsers: when credentials are allowed, the wildcard origin * must not be used. The gin-contrib/cors library panics or ignores credentials in this case, but the response headers are set manually below to Access-Control-Allow-Origin: * and Access-Control-Allow-Credentials: true simultaneously, which browsers will block — making this a DoS against legitimate cross-origin clients, or a misconfiguration that some non-browser HTTP clients may exploit",
      "The CORS middleware is added via s.router.Use() inside a per-request handler (setCorsHeader), which is called once per request. This adds a new middleware layer on every request, causing middleware stack growth and memory/CPU leak over time (DoS vector)",
      "CORS wildcard with no origin allowlist exposes the policy API to any web origin"
    ],
    "impact": "The combination of AllowAllOrigins and AllowCredentials causes the CORS middleware to panic or produce invalid headers in conformant implementations. In practice, the manual header setting produces Access-Control-Allow-Origin: * alongside Access-Control-Allow-Credentials: true — a configuration rejected by all standard browsers. This breaks legitimate cross-origin access (DoS for browser-based NMS tools). Additionally, calling router.Use() inside a handler grows the middleware chain indefinitely, causing memory growth and eventual OOM crash under sustained traffic.",
    "fix": "Configure CORS once at router initialization, not inside handlers. Use an explicit AllowOrigins list instead of AllowAllOrigins: true. If credentials are needed, list each allowed origin explicitly. Remove the duplicate manual header setting."
  },
  "type": "textual_reasoning"
}
```

## GT Rationale

- W3C CORS spec §6.1: when `Access-Control-Allow-Credentials: true`, the origin must not be `*`
- gin-contrib/cors: if both `AllowAllOrigins` and `AllowCredentials` are set, the library itself panics with a configuration error in newer versions
- `s.router.Use()` called inside a gin handler does not affect the current request routing — it appends to the router's middleware list and takes effect only for future requests, growing the list on every request
- The OAM endpoint returns subscriber AM policy data, making unauthorized cross-origin access a confidentiality concern
- The DoS via middleware accumulation was the primary CVE finding

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + code snippet + this rubric.

```json
{
  "rubrica": {
    "vulnerability_identification_score": {
      "max": 4,
      "criteri": {
        "4": "Identifies both: (a) AllowAllOrigins+AllowCredentials incompatibility AND (b) router.Use() called inside a per-request handler causing middleware growth",
        "3": "Identifies one of the two issues precisely, or both but with partial explanation",
        "2": "Identifies the CORS wildcard problem generically without referencing the credentials conflict or middleware growth",
        "1": "Notes that CORS is misconfigured but cannot specify how",
        "0": "No vulnerability identified or wrong vulnerability"
      }
    },
    "impact_score": {
      "max": 2,
      "criteri": {
        "2": "Explains DoS or security bypass with concrete mechanism (browser rejection, middleware stack growth, or credentials leak)",
        "1": "States impact exists but is vague ('could be exploited')",
        "0": "No meaningful impact"
      }
    },
    "fix_score": {
      "max": 2,
      "criteri": {
        "2": "Proposes moving CORS setup to router initialization AND restricting origins explicitly",
        "1": "Proposes only one of the two corrections",
        "0": "No fix or incorrect fix"
      }
    },
    "clarity_score": {
      "max": 1,
      "criteri": {
        "1": "Clear, structured JSON, vulnerabilities as a list",
        "0": "Malformed JSON or incoherent response"
      }
    }
  },
  "total_max": 9
}
```
