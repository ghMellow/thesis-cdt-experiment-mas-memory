# Unmatched finding — task8_vuln_udm_full (1A) — agent, rep 3

| field | value |
| --- | --- |
| function | `getPlmnIDStruct` |
| vector (estimated) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| score declared | 4.1 |
| score computed (official CVSS 4.0 math) | 7.1 |
| group (recurs across reps) | a |

## Agent narrative for this repetition

_Shared across every finding reported in the same repetition — occurrences of `getPlmnIDStruct` are **bolded** below to help locate the relevant passage._

**Answer:**

The review identified critical missing input validation for SUPIs across multiple handlers, a potential DoS vulnerability due to unsafe JSON unmarshaling of query parameters, and logic errors in the custom routing mechanism and PLMN ID processing. These issues could lead to resource exhaustion or unexpected behavior in the UDM.

**Reasoning:**

1. **Missing Input Validation (SUPI/UEID):** 
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`.
   - **Pattern:** These handlers extract the `supi` parameter from the URL path (`c.Params.ByName("supi")`) but fail to call `validator.IsValidSupi(supi)` before passing it to the processor. In contrast, `HandleGetAmData` and `HandleUnsubscribe` correctly implement this check.
   - **Impact:** While the SBI is protected by mTLS/OAuth2, allowing malformed SUPIs to reach the processor can lead to unexpected behavior in the database layer or downstream NFs, potentially causing Denial of Service (DoS) via malformed queries or logic errors in the processor.
   - **Fix:** Implement `if !validator.IsValidSupi(supi) { ... return }` at the start of each handler.

2. **Unsafe JSON Unmarshaling of Query Parameters:**
   - **Location:** **`getPlmnIDStruct`**
   - **Pattern:** The code takes a string directly from a URL query parameter (`plmn-id`) and passes it to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact:** This is a dangerous pattern. An attacker (or a compromised NF) could send extremely large or deeply nested JSON strings in the query parameter. Since `json.Unmarshal` in Go can be CPU/memory intensive, this could lead to a Resource Exhaustion DoS.
   - **Fix:** Validate the length of the `plmn-id` string before unmarshaling and use a decoder with a limit.

3. **Inconsistent Parameter Handling (Logic Error):**
   - **Location:** `HandleGetTraceData`
   - **Pattern:** `plmnID := c.Query("plmn-id")`.
   - **Impact:** Unlike other handlers (e.g., `HandleGetAmData`), this handler does not use **`getPlmnIDStruct`**. It treats `plmn-id` as a raw string instead of a JSON object. This creates a logic mismatch between the API specification (which expects a JSON object for PLMN ID) and the implementation, leading to functional failures or incorrect data retrieval.
   - **Fix:** Use `s.**getPlmnIDStruct**(c.Request.URL.Query())` to maintain consistency with the 3GPP specification.

4. **Potential Path Traversal/Logic Bypass in Custom Router:**
   - **Location:** `OneLayerPathHandlerFunc`, `TwoLayerPathHandlerFunc`, `ThreeLayerPathHandlerFunc`.
   - **Pattern:** The use of `strings.Contains(route.Pattern, supi)` to match routes.
   - **Impact:** `strings.Contains` is not a strict equality check. If a `supi` parameter contains a substring that matches another route's pattern, the wrong handler might be triggered. While the risk is lowered by the structure of the patterns, using `Contains` for routing is a fragile and unsafe pattern that can lead to unexpected API behavior.
   - **Fix:** Use exact matching or a proper regex-based router instead of `strings.Contains`.

---
_Source: `results/task8_vuln_udm_full/1A/agent/*.json`, run_id `20260713T174027Z`, repetition 3._
