# Comparison 1A vs 1B

> **Run(s) in this report:**
> - `agent`: 20260714T152535Z

| role | accuracy_1A | accuracy_1B | delta |
| --- | --- | --- | --- |
| agent | 60.0% | n/a | n/a |

No accuracy difference between 1A and 1B.

## 1A — pooled across all tasks

<a id="detection-metrics"></a>
### Detection (M1, M2, M3 — final answer vs first attempt)

| role | answer | reps | detection rate | avg coverage | TP | FP | FN | precision | recall | F1 | alerts/TP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent | final answer | 15 | 100.0% | 83.3% | 15 | 84 | 12 | 15.2% | 55.6% | 23.8% | 6.6 |
| agent | final answer (macro avg, n=4 tasks) | — | — | — | — | — | — | 38.9% | 83.3% | 43.7% | 5.7 |
| agent | first attempt | 15 | 91.7% | 72.2% | 12 | 67 | 15 | 15.2% | 44.4% | 22.6% | 6.6 |
| agent | first attempt (macro avg, n=4 tasks) | — | — | — | — | — | — | 39.8% | 72.2% | 38.8% | 4.6 |

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
### Precision@K (final answer, ranked by agent's own severity estimate)

| role | P@1 | P@3 | P@5 |
| --- | --- | --- | --- |
| agent | 60.0% (15/15 reps) | 30.6% (12/15 reps) | 20.0% (12/15 reps) |

**Legend**

- Within each repetition, all final findings (matched + unmatched) are ranked by `computed_score_B` — the official CVSS score recomputed from the *agent's own estimated vector*, never the ground-truth score (that would leak the answer into the ranking). Precision@K = share of true positives among the top K findings of that repetition.
- The value shown is the **mean across repetitions**, each weighted equally — not a count pooled by volume (same macro logic as the Detection table above).
- A repetition with fewer than K findings is **excluded** from that K's average, not counted as 0 — the `(n/total reps)` fraction shows how many repetitions actually had enough findings to fill the slot; a low fraction (e.g. 1/3) means the number is based on very little data and should be read with caution.
- Answers: "if I only trust the top-K most severe alerts, how many are real?" — a high P@1 with a lower P@5 would mean the agent's own severity ranking is doing real triage work; flat values across K mean severity doesn't predict correctness here.

<a id="variability"></a>
### Run-to-run variability (final answer, TP/FP per repetition)

| role | task | n reps | TP mean ± std | FP mean ± std |
| --- | --- | --- | --- | --- |
| agent | task5_vuln_pcf | 3 | 1.00 ± 0.00 (CI95 ±0.00) | 0.00 ± 0.00 (CI95 ±0.00) |
| agent | task6_vuln_udr_full | 3 | 2.00 ± 0.00 (CI95 ±0.00) | 4.33 ± 0.58 (CI95 ±1.43) |
| agent | task7_vuln_amf_full | 3 | 1.00 ± 0.00 (CI95 ±0.00) | 5.33 ± 2.31 (CI95 ±5.74) |
| agent | task8_vuln_udm_full | 3 | 1.00 ± 0.00 (CI95 ±0.00) | 11.33 ± 0.58 (CI95 ±1.43) |
| agent | task9_vuln_cross | 3 | 0.00 ± 0.00 (CI95 ±0.00) | 7.00 ± 1.73 (CI95 ±4.30) |

**Legend**

