# 1B — task9_vuln_cross

> **Run(s) in this report:**
> - `agent`: 20260712T142416Z

## CVSS estimate (Blocco B, deterministic)

| role | estimates | matched | missed CVEs | unmatched findings | avg band vs published (0-3) | avg band vs B (0-3) | avg exploitability (0-5) | avg impact (0-3) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent | 3/3 | 0 | 0 | 14 | n/a | n/a | n/a | n/a |

- `estimates` = X/Y — X = repetitions where the agent emitted *at least one* CVSS finding block; Y = total repetitions evaluated for this task. **This is block presence, not correctness** — it says nothing about how many vulnerabilities were actually found or matched (see `matched`/`missed CVEs` below for that).
- `matched` = total findings, summed across all repetitions, successfully paired to a ground-truth CVE (by comparing the function name the agent reported to that CVE's known handler function).
- `missed CVEs` = total ground-truth CVEs, summed across all repetitions, that no finding in that repetition matched — i.e. vulnerabilities the agent failed to surface at all.
- `unmatched findings` = total findings, summed across all repetitions, that matched no ground-truth CVE — either a false positive, or a genuine extra vulnerability with no catalogued CVE (ranked for triage in the table further down).
- ⚠️ **The remaining four columns are diagnostic only, not the headline metric**: `avg band vs published` / `avg band vs B` score how close the *declared* score is to the reference (0 = far, 3 = exact band), and `avg exploitability` (0-5) / `avg impact` (0-3) count binary field matches on the estimated vector. The declared score is produced independently of the vector the agent also emits and carries no official rigor of its own (F17: systematically lower than what the vector is actually worth). These four columns exist only for comparability with runs 1-3.
- The metrics that actually count — recomputed from the vector with the official CVSS 4.0 algorithm — are in the table below.

### Official CVSS 4.0 math (score recomputed from the estimated vector) — the reference metrics

| role | avg coherence Δ (score↔vector) | avg computed Δ vs B | avg band computed vs B (0-3) | avg expl. distance (0-1) | avg impact distance (0-1) | avg subseq. distance (0-1) | avg Hamming (0-8) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| agent | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

- The estimated vector is rescored with the official FIRST CVSS 4.0 algorithm (macrovector + lookup table, `cvss` library).
- `coherence Δ` = |score declared by the agent − score its own vector actually produces| (the two outputs are independent, nothing forces them to agree).
- `computed Δ vs B` compares the recomputed score against the ground-truth pure base score — a vector distance in official score space.
- Severity distances are ordinal and normalized per metric group (0 = identical vector, 1 = every field at the opposite end of its scale).
- The subsequent-system triad SC/SI/SA is part of the required vector; its distance is scored only when the agent's estimate actually includes all three fields (older/legacy runs may lack them, shown as `n/a`).
- Hamming counts plainly differing fields among the 8 vulnerable-system metrics (n/a = older runs, recompute with `python -m utils.cvss_eval`).

### Unmatched findings — no GT CVE, ranked by recomputed score (triage order)

| # | score (from vector) | declared | function | task | role | rep | vector |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 8.3 | 6.2 | `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` | task9_vuln_cross | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N` |
| 2 | 7.1 | 4.1 | `HTTPUEContextTransfer` | task9_vuln_cross | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 3 | 6.9 | 4.1 | `HTTPUEContextTransfer` | task9_vuln_cross | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| 4 | 6.9 | 4.1 | `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete` | task9_vuln_cross | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N` |
| 5 | 5.3 | 3.1 | `setCorsHeader` | task9_vuln_cross | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 6 | 5.3 | 4.3 | `HandleGetSmfSelectData / HandleQueryAmfContext3gpp` | task9_vuln_cross | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N` |
| 7 | 5.3 | 3.5 | `HandleCreateEeSubscriptions` | task9_vuln_cross | agent | 1 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N` |
| 8 | 5.3 | 3.1 | `setCorsHeader (PCF)` | task9_vuln_cross | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:N/VA:N/SC:L/SI:N/SA:N` |
| 9 | 5.3 | 4.1 | `HTTPUEContextTransfer (AMF)` | task9_vuln_cross | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N` |
| 10 | 5.3 | 5.3 | `HandleGetSmfSelectData / HandleQueryAmfContext3gpp (UDM/UDR)` | task9_vuln_cross | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N` |
| 11 | 5.3 | 4.1 | `HandleApplicationDataInfluenceDataSubsToNotifySubscriptionIdDelete (UDR)` | task9_vuln_cross | agent | 2 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N` |
| 12 | 5.3 | 5.1 | `setCorsHeader` | task9_vuln_cross | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N` |
| 13 | 5.1 | 4.3 | `HandleQueryAmfContext3gpp (Cross-NF Validation)` | task9_vuln_cross | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:L/VA:L/SC:L/SI:L/SA:L` |
| 14 | 0.0 | 0.0 | `HandleCreateEeSubscriptions` | task9_vuln_cross | agent | 3 | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N` |

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
| truly inconsistent tasks | 0 |
| surface-only differences (semantically equiv.) | 1 |

_truly inconsistent_: LLM confirmed different conclusions across repetitions. _surface-only_: string-different but semantically equivalent (paraphrases, same logic).

All tasks passed with full consistency — no anomalies detected.

### Scores by role

| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_textual_norm |
| --- | --- | --- | --- | --- | --- |
| agent | 100.0% | 0.933 | 0.0067 | 1.00 | 1.000 |

**Legend**

| metric | scope | meaning |
| --- | --- | --- |
| `accuracy` | all | share of repetitions with verdict = correct |
| `avg_confidence` | all | mean self-reported confidence (0–1) |
| `brier_score` | all | mean((confidence − is\_correct)²) — calibration error; 0 = perfect, 0.5 = poor; note: depends on both accuracy AND confidence (e.g., 100% accuracy + 50% confidence = 0.25) |
| `avg_attempts` | all | mean LLM call attempts per repetition (>1 means retry was triggered) |
| `avg_math_delta` | math | mean \|answer − ground\_truth\| on math tasks — lower = more precise |
| `avg_textual_norm` | textual | mean normalized judge score (0–1) — higher = better rubric coverage |

