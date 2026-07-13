# 1B — task6_vuln_udr_full

> **Run(s) in this report:**
> - `agent`: 20260712T142416Z

## CVSS estimate (Blocco B, deterministic)

| role | estimates | matched | missed CVEs | unmatched findings | avg band vs published (0-3) | avg band vs B (0-3) | avg exploitability (0-5) | avg impact (0-3) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent | 3/3 | 3 | 15 | 9 | 1.67 | 1.67 | 4.00 | 1.67 |

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
| agent | 0.73 | 0.70 | 2.33 | 0.10 | 0.33 | 0.06 | 2.33 |

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
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | L | L |
| VA — Availability Impact to the Vulnerable System | **L** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | **L** | **N** |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 4.5 / **5.3** | 6.9 |

| **CVE-2026-40249** — agent, rep 2 | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **H** | **N** |
| VI — Integrity Impact to the Vulnerable System | L | L |
| VA — Availability Impact to the Vulnerable System | **H** | **N** |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 7.7 / **7.2** | 6.9 |

| **CVE-2026-40343** — agent, rep 3 | estimated | published |
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
| base score — declared / from vector (official math) | 6.2 / **7.1** | 6.9 |

### Unmatched findings — no GT CVE, ranked by recomputed score (triage order)

| # | score (from vector) | declared | function | task | role | rep | vector | details |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 8.6 | 6.8 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task6_vuln_udr_full_1B_agent_rep3_f1.md) |
| 2 | 8.3 | 7.1 | `HandleCreateSdmSubscriptions` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N` | [detail](unmatched_findings/task6_vuln_udr_full_1B_agent_rep2_f1.md) |
| 3 | 7.1 | 5.3 | `HandleCreateSmfContextNon3gpp` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:L/SA:N` | [detail](unmatched_findings/task6_vuln_udr_full_1B_agent_rep1_f1.md) |
| 4 | 7.1 | 7.1 | `HandlePolicyDataUesUeIdSmDataGet, HandleQuerySmData` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task6_vuln_udr_full_1B_agent_rep2_f2.md) |
| 5 | 7.1 | 6.2 | `HandlePolicyDataUesUeIdSmDataGet` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task6_vuln_udr_full_1B_agent_rep3_f2.md) |
| 6 | 5.3 | 5.1 | `HandleCreateEeSubscriptions / HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N` | [detail](unmatched_findings/task6_vuln_udr_full_1B_agent_rep1_f2.md) |
| 7 | 5.3 | 4.0 | `HandleApplicationDataInfluenceDataGet` | task6_vuln_udr_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` | [detail](unmatched_findings/task6_vuln_udr_full_1B_agent_rep1_f3.md) |
| 8 | 5.3 | 5.1 | `HandleCreateEeSubscriptions, HandleQueryeesubscriptions` | task6_vuln_udr_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N` | [detail](unmatched_findings/task6_vuln_udr_full_1B_agent_rep2_f3.md) |
| 9 | 5.3 | 4.0 | `HandleCreateEeSubscriptions` | task6_vuln_udr_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` | [detail](unmatched_findings/task6_vuln_udr_full_1B_agent_rep3_f3.md) |

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
| agent | 0.0% | 0.967 | 0.9350 | 3.00 | 0.444 |

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
| agent | task6_vuln_udr_full | 1 | 3 | 1.000 | 4.0 |
| agent | task6_vuln_udr_full | 2 | 3 | 0.950 | 4.0 |
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
> The three passages identify different sets of vulnerabilities: the first includes a NoSQL injection and an integer parsing error not mentioned in others, while the second and third identify a database collection logic error and a JSON unmarshaling DoS that the first misses.

**rep 1:**

1. **Improper Input Validation (Regex Bypass):**
   - **Location:** `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`.
   - **Pattern:** The regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` contains a final alternative `.+`.
   - **Impact:** The `.+` matches any character sequence, rendering all previous specific 3GPP format checks (IMSI, MSISDN, etc.) useless. Any non-empty string is accepted. While SBI is protected by mTLS/OAuth2, this allows a compromised NF to inject arbitrary strings into the UDR database, potentially causing downstream processing errors in other NFs that rely on strict 3GPP identity formats.
   - **Fix:** Remove the `.+` alternative from the regular expression.

2. **Incorrect API Usage (Deserialization Failure):**
   - **Location:** `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`.
   - **Pattern:** `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")` is called where `policyDataSubscription` is passed by value, not by reference.
   - **Impact:** In Go, deserialization functions require a pointer to modify the target variable. Passing a value results in the variable remaining empty/default. The UDR will store empty policy subscription data, leading to a Denial of Service (DoS) of the policy notification functionality for the affected UEs.
   - **Fix:** Pass the address of the variable: `openapi.Deserialize(&policyDataSubscription, reqBody, "application/json")`.

3. **Improper Error Handling (Logic Error/Data Corruption):**
   - **Location:** `HandleCreateSmfContextNon3gpp`.
   - **Pattern:** `pduSessionId, err := strconv.ParseInt(c.Param("pduSessionId"), 10, 64)` is followed by a log warning if `err != nil`, but the function continues execution.
   - **Impact:** If a non-integer value is provided in the URL, `pduSessionId` defaults to `0`. The UDR will then create or overwrite a session context with ID `0`. This can lead to data corruption and session collisions, where multiple PDU sessions are mapped to the same ID, disrupting connectivity for UEs.
   - **Fix:** Return a `http.StatusBadRequest` (400) if `strconv.ParseInt` fails.

