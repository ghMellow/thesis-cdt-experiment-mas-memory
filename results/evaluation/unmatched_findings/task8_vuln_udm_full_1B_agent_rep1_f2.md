# Unmatched finding — task8_vuln_udm_full (1B) — agent, rep 1

| field | value |
| --- | --- |
| function | `HandleSubscribe` |
| vector (estimated) | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| score declared | 4.1 |
| score computed (official CVSS 4.0 math) | 5.1 |

## Agent narrative for this repetition

_Shared across every finding reported in the same repetition — occurrences of `HandleSubscribe` are **bolded** below to help locate the relevant passage._

**Answer:**

The review identified critical missing input validations for SUPI/UEID across several handlers, leading to inconsistent security enforcement. Additionally, the code suffers from unsafe JSON unmarshaling of query parameters and leaks internal system details through raw error messages in HTTP responses.

**Reasoning:**

1. **Improper Input Validation (Missing SUPI Validation):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`.
   - **Pattern:** These functions extract the `supi` parameter from the URL path (`c.Params.ByName("supi")`) but fail to call `validator.IsValidSupi(supi)` before passing it to the `Processor` layer. In contrast, `HandleGetAmData` correctly implements this check.
   - **Impact:** While the SBI is protected by mTLS/OAuth2, an authorized but compromised NF (or a malicious internal actor) could send malformed SUPIs. This may lead to unexpected behavior in the database layer, potential injection attacks if the processor doesn't sanitize inputs, or crashes (DoS) in the backend logic.
   - **Fix:** Add `if !validator.IsValidSupi(supi) { ... return }` blocks to all handlers that accept a SUPI.

2. **Unsafe JSON Unmarshaling of User Input (Potential DoS/Resource Exhaustion):**
   - **Location:** `getPlmnIDStruct`
   - **Pattern:** The code takes a query parameter `plmn-id` and passes it directly to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact:** Query parameters are typically short, but an attacker could send a very large string in the `plmn-id` parameter. Since `json.Unmarshal` is used on a byte slice derived from a URL query, it can lead to high CPU/memory consumption. Furthermore, the logic expects a JSON object in a query string, which is an unconventional and fragile pattern.
   - **Fix:** Validate the length of the `plmn-id` string before unmarshaling and consider using a standard key-value format instead of JSON within a URL query parameter.

3. **Inconsistent Parameter Validation (UE ID):**
   - **Location:** `HandleUnsubscribe`, `HandleModify`, `HandleGetIdTranslationResult`.
   - **Pattern:** These functions validate `ueId` using `validator.IsValidGpsi(ueId) || validator.IsValidSupi(ueId)`. However, **`HandleSubscribe`** (which also takes a SUPI in the path) does **not** perform this validation.
   - **Impact:** Inconsistency in security posture. **`HandleSubscribe`** allows any string to be passed as a SUPI to the processor, potentially bypassing business logic constraints.
   - **Fix:** Implement the same `IsValidGpsi` / `IsValidSupi` check in **`HandleSubscribe`**.

4. **Information Leakage via Error Messages:**
   - **Location:** `getPlmnIDStruct`, `HandleSubscribeToSharedData`, **`HandleSubscribe`**, `HandleModify`, `HandleModifyForSharedData`.
   - **Pattern:** The code returns `err.Error()` directly to the client in the `ProblemDetails` response (e.g., `Reason: err.Error()` or `Detail: err.Error()`).
   - **Impact:** Returning raw Go error messages from `json.Unmarshal` or `openapi.Deserialize` can leak internal implementation details, library versions, or structural information about the expected data models to a calling NF.
   - **Fix:** Use generic error messages for the client (e.g., "Invalid request body") and log the detailed error internally.

---
_Source: `results/task8_vuln_udm_full/1B/agent/*.json`, run_id `20260712T142416Z`, repetition 1._
