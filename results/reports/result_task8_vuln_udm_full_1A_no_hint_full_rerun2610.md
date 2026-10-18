# 1A_no_hint_full_rerun2610 — task8_vuln_udm_full

> **Run(s) in this report:**
> - `agent`: 20261016T123849Z

<a id="toc"></a>
**Contents**

- [Vector detail (estimated vs. published)](#vector-detail)
- [Unmatched findings](#unmatched-findings)
- [Metrics across repetitions](#metrics-across-reps)
  - [Detection (M1, M2, M3 — final answer vs first attempt)](#detection-metrics)
  - [CVE × repetition](#cve-rep-matrix)
  - [Detection delta by retry channel](#retry-channel)
  - [Detection × SGV conformity](#sgv-detection-cross)
  - [Severity (S1, S2, S3)](#severity-metrics)
  - [Legacy diagnostics (runs 1–3 comparability)](#legacy-diagnostics)
- [SGV — Syntactic Grounding Verifier](#sgv)
- [Rubric evaluation](#rubric-evaluation)
  - [Summary](#rubric-summary)
  - [Scores by role](#rubric-scores)
  - [Cost (M5)](#cost-metrics)
  - [Anomalies](#rubric-anomalies)

<a id="cvss-estimate"></a>
## CVSS estimate (Blocco B, deterministic)

<a id="vector-detail"></a>
### Vector detail (estimated vs. published)

_`group` letter (when present) = this CVE recurs — same letter on other matched reps and/or on rows of the unmatched table below (there it marks a finding on one of this CVE's handler functions: a probable duplicate to confirm in triage, not necessarily the same bug — see the unmatched legend)._

| **CVE-2026-42459** — agent, rep 1 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **H** |
| VI — Integrity Impact to the Vulnerable System | N | N |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep1_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 2 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **H** |
| VI — Integrity Impact to the Vulnerable System | N | N |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep2_CVE-2026-42459.md) | | |

| **CVE-2026-42459** — agent, rep 3 — group a | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | **L** | **N** |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | **L** | **H** |
| VI — Integrity Impact to the Vulnerable System | N | N |
| VA — Availability Impact to the Vulnerable System | N | N |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.3 / **5.3** | 7.7 |
| [reasoning detail](matched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep3_CVE-2026-42459.md) | | |

<a id="unmatched-findings"></a>
### Unmatched findings — no GT CVE, ranked by recomputed score (triage order)

| # | group | details | score (from vector) | declared | function | task | role | rep | vector |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep2_f1.md) | 7.1 | 5.3 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 2 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep1_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 3 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep1_f2.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 4 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep1_f3.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 5 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep1_f4.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 6 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep1_f5.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 7 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep1_f6.md) | 5.3 | 5.3 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 8 | b | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep1_f7.md) | 5.3 | 5.3 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 9 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep1_f8.md) | 5.3 | 5.3 | `HandleSubscribeToSharedData` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 10 | d | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep1_f9.md) | 5.3 | 5.3 | `HandleSubscribe` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 11 | e | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep1_f10.md) | 5.3 | 5.3 | `HandleModify` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 12 | f | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep1_f11.md) | 5.3 | 5.3 | `HandleModifyForSharedData` | task8_vuln_udm_full | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 13 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep2_f2.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 14 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep2_f3.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 15 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep2_f4.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 16 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep2_f5.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 17 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep2_f6.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 18 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep2_f7.md) | 5.3 | 5.3 | `HandleSubscribeToSharedData` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 19 | d | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep2_f8.md) | 5.3 | 5.3 | `HandleSubscribe` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 20 | e | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep2_f9.md) | 5.3 | 5.3 | `HandleModify` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 21 | f | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep2_f10.md) | 5.3 | 5.3 | `HandleModifyForSharedData` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 22 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep2_f11.md) | 5.3 | 5.3 | `OneLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 23 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep3_f1.md) | 5.3 | 5.3 | `HandleGetSupi` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 24 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep3_f2.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 25 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep3_f3.md) | 5.3 | 5.3 | `HandleGetUeContextInSmfData` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 26 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep3_f4.md) | 5.3 | 5.3 | `HandleGetNssai` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 27 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep3_f5.md) | 5.3 | 5.3 | `HandleGetSmData` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 28 | a | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep3_f6.md) | 5.3 | 5.3 | `HandleGetTraceData` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 29 | b | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep3_f7.md) | 5.3 | 5.3 | `getPlmnIDStruct` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 30 | c | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep3_f8.md) | 5.3 | 5.3 | `HandleSubscribeToSharedData` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 31 | d | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep3_f9.md) | 5.3 | 5.3 | `HandleSubscribe` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 32 | e | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep3_f10.md) | 5.3 | 5.3 | `HandleModify` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 33 | f | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep3_f11.md) | 5.3 | 5.3 | `HandleModifyForSharedData` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N` |
| 34 | ≠ | [detail](unmatched_findings/task8_vuln_udm_full_1A_no_hint_full_rerun2610_agent_rep3_f12.md) | 5.3 | 5.3 | `OneLayerPathHandlerFunc` | task8_vuln_udm_full | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N` |

**Legend**

- One row per finding the agent reported that matched no ground-truth CVE — either a false positive, or a genuine extra vulnerability with no catalogued CVE. Never counted against the evaluation (design choice: this is the practical use case, findings worth a human's triage).
- `group` = a letter (a, b, c…) means same-letter rows recur. **Letters are shared with the vector-detail section above**: an unmatched row carrying the same letter as a matched CVE sits on one of that CVE's handler functions (the CVE was already consumed in that repetition) — the same *location identity* the ground truth itself uses, so it is a **probable duplicate** of the matched CVE, not verified semantically: a handler can host more than one distinct bug, so in triage treat it as a duplicate to confirm quickly, not as a new candidate to score. Letters on unmatched-only clusters mean same function + identical vector (or an LLM-confirmed equivalent one). `≠` means the function recurred with a different vector and the LLM judged it a genuinely different finding, not a re-estimate. `—` means the function was seen only once — nothing to compare, no LLM call made. Grouping never removes or merges rows, it only labels them.
- `score (from vector)` = the recomputed score, official CVSS 4.0 math — sort key, most severe first.
- `declared` = the score the agent stated directly; diagnostic only (see note above, not produced from the vector).
- `function` = the Go function the agent pointed to as the vulnerability's location.
- `task` / `role` = which task and role produced this finding.
- `rep` = repetition index (1-based) — which run of that task/role produced this finding.
- `vector` = the full CVSS 4.0 vector string the agent estimated.
- `details` = link to a self-contained file with this finding's structured data plus the agent's full narrative for that repetition (function name bolded for quick scanning) — everything needed to review it without opening the raw JSON.

<a id="metrics-across-reps"></a>
### Metrics across repetitions

_Every table in this section aggregates over all repetitions of the task (one row per role); the per-finding detail is above._

<a id="detection-metrics"></a>
#### Detection (M1, M2, M3 — final answer vs first attempt)

| role | answer | reps | detection rate | avg coverage | TP | FP | FN | precision | recall | F1 | alerts/TP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent | final answer | 3 | 100.0% | 100.0% | 3 | 34 | 0 | 8.1% | 100.0% | 15.0% | 12.3 |
| agent | first attempt | 3 | 100.0% | 100.0% | 3 | 29 | 0 | 9.4% | 100.0% | 17.1% | 10.7 |

**Legend**

- `M1` = detection rate / avg coverage, `M2` = precision / recall / F1, `M3` = alerts/TP.
- The headline row is a **micro-average**: TP/FP/FN summed across every pooled task/repetition, then precision/recall/F1 computed once on the totals — a task with more findings (e.g. UDM, over a third of all pooled FP) weighs more just by volume. `macro avg`, shown only when ≥2 tasks are pooled, is the simple arithmetic mean of each task's own precision/recall/F1/alerts-per-TP — every task counts equally regardless of how many findings it produced. Read both: a large gap between them means one noisy task is driving the micro number.
- Unit of analysis is the CVE (docs/sgv_protocol/00_proposta_relatore.md §2): TP = matched CVEs, FN = missed CVEs, FP = findings that paired to no candidate CVE (includes genuine extra vulnerabilities with no catalogued CVE, not only false positives — see the unmatched-findings legend above).
- `reps` = repetitions pooled into this row (across every task in scope, for pooled tables). Counts sum over all of them (unit = CVE × repetition): a CVE found in every repetition contributes one TP per repetition, and TP + FN = sum of each pooled repetition's target CVEs (single task: target CVEs × reps) — read TP against that ceiling, not against the number of distinct target CVEs.
- `final answer` (the headline row) = evaluated against the final accepted answer, after every retry — the system as a black box; same numbers as the `matched`/`missed CVEs`/`unmatched findings` counts above. Formerly labelled `pass@k`.
- `first attempt` = diagnostic counterfactual: same evaluation against the agent's *first* attempt only, as if the SGV/rubric retry loop didn't exist. Formerly labelled `pass@1`.
- `detection rate` = share of repetitions (with at least one target CVE) where ≥1 CVE was matched. `avg coverage` = mean matched/target CVEs per repetition.
- `alerts/TP` (M3) = (TP+FP)/TP — how many findings a reviewer has to read for every true positive actually surfaced; lower is better (less noise per real vulnerability). `n/a` when TP = 0 (nothing to divide by).
- A final-answer row with higher recall (or F1) than its first-attempt row is the retry loop actually finding more; if precision drops (or alerts/TP rises) at the same time, the extra findings came at a cost — read them together, not recall alone.
- Full definitions: docs/sgv_protocol/07_metriche_M_S_2026-07-14.md.

<a id="precision-at-k"></a>
#### Precision@K (final answer, ranked by agent's own severity estimate)

| role | P@1 | P@3 | P@5 |
| --- | --- | --- | --- |
| agent | 66.7% (3/3 reps) | 33.3% (3/3 reps) | 20.0% (3/3 reps) |

**Legend**

- Within each repetition, all final findings (matched + unmatched) are ranked by `computed_score_B` — the official CVSS score recomputed from the *agent's own estimated vector*, never the ground-truth score (that would leak the answer into the ranking). Precision@K = share of true positives among the top K findings of that repetition.
- The value shown is the **mean across repetitions**, each weighted equally — not a count pooled by volume (same macro logic as the Detection table above).
- A repetition with fewer than K findings is **excluded** from that K's average, not counted as 0 — the `(n/total reps)` fraction shows how many repetitions actually had enough findings to fill the slot; a low fraction (e.g. 1/3) means the number is based on very little data and should be read with caution.
- Answers: "if I only trust the top-K most severe alerts, how many are real?" — a high P@1 with a lower P@5 would mean the agent's own severity ranking is doing real triage work; flat values across K mean severity doesn't predict correctness here.

<a id="variability"></a>
#### Run-to-run variability (final answer, TP/FP per repetition)

| role | task | n reps | TP mean ± std | FP mean ± std |
| --- | --- | --- | --- | --- |
| agent | task8_vuln_udm_full | 3 | 1.00 ± 0.00 (CI95 ±0.00) | 11.33 ± 0.58 (CI95 ±1.43) |

**Legend**

- Mean, sample standard deviation, and 95% confidence interval (Student's t, df = n−1) of the TP and FP *counts* across the repetitions of that task — not pooled across tasks, since that would average away the instability this section exists to show.
- With n=3 the CI is wide (t≈4.30 at 95%, vs. ≈2.0 at n=30) — treat it as a rough order-of-magnitude bound on stability, not a tight statistical guarantee. More repetitions would narrow it.
- A task where std ≈ 0 for both TP and FP is stable run-to-run (e.g. always finding the same CVEs with the same amount of noise); a high FP std means the noise volume itself is unpredictable, on top of whatever the pooled alerts/TP average already says.

<a id="cve-rep-matrix"></a>
#### CVE × repetition (final answer)

_✓ = CVE matched in that repetition, ✗ = missed. `unmatched (FP)` = findings with no GT CVE in that repetition — the per-rep noise. A CVE row that is all ✗ is a systematic miss (never found), one with mixed ✓/✗ is a sampling instability._

| task8_vuln_udm_full — agent | rep 1 | rep 2 | rep 3 | hit rate |
| --- | --- | --- | --- | --- |
| CVE-2026-42459 | ✓ | ✓ | ✓ | 3/3 |
| unmatched (FP) | 11 | 11 | 12 | 34 tot |

<a id="retry-channel"></a>
#### Detection delta by retry channel (doc 07, variation 1)

| role | retry cause | transitions | ΔTP | ΔFP |
| --- | --- | --- | --- | --- |
| agent | rubric | 3 | +0 | +5 |

**Legend**

- Each retry transition (attempt i → i+1) is attributed to the gate that rejected attempt i: `SGV` when the syntactic verifier failed (it runs first), `rubric` when the SGV passed and the retry came from the judge, `unknown` when the attempt carries neither signal. ΔTP/ΔFP = matched/unmatched findings gained (+) or lost (−) across that transition, summed per channel.
- The channel sums together equal the first-attempt → final-answer gap in the detection table above — this table splits that gap by cause (docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 1; answers the §4 open question of the proposal).
- Positive ΔTP with small ΔFP = that channel's re-examination genuinely recovers vulnerabilities; ΔFP-only = that channel adds noise.

<a id="sgv-detection-cross"></a>
#### Detection × SGV conformity (doc 07, variation 2 — M2 × Blocco C)

| role | SGV status (final answer) | TP | FP | precision |
| --- | --- | --- | --- | --- |
| agent | conform | 3 | 34 | 8.1% |

**Legend**

- Findings of the final answer bucketed by their per-finding SGV outcome (G2–G4, `sgv_eval.per_finding` of the last attempt): `non-conform` = the SGV let it through after exhausting retries (non-discard policy), `no SGV record` = the SGV reported nothing for that function name.
- If `non-conform` precision is clearly lower than `conform`, the syntactic checks correlate with substantive correctness — first empirical evidence for (or against) the §4.5 discard, gathered without discarding anything (docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 2).
- A table with only `conform` rows means every final finding passed the SGV in this run — no signal either way, not a confirmation.

<a id="severity-metrics"></a>
#### Severity (S1, S2, S3 — computed on TP only)

| role | n (TP) | S1 exact match | S3 baseline exact match |
| --- | --- | --- | --- |
| agent | 3 | 0.0% | 100.0% |

##### S2 — per-metric accuracy (agent vs. baseline), ordinal distance

| role | metric | n | accuracy | baseline accuracy | avg ordinal distance |
| --- | --- | --- | --- | --- | --- |
| agent | AV | 3 | 100.0% | 100.0% | 0.00 |
| agent | AC | 3 | 100.0% | 100.0% | 0.00 |
| agent | AT | 3 | 100.0% | 100.0% | 0.00 |
| agent | PR | 3 | 0.0% | 100.0% | 0.50 |
| agent | UI | 3 | 100.0% | 100.0% | 0.00 |
| agent | VC | 3 | 0.0% | 100.0% | 0.50 |
| agent | VI | 3 | 100.0% | 100.0% | 0.00 |
| agent | VA | 3 | 100.0% | 100.0% | 0.00 |
| agent | SC | 3 | 100.0% | 100.0% | 0.00 |
| agent | SI | 3 | 100.0% | 100.0% | 0.00 |
| agent | SA | 3 | 100.0% | 100.0% | 0.00 |

**Legend**

- `S1` = exact match of the whole vector, `S2` = per-metric accuracy / ordinal distance (table above), `S3` = null-model baseline both are read against.
- Computed only on matched findings (TP) — unmatched findings and missed CVEs carry no severity comparison, per the proposal (§5.2).
- When a repetition reports the same handler more than once, the finding paired to the CVE (whose vector S reads) is the first in agent output order — function name is the only identity available, and a GT-aware tie-break would bias S upward (see cvss_eval._match_finding). The duplicates are visible in the unmatched table via the shared `group` letter.
- `S1 exact match` = share of TP findings whose *entire* estimated vector (8 base metrics, 11 when SC/SI/SA were emitted) matches the published one field for field.
- `S3 baseline` = a null model that always guesses the modal vector among the target CVEs in scope (one task, or every task pooled together) — read S1/accuracy as a margin **above** this, not in absolute terms. With a single target CVE in scope the baseline degenerates to 100% by construction (the modal vector of one CVE is that CVE's own vector) — real property of the dataset, not a bug; the margin is only informative with several target CVEs with differing vectors in scope.
- `avg ordinal distance` (0-1, 0 = identical, 1 = opposite ends of the scale) — severity-aware: a None→High miss is penalized more than a None→Low one.
- Full definitions: docs/sgv_protocol/07_metriche_M_S_2026-07-14.md.

<a id="legacy-diagnostics"></a>
#### Legacy diagnostics (runs 1–3 comparability)

_Diagnostic roll-up kept for comparability with runs 1–3, useful for a global read once you've checked the detail above isn't spitting nonsense — the headline metrics are M1–M3/S1–S3 above._

<a id="estimates-vs-gt"></a>
##### Estimates vs ground truth

| role | estimates | matched | missed CVEs | unmatched findings | avg band vs published (0-3) | avg band vs B (0-3) | avg exploitability (0-5) | avg impact (0-3) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent | 3/3 | 3 | 0 | 34 | 1.00 | 0.00 | 4.00 | 2.00 |

**Legend**

- `estimates` = X/Y — X = repetitions where the agent emitted *at least one* CVSS finding block; Y = total repetitions evaluated for this task. **This is block presence, not correctness** — it says nothing about how many vulnerabilities were actually found or matched (see `matched`/`missed CVEs` below for that).
- `matched` = total findings, summed across all repetitions, successfully paired to a ground-truth CVE (by comparing the function name the agent reported to that CVE's known handler function).
- `missed CVEs` = total ground-truth CVEs, summed across all repetitions, that no finding in that repetition matched — i.e. vulnerabilities the agent failed to surface at all.
- `unmatched findings` = total findings, summed across all repetitions, that matched no ground-truth CVE — either a false positive, or a genuine extra vulnerability with no catalogued CVE (ranked for triage in the table further down).
- ⚠️ **The remaining four columns are diagnostic only, not the headline metric**: `avg band vs published` / `avg band vs B` score how close the *declared* score is to the reference (0 = far, 3 = exact band), and `avg exploitability` (0-5) / `avg impact` (0-3) count binary field matches on the estimated vector. The declared score is produced independently of the vector the agent also emits and carries no official rigor of its own (F17: systematically lower than what the vector is actually worth). These four columns exist only for comparability with runs 1-3.
- The metrics that actually count — recomputed from the vector with the official CVSS 4.0 algorithm — are in the table below.

<a id="official-cvss-math"></a>
##### Official CVSS 4.0 math (score recomputed from the estimated vector) — the reference metrics

| role | avg coherence Δ (score↔vector) | avg computed Δ vs B | avg band computed vs B (0-3) | avg expl. distance (0-1) | avg impact distance (0-1) | avg subseq. distance (0-1) | avg Hamming (0-8) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| agent | 0.00 | 3.40 | 0.00 | 0.10 | 0.17 | 0.00 | 2.00 |

**Legend**

- The estimated vector is rescored with the official FIRST CVSS 4.0 algorithm (macrovector + lookup table, `cvss` library).
- `coherence Δ` = |score declared by the agent − score its own vector actually produces| (the two outputs are independent, nothing forces them to agree).
- `computed Δ vs B` compares the recomputed score against the ground-truth pure base score — a vector distance in official score space.
- Severity distances are ordinal and normalized per metric group (0 = identical vector, 1 = every field at the opposite end of its scale).
- The subsequent-system triad SC/SI/SA is part of the required vector; its distance is scored only when the agent's estimate actually includes all three fields (older/legacy runs may lack them, shown as `n/a`).
- Hamming counts plainly differing fields among the 8 vulnerable-system metrics (n/a = older runs, recompute with `python -m utils.cvss_eval`).


---

<a id="sgv"></a>
## SGV — Syntactic Grounding Verifier (Blocco C, deterministic, no ground truth)

| metric | value |
| --- | --- |
| repetitions with at least one SGV retry | 0 |
| repetitions where SGV never passed (scored downstream anyway) | 0 |


---

<a id="rubric-evaluation"></a>
## Rubric evaluation (Blocco A, LLM judge)

<a id="rubric-summary"></a>
### Summary

| metric | value |
| --- | --- |
| total results | 3 |
| correct | 2 (66.7%) |
| wrong | 1 |
| retried (attempts > 1) | 2 |
| truly inconsistent tasks | 1 |
| surface-only differences (semantically equiv.) | 0 |

**Legend**

- `truly inconsistent` = LLM confirmed different conclusions across repetitions.
- `surface-only` = string-different but semantically equivalent (paraphrases, same logic).

<a id="rubric-scores"></a>
### Scores by role

| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_textual_norm |
| --- | --- | --- | --- | --- | --- |
| agent | 66.7% | 0.900 | 0.2767 | 2.00 | 0.741 |

**Legend**

| metric | scope | meaning |
| --- | --- | --- |
| `accuracy` | all | share of repetitions with verdict = correct |
| `avg_confidence` | all | mean self-reported confidence (0–1) |
| `brier_score` | all | mean((confidence − is\_correct)²) — calibration error; 0 = perfect, 0.5 = poor; note: depends on both accuracy AND confidence (e.g., 100% accuracy + 50% confidence = 0.25) |
| `avg_attempts` | all | mean LLM call attempts per repetition (>1 means retry was triggered) |
| `avg_math_delta` | math | mean \|answer − ground\_truth\| on math tasks — lower = more precise |
| `avg_textual_norm` | textual | mean normalized judge score (0–1) — higher = better rubric coverage |

<a id="cost-metrics"></a>
### Cost (M5)

| role | n | avg elapsed (s) | avg agent tokens in | avg agent tokens out | avg judge tokens in | avg judge tokens out |
| --- | --- | --- | --- | --- | --- | --- |
| agent | 3 | 18.8 | n/a | n/a | n/a | n/a |

**Legend**

- `M5` = cost per repetition: wall-clock time + tokens in/out for agent and judge.
- `n` = repetitions included, across every task type (not restricted to CVSS tasks).
- `avg elapsed` = wall-clock seconds per repetition, start to save — includes every attempt when a retry (SGV or rubric) was triggered.
- Token columns = mean prompt/completion tokens the backend reported for the agent and judge calls; `n/a` when the backend didn't report them (seen on hosted Ollama Cloud runs in this project — the field is requested but not always populated, unlike local Ollama which reports it reliably).

<a id="rubric-anomalies"></a>
### Anomalies

#### Wrong verdicts (1)

| role | task_id | rep | attempts | confidence | score/delta |
| --- | --- | --- | --- | --- | --- |
| agent | task8_vuln_udm_full | 3 | 3 | 0.900 | 6.0 |

**Legend**

- `rep` = repetition index (1-based).
- `attempts` = total LLM calls (all failed).
- `confidence` = agent self-reported confidence on the final answer.
- `score/delta` = normalized rubric score (textual) or |answer − ground_truth| (math).

#### Retries triggered (2)

| role | task_id | rep | attempts | final_verdict |
| --- | --- | --- | --- | --- |
| agent | task8_vuln_udm_full | 2 | 2 | correct |
| agent | task8_vuln_udm_full | 3 | 3 | wrong |

**Legend**

- Each row is one repetition.
- `rep` = repetition index (1-based).
- `attempts` = LLM calls within that repetition (2 means wrong on attempt 1, correct on attempt 2).
- `final_verdict` = outcome after all attempts.

#### Truly inconsistent reasoning (1)

**agent — task8_vuln_udm_full**
> The reasonings differ significantly on the fourth vulnerability: the first identifies a parameter mapping issue in 'ThreeLayerPathHandlerFunc', the second identifies a 'strings.Contains' logic error in 'OneLayerPathHandlerFunc', and the third identifies a substring matching error in 'OneLayerPathHandlerFunc' with different impact details.

**rep 1:**

1. **Improper Input Validation (Missing SUPI Validation):**
   - **Location:** `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`.
   - **Pattern:** These handlers extract the `supi` parameter using `c.Params.ByName("supi")` but fail to call `validator.IsValidSupi(supi)` before passing it to the processor. In contrast, `HandleGetAmData` correctly performs this check.
   - **Impact:** While the SBI is protected by mTLS/OAuth2, allowing malformed SUPIs into the internal processor can lead to unexpected behavior, database query errors, or potential injection if the processor does not sanitize inputs.
   - **Fix:** Add `if !validator.IsValidSupi(supi) { ... return }` blocks to all handlers receiving a SUPI.

2. **Unsafe JSON Unmarshaling (Potential DoS/Resource Exhaustion):**
   - **Location:** `getPlmnIDStruct`.
   - **Pattern:** The function takes a string directly from a URL query parameter (`values[0]`) and passes it to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact:** Since the input comes from a query string, an attacker (or a compromised NF) could send an extremely large or deeply nested JSON string. While Gin has some limits, unmarshaling arbitrary user-provided JSON into a struct without size constraints can lead to high CPU/Memory usage (DoS).
   - **Fix:** Validate the length of `plmnIDJson` before unmarshaling and use a decoder with a limit.

3. **Information Exposure via Error Messages:**
   - **Location:** `getPlmnIDStruct`, `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.
   - **Pattern:** The code returns `err.Error()` directly to the client in the `ProblemDetails` response (e.g., `Reason: err.Error()` or `Detail: err.Error()`).
   - **Impact:** This leaks internal implementation details, such as Go package names, struct fields, or parsing logic, which aids an attacker in fingerprinting the system.
   - **Fix:** Use generic error messages for the client and log the detailed error internally.

4. **Logic Error / Parameter Mismanagement (Incorrect Param Mapping):**
   - **Location:** `ThreeLayerPathHandlerFunc`.
   - **Pattern:** In the `sdm-subscriptions` logic, the code maps `c.Param("supi")` to `ueId` and `c.Param("thirdLayer")` to `subscriptionId`.
   - **Impact:** This is a fragile routing implementation. If the URL structure changes or if the `supi` parameter contains unexpected characters, the mapping to `ueId` might be incorrect, leading to unauthorized modification or deletion of subscriptions if the processor relies on these specific keys.
   - **Fix:** Use a structured routing framework or a more robust mapping mechanism that doesn't rely on manual `gin.Params` slice manipulation.

**rep 2:**

1. **Missing Input Validation (SUPI/UE ID)**: 
   - **Location**: `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`.
   - **Pattern**: These functions extract `supi := c.Params.ByName("supi")` but fail to call `validator.IsValidSupi(supi)` before passing the value to the `Processor`.
   - **Impact**: While mTLS/OAuth2 protects the interface, allowing unvalidated identifiers into the core logic can lead to unexpected behavior in the database layer or downstream processors, potentially causing crashes or logic bypasses.
   - **Fix**: Implement `if !validator.IsValidSupi(supi) { ... return }` at the start of each handler.

2. **Unsafe JSON Unmarshaling of Query Parameters**:
   - **Location**: `getPlmnIDStruct`.
   - **Pattern**: The code takes a raw string from the URL query parameter `plmn-id` and passes it directly to `json.Unmarshal([]byte(plmnIDJson), plmnIDStruct)`.
   - **Impact**: This allows an attacker (via a compromised NF) to send maliciously crafted JSON payloads. Since `json.Unmarshal` can be resource-intensive with deeply nested structures or very large strings, this can lead to CPU/Memory exhaustion (DoS).
   - **Fix**: Validate the length of the input string before unmarshaling and use a decoder with a limit.

3. **Information Leakage via Error Responses**:
   - **Location**: `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`.
   - **Pattern**: The code returns `err.Error()` directly to the client in the `ProblemDetails.Detail` field (e.g., `Detail: err.Error()`).
   - **Impact**: Raw error messages from `c.GetRawData()` or `openapi.Deserialize` can leak internal implementation details, library versions, or system paths, aiding an attacker in further exploitation.
   - **Fix**: Use generic error messages for the client and log the detailed error internally.

4. **Flawed Route Matching Logic**:
   - **Location**: `OneLayerPathHandlerFunc`.
   - **Pattern**: The check `strings.Contains(route.Pattern, supi)` is used to match a route. `route.Pattern` is a template (e.g., `/:supi`), while `supi` is the actual value from the request.
   - **Impact**: This logic is fundamentally broken. If `supi` is "123", it will not be "contained" in `/:supi`. Conversely, if a user provides a `supi` that matches a keyword in another route's pattern, it could trigger the wrong handler.
   - **Fix**: Use exact matching or a proper regex-based router instead of `strings.Contains` on the pattern template.

**rep 3:**

1. **Missing Input Validation (SUPI/UE ID):** In a 5G Core, the SUPI is a critical identifier. While `HandleGetAmData` and `HandleUnsubscribe` validate the SUPI/UE ID using `validator.IsValidSupi` or `validator.IsValidGpsi`, several other handlers (`HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetNssai`, `HandleGetSmData`) extract the `supi` parameter and pass it directly to the `Processor` without validation. This allows malformed identifiers to reach the core logic, potentially leading to unexpected behavior or database errors.
2. **Inconsistent PLMN ID Validation:** The `getPlmnIDStruct` helper ensures the `plmn-id` query parameter is a valid JSON object. However, `HandleGetTraceData` retrieves `plmn-id` using `c.Query("plmn-id")` and passes it as a raw string. This bypasses the structural validation used in other handlers, creating an inconsistency that could lead to processing errors in the `Processor`.
3. **Information Exposure through Error Messages:** Several handlers (`getPlmnIDStruct`, `HandleSubscribeToSharedData`, `HandleSubscribe`, `HandleModify`, `HandleModifyForSharedData`) return `err.Error()` directly in the `ProblemDetails` response. Specifically, `getPlmnIDStruct` returns the raw `json.Unmarshal` error. This leaks internal implementation details (e.g., Go's JSON parser specifics) to the caller.
4. **Logic Error in Custom Routing (Substring Matching):** In `OneLayerPathHandlerFunc`, the code uses `strings.Contains(route.Pattern, supi)` to determine which handler to call. Since `supi` is a user-controlled path parameter, if a user provides a value that is a substring of a defined route pattern (e.g., providing "shared-data" as the SUPI), the router may dispatch the request to the wrong handler, bypassing the intended API structure.


