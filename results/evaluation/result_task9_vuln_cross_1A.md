# 1A — task9_vuln_cross

> **Run(s) in this report:**
> - `agent`: 20260714T152535Z

<a id="toc"></a>
**Contents**

- [SGV — Syntactic Grounding Verifier](#sgv)
- [Unmatched findings](#unmatched-findings)
- [Detection (M1, M2, M3 — pass@1 vs pass@k)](#detection-metrics)
- [Aggregate metrics (across repetitions)](#aggregate-metrics)
  - [Estimates vs ground truth](#estimates-vs-gt)
  - [Official CVSS 4.0 math](#official-cvss-math)
- [Rubric evaluation](#rubric-evaluation)
  - [Summary](#rubric-summary)
  - [Scores by role](#rubric-scores)
  - [Cost (M5)](#cost-metrics)

<a id="sgv"></a>
## SGV — Syntactic Grounding Verifier (Blocco C, deterministic, no ground truth)

| metric | value |
| --- | --- |
| repetitions with at least one SGV retry | 0 |
| repetitions where SGV never passed (scored downstream anyway) | 0 |

<a id="cvss-estimate"></a>
## CVSS estimate (Blocco B, deterministic)

<a id="unmatched-findings"></a>
### Unmatched findings — no GT CVE, ranked by recomputed score (triage order)

| # | group | details | score (from vector) | declared | function | task | role | rep | vector |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ≠ | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep2_f1.md) | 8.3 | 8.4 | `HandleQueryAmfContext3gpp` | task9_vuln_cross | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N` |
| 2 | ≠ | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep2_f2.md) | 8.3 | 7.1 | `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` | task9_vuln_cross | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N` |
| 3 | ≠ | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep3_f1.md) | 8.3 | 4.8 | `HandleQueryAmfContext3gpp` | task9_vuln_cross | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N` |
| 4 | ≠ | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep3_f2.md) | 8.2 | 4.1 | `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` | task9_vuln_cross | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N` |
| 5 | ≠ | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep2_f3.md) | 7.1 | 7.1 | `HTTPUEContextTransfer` | task9_vuln_cross | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 6 | ≠ | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep2_f4.md) | 6.9 | 5.3 | `setCorsHeader` | task9_vuln_cross | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 7 | a | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep1_f1.md) | 5.3 | 3.1 | `setCorsHeader` | task9_vuln_cross | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 8 | ≠ | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep1_f2.md) | 5.3 | 4.3 | `HTTPUEContextTransfer` | task9_vuln_cross | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N` |
| 9 | — | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep1_f3.md) | 5.3 | 3.7 | `HTTPCreateUEContext` | task9_vuln_cross | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 10 | b | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep1_f4.md) | 5.3 | 4.3 | `HandleGetSmfSelectData` | task9_vuln_cross | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 11 | ≠ | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep1_f5.md) | 5.3 | 5.3 | `HandleQueryAmfContext3gpp` | task9_vuln_cross | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N` |
| 12 | ≠ | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep1_f6.md) | 5.3 | 4.3 | `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` | task9_vuln_cross | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:L/SA:N` |
| 13 | — | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep1_f7.md) | 5.3 | 4.3 | `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdGet` | task9_vuln_cross | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:L/SA:N` |
| 14 | — | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep1_f8.md) | 5.3 | 4.3 | `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdPut` | task9_vuln_cross | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:L/SC:N/SI:L/SA:N` |
| 15 | ≠ | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep1_f9.md) | 5.3 | 3.7 | `HandleCreateEeSubscriptions` | task9_vuln_cross | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N` |
| 16 | b | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep2_f5.md) | 5.3 | 5.3 | `HandleGetSmfSelectData` | task9_vuln_cross | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 17 | ≠ | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep2_f6.md) | 5.3 | 4.0 | `HandleCreateEeSubscriptions` | task9_vuln_cross | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:N/SC:L/SI:L/SA:N` |
| 18 | a | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep3_f3.md) | 5.3 | 3.1 | `setCorsHeader` | task9_vuln_cross | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 19 | ≠ | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep3_f4.md) | 5.1 | 2.0 | `HTTPUEContextTransfer` | task9_vuln_cross | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 20 | ≠ | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep3_f5.md) | 5.1 | 2.7 | `HandleGetSmfSelectData` | task9_vuln_cross | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 21 | ≠ | [detail](unmatched_findings/task9_vuln_cross_1A_agent_rep3_f6.md) | 5.1 | 2.0 | `HandleCreateEeSubscriptions` | task9_vuln_cross | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N` |

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

<a id="detection-metrics"></a>
### Detection (M1, M2, M3 — pass@1 vs pass@k)

| role | pass | detection rate | avg coverage | TP | FP | FN | precision | recall | F1 | alerts/TP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent | pass@1 | n/a | n/a | 0 | 21 | 0 | 0.0% | n/a | n/a | n/a |
| agent | pass@k | n/a | n/a | 0 | 21 | 0 | 0.0% | n/a | n/a | n/a |

**Legend**

- Unit of analysis is the CVE (docs/sgv_protocol/00_proposta_relatore.md §2): TP = matched CVEs, FN = missed CVEs, FP = findings that paired to no candidate CVE (includes genuine extra vulnerabilities with no catalogued CVE, not only false positives — see the unmatched-findings legend above).
- `pass@1` = evaluated against the agent's *first* attempt only, as if the SGV/rubric retry loop didn't exist.
- `pass@k` = evaluated against the final accepted answer, after every retry — same numbers as the `matched`/`missed CVEs`/`unmatched findings` counts above.
- `detection rate` = share of repetitions (with at least one target CVE) where ≥1 CVE was matched. `avg coverage` = mean matched/target CVEs per repetition.
- `alerts/TP` (M3) = (TP+FP)/TP — how many findings a reviewer has to read for every true positive actually surfaced; lower is better (less noise per real vulnerability). `n/a` when TP = 0 (nothing to divide by).
- A pass@k row with higher recall (or F1) than its pass@1 row is the retry loop actually finding more; if precision drops (or alerts/TP rises) at the same time, the extra findings came at a cost — read them together, not recall alone.

<a id="aggregate-metrics"></a>
### Aggregate metrics (across repetitions)

_Diagnostic roll-up, useful for a global read once you've checked the detail above isn't spitting nonsense — not the first thing to read._

<a id="estimates-vs-gt"></a>
#### Estimates vs ground truth

| role | estimates | matched | missed CVEs | unmatched findings | avg band vs published (0-3) | avg band vs B (0-3) | avg exploitability (0-5) | avg impact (0-3) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent | 3/3 | 0 | 0 | 21 | n/a | n/a | n/a | n/a |

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
| agent | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

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
| truly inconsistent tasks | 0 |
| surface-only differences (semantically equiv.) | 1 |

**Legend**

- `truly inconsistent` = LLM confirmed different conclusions across repetitions.
- `surface-only` = string-different but semantically equivalent (paraphrases, same logic).

All tasks passed with full consistency — no anomalies detected.

<a id="rubric-scores"></a>
### Scores by role

| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_textual_norm |
| --- | --- | --- | --- | --- | --- |
| agent | 100.0% | 0.967 | 0.0033 | 1.00 | 1.000 |

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
| agent | 3 | 31.2 | n/a | n/a | n/a | n/a |

**Legend**

- `n` = repetitions included, across every task type (not restricted to CVSS tasks).
- `avg elapsed` = wall-clock seconds per repetition, start to save — includes every attempt when a retry (SGV or rubric) was triggered.
- Token columns = mean prompt/completion tokens the backend reported for the agent and judge calls; `n/a` when the backend didn't report them (seen on hosted Ollama Cloud runs in this project — the field is requested but not always populated, unlike local Ollama which reports it reliably).

