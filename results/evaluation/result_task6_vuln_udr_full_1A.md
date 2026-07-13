# 1A — task6_vuln_udr_full

> **Run(s) in this report:**
> - `agent`: 20260712T142416Z

## CVSS estimate (Blocco B, deterministic)

| role | estimates | matched | missed CVEs | unmatched findings | avg band vs published (0-3) | avg band vs B (0-3) | avg exploitability (0-5) | avg impact (0-3) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent | 3/3 | 2 | 16 | 10 | 1.00 | 1.00 | 4.00 | 2.00 |

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
| agent | 2.10 | 0.10 | 3.00 | 0.15 | 0.17 | 0.00 | 2.00 |

**Legend**

- The estimated vector is rescored with the official FIRST CVSS 4.0 algorithm (macrovector + lookup table, `cvss` library).
- `coherence Δ` = |score declared by the agent − score its own vector actually produces| (the two outputs are independent, nothing forces them to agree).
- `computed Δ vs B` compares the recomputed score against the ground-truth pure base score — a vector distance in official score space.
- Severity distances are ordinal and normalized per metric group (0 = identical vector, 1 = every field at the opposite end of its scale).
- The subsequent-system triad SC/SI/SA is part of the required vector; its distance is scored only when the agent's estimate actually includes all three fields (older/legacy runs may lack them, shown as `n/a`).
- Hamming counts plainly differing fields among the 8 vulnerable-system metrics (n/a = older runs, recompute with `python -m utils.cvss_eval`).

### Vector detail (estimated vs. published)

| **CVE-2026-40249** — agent, rep 1 | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **H** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.5 / **6.9** | 6.9 |

| **CVE-2026-40249** — agent, rep 3 | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | **H** | **L** |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **7.1** | 6.9 |

### Unmatched findings — no GT CVE, ranked by recomputed score (triage order)

| # | score (from vector) | declared | function | task | role | rep | vector | details |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 8.7 | 7.1 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task6_vuln_udr_full_1A_agent_rep3_f1.md) |
| 2 | 8.6 | 7.1 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task6_vuln_udr_full_1A_agent_rep2_f1.md) |
| 3 | 7.1 | 5.3 | `HandlePolicyDataUesUeIdSmDataGet, HandleQuerySmData` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task6_vuln_udr_full_1A_agent_rep2_f2.md) |
| 4 | 7.1 | 5.3 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task6_vuln_udr_full_1A_agent_rep3_f2.md) |
| 5 | 6.9 | 4.5 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task6_vuln_udr_full_1A_agent_rep1_f1.md) |
| 6 | 6.9 | 4.1 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task6_vuln_udr_full_1A_agent_rep1_f2.md) |
| 7 | 5.3 | 4.0 | `HandleCreateEeSubscriptions, HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N` | [detail](unmatched_findings/task6_vuln_udr_full_1A_agent_rep2_f3.md) |
| 8 | 5.3 | 4.0 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task6_vuln_udr_full_1A_agent_rep2_f4.md) |
| 9 | 5.3 | 3.1 | `HandleCreateEeSubscriptions, HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task6_vuln_udr_full_1A_agent_rep3_f3.md) |
| 10 | 5.1 | 2.7 | `HandleCreateEeSubscriptions, HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task6_vuln_udr_full_1A_agent_rep1_f3.md) |

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
| correct | 0 (0.0%) |
| wrong | 3 |
| retried (attempts > 1) | 3 |
| truly inconsistent tasks | 1 |
| surface-only differences (semantically equiv.) | 0 |

**Legend**

- `truly inconsistent` = LLM confirmed different conclusions across repetitions.
- `surface-only` = string-different but semantically equivalent (paraphrases, same logic).

### Scores by role

| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_textual_norm |
| --- | --- | --- | --- | --- | --- |
| agent | 0.0% | 0.950 | 0.9042 | 3.00 | 0.481 |

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

#### Wrong verdicts (3)

| role | task_id | rep | attempts | confidence | score/delta |
| --- | --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 1 | 3 | 0.900 | 4.0 |
| agent | task6_vuln_udr_full | 2 | 3 | 1.000 | 5.0 |
| agent | task6_vuln_udr_full | 3 | 3 | 0.950 | 4.0 |

**Legend**

- `rep` = repetition index (1-based).
- `attempts` = total LLM calls (all failed).
- `confidence` = agent self-reported confidence on the final answer.
- `score/delta` = normalized rubric score (textual) or |answer − ground_truth| (math).

#### Retries triggered (3)

| role | task_id | rep | attempts | final_verdict |
| --- | --- | --- | --- | --- |
| agent | task6_vuln_udr_full | 1 | 3 | wrong |
| agent | task6_vuln_udr_full | 2 | 3 | wrong |
| agent | task6_vuln_udr_full | 3 | 3 | wrong |

**Legend**

- Each row is one repetition.
- `rep` = repetition index (1-based).
- `attempts` = LLM calls within that repetition (2 means wrong on attempt 1, correct on attempt 2).
- `final_verdict` = outcome after all attempts.

#### Truly inconsistent reasoning (1)

**agent — task6_vuln_udr_full**
> The three reasonings differ in their identification of vulnerabilities: the second reasoning identifies a DoS via unbounded JSON unmarshaling in `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`, which is absent in the first and third, and the first and third reasonings identify an improper deserialization issue that the second one ignores.

**rep 1:**

