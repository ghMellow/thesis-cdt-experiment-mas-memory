# Unmatched finding — task8_vuln_udm_full (1B) — agent, rep 2

| field | value |
| --- | --- |
| function | `getPlmnIDStruct` |
| vector (estimated) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| score declared | 4.1 |
| score computed (official CVSS 4.0 math) | 5.3 |

## Agent narrative for this repetition

_Shared across every finding reported in the same repetition — occurrences of `getPlmnIDStruct` are **bolded** below to help locate the relevant passage._

**Answer:**

The review identified missing SUPI validation in several critical data retrieval handlers, potential DoS via unvalidated JSON input in query parameters, and information leakage through verbose error responses. Additionally, there are logic inconsistencies in the multi-layer path routing that may cause request failures.

**Reasoning:**

1. **Improper Input Validation (Missing SUPI Validation):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`.
   - **Pattern:** These functions retrieve the `supi` parameter from the URL path (`c.Params.ByName("supi")`) but fail to call `validator.IsValidSupi(supi)` before passing it to the processor. In contrast, `HandleGetAmData` correctly implements this check.
   - **Impact:** While the SBI is protected by mTLS/OAuth2, allowing malformed or oversized SUPI strings to reach the processor/database layer can lead to unexpected behavior, potential injection attacks in the backend storage, or DoS via resource exhaustion if the validator was intended to limit input length.
   - **Fix:** Implement `if !validator.IsValidSupi(supi) { ... return }` at the start of every handler that accepts a SUPI.

2. **Unsafe JSON Unmarshaling (Potential DoS/Resource Exhaustion):**
   - **Location:** **`getPlmnIDStruct`**.
   - **Pattern:** The code takes a query parameter `plmn-id` and directly passes it to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact:** Since query parameters can be large, an attacker (compromised NF) could send a deeply nested or massive JSON string. While `json.Unmarshal` in Go is relatively safe, repeated large allocations in a high-throughput UDM can lead to memory exhaustion (DoS).
   - **Fix:** Validate the length of the `plmn-id` string before attempting to unmarshal it.

3. **Logic Error / Parameter Mismatch (Incorrect Parameter Mapping):**
   - **Location:** `ThreeLayerPathHandlerFunc`.
   - **Pattern:** For the `sdm-subscriptions` route, the code maps `c.Param("supi")` to `ueId` and `c.Param("thirdLayer")` to `subscriptionId`. However, the route definition in the comments and logic suggests a structure where `supi` is the first segment. If the routing is inconsistent with the handler's expectations, it leads to 404s or incorrect data access.
   - **Impact:** Functional instability. If a request is routed incorrectly, the UDM may fail to process legitimate subscription modifications or deletions.
   - **Fix:** Standardize the parameter naming in the Gin router and the handler functions to ensure consistency.

4. **Information Exposure (Verbose Error Messages):**
   - **Location:** `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.
   - **Pattern:** The code returns `err.Error()` from `c.GetRawData()` or `openapi.Deserialize` directly in the `ProblemDetails.Detail` field.
   - **Impact:** This can leak internal system details, library versions, or memory addresses to a calling NF, aiding an attacker in reconnaissance.
   - **Fix:** Use generic error messages for internal failures (e.g., "Internal Server Error") and log the detailed error internally.

---
_Source: `results/task8_vuln_udm_full/1B/agent/*.json`, run_id `20260712T142416Z`, repetition 2._
