# Unmatched finding — task8_vuln_udm_full (1A) — agent, rep 2

| field | value |
| --- | --- |
| function | `OneLayerPathHandlerFunc, TwoLayerPathHandlerFunc` |
| vector (estimated) | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| score declared | 4.3 |
| score computed (official CVSS 4.0 math) | 2.3 |
| group (recurs across reps) | — |

## Agent narrative for this repetition

_Shared across every finding reported in the same repetition — occurrences of `OneLayerPathHandlerFunc, TwoLayerPathHandlerFunc` are **bolded** below to help locate the relevant passage._

**Answer:**

The UDM implementation suffers from inconsistent input validation of SUPIs/UEIDs across different handlers and a dangerous pattern of unmarshaling JSON directly from URL query parameters. Additionally, it leaks internal error details to the API response and employs a fragile, manual route-matching logic that could lead to handler collisions.

**Reasoning:**

1. **Missing Input Validation (SUPI/UEID):** In several handlers, the `supi` or `ueId` parameter is extracted from the URL but never validated before being passed to the processor. Specifically, `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, and `HandleGetNssai` lack the `validator.IsValidSupi(supi)` check present in `HandleGetAmData`.
   - **Impact:** While the processor might handle it, allowing malformed identifiers into the business logic can lead to unexpected behavior, potential injection into backend database queries (depending on the processor implementation), or DoS via malformed strings.
   - **Fix:** Apply `validator.IsValidSupi(supi)` or `validator.IsValidGpsi(ueId)` consistently across all handlers using these parameters.

2. **Unsafe JSON Unmarshaling of Query Parameters:** The function `getPlmnIDStruct` takes a query parameter `plmn-id` and passes it directly to `json.Unmarshal`.
   - **Impact:** Query parameters are typically plain strings. Expecting a JSON object in a query string is non-standard and dangerous. A malicious NF could send a large or deeply nested JSON payload in the URL, potentially leading to CPU/Memory exhaustion (DoS) during unmarshaling.
   - **Fix:** Use standard query parameter parsing (e.g., `c.Query("mcc")` and `c.Query("mnc")`) instead of requiring a JSON string inside a URL parameter.

3. **Information Exposure via Error Messages:** In `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, and `HandleModifyForSharedData`, the code returns `err.Error()` from `c.GetRawData()` or `openapi.Deserialize` directly to the client in the `ProblemDetails.Detail` field.
   - **Impact:** This can leak internal system details, library versions, or memory addresses to a calling NF, aiding an attacker in reconnaissance.
   - **Fix:** Use generic error messages for the client (e.g., "Invalid request body") and log the specific error internally.

4. **Logic Error in Route Matching (Path Traversal/Collision):** The `OneLayerPathHandlerFunc` and `TwoLayerPathHandlerFunc` use `strings.Contains(route.Pattern, supi)` to match routes.
   - **Impact:** This is highly fragile. If a `supi` contains a substring that matches another route pattern, the wrong handler may be invoked. For example, if a SUPI was somehow named "shared-data", it could collide with the shared data routes.
   - **Fix:** Use a proper router (like Gin's built-in tree router) instead of manual string matching and loop-based dispatching.

---
_Source: `results/task8_vuln_udm_full/1A/agent/*.json`, run_id `20260713T174027Z`, repetition 2._
