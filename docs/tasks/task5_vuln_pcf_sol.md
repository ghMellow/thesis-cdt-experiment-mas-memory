# Solution — Task 5 (PCF OAM CORS misconfiguration)

**ID:** task5_vuln_pcf_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent

---

## Ground Truth

```json
{
  "answer": {
    "vulnerability": "CORS misconfiguration: AllowAllOrigins: true combined with AllowCredentials: true (CWE-942, GHSA-98cp-84m9-q3qp), plus redundant manual headers re-setting Access-Control-Allow-Origin: * and Access-Control-Allow-Credentials: true",
    "impact": "Access-Control-Allow-Credentials: true with Access-Control-Allow-Origin: * violates the CORS spec (RFC 6454 / Fetch Standard). Browsers reject this combination, but a custom client or proxy does not enforce it, so any party reachable on the core network can issue credentialed cross-origin requests to /am-policy/:supi, bypassing origin restrictions on the PCF OAM endpoint.",
    "fix": "Remove AllowAllOrigins: true and replace it with an explicit allow-list of trusted origins (AllowOrigins: [...]); remove the redundant manual Access-Control-Allow-Origin/Access-Control-Allow-Credentials header writes that duplicate (and conflict with) the cors middleware configuration."
  },
  "type": "textual_vuln_analysis"
}
```

## GT Rationale

- `AllowAllOrigins: true` sets `Access-Control-Allow-Origin: *` for every response.
- `AllowCredentials: true` adds `Access-Control-Allow-Credentials: true`.
- Per the Fetch/CORS spec these two are mutually exclusive: a wildcard origin must never be paired with credentialed requests. Browsers refuse to expose the response in this case, but non-browser clients (common between NFs/proxies inside a 5G core) are not bound by this check.
- The handler additionally re-sets the same headers manually (lines after `cors.New(...)`), which is redundant and reinforces the wildcard+credentials combination regardless of the middleware configuration.
- Net effect: any network-adjacent actor can perform credentialed cross-origin requests against the PCF AM-policy OAM endpoint without origin restriction — mapped to GHSA-98cp-84m9-q3qp (high severity).

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "vuln_identified_score": {
      "max": 3,
      "criteri": {
        "3": "Identifies the AllowAllOrigins + AllowCredentials combination as a CORS spec violation AND notes the redundant manual header duplication as a contributing problem",
        "2": "Identifies the AllowAllOrigins + AllowCredentials combination as a CORS spec violation but does not mention the manual header duplication",
        "1": "Identifies AllowAllOrigins (or the wildcard '*' header) as risky/bad practice but does not explain the conflict with AllowCredentials",
        "0": "Does not identify any CORS-related vulnerability"
      }
    },
    "impact_assessment_score": {
      "max": 2,
      "criteri": {
        "0": "No impact assessment, or generic 'security risk'",
        "1": "Generic impact (e.g. 'cross-origin attacks possible') without context-specific consequence",
        "2": "Impact specific to the 5G core context: unrestricted credentialed cross-origin access to the AM-policy OAM endpoint by non-browser clients/proxies on the core network"
      }
    },
    "fix_proposed_score": {
      "max": 2,
      "criteri": {
        "0": "No fix proposed, or incorrect fix",
        "1": "Generic fix (e.g. 'restrict origins' or 'use a whitelist') without addressing AllowCredentials or the duplicated headers",
        "2": "Specific correct fix: replace AllowAllOrigins with an explicit origin allow-list compatible with AllowCredentials, and remove the redundant manual header writes"
      }
    },
    "false_positives_score": {
      "max": 1,
      "criteri": {
        "1": "No misleading or unrelated vulnerabilities reported as the primary finding",
        "0": "Reports unrelated/incorrect vulnerabilities as the main finding, obscuring or replacing the CORS issue"
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
        "1": "Confidence >= 0.7 if the CORS vulnerability is correctly identified, or low confidence if it is missed",
        "0": "High confidence despite missing the vulnerability, or inexplicably low confidence on a correct finding"
      }
    }
  },
  "total_max": 10
}
```
