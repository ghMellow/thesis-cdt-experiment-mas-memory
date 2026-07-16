# Comparison 1A vs 1B

> **Run(s) in this report:**
> - `agent`: 20260714T152535Z

| role | accuracy_1A | accuracy_1B | delta |
| --- | --- | --- | --- |
| agent | 60.0% | n/a | n/a |

No accuracy difference between 1A and 1B.

## 1A — pooled across all tasks

<a id="detection-metrics"></a>
### Detection (M1, M2, M3 — pass@1 vs pass@k)

| role | pass | detection rate | avg coverage | TP | FP | FN | precision | recall | F1 | alerts/TP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent | pass@1 | 91.7% | 72.2% | 12 | 67 | 15 | 15.2% | 44.4% | 22.6% | 6.6 |
| agent | pass@k | 100.0% | 83.3% | 15 | 84 | 12 | 15.2% | 55.6% | 23.8% | 6.6 |

**Legend**

- `M1` = detection rate / avg coverage, `M2` = precision / recall / F1, `M3` = alerts/TP.
- Unit of analysis is the CVE (docs/sgv_protocol/00_proposta_relatore.md §2): TP = matched CVEs, FN = missed CVEs, FP = findings that paired to no candidate CVE (includes genuine extra vulnerabilities with no catalogued CVE, not only false positives — see the unmatched-findings legend above).
- `pass@1` = evaluated against the agent's *first* attempt only, as if the SGV/rubric retry loop didn't exist.
- `pass@k` = evaluated against the final accepted answer, after every retry — same numbers as the `matched`/`missed CVEs`/`unmatched findings` counts above.
- `detection rate` = share of repetitions (with at least one target CVE) where ≥1 CVE was matched. `avg coverage` = mean matched/target CVEs per repetition.
- `alerts/TP` (M3) = (TP+FP)/TP — how many findings a reviewer has to read for every true positive actually surfaced; lower is better (less noise per real vulnerability). `n/a` when TP = 0 (nothing to divide by).
- A pass@k row with higher recall (or F1) than its pass@1 row is the retry loop actually finding more; if precision drops (or alerts/TP rises) at the same time, the extra findings came at a cost — read them together, not recall alone.
- Full definitions: docs/sgv_protocol/07_metriche_M_S_2026-07-14.md.

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

