# Unmatched finding — task8_vuln_udm_full (1A) — agent, rep 3

| field | value |
| --- | --- |
| function | `getPlmnIDStruct` |
| vector (estimated) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| score declared | 4.0 |
| score computed (official CVSS 4.0 math) | 5.3 |

## Agent narrative for this repetition

_Shared across every finding reported in the same repetition — occurrences of `getPlmnIDStruct` are **bolded** below to help locate the relevant passage._

**Answer:**

The review identified missing SUPI validation in multiple handlers, which could lead to processing malformed identifiers. Additionally, there are logic errors in parameter handling within the `ThreeLayerPathHandlerFunc` and a tendency to leak internal error details via API responses.

**Reasoning:**

1. **Improper Input Validation (Missing SUPI Validation):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`.
   - **Pattern:** These functions extract the `supi` parameter from the URL path (`c.Params.ByName("supi")`) but fail to call `validator.IsValidSupi(supi)` before passing it to the `Processor()`. In contrast, `HandleGetAmData` correctly performs this check.
   - **Impact:** While the SBI is protected by mTLS/OAuth2, an authorized but compromised NF (or a malicious internal actor) could send malformed SUPIs to the UDM. This could lead to unexpected behavior in the backend processor, potential database query errors, or logic bypasses if the processor assumes the input is already validated.
   - **Fix:** Implement `if !validator.IsValidSupi(supi) { ... return }` at the start of each handler that accepts a SUPI.

2. **Unsafe JSON Unmarshaling (Potential DoS/Resource Exhaustion):**
   - **Location:** **`getPlmnIDStruct`**
   - **Pattern:** The code takes a string directly from a query parameter (`plmn-id`) and passes it to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact:** Query parameters have size limits, but `json.Unmarshal` on untrusted input without size constraints or schema validation can be used for "JSON bombs" or resource exhaustion if the input is crafted to be deeply nested or extremely large (though limited by the HTTP server's max header/query size).
   - **Fix:** Validate the length of the `plmn-id` string before unmarshaling and ensure the `models.PlmnId` struct has strict bounds.

3. **Logic Error / Parameter Mismanagement (Incorrect Param Mapping):**
   - **Location:** `ThreeLayerPathHandlerFunc`
   - **Pattern:** In the `sdm-subscriptions` block for `http.MethodDelete` and `http.MethodPatch`, the code manually overwrites `c.Params` with a new slice: `tmpParams = append(tmpParams, ...); c.Params = tmpParams`.
   - **Impact:** This is a dangerous pattern in Gin. Overwriting the `Params` slice can lead to the loss of other important routing parameters or cause unexpected behavior in middleware that relies on the original parameter set.
   - **Fix:** Use `c.Set("ueId", ...)` and `c.Set("subscriptionId", ...)` to pass values to the handler, or modify the route definition to use named parameters that match the handler's expectations.

4. **Information Leakage (Verbose Error Messages):**
   - **Location:** `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.
   - **Pattern:** The code returns `err.Error()` directly in the `ProblemDetails.Detail` field when `c.GetRawData()` or `openapi.Deserialize` fails.
   - **Impact:** Returning raw Go error messages to the caller can leak internal implementation details, library versions, or memory addresses, aiding an attacker in reconnaissance.
   - **Fix:** Use generic error messages for the client (e.g., "Invalid request body") and log the detailed error internally.

---
_Source: `results/task8_vuln_udm_full/1A/agent/*.json`, run_id `20260712T142416Z`, repetition 3._
