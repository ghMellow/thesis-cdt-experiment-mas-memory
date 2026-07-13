# Unmatched finding — task8_vuln_udm_full (1B) — agent, rep 3

| field | value |
| --- | --- |
| function | `HandleSubscribe, HandleModify, HandleSubscribeToSharedData, HandleModifyForSharedData` |
| vector (estimated) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| score declared | 3.1 |
| score computed (official CVSS 4.0 math) | 5.3 |

## Agent narrative for this repetition

_Shared across every finding reported in the same repetition — occurrences of `HandleSubscribe, HandleModify, HandleSubscribeToSharedData, HandleModifyForSharedData` are **bolded** below to help locate the relevant passage._

**Answer:**

The UDM implementation suffers from inconsistent input validation of SUPIs across multiple handlers, unsafe JSON unmarshaling of URL query parameters in `getPlmnIDStruct`, and information leakage through raw error messages. These issues could lead to unexpected processor behavior, potential DoS, and reconnaissance opportunities for a compromised internal NF.

**Reasoning:**

1. **Missing Input Validation (SUPI/UEID):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`.
   - **Pattern:** These functions extract the `supi` parameter from the URL path (`c.Params.ByName("supi")`) but fail to call `validator.IsValidSupi(supi)` before passing it to the processor. In contrast, `HandleGetAmData` and `HandleUnsubscribe` correctly implement this check.
   - **Impact:** While the SBI is protected by mTLS/OAuth2, allowing malformed SUPIs into the business logic layer can lead to unexpected behavior in the database queries or downstream processors (e.g., injection if the processor doesn't sanitize inputs), potentially causing Denial of Service (DoS) or data leakage if the backend treats malformed IDs as wildcards.
   - **Fix:** Implement `if !validator.IsValidSupi(supi) { ... return }` at the start of each handler.

2. **Unsafe JSON Unmarshaling of User-Controlled Query Parameters:**
   - **Location:** `getPlmnIDStruct`
   - **Pattern:** The code takes a raw string from the `plmn-id` query parameter and passes it directly to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact:** This is a dangerous pattern. An attacker (or a compromised NF) can send a specially crafted JSON string in the query parameter. While `models.PlmnId` is likely a simple struct, this pattern is prone to "JSON injection" or resource exhaustion if the parser is stressed. More importantly, it violates the expected 3GPP REST API design where `plmn-id` is typically a simple string or a specific format, not a JSON blob embedded in a URL query.
   - **Fix:** Use standard query parameter parsing or a strict schema validator instead of `json.Unmarshal` on raw URL query values.

3. **Inconsistent Parameter Handling (Logic Error):**
   - **Location:** `HandleGetAmData`, `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`.
   - **Pattern:** The code creates a `url.Values` object (`query := url.Values{}`) and manually sets values from `c.Query()`, but then calls `s.getPlmnIDStruct(c.Request.URL.Query())`.
   - **Impact:** This is redundant and confusing logic. It doesn't directly create a security hole but indicates a lack of input sanitization consistency, increasing the risk of "Parameter Pollution" where different parts of the application interpret the query string differently.
   - **Fix:** Use a single source of truth for query parameters (either `c.Request.URL.Query()` or Gin's `c.Query()`).

4. **Improper Error Detail Leakage:**
   - **Location:** `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.
   - **Pattern:** The code returns `err.Error()` directly in the `ProblemDetails.Detail` field when `openapi.Deserialize` or `c.GetRawData()` fails.
   - **Impact:** Returning raw internal error messages to the caller can leak implementation details about the underlying libraries, data structures, or the state of the system, aiding an attacker in reconnaissance.
   - **Fix:** Use generic error messages for the client and log the detailed error internally.

---
_Source: `results/task8_vuln_udm_full/1B/agent/*.json`, run_id `20260712T142416Z`, repetition 3._