4. **Potential NoSQL Injection/Information Disclosure:**
   - **Location:** `HandleApplicationDataInfluenceDataGet`.
   - **Pattern:** Query parameters like `influence-Ids` and `dnns` are split by commas and passed directly into BSON `$in` operators: `bson.M{"influenceId": bson.M{"$in": influenceIds}}`.
   - **Impact:** Although `$in` is safer than raw query injection, the lack of validation on the split elements allows an authorized NF to perform "blind" probing of the database. By iterating through possible IDs, a compromised NF can enumerate existing influence data or verify the existence of specific DNNs/SUPIs across the repository.
   - **Fix:** Implement strict validation (type, length, and character set) for each element in the slice before constructing the BSON filter.

**rep 2:**

1. **Improper Error Handling (Missing Return/Control Flow):**
   - **Location:** `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`.
   - **Pattern:** In both functions, the code checks for errors from `c.GetRawData()` and `openapi.Deserialize()`. If an error occurs, it sends a JSON response to the client, but it **fails to return** from the handler.
   - **Impact:** The execution continues to the `s.Processor()...Procedure()` call. Because the target object (`policyDataSubscription`) was not successfully populated, the processor will receive a zero-valued or nil object. This will likely cause a **panic (null pointer dereference)** in the processor layer or result in the insertion of corrupted/empty records into the MongoDB database, affecting the availability and integrity of the UDR.
   - **Fix:** Add `return` statements immediately after the `c.JSON()` calls in the error handling blocks.

2. **Logic Error (Incorrect Database Collection):**
   - **Location:** `HandleCreateSdmSubscriptions`.
   - **Pattern:** The variable `collName` is explicitly set to `"subscriptionData.contextData.amfNon3gppAccess"`.
   - **Impact:** This is a critical logic error. SDM (Subscription Data Management) subscription data is being written into the collection reserved for AMF Non-3GPP access. This causes **data cross-contamination** and ensures that the data cannot be retrieved by the correct query procedures, effectively breaking the SDM subscription functionality and polluting the AMF context data.
   - **Fix:** Correct `collName` to the appropriate SDM subscription collection (e.g., `"subscriptionData.sdmSubscriptions"`).

3. **Ineffective Input Validation (Regex Bypass):**
   - **Location:** `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`.
   - **Pattern:** The regex used to validate `ueId` is `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`.
   - **Impact:** The final alternative `.+` matches any character sequence of length 1 or more. This renders the entire regex useless as it accepts any non-empty string, bypassing all 3GPP-defined identifier constraints. While SBI is protected by mTLS, this allows a compromised NF to perform **database pollution** or potentially exploit downstream logic that expects a specific format.
   - **Fix:** Remove the `.+` alternative from the regular expression.

4. **Potential Denial of Service (Unsafe JSON Unmarshaling):**
   - **Location:** `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`.
   - **Pattern:** The code takes a query parameter (`snssai` or `single-nssai`) and passes it directly into `json.Unmarshal([]byte(queryParam), &target)`.
   - **Impact:** There is no limit on the size of the query parameter. An attacker (or compromised NF) could send a massive JSON string or a "JSON bomb" (deeply nested structures), leading to **excessive memory consumption or CPU exhaustion** during the unmarshaling process, causing a Denial of Service (DoS) for the UDR.
   - **Fix:** Implement a strict length limit on the query parameter before attempting to unmarshal it.

**rep 3:**

1. **Logic Error (Incorrect Database Collection)**:
   - **Location**: `HandleCreateSdmSubscriptions`
   - **Pattern**: The handler defines `collName := "subscriptionData.contextData.amfNon3gppAccess"`.
   - **Impact**: This is a severe logic error. Data intended for SDM (Subscription Data Management) subscriptions is written into the collection used for AMF Non-3GPP access. This results in data corruption for AMF contexts and failure to store SDM subscriptions, breaking core UDR functionality.
   - **Fix**: Update `collName` to the correct SDM subscription collection path.

2. **Improper Input Validation (Regex Bypass)**:
   - **Location**: `HandleCreateEeSubscriptions` and `HandleQueryeesubscriptions`
   - **Pattern**: The regex `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$` ends with `.+`.
   - **Impact**: The `.+` alternative matches any string of length 1 or more, rendering the entire regex validation useless. While SBI is protected by mTLS, this allows malformed identifiers to reach the database, potentially causing issues in the `Processor` layer or allowing the injection of non-compliant data.
   - **Fix**: Remove the `.+` alternative to enforce strict 3GPP identifier formats.

3. **Improper Error Handling (Nil Pointer/Value Copy Bug)**:
   - **Location**: `HandlePolicyDataSubsToNotifyPost` and `HandlePolicyDataSubsToNotifySubsIdPut`
   - **Pattern**: The code calls `openapi.Deserialize(policyDataSubscription, reqBody, "application/json")` instead of passing a pointer (`&policyDataSubscription`).
   - **Impact**: In Go, passing a struct by value to a deserialization function means the function operates on a copy. The original `policyDataSubscription` variable remains empty (zero-valued). Consequently, the `Processor` receives empty data, leading to the creation or update of corrupted/empty records in the database.
   - **Fix**: Pass the address of the variable: `openapi.Deserialize(&policyDataSubscription, ...)`

4. **Potential Denial of Service (Unsafe JSON Unmarshaling)**:
   - **Location**: `HandlePolicyDataUesUeIdSmDataGet` and `HandleQuerySmData`
   - **Pattern**: `json.Unmarshal([]byte(sNssaiQuery), &sNssai)` is called on a raw query parameter string.
   - **Impact**: An attacker (or compromised NF) can provide a massive or deeply nested JSON string in the `snssai` or `single-nssai` query parameter. This can lead to excessive memory consumption or CPU exhaustion during unmarshaling, causing a Denial of Service (DoS) of the UDR.
   - **Fix**: Implement a maximum length check on the query parameter before attempting to unmarshal.


