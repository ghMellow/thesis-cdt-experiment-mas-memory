# 1A — task5_vuln_pcf

> **Run(s) in this report:**
> - `agent`: 20260712T142416Z

<a id="toc"></a>
**Contents**

- [Vector detail (estimated vs. published)](#vector-detail)
- [Unmatched findings](#unmatched-findings)
- [Aggregate metrics (across repetitions)](#aggregate-metrics)
  - [Estimates vs ground truth](#estimates-vs-gt)
  - [Official CVSS 4.0 math](#official-cvss-math)
- [Rubric evaluation](#rubric-evaluation)
  - [Summary](#rubric-summary)
  - [Scores by role](#rubric-scores)
  - [Anomalies](#rubric-anomalies)

<a id="cvss-estimate"></a>
## CVSS estimate (Blocco B, deterministic)

<a id="vector-detail"></a>
### Vector detail (estimated vs. published)

| **CVE-2026-41135** — agent, rep 1 | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | N | N |
| UI — User Interaction | **P** | **N** |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **N** |
| VI — Integrity Impact to the Vulnerable System | N | N |
| VA — Availability Impact to the Vulnerable System | **N** | **H** |
| SC — Confidentiality Impact to the Subsequent System | **L** | **N** |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.1 / **5.3** | 8.7 |

| **CVE-2026-41135** — agent, rep 2 | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | N | N |
| UI — User Interaction | **P** | **N** |
| VC — Confidentiality Impact to the Vulnerable System | **H** | **N** |
| VI — Integrity Impact to the Vulnerable System | N | N |
| VA — Availability Impact to the Vulnerable System | **N** | **H** |
| SC — Confidentiality Impact to the Subsequent System | **L** | **N** |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 6.2 / **7.1** | 8.7 |

| **CVE-2026-41135** — agent, rep 3 | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | N | N |
| UI — User Interaction | **P** | **N** |
| VC — Confidentiality Impact to the Vulnerable System | **H** | **N** |
| VI — Integrity Impact to the Vulnerable System | N | N |
| VA — Availability Impact to the Vulnerable System | **N** | **H** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **7.1** | 8.7 |

<a id="unmatched-findings"></a>
### Unmatched findings — no GT CVE, ranked by recomputed score (triage order)

| # | group | details | score (from vector) | declared | function | task | role | rep | vector |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | a | [detail](unmatched_findings/task5_vuln_pcf_1A_agent_rep2_f1.md) | 8.7 | 5.3 | `setCorsHeader` | task5_vuln_pcf | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 2 | a | [detail](unmatched_findings/task5_vuln_pcf_1A_agent_rep3_f1.md) | 8.7 | 7.1 | `setCorsHeader` | task5_vuln_pcf | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |

**Legend**

- One row per finding the agent reported that matched no ground-truth CVE — either a false positive, or a genuine extra vulnerability with no catalogued CVE. Never counted against the evaluation (design choice: this is the practical use case, findings worth a human's triage).
- `group` = a letter (a, b, c…) means same-letter rows are the same finding re-reported across repetitions (same function; identical vector, or an LLM-confirmed equivalent one). `≠` means the function recurred with a different vector and the LLM was asked and judged it a genuinely different finding, not a re-estimate. `—` means the function was seen only once — nothing to compare, no LLM call made. Grouping never removes or merges rows, it only labels them.
- `score (from vector)` = the recomputed score, official CVSS 4.0 math — sort key, most severe first.
- `declared` = the score the agent stated directly; diagnostic only (see note above, not produced from the vector).
- `function` = the Go function the agent pointed to as the vulnerability's location.
- `task` / `role` = which task and role produced this finding.
- `rep` = repetition index (1-based) — which run of that task/role produced this finding.
- `vector` = the full CVSS 4.0 vector string the agent estimated.
- `details` = link to a self-contained file with this finding's structured data plus the agent's full narrative for that repetition (function name bolded for quick scanning) — everything needed to review it without opening the raw JSON.

<a id="aggregate-metrics"></a>
### Aggregate metrics (across repetitions)

_Diagnostic roll-up, useful for a global read once you've checked the detail above isn't spitting nonsense — not the first thing to read._

<a id="estimates-vs-gt"></a>
#### Estimates vs ground truth

| role | estimates | matched | missed CVEs | unmatched findings | avg band vs published (0-3) | avg band vs B (0-3) | avg exploitability (0-5) | avg impact (0-3) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent | 3/3 | 3 | 0 | 2 | 0.33 | 0.33 | 4.00 | 1.00 |

**Legend**

- `estimates` = X/Y — X = repetitions where the agent emitted *at least one* CVSS finding block; Y = total repetitions evaluated for this task. **This is block presence, not correctness** — it says nothing about how many vulnerabilities were actually found or matched (see `matched`/`missed CVEs` below for that).
- `matched` = total findings, summed across all repetitions, successfully paired to a ground-truth CVE (by comparing the function name the agent reported to that CVE's known handler function).
- `missed CVEs` = total ground-truth CVEs, summed across all repetitions, that no finding in that repetition matched — i.e. vulnerabilities the agent failed to surface at all.
- `unmatched findings` = total findings, summed across all repetitions, that matched no ground-truth CVE — either a false positive, or a genuine extra vulnerability with no catalogued CVE (ranked for triage in the table further down).
- ⚠️ **The remaining four columns are diagnostic only, not the headline metric**: `avg band vs published` / `avg band vs B` score how close the *declared* score is to the reference (0 = far, 3 = exact band), and `avg exploitability` (0-5) / `avg impact` (0-3) count binary field matches on the estimated vector. The declared score is produced independently of the vector the agent also emits and carries no official rigor of its own (F17: systematically lower than what the vector is actually worth). These four columns exist only for comparability with runs 1-3.
- The metrics that actually count — recomputed from the vector with the official CVSS 4.0 algorithm — are in the table below.

<a id="official-cvss-math"></a>
#### Official CVSS 4.0 math (score recomputed from the estimated vector) — the reference metrics

| role | avg coherence Δ (score↔vector) | avg computed Δ vs B | avg band computed vs B (0-3) | avg expl. distance (0-1) | avg impact distance (0-1) | avg subseq. distance (0-1) | avg Hamming (0-8) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| agent | 1.30 | 2.20 | 0.67 | 0.10 | 0.61 | 0.11 | 3.00 |

**Legend**

- The estimated vector is rescored with the official FIRST CVSS 4.0 algorithm (macrovector + lookup table, `cvss` library).
- `coherence Δ` = |score declared by the agent − score its own vector actually produces| (the two outputs are independent, nothing forces them to agree).
- `computed Δ vs B` compares the recomputed score against the ground-truth pure base score — a vector distance in official score space.
- Severity distances are ordinal and normalized per metric group (0 = identical vector, 1 = every field at the opposite end of its scale).
- The subsequent-system triad SC/SI/SA is part of the required vector; its distance is scored only when the agent's estimate actually includes all three fields (older/legacy runs may lack them, shown as `n/a`).
- Hamming counts plainly differing fields among the 8 vulnerable-system metrics (n/a = older runs, recompute with `python -m utils.cvss_eval`).


---

<a id="rubric-evaluation"></a>
## Rubric evaluation (Blocco A, LLM judge)

<a id="rubric-summary"></a>
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

<a id="rubric-scores"></a>
### Scores by role

| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_textual_norm |
| --- | --- | --- | --- | --- | --- |
| agent | 100.0% | 0.983 | 0.0008 | 1.00 | 1.000 |

**Legend**

| metric | scope | meaning |
| --- | --- | --- |
| `accuracy` | all | share of repetitions with verdict = correct |
| `avg_confidence` | all | mean self-reported confidence (0–1) |
| `brier_score` | all | mean((confidence − is\_correct)²) — calibration error; 0 = perfect, 0.5 = poor; note: depends on both accuracy AND confidence (e.g., 100% accuracy + 50% confidence = 0.25) |
| `avg_attempts` | all | mean LLM call attempts per repetition (>1 means retry was triggered) |
| `avg_math_delta` | math | mean \|answer − ground\_truth\| on math tasks — lower = more precise |
| `avg_textual_norm` | textual | mean normalized judge score (0–1) — higher = better rubric coverage |

<a id="rubric-anomalies"></a>
### Anomalies

#### Truly inconsistent reasoning (1)

**agent — task5_vuln_pcf**
> The first reasoning only identifies the CORS misconfiguration and the middleware memory leak, whereas the second and third reasonings also identify a third vulnerability regarding lack of input validation/sanitization for the SUPI parameter.

**rep 1:**

The code contains a critical **CORS (Cross-Origin Resource Sharing) Misconfiguration**. 

1. **Vulnerability Class:** CORS Misconfiguration / Overly Permissive Policy.
2. **Location:** `setCorsHeader` function.
3. **Analysis:** 
    - The code uses `AllowAllOrigins: true` and explicitly sets `Access-Control-Allow-Origin: "*"`.
    - Simultaneously, it sets `AllowCredentials: true` and `Access-Control-Allow-Credentials: "true"`.
    - According to the CORS specification, the combination of `Allow-Origin: *` and `Allow-Credentials: true` is forbidden and insecure. Most modern browsers will block this, but if the server dynamically reflects the origin, it allows any website to make authenticated requests to the PCF.
    - Furthermore, the `setCorsHeader` function is called *inside* the request handler (`HTTPOAMGetAmPolicy`), but it calls `s.router.Use(...)`. In Gin, `router.Use` adds middleware globally to the router. Calling this inside a handler means every time the `/am-policy/:supi` endpoint is hit, a new instance of the CORS middleware is appended to the global middleware stack, leading to a **Memory Leak** and degraded performance (DoS).
4. **5G Context Impact:** The PCF handles sensitive subscriber policy data (AM Policy). While SBI is typically protected by mTLS/OAuth2, OAM interfaces are sometimes exposed to internal management networks. If a network administrator accesses a malicious website while logged into a management console, the browser could be used to exfiltrate subscriber policies (SUPI-linked data) via CSRF/CORS attacks.
5. **Proposed Fix:** 
    - Remove `setCorsHeader` from the request handler.
    - Move CORS configuration to the server initialization phase.
    - Replace `AllowAllOrigins: true` with a strict whitelist of trusted management domains.
    - Remove `AllowCredentials: true` unless explicitly required by a specific authentication mechanism.

**rep 2:**

1. **CORS Misconfiguration (Permissive Policy):**
   - **Location:** `setCorsHeader` function.
   - **Analysis:** The code implements an extremely permissive Cross-Origin Resource Sharing (CORS) policy. It sets `AllowAllOrigins: true` and explicitly sets the header `Access-Control-Allow-Origin: "*"`. Furthermore, it sets `AllowCredentials: true`. 
   - **5G Context Impact:** In a 5G Core, the SBI is intended for inter-NF communication. While SBI is typically protected by mTLS/OAuth2, if this OAM interface is exposed to a management network or a web-based dashboard, a permissive CORS policy allows any website visited by an administrator to make authenticated requests to the PCF. The combination of `AllowAllOrigins: true` and `AllowCredentials: true` is a critical security flaw that can lead to Cross-Site Request Forgery (CSRF) or unauthorized data extraction if the browser session is used for authentication.
   - **Fix:** Replace `AllowAllOrigins: true` and `"*"` with a strict whitelist of trusted management domains. Remove `AllowCredentials: true` unless explicitly required by a secure authentication mechanism.

2. **Inefficient/Incorrect Middleware Application:**
   - **Location:** `setCorsHeader` function.
   - **Analysis:** The function calls `s.router.Use(cors.New(...))` inside a request handler. In the Gin framework, `.Use()` attaches middleware to the router globally or for a group. Calling this inside a handler means the middleware is re-added to the router on every single request to `HTTPOAMGetAmPolicy`.
   - **5G Context Impact:** This leads to a memory leak and performance degradation (DoS) as the middleware chain grows indefinitely with every request. In a high-traffic 5G core, this could crash the PCF OAM handler, impacting the availability of policy management.
   - **Fix:** Move the CORS middleware configuration to the server initialization phase (e.g., in `getOamRoutes` or a dedicated setup function) so it is applied once at startup.

3. **Lack of Input Validation/Sanitization (Potential IDOR/Injection):**
   - **Location:** `HTTPOAMGetAmPolicy` function, line `supi := c.Params.ByName("supi")`.
   - **Analysis:** The `supi` (Subscription Permanent Identifier) is taken directly from the URL path and passed to the processor without any validation or sanitization.
   - **5G Context Impact:** While the processor might handle validation, the handler allows any string to be passed. If the underlying processor uses this value in a database query or log without escaping, it could lead to injection. More importantly, it facilitates Insecure Direct Object Reference (IDOR) if the OAM layer doesn't verify that the requester has the authority to access the policy of that specific SUPI.
   - **Fix:** Implement a regex check to ensure the `supi` conforms to the expected 3GPP format (numeric string) before passing it to the processor.

**rep 3:**

1. **CORS Misconfiguration (Permissive Policy):**
   - **Location:** `setCorsHeader` function.
   - **Analysis:** The code implements an extremely permissive Cross-Origin Resource Sharing (CORS) policy. It sets `AllowAllOrigins: true` and explicitly sets the `Access-Control-Allow-Origin` header to `*`. Furthermore, it sets `AllowCredentials: true`. 
   - **5G Context Impact:** In a 5G Core, the SBI is intended for inter-NF communication. While SBI is typically protected by mTLS/OAuth2, OAM interfaces are often accessed via management consoles. A permissive CORS policy combined with `AllowCredentials: true` is a dangerous combination; it allows any website visited by an administrator to make authenticated requests to the PCF OAM interface on behalf of the admin (Cross-Site Request Forgery/Data Exfiltration).
   - **Fix:** Replace `AllowAllOrigins: true` and `*` with a strict whitelist of trusted management domains. Remove `AllowCredentials: true` unless strictly necessary and paired with a specific origin.

2. **Inefficient/Incorrect Middleware Application:**
   - **Location:** `setCorsHeader` function.
   - **Analysis:** The function calls `s.router.Use(cors.New(...))` inside a request handler. In Gin, `.Use()` adds middleware to the router's global chain. Calling this inside a handler means every single request to the OAM endpoint adds a *new* instance of the CORS middleware to the router.
   - **5G Context Impact:** This leads to a memory leak and performance degradation (Availability). As the number of requests increases, the middleware chain grows indefinitely, eventually causing the PCF to crash or become unresponsive (DoS).
   - **Fix:** Move the CORS middleware configuration to the server initialization phase (e.g., in `getOamRoutes` or a separate setup function), not inside the request handler.

3. **Information Exposure / Lack of Input Validation:**
   - **Location:** `HTTPOAMGetAmPolicy` function.
   - **Analysis:** The `supi` (Subscription Permanent Identifier) is taken directly from the URL path and passed to the processor. While there is a check for an empty string, there is no validation of the SUPI format (e.g., length, numeric characters).
   - **5G Context Impact:** SUPI is a highly sensitive unique identifier. If the `HandleOAMGetAmPolicyRequest` does not perform strict authorization checks, an attacker with access to the OAM interface could enumerate SUPIs to extract policy information for arbitrary subscribers.
   - **Fix:** Implement strict regex validation for the `supi` parameter to ensure it conforms to 3GPP standards before processing.


