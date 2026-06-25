# Solution — Task 5 (Security Review: PCF OAM Handler)

**ID:** task5_vuln_pcf_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent  
**CVE reference:** GHSA-98cp-84m9-q3qp

---

## Ground Truth

```json
{
  "answer": "CORS misconfiguration: AllowAllOrigins and AllowCredentials are both set to true, violating CORS spec and enabling credentialed cross-origin requests from any origin",
  "type": "textual_security_review"
}
```

## GT Rationale

The `setCorsHeader` function has two interrelated issues:

1. **Core misconfiguration**: `AllowAllOrigins: true` and `AllowCredentials: true` are set simultaneously. Per the CORS specification (Fetch Standard §3.2), a response with `Access-Control-Allow-Credentials: true` must not use a wildcard (`*`) for `Access-Control-Allow-Origin`. Compliant browsers reject such responses, but non-browser HTTP clients (curl, other NFs, malicious proxies) do not.

2. **Redundant manual headers**: After configuring the CORS middleware, the function also manually sets `Access-Control-Allow-Origin: *` and `Access-Control-Allow-Credentials: true` via `c.Writer.Header().Set(...)`. This is redundant and reinforces the misconfiguration.

3. **Impact in 5G core**: The `/am-policy/:supi` endpoint exposes UE Access and Mobility policy data indexed by SUPI. Any origin can make credentialed requests to retrieve or manipulate policy data for arbitrary UEs. In a deployment where the OAM API is accessible from a broader network segment, this is a significant data exposure and potential DoS vector (exhausting PCF policy sessions).

**Fix**: Replace `AllowAllOrigins: true` with an explicit `AllowOrigins: []string{"https://trusted-mgmt.example.com"}`. Remove the manual header-setting block entirely. Never combine wildcard origin with credentials.

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "vulnerability_identified_score": {
      "max": 3,
      "criteri": {
        "3": "Correctly identifies the CORS misconfiguration as the combination of AllowAllOrigins (or wildcard origin) AND AllowCredentials being simultaneously true, and notes this violates CORS spec",
        "2": "Identifies CORS as a problem and mentions AllowAllOrigins or AllowCredentials, but does not explain why their combination is specifically the issue",
        "1": "Mentions CORS in a generic way without identifying the specific misconfiguration",
        "0": "Does not identify any CORS issue, or identifies a completely different (non-existent) vulnerability as the primary finding"
      }
    },
    "location_precision_score": {
      "max": 2,
      "criteri": {
        "2": "Points specifically to the setCorsHeader function and/or the cors.Config block with AllowAllOrigins+AllowCredentials; optionally also notes the redundant manual headers",
        "1": "References the file or handler in a general way without identifying the exact location of the misconfiguration",
        "0": "No location information provided"
      }
    },
    "impact_assessment_score": {
      "max": 2,
      "criteri": {
        "2": "Explains concrete impact in 5G context: unauthorized cross-origin access to UE policy data (SUPI-indexed), potential DoS, or access from untrusted network segments",
        "1": "Mentions generic security impact (data exposure, unauthorized access) without 5G-specific context",
        "0": "No impact assessment or incorrect impact claim"
      }
    },
    "fix_quality_score": {
      "max": 2,
      "criteri": {
        "2": "Proposes a correct and specific fix: replace AllowAllOrigins with explicit allowlist, remove or fix the manual headers, never combine wildcard with credentials",
        "1": "Suggests a direction (use allowlist, restrict origins) without specifying the exact change needed",
        "0": "No fix proposed, or fix is incorrect (e.g., suggests removing credentials entirely without addressing the origin wildcard)"
      }
    }
  },
  "total_max": 9
}
```
