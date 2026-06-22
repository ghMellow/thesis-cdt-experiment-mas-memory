# Solution — Task 5 (PCF vulnerability detection)

**ID:** task5_vuln_pcf_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent  
**Reference:** free5gc advisory GHSA-98cp-84m9-q3qp (CORS / DoS)

---

## Ground Truth

```json
{
  "answer": {
    "vulnerability": "Denial of Service via per-request CORS middleware registration",
    "location": "setCorsHeader",
    "severity": "high",
    "mechanism": "setCorsHeader is called inside the request handler HTTPOAMGetAmPolicy and registers a new global router middleware with s.router.Use(cors.New(...)) on EVERY request. The middleware chain grows unbounded with each incoming request, exhausting memory/CPU and degrading the service until denial of service."
  },
  "type": "textual_security"
}
```

## GT Rationale

- The CORS middleware must be configured **once at router setup**, not inside a
  per-request handler. `s.router.Use(...)` appends to the global middleware
  chain; calling it per request makes the chain grow without bound → resource
  exhaustion → DoS.
- Secondary (not required for full score): the CORS policy itself is unsafe —
  `AllowAllOrigins: true` together with `AllowCredentials: true` and a manual
  `Access-Control-Allow-Origin: *` is a permissive-CORS misconfiguration.

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "detection_score": {
      "max": 3,
      "criteri": {
        "3": "Identifies the DoS caused by registering router middleware (s.router.Use) on every request inside the handler",
        "2": "Identifies the CORS misconfiguration (AllowAllOrigins + AllowCredentials / wildcard with credentials) but not the per-request middleware DoS",
        "1": "Flags a CORS-related concern generically without naming the concrete defect",
        "0": "Does not identify any real vulnerability in the code"
      }
    },
    "impact_score": {
      "max": 2,
      "criteri": {
        "2": "Explains the mechanism (unbounded middleware chain growth) AND its impact (memory/CPU exhaustion, DoS)",
        "1": "States the impact or the mechanism but not both",
        "0": "No correct explanation of mechanism or impact"
      }
    },
    "localization_score": {
      "max": 1,
      "criteri": {
        "1": "Points to setCorsHeader / the s.router.Use call as the responsible location",
        "0": "Wrong or missing location"
      }
    },
    "clarity_score": {
      "max": 1,
      "criteri": {
        "1": "Clear, structured response, valid JSON",
        "0": "Malformed JSON or confused response"
      }
    },
    "confidence_calibration_score": {
      "max": 1,
      "criteri": {
        "1": "Confidence >= 0.7 if detection is correct, or low confidence if detection is wrong",
        "0": "High confidence on wrong detection, or inexplicably low confidence on correct detection"
      }
    }
  },
  "total_max": 8
}
```
