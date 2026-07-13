# 1A — task8_vuln_udm_full

> **Run(s) in this report:**
> - `agent`: 20260712T142416Z

## CVSS estimate (Blocco B, deterministic)

| role | estimates | matched | missed CVEs | unmatched findings | avg band vs published (0-3) | avg band vs B (0-3) | avg exploitability (0-5) | avg impact (0-3) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent | 3/3 | 3 | 0 | 7 | 0.33 | 0.00 | 4.00 | 1.33 |

**Legend**

- `estimates` = X/Y — X = repetitions where the agent emitted *at least one* CVSS finding block; Y = total repetitions evaluated for this task. **This is block presence, not correctness** — it says nothing about how many vulnerabilities were actually found or matched (see `matched`/`missed CVEs` below for that).
- `matched` = total findings, summed across all repetitions, successfully paired to a ground-truth CVE (by comparing the function name the agent reported to that CVE's known handler function).
- `missed CVEs` = total ground-truth CVEs, summed across all repetitions, that no finding in that repetition matched — i.e. vulnerabilities the agent failed to surface at all.
- `unmatched findings` = total findings, summed across all repetitions, that matched no ground-truth CVE — either a false positive, or a genuine extra vulnerability with no catalogued CVE (ranked for triage in the table further down).
- ⚠️ **The remaining four columns are diagnostic only, not the headline metric**: `avg band vs published` / `avg band vs B` score how close the *declared* score is to the reference (0 = far, 3 = exact band), and `avg exploitability` (0-5) / `avg impact` (0-3) count binary field matches on the estimated vector. The declared score is produced independently of the vector the agent also emits and carries no official rigor of its own (F17: systematically lower than what the vector is actually worth). These four columns exist only for comparability with runs 1-3.
- The metrics that actually count — recomputed from the vector with the official CVSS 4.0 algorithm — are in the table below.

### Official CVSS 4.0 math (score recomputed from the estimated vector) — the reference metrics

| role | avg coherence Δ (score↔vector) | avg computed Δ vs B | avg band computed vs B (0-3) | avg expl. distance (0-1) | avg impact distance (0-1) | avg subseq. distance (0-1) | avg Hamming (0-8) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| agent | 1.40 | 3.53 | 0.00 | 0.17 | 0.28 | 0.06 | 2.67 |

**Legend**

- The estimated vector is rescored with the official FIRST CVSS 4.0 algorithm (macrovector + lookup table, `cvss` library).
- `coherence Δ` = |score declared by the agent − score its own vector actually produces| (the two outputs are independent, nothing forces them to agree).
- `computed Δ vs B` compares the recomputed score against the ground-truth pure base score — a vector distance in official score space.
- Severity distances are ordinal and normalized per metric group (0 = identical vector, 1 = every field at the opposite end of its scale).
- The subsequent-system triad SC/SI/SA is part of the required vector; its distance is scored only when the agent's estimate actually includes all three fields (older/legacy runs may lack them, shown as `n/a`).
- Hamming counts plainly differing fields among the 8 vulnerable-system metrics (n/a = older runs, recompute with `python -m utils.cvss_eval`).

### Vector detail (estimated vs. published)

| **CVE-2026-42459** — agent, rep 1 | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **H** |
| VI — Integrity Impact to the Vulnerable System | **L** | **N** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 3.1 / **5.1** | 7.7 |

| **CVE-2026-42459** — agent, rep 2 | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **H** |
| VI — Integrity Impact to the Vulnerable System | N | N |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | **L** | **N** |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 3.1 / **5.1** | 7.7 |

| **CVE-2026-42459** — agent, rep 3 | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **H** |
| VI — Integrity Impact to the Vulnerable System | N | N |
| VA — Availability Impact to the Vulnerable System | **L** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.1 / **5.3** | 7.7 |

### Unmatched findings — no GT CVE, ranked by recomputed score (triage order)

| # | score (from vector) | declared | function | task | role | rep | vector | details |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 6.9 | 4.1 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task8_vuln_udm_full_1A_agent_rep1_f1.md) |
| 2 | 5.3 | 4.0 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task8_vuln_udm_full_1A_agent_rep3_f1.md) |
| 3 | 5.3 | 4.0 | `ThreeLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task8_vuln_udm_full_1A_agent_rep3_f2.md) |
| 4 | 5.3 | 4.0 | `HandleSubscribe, HandleModify` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task8_vuln_udm_full_1A_agent_rep3_f3.md) |
| 5 | 5.1 | 3.1 | `TwoLayerPathHandlerFunc, ThreeLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task8_vuln_udm_full_1A_agent_rep1_f2.md) |
| 6 | 5.1 | 2.2 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task8_vuln_udm_full_1A_agent_rep2_f1.md) |
| 7 | 5.1 | 3.1 | `TwoLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task8_vuln_udm_full_1A_agent_rep2_f2.md) |

**Legend**

- One row per finding the agent reported that matched no ground-truth CVE — either a false positive, or a genuine extra vulnerability with no catalogued CVE. Never counted against the evaluation (design choice: this is the practical use case, findings worth a human's triage).
- `score (from vector)` = the recomputed score, official CVSS 4.0 math — sort key, most severe first.
- `declared` = the score the agent stated directly; diagnostic only (see note above, not produced from the vector).
- `function` = the Go function the agent pointed to as the vulnerability's location.
- `task` / `role` = which task and role produced this finding.
- `rep` = repetition index (1-based) — which run of that task/role produced this finding.
- `vector` = the full CVSS 4.0 vector string the agent estimated.
- `details` = link to a self-contained file with this finding's structured data plus the agent's full narrative for that repetition (function name bolded for quick scanning) — everything needed to review it without opening the raw JSON.


---

## Rubric evaluation (Blocco A, LLM judge)

### Summary

| metric | value |
| --- | --- |
| total results | 3 |
| correct | 3 (100.0%) |
| wrong | 0 |
| retried (attempts > 1) | 0 |
| truly inconsistent tasks | 1 |
| surface-only differences (semantically equiv.) | 0 |

**Legend**

- `truly inconsistent` = LLM confirmed different conclusions across repetitions.
- `surface-only` = string-different but semantically equivalent (paraphrases, same logic).

### Scores by role

| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_textual_norm |
| --- | --- | --- | --- | --- | --- |
| agent | 100.0% | 0.900 | 0.0100 | 1.00 | 0.778 |

**Legend**

| metric | scope | meaning |
| --- | --- | --- |
| `accuracy` | all | share of repetitions with verdict = correct |
| `avg_confidence` | all | mean self-reported confidence (0–1) |
| `brier_score` | all | mean((confidence − is\_correct)²) — calibration error; 0 = perfect, 0.5 = poor; note: depends on both accuracy AND confidence (e.g., 100% accuracy + 50% confidence = 0.25) |
| `avg_attempts` | all | mean LLM call attempts per repetition (>1 means retry was triggered) |
| `avg_math_delta` | math | mean \|answer − ground\_truth\| on math tasks — lower = more precise |
| `avg_textual_norm` | textual | mean normalized judge score (0–1) — higher = better rubric coverage |

### Anomalies

#### Truly inconsistent reasoning (1)

**agent — task8_vuln_udm_full**
> The third reasoning identifies an additional 'Information Leakage' vulnerability not mentioned in the others, and the three reasonings disagree on the specific location and nature of the routing/parameter logic error (comparing TwoLayer vs ThreeLayer and strings.Contains vs manual slice manipulation).

**rep 1:**

1. **Improper Input Validation (Missing SUPI Validation):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`.
   - **Pattern:** These functions retrieve the `supi` parameter from the URL path (`c.Params.ByName("supi")`) but fail to call `validator.IsValidSupi(supi)` before passing it to the processor. In contrast, `HandleGetAmData` correctly implements this check.
   - **Impact:** While the SBI is protected by mTLS/OAuth2, an authorized but compromised NF (or a malicious internal actor) could send malformed SUPIs. This could lead to unexpected behavior in the `Processor` layer, potential database query errors, or logic bypasses if the processor assumes the input is already validated.
   - **Fix:** Add the `validator.IsValidSupi(supi)` check at the beginning of each handler.