1. **Improper Deserialization (Nil Pointer/Logic Error)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the variable `policyDataSubscription` is declared as a value (`var policyDataSubscription models.PolicyDataSubscription`). It is then passed to `openapi.Deserialize(policyDataSubscription, ...)` without the address-of operator (`&`). In Go, passing a value to a function expecting an interface for deserialization (which typically requires a pointer to modify the underlying object) results in the object remaining empty. The `Processor` then receives a zero-valued struct, leading to data loss or corrupted database entries.

2. **Logic Error (Incorrect Collection Mapping)**: In `HandleCreateSdmSubscriptions`, the `collName` is hardcoded as `"subscriptionData.contextData.amfNon3gppAccess"`. This is a critical logic error as the handler is specifically for SDM (Subscription Data Management) subscriptions. Storing this data in the AMF Non-3GPP access collection will cause the data to be misplaced, making it unreachable by the correct query handlers and potentially corrupting AMF-specific records.

3. **Ineffective Input Validation (Regex Bypass)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regex used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The inclusion of `.+` as the final alternative makes the entire regex match any string of length 1 or more. This renders the specific 3GPP format validations useless, allowing arbitrary strings to be processed as `ueId`.

4. **Potential NoSQL Query Manipulation/DoS**: In `HandleApplicationDataInfluenceDataGet`, parameters such as `influence-Ids`, `dnns`, and `supis` are taken from the query string, split by commas, and passed directly into a `$in` operator in a MongoDB filter. While the driver prevents traditional injection, the lack of length limits on the resulting slices allows a malicious NF to send thousands of IDs in a single request, potentially causing high CPU/Memory usage on the MongoDB instance (Resource Exhaustion/DoS).

**rep 2:**

1. **Logic Error (Incorrect Collection Mapping)**:
   - **Location**: `HandleCreateSdmSubscriptions`
   - **Pattern**: The handler explicitly sets `collName := "subscriptionData.contextData.amfNon3gppAccess"`.
   - **Impact**: This is a severe logic error. Data intended for SDM subscriptions is stored in the AMF Non-3GPP access collection. This results in data corruption and loss of data integrity, as the UDR will fail to retrieve SDM subscriptions via the correct query paths, and the AMF context collection will be polluted with unrelated data.
   - **Fix**: Change `collName` to the correct SDM subscription collection path (e.g., `subscriptionData.sdmSubscriptions`).

2. **Improper Input Validation (Regex Bypass)**:
   - **Location**: `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`
   - **Pattern**: The regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` contains a trailing `.+` alternative.
   - **Impact**: The `.+` matches any string of length 1 or more, rendering all previous specific format checks (IMSI, MSISDN, etc.) irrelevant. This allows any arbitrary string to be accepted as a `ueId`. While mTLS restricts the attacker to a compromised NF, this allows for database pollution and potential exploitation of downstream NFs that expect strictly formatted 3GPP identifiers.
   - **Fix**: Remove the `.+` alternative from the regular expression to enforce strict validation.

3. **Denial of Service (Unbounded JSON Unmarshaling)**:
   - **Location**: `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`
   - **Pattern**: Query parameters `snssai` and `single-nssai` are passed directly to `json.Unmarshal` without length validation.
   - **Impact**: A compromised NF can send an extremely large or deeply nested JSON string in the URL. This can lead to excessive memory consumption or CPU exhaustion (algorithmic complexity attack) during unmarshaling, causing a Denial of Service (DoS) of the UDR.
   - **Fix**: Implement a strict maximum length limit on the query parameter string before attempting to unmarshal it.

4. **NoSQL Injection / Query Manipulation**:
   - **Location**: `HandleApplicationDataInfluenceDataGet`
   - **Pattern**: Query parameters (`influence-Ids`, `dnns`, `internal-Group-Id`, `supis`) are split by commas and inserted directly into `bson.M` filters using `$in` and `$or`.
   - **Impact**: Although the MongoDB Go driver prevents classic string-concatenation injection, the lack of value validation allows a compromised NF to perform "Query Manipulation." By providing unexpected values, an attacker can broaden the query scope to retrieve influence data for UEs or groups they should not have access to, violating the principle of least privilege.
   - **Fix**: Validate that each element resulting from the `strings.Split` operation conforms to the expected 3GPP format before adding it to the BSON filter.

**rep 3:**

1. **Logic Error (Incorrect Collection Mapping)**: In `HandleCreateSdmSubscriptions`, the `collName` is explicitly set to `"subscriptionData.contextData.amfNon3gppAccess"`. This is a critical mapping error. SDM subscriptions should be stored in their own dedicated collection. By writing to the AMF Non-3GPP access collection, the UDR will corrupt AMF context data and store SDM data in the wrong location, leading to functional failure of both the SDM and AMF context services.

2. **Improper Deserialization (Pass-by-Value)**: In `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`, the code calls `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")`. In Go, `policyDataSubscription` is a struct passed by value. The `Deserialize` function cannot populate the original variable. As a result, the processor receives an empty/zero-initialized struct, leading to the creation or update of empty records in the database.

3. **Input Validation Bypass (Permissive Regex)**: In `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`, the regular expression used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`. The final alternative `.+` matches any character one or more times. This effectively nullifies all previous specific 3GPP format constraints, allowing any arbitrary string to be accepted as a valid `ueId`.

4. **Potential Denial of Service (Resource Exhaustion)**: In `HandleApplicationDataInfluenceDataGet`, the code takes query parameters (e.g., `influence-Ids`, `dnns`) and performs `strings.Split(param[0], ",")` without limiting the number of elements. A malicious or malfunctioning NF could send a very large comma-separated list, leading to high memory consumption and potentially crashing the UDR process via an OOM (Out of Memory) event or causing a database performance collapse due to an oversized `$in` query.


