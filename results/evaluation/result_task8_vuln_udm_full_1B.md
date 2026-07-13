# 1B — task8_vuln_udm_full

> **Run(s) in this report:**
> - `agent`: 20260712T142416Z

## CVSS estimate (Blocco B, deterministic)

| role | estimates | matched | missed CVEs | unmatched findings | avg band vs published (0-3) | avg band vs B (0-3) | avg exploitability (0-5) | avg impact (0-3) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent | 3/3 | 3 | 0 | 7 | 0.67 | 0.00 | 4.00 | 0.33 |

- `estimates` = X/Y — X = repetitions where the agent emitted *at least one* CVSS finding block; Y = total repetitions evaluated for this task. **This is block presence, not correctness** — it says nothing about how many vulnerabilities were actually found or matched (see `matched`/`missed CVEs` below for that).
- `matched` = total findings, summed across all repetitions, successfully paired to a ground-truth CVE (by comparing the function name the agent reported to that CVE's known handler function).
- `missed CVEs` = total ground-truth CVEs, summed across all repetitions, that no finding in that repetition matched — i.e. vulnerabilities the agent failed to surface at all.
- `unmatched findings` = total findings, summed across all repetitions, that matched no ground-truth CVE — either a false positive, or a genuine extra vulnerability with no catalogued CVE (ranked for triage in the table further down).
- ⚠️ **The remaining four columns are diagnostic only, not the headline metric**: `avg band vs published` / `avg band vs B` score how close the *declared* score is to the reference (0 = far, 3 = exact band), and `avg exploitability` (0-5) / `avg impact` (0-3) count binary field matches on the estimated vector. The declared score is produced independently of the vector the agent also emits and carries no official rigor of its own (F17: systematically lower than what the vector is actually worth). These four columns exist only for comparability with runs 1-3.
- The metrics that actually count — recomputed from the vector with the official CVSS 4.0 algorithm — are in the table below.

### Official CVSS 4.0 math (score recomputed from the estimated vector) — the reference metrics

| role | avg coherence Δ (score↔vector) | avg computed Δ vs B | avg band computed vs B (0-3) | avg expl. distance (0-1) | avg impact distance (0-1) | avg subseq. distance (0-1) | avg Hamming (0-8) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| agent | 0.40 | 3.47 | 0.00 | 0.13 | 0.44 | 0.00 | 3.67 |

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
| VA — Availability Impact to the Vulnerable System | **L** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.1 / **5.1** | 7.7 |

| **CVE-2026-42459** — agent, rep 2 | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **H** |
| VI — Integrity Impact to the Vulnerable System | **L** | **N** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 7.7 |

| **CVE-2026-42459** — agent, rep 3 | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **H** |
| VI — Integrity Impact to the Vulnerable System | **L** | **N** |
| VA — Availability Impact to the Vulnerable System | **L** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.1 / **5.3** | 7.7 |

### Unmatched findings — no GT CVE, ranked by recomputed score (triage order)

| # | score (from vector) | declared | function | task | role | rep | vector |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5.3 | 4.1 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 2 | 5.3 | 4.1 | `HandleSubscribe (and others returning raw errors)` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 3 | 5.3 | 3.1 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 4 | 5.3 | 3.1 | `HandleSubscribe, HandleModify, HandleSubscribeToSharedData, HandleModifyForSharedData` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 5 | 5.1 | 2.3 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 6 | 5.1 | 4.1 | `HandleSubscribe` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 7 | 5.1 | 3.0 | `getPlmnIDStruct, HandleSubscribeToSharedData, HandleSubscribe, HandleModify, HandleModifyForSharedData` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |

- One row per finding the agent reported that matched no ground-truth CVE — either a false positive, or a genuine extra vulnerability with no catalogued CVE. Never counted against the evaluation (design choice: this is the practical use case, findings worth a human's triage).
- `score (from vector)` = the recomputed score, official CVSS 4.0 math — sort key, most severe first.
- `declared` = the score the agent stated directly; diagnostic only (see note above, not produced from the vector).
- `function` = the Go function the agent pointed to as the vulnerability's location.
- `task` / `role` = which task and role produced this finding.
- `rep` = repetition index (1-based) — which run of that task/role produced this finding; cross-reference the raw result JSON with `task`+`role`+`rep`.
- `vector` = the full CVSS 4.0 vector string the agent estimated.
- Full raw data in each result JSON under `cvss_eval.unmatched` (and the original agent output in `final_answer.cvss_estimate.findings`).


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

_truly inconsistent_: LLM confirmed different conclusions across repetitions. _surface-only_: string-different but semantically equivalent (paraphrases, same logic).

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
> The three reasonings identify different sets of vulnerabilities: the first focuses on inconsistent UE ID validation in HandleSubscribe, the second identifies a logic error in ThreeLayerPathHandlerFunc, and the third identifies redundant query parameter handling logic.

- **rep 1:** 1. **Improper Input Validation (Missing SUPI Validation):**    - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`.    - **Pattern:** These functions extract the `supi` parameter from the URL path (`c.Params.ByName("supi")`) but fail to call `validator.IsValidSupi(supi)` before passing it to the `Processor` layer. In contrast, `HandleGetAmData` correctly implements this check.    - **Impact:** While the SBI is protected by mTLS/OAuth2, an authorized but compromised NF (or a malicious internal actor) could send malformed SUPIs. This may lead to unexpected behavior in the database layer, potential injection attacks if the processor doesn't sanitize inputs, or crashes (DoS) in the backend logic.    - **Fix:** Add `if !validator.IsValidSupi(supi) { ... return }` blocks to all handlers that accept a SUPI.  2. **Unsafe JSON Unmarshaling of User Input (Potential DoS/Resource Exhaustion):**    - **Location:** `getPlmnIDStruct`    - **Pattern:** The code takes a query parameter `plmn-id` and passes it directly to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.    - **Impact:** Query parameters are typically short, but an attacker could send a very large string in the `plmn-id` parameter. Since `json.Unmarshal` is used on a byte slice derived from a URL query, it can lead to high CPU/memory consumption. Furthermore, the logic expects a JSON object in a query string, which is an unconventional and fragile pattern.    - **Fix:** Validate the length of the `plmn-id` string before unmarshaling and consider using a standard key-value format instead of JSON within a URL query parameter.  3. **Inconsistent Parameter Validation (UE ID):**    - **Location:** `HandleUnsubscribe`, `HandleModify`, `HandleGetIdTranslationResult`.    - **Pattern:** These functions validate `ueId` using `validator.IsValidGpsi(ueId) || validator.IsValidSupi(ueId)`. However, `HandleSubscribe` (which also takes a SUPI in the path) does **not** perform this validation.    - **Impact:** Inconsistency in security posture. `HandleSubscribe` allows any string to be passed as a SUPI to the processor, potentially bypassing business logic constraints.    - **Fix:** Implement the same `IsValidGpsi` / `IsValidSupi` check in `HandleSubscribe`.  4. **Information Leakage via Error Messages:**    - **Location:** `getPlmnIDStruct`, `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.    - **Pattern:** The code returns `err.Error()` directly to the client in the `ProblemDetails` response (e.g., `Reason: err.Error()` or `Detail: err.Error()`).    - **Impact:** Returning raw Go error messages from `json.Unmarshal` or `openapi.Deserialize` can leak internal implementation details, library versions, or structural information about the expected data models to a calling NF.    - **Fix:** Use generic error messages for the client (e.g., "Invalid request body") and log the detailed error internally.

- **rep 2:** 1. **Improper Input Validation (Missing SUPI Validation):**    - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`.    - **Pattern:** These functions retrieve the `supi` parameter from the URL path (`c.Params.ByName("supi")`) but fail to call `validator.IsValidSupi(supi)` before passing it to the processor. In contrast, `HandleGetAmData` correctly implements this check.    - **Impact:** While the SBI is protected by mTLS/OAuth2, allowing malformed or oversized SUPI strings to reach the processor/database layer can lead to unexpected behavior, potential injection attacks in the backend storage, or DoS via resource exhaustion if the validator was intended to limit input length.    - **Fix:** Implement `if !validator.IsValidSupi(supi) { ... return }` at the start of every handler that accepts a SUPI.  2. **Unsafe JSON Unmarshaling (Potential DoS/Resource Exhaustion):**    - **Location:** `getPlmnIDStruct`.    - **Pattern:** The code takes a query parameter `plmn-id` and directly passes it to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.    - **Impact:** Since query parameters can be large, an attacker (compromised NF) could send a deeply nested or massive JSON string. While `json.Unmarshal` in Go is relatively safe, repeated large allocations in a high-throughput UDM can lead to memory exhaustion (DoS).    - **Fix:** Validate the length of the `plmn-id` string before attempting to unmarshal it.  3. **Logic Error / Parameter Mismatch (Incorrect Parameter Mapping):**    - **Location:** `ThreeLayerPathHandlerFunc`.    - **Pattern:** For the `sdm-subscriptions` route, the code maps `c.Param("supi")` to `ueId` and `c.Param("thirdLayer")` to `subscriptionId`. However, the route definition in the comments and logic suggests a structure where `supi` is the first segment. If the routing is inconsistent with the handler's expectations, it leads to 404s or incorrect data access.    - **Impact:** Functional instability. If a request is routed incorrectly, the UDM may fail to process legitimate subscription modifications or deletions.    - **Fix:** Standardize the parameter naming in the Gin router and the handler functions to ensure consistency.  4. **Information Exposure (Verbose Error Messages):**    - **Location:** `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.    - **Pattern:** The code returns `err.Error()` from `c.GetRawData()` or `openapi.Deserialize` directly in the `ProblemDetails.Detail` field.    - **Impact:** This can leak internal system details, library versions, or memory addresses to a calling NF, aiding an attacker in reconnaissance.    - **Fix:** Use generic error messages for internal failures (e.g., "Internal Server Error") and log the detailed error internally.

- **rep 3:** 1. **Missing Input Validation (SUPI/UEID):**    - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`.    - **Pattern:** These functions extract the `supi` parameter from the URL path (`c.Params.ByName("supi")`) but fail to call `validator.IsValidSupi(supi)` before passing it to the processor. In contrast, `HandleGetAmData` and `HandleUnsubscribe` correctly implement this check.    - **Impact:** While the SBI is protected by mTLS/OAuth2, allowing malformed SUPIs into the business logic layer can lead to unexpected behavior in the database queries or downstream processors (e.g., injection if the processor doesn't sanitize inputs), potentially causing Denial of Service (DoS) or data leakage if the backend treats malformed IDs as wildcards.    - **Fix:** Implement `if !validator.IsValidSupi(supi) { ... return }` at the start of each handler.  2. **Unsafe JSON Unmarshaling of User-Controlled Query Parameters:**    - **Location:** `getPlmnIDStruct`    - **Pattern:** The code takes a raw string from the `plmn-id` query parameter and passes it directly to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.    - **Impact:** This is a dangerous pattern. An attacker (or a compromised NF) can send a specially crafted JSON string in the query parameter. While `models.PlmnId` is likely a simple struct, this pattern is prone to "JSON injection" or resource exhaustion if the parser is stressed. More importantly, it violates the expected 3GPP REST API design where `plmn-id` is typically a simple string or a specific format, not a JSON blob embedded in a URL query.    - **Fix:** Use standard query parameter parsing or a strict schema validator instead of `json.Unmarshal` on raw URL query values.  3. **Inconsistent Parameter Handling (Logic Error):**    - **Location:** `HandleGetAmData`, `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`.    - **Pattern:** The code creates a `url.Values` object (`query := url.Values{}`) and manually sets values from `c.Query()`, but then calls `s.getPlmnIDStruct(c.Request.URL.Query())`.    - **Impact:** This is redundant and confusing logic. It doesn't directly create a security hole but indicates a lack of input sanitization consistency, increasing the risk of "Parameter Pollution" where different parts of the application interpret the query string differently.    - **Fix:** Use a single source of truth for query parameters (either `c.Request.URL.Query()` or Gin's `c.Query()`).  4. **Improper Error Detail Leakage:**    - **Location:** `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.    - **Pattern:** The code returns `err.Error()` directly in the `ProblemDetails.Detail` field when `openapi.Deserialize` or `c.GetRawData()` fails.    - **Impact:** Returning raw internal error messages to the caller can leak implementation details about the underlying libraries, data structures, or the state of the system, aiding an attacker in reconnaissance.    - **Fix:** Use generic error messages for the client and log the detailed error internally.