- Mean, sample standard deviation, and 95% confidence interval (Student's t, df = n−1) of the TP and FP *counts* across the repetitions of that task — not pooled across tasks, since that would average away the instability this section exists to show.
- With n=3 the CI is wide (t≈4.30 at 95%, vs. ≈2.0 at n=30) — treat it as a rough order-of-magnitude bound on stability, not a tight statistical guarantee. More repetitions would narrow it.
- A task where std ≈ 0 for both TP and FP is stable run-to-run (e.g. always finding the same CVEs with the same amount of noise); a high FP std means the noise volume itself is unpredictable, on top of whatever the pooled alerts/TP average already says.

<a id="cve-rep-matrix"></a>
### CVE × repetition (final answer)

_✓ = CVE matched in that repetition, ✗ = missed. `unmatched (FP)` = findings with no GT CVE in that repetition — the per-rep noise. A CVE row that is all ✗ is a systematic miss (never found), one with mixed ✓/✗ is a sampling instability._

| task5_vuln_pcf — agent | rep 1 | rep 2 | rep 3 | hit rate |
| --- | --- | --- | --- | --- |
| CVE-2026-41135 | ✓ | ✓ | ✓ | 3/3 |
| unmatched (FP) | 0 | 0 | 0 | 0 tot |

| task6_vuln_udr_full — agent | rep 1 | rep 2 | rep 3 | hit rate |
| --- | --- | --- | --- | --- |
| CVE-2026-40245 | ✗ | ✗ | ✗ | 0/3 |
| CVE-2026-40246 | ✗ | ✗ | ✗ | 0/3 |
| CVE-2026-40247 | ✗ | ✗ | ✗ | 0/3 |
| CVE-2026-40248 | ✗ | ✗ | ✗ | 0/3 |
| CVE-2026-40249 | ✓ | ✓ | ✓ | 3/3 |
| CVE-2026-40343 | ✓ | ✓ | ✓ | 3/3 |
| unmatched (FP) | 5 | 4 | 4 | 13 tot |

| task7_vuln_amf_full — agent | rep 1 | rep 2 | rep 3 | hit rate |
| --- | --- | --- | --- | --- |
| CVE-2026-41136 | ✓ | ✓ | ✓ | 3/3 |
| unmatched (FP) | 4 | 4 | 8 | 16 tot |

| task8_vuln_udm_full — agent | rep 1 | rep 2 | rep 3 | hit rate |
| --- | --- | --- | --- | --- |
| CVE-2026-42459 | ✓ | ✓ | ✓ | 3/3 |
| unmatched (FP) | 12 | 11 | 11 | 34 tot |

| task9_vuln_cross — agent | rep 1 | rep 2 | rep 3 | hit rate |
| --- | --- | --- | --- | --- |
| unmatched (FP) | 9 | 6 | 6 | 21 tot |

<a id="retry-channel"></a>
### Detection delta by retry channel (doc 07, variation 1)

| role | retry cause | transitions | ΔTP | ΔFP |
| --- | --- | --- | --- | --- |
| agent | SGV | 1 | +1 | +0 |
| agent | rubric | 12 | +2 | +17 |

**Legend**

- Each retry transition (attempt i → i+1) is attributed to the gate that rejected attempt i: `SGV` when the syntactic verifier failed (it runs first), `rubric` when the SGV passed and the retry came from the judge, `unknown` when the attempt carries neither signal. ΔTP/ΔFP = matched/unmatched findings gained (+) or lost (−) across that transition, summed per channel.
- The channel sums together equal the first-attempt → final-answer gap in the detection table above — this table splits that gap by cause (docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 1; answers the §4 open question of the proposal).
- Positive ΔTP with small ΔFP = that channel's re-examination genuinely recovers vulnerabilities; ΔFP-only = that channel adds noise.

<a id="sgv-detection-cross"></a>
### Detection × SGV conformity (doc 07, variation 2 — M2 × Blocco C)

| role | SGV status (final answer) | TP | FP | precision |
| --- | --- | --- | --- | --- |
| agent | conform | 15 | 84 | 15.2% |

**Legend**

- Findings of the final answer bucketed by their per-finding SGV outcome (G2–G4, `sgv_eval.per_finding` of the last attempt): `non-conform` = the SGV let it through after exhausting retries (non-discard policy), `no SGV record` = the SGV reported nothing for that function name.
- If `non-conform` precision is clearly lower than `conform`, the syntactic checks correlate with substantive correctness — first empirical evidence for (or against) the §4.5 discard, gathered without discarding anything (docs/sgv_protocol/07_metriche_M_S_2026-07-14.md, variation 2).
- A table with only `conform` rows means every final finding passed the SGV in this run — no signal either way, not a confirmation.

<a id="severity-metrics"></a>
### Severity (S1, S2, S3 — computed on TP only)

| role | n (TP) | S1 exact match | S3 baseline exact match |
| --- | --- | --- | --- |
| agent | 15 | 0.0% | 0.0% |

#### S2 — per-metric accuracy (agent vs. baseline), ordinal distance

| role | metric | n | accuracy | baseline accuracy | avg ordinal distance |
| --- | --- | --- | --- | --- | --- |
| agent | AV | 15 | 100.0% | 100.0% | 0.00 |
| agent | AC | 15 | 100.0% | 100.0% | 0.00 |
| agent | AT | 15 | 100.0% | 100.0% | 0.00 |
| agent | PR | 15 | 20.0% | 100.0% | 0.53 |
| agent | UI | 15 | 86.7% | 100.0% | 0.07 |
| agent | VC | 15 | 66.7% | 80.0% | 0.20 |
| agent | VI | 15 | 46.7% | 40.0% | 0.27 |
| agent | VA | 15 | 60.0% | 80.0% | 0.33 |
| agent | SC | 15 | 73.3% | 100.0% | 0.13 |
| agent | SI | 15 | 60.0% | 80.0% | 0.27 |
| agent | SA | 15 | 93.3% | 100.0% | 0.03 |

**Legend**

- `S1` = exact match of the whole vector, `S2` = per-metric accuracy / ordinal distance (table above), `S3` = null-model baseline both are read against.
- Computed only on matched findings (TP) — unmatched findings and missed CVEs carry no severity comparison, per the proposal (§5.2).
- When a repetition reports the same handler more than once, the finding paired to the CVE (whose vector S reads) is the first in agent output order — function name is the only identity available, and a GT-aware tie-break would bias S upward (see cvss_eval._match_finding). The duplicates are visible in the unmatched table via the shared `group` letter.
- `S1 exact match` = share of TP findings whose *entire* estimated vector (8 base metrics, 11 when SC/SI/SA were emitted) matches the published one field for field.
- `S3 baseline` = a null model that always guesses the modal vector among the target CVEs in scope (one task, or every task pooled together) — read S1/accuracy as a margin **above** this, not in absolute terms. With a single target CVE in scope the baseline degenerates to 100% by construction (the modal vector of one CVE is that CVE's own vector) — real property of the dataset, not a bug; the margin is only informative with several target CVEs with differing vectors in scope.
- `avg ordinal distance` (0-1, 0 = identical, 1 = opposite ends of the scale) — severity-aware: a None→High miss is penalized more than a None→Low one.
- Full definitions: docs/sgv_protocol/07_metriche_M_S_2026-07-14.md.

<a id="cost-metrics"></a>
### Cost (M5)

| role | n | avg elapsed (s) | avg agent tokens in | avg agent tokens out | avg judge tokens in | avg judge tokens out |
| --- | --- | --- | --- | --- | --- | --- |
| agent | 15 | 56.2 | n/a | n/a | n/a | n/a |

**Legend**

- `M5` = cost per repetition: wall-clock time + tokens in/out for agent and judge.
- `n` = repetitions included, across every task type (not restricted to CVSS tasks).
- `avg elapsed` = wall-clock seconds per repetition, start to save — includes every attempt when a retry (SGV or rubric) was triggered.
- Token columns = mean prompt/completion tokens the backend reported for the agent and judge calls; `n/a` when the backend didn't report them (seen on hosted Ollama Cloud runs in this project — the field is requested but not always populated, unlike local Ollama which reports it reliably).

