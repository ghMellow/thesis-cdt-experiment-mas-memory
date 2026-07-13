# Unmatched finding — task8_vuln_udm_full (1A) — agent, rep 2

| field | value |
| --- | --- |
| function | `TwoLayerPathHandlerFunc` |
| vector (estimated) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N` |
| score declared | 3.1 |
| score computed (official CVSS 4.0 math) | 5.1 |

## Agent narrative for this repetition

_Shared across every finding reported in the same repetition — occurrences of `TwoLayerPathHandlerFunc` are **bolded** below to help locate the relevant passage._

**Answer:**

The code suffers from inconsistent input validation (missing SUPI checks in multiple handlers), a dangerous pattern of unmarshaling JSON directly from URL query parameters, and a fragile manual routing mechanism that uses `strings.Contains` and manual parameter overrides, which could lead to logic errors and unauthorized data access.

**Reasoning:**

1. **Improper Input Validation (Missing SUPI Validation):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`.
   - **Pattern:** These functions extract the `supi` parameter from the URL path (`c.Params.ByName("supi")`) but fail to call `validator.IsValidSupi(supi)` before passing it to the `Processor` layer. In contrast, `HandleGetAmData` correctly implements this check.
   - **Impact:** While the SBI is protected by mTLS/OAuth2, an authenticated but compromised NF (or a malicious internal actor) could send malformed SUPIs. This could lead to unexpected behavior in the database layer, potential injection attacks if the processor doesn't sanitize inputs, or logic errors in subscriber data retrieval.
   - **Fix:** Add the `validator.IsValidSupi(supi)` check at the beginning of each handler that accepts a SUPI.

2. **Unsafe JSON Unmarshaling from Query Parameters:**
   - **Location:** `getPlmnIDStruct`
   - **Pattern:** The code takes a raw string from a URL query parameter (`plmn-id`) and passes it directly into `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact:** This is a highly unusual pattern. Query parameters are typically key-value pairs, not JSON blobs. If an attacker can control the `plmn-id` parameter, they can provide complex JSON structures. While Go's `json.Unmarshal` is generally safe from memory corruption, this pattern can be used for "JSON injection" or causing resource exhaustion (DoS) if the parser is hit with deeply nested objects or extremely large strings, potentially crashing the UDM instance.
   - **Fix:** Change the `plmn-id` parameter to a standard format (e.g., `mcc,mnc`) or use a dedicated POST body for complex objects. If JSON must be used in a query, implement strict length limits on the input string before unmarshaling.

3. **Logic Error / Path Routing Ambiguity:**
   - **Location:** `OneLayerPathHandlerFunc` and **`TwoLayerPathHandlerFunc`**
   - **Pattern:** The routing logic uses `strings.Contains(route.Pattern, supi)` to match routes.
   - **Impact:** `strings.Contains` is too permissive. If a `supi` value contains a substring that matches another route pattern, it may trigger the wrong handler. Furthermore, the manual manipulation of `c.Params` (e.g., `c.Params = append(...)` in **`TwoLayerPathHandlerFunc`**) is error-prone and can lead to parameter pollution or incorrect data being passed to the business logic.
   - **Fix:** Use a proper router (like Gin's built-in group routing) instead of manual string matching and parameter overriding.

---
_Source: `results/task8_vuln_udm_full/1A/agent/*.json`, run_id `20260712T142416Z`, repetition 2._