2. **Unsafe JSON Unmarshaling (Potential Denial of Service):**
   - **Location:** `getPlmnIDStruct`.
   - **Pattern:** The code takes a string directly from a query parameter (`plmn-id`) and passes it to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact:** Query parameters can be manipulated to send very large or deeply nested JSON strings. Since `json.Unmarshal` is used on raw user input without length constraints, this could lead to excessive memory consumption or CPU spikes (DoS), affecting the availability of the UDM.
   - **Fix:** Implement a maximum length check for the `plmn-id` query parameter before attempting to unmarshal it.

3. **Inconsistent Parameter Handling (Logic Error/Potential Bypass):**
   - **Location:** `TwoLayerPathHandlerFunc` and `ThreeLayerPathHandlerFunc`.
   - **Pattern:** The code manually manipulates `c.Params` (e.g., `c.Params = append(c.Params, ...)` or `c.Params = tmpParams`).
   - **Impact:** Manually overriding the Gin context parameters is error-prone. If the routing logic in `OneLayerPathHandlerFunc` or `TwoLayerPathHandlerFunc` incorrectly matches a pattern, it might pass an incorrect `ueId` or `subscriptionId` to the handler. This could lead to unauthorized data access or modification of the wrong subscription if the `Processor` relies solely on these parameters.
   - **Fix:** Use a structured routing system (Gin's native router) instead of custom "Layer" handler functions that manually parse and re-assign parameters.

**rep 2:**

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
   - **Location:** `OneLayerPathHandlerFunc` and `TwoLayerPathHandlerFunc`
   - **Pattern:** The routing logic uses `strings.Contains(route.Pattern, supi)` to match routes.
   - **Impact:** `strings.Contains` is too permissive. If a `supi` value contains a substring that matches another route pattern, it may trigger the wrong handler. Furthermore, the manual manipulation of `c.Params` (e.g., `c.Params = append(...)` in `TwoLayerPathHandlerFunc`) is error-prone and can lead to parameter pollution or incorrect data being passed to the business logic.
   - **Fix:** Use a proper router (like Gin's built-in group routing) instead of manual string matching and parameter overriding.

**rep 3:**

1. **Improper Input Validation (Missing SUPI Validation):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`.
   - **Pattern:** These functions extract the `supi` parameter from the URL path (`c.Params.ByName("supi")`) but fail to call `validator.IsValidSupi(supi)` before passing it to the `Processor()`. In contrast, `HandleGetAmData` correctly performs this check.
   - **Impact:** While the SBI is protected by mTLS/OAuth2, an authorized but compromised NF (or a malicious internal actor) could send malformed SUPIs to the UDM. This could lead to unexpected behavior in the backend processor, potential database query errors, or logic bypasses if the processor assumes the input is already validated.
   - **Fix:** Implement `if !validator.IsValidSupi(supi) { ... return }` at the start of each handler that accepts a SUPI.

2. **Unsafe JSON Unmarshaling (Potential DoS/Resource Exhaustion):**
   - **Location:** `getPlmnIDStruct`
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


