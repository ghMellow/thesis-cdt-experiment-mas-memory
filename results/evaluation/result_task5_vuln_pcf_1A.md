# 1A — task5_vuln_pcf

> **Run(s) in this report:**
> - `agent`: 20260714T152535Z

<a id="toc"></a>
**Contents**

- [SGV — Syntactic Grounding Verifier](#sgv)
- [Vector detail (estimated vs. published)](#vector-detail)
- [Detection (M1, M2, M3 — pass@1 vs pass@k)](#detection-metrics)
- [Severity (S1, S2, S3)](#severity-metrics)
- [Aggregate metrics (across repetitions)](#aggregate-metrics)
  - [Estimates vs ground truth](#estimates-vs-gt)
  - [Official CVSS 4.0 math](#official-cvss-math)
- [Rubric evaluation](#rubric-evaluation)
  - [Summary](#rubric-summary)
  - [Scores by role](#rubric-scores)
  - [Cost (M5)](#cost-metrics)
  - [Anomalies](#rubric-anomalies)

<a id="sgv"></a>
## SGV — Syntactic Grounding Verifier (Blocco C, deterministic, no ground truth)

| metric | value |
| --- | --- |
| repetitions with at least one SGV retry | 1 |
| repetitions where SGV never passed (scored downstream anyway) | 0 |

#### Retries resolved by the agent (1)

| role | task_id | rep | attempts | fixed on attempt |
| --- | --- | --- | --- | --- |
| agent | task5_vuln_pcf | 3 | 2 | 2 |

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
| [reasoning detail](matched_findings/task5_vuln_pcf_1A_agent_rep1_CVE-2026-41135.md) | | |

| **CVE-2026-41135** — agent, rep 2 | estimated | published |
|---|---|---|
| AV — Attack Vector | N | N |
| AC — Attack Complexity | L | L |
| AT — Attack Requirements | N | N |
| PR — Privileges Required | N | N |
| UI — User Interaction | N | N |
| VC — Confidentiality Impact to the Vulnerable System | N | N |
| VI — Integrity Impact to the Vulnerable System | N | N |
| VA — Availability Impact to the Vulnerable System | H | H |
| SC — Confidentiality Impact to the Subsequent System | N | N |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 7.1 / **8.7** | 8.7 |
| [reasoning detail](matched_findings/task5_vuln_pcf_1A_agent_rep2_CVE-2026-41135.md) | | |

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
| SC — Confidentiality Impact to the Subsequent System | **L** | **N** |
| SI — Integrity Impact to the Subsequent System | N | N |
| SA — Availability Impact to the Subsequent System | N | N |
| base score — declared / from vector (official math) | 5.1 / **7.1** | 8.7 |
| [reasoning detail](matched_findings/task5_vuln_pcf_1A_agent_rep3_CVE-2026-41135.md) | | |

<a id="detection-metrics"></a>
### Detection (M1, M2, M3 — pass@1 vs pass@k)

| role | pass | detection rate | avg coverage | TP | FP | FN | precision | recall | F1 | alerts/TP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent | pass@1 | 66.7% | 66.7% | 2 | 0 | 1 | 100.0% | 66.7% | 80.0% | 1.0 |
| agent | pass@k | 100.0% | 100.0% | 3 | 0 | 0 | 100.0% | 100.0% | 100.0% | 1.0 |

**Legend**

- Unit of analysis is the CVE (docs/sgv_protocol/00_proposta_relatore.md §2): TP = matched CVEs, FN = missed CVEs, FP = findings that paired to no candidate CVE (includes genuine extra vulnerabilities with no catalogued CVE, not only false positives — see the unmatched-findings legend above).
- `pass@1` = evaluated against the agent's *first* attempt only, as if the SGV/rubric retry loop didn't exist.
- `pass@k` = evaluated against the final accepted answer, after every retry — same numbers as the `matched`/`missed CVEs`/`unmatched findings` counts above.
- `detection rate` = share of repetitions (with at least one target CVE) where ≥1 CVE was matched. `avg coverage` = mean matched/target CVEs per repetition.
- `alerts/TP` (M3) = (TP+FP)/TP — how many findings a reviewer has to read for every true positive actually surfaced; lower is better (less noise per real vulnerability). `n/a` when TP = 0 (nothing to divide by).
- A pass@k row with higher recall (or F1) than its pass@1 row is the retry loop actually finding more; if precision drops (or alerts/TP rises) at the same time, the extra findings came at a cost — read them together, not recall alone.

<a id="severity-metrics"></a>
### Severity (S1, S2, S3 — computed on TP only)

| role | n (TP) | S1 exact match | S3 baseline exact match |
| --- | --- | --- | --- |
| agent | 3 | 0.0% | 100.0% |

#### S2 — per-metric accuracy (agent vs. baseline), ordinal distance

| role | metric | n | accuracy | baseline accuracy | avg ordinal distance |
| --- | --- | --- | --- | --- | --- |
| agent | AV | 3 | 100.0% | 100.0% | 0.00 |
| agent | AC | 3 | 100.0% | 100.0% | 0.00 |
| agent | AT | 3 | 100.0% | 100.0% | 0.00 |
| agent | PR | 3 | 100.0% | 100.0% | 0.00 |
| agent | UI | 3 | 33.3% | 100.0% | 0.33 |
| agent | VC | 3 | 33.3% | 100.0% | 0.50 |
| agent | VI | 3 | 100.0% | 100.0% | 0.00 |
| agent | VA | 3 | 33.3% | 100.0% | 0.67 |
| agent | SC | 3 | 33.3% | 100.0% | 0.33 |
| agent | SI | 3 | 100.0% | 100.0% | 0.00 |
| agent | SA | 3 | 100.0% | 100.0% | 0.00 |

**Legend**

- Computed only on matched findings (TP) — unmatched findings and missed CVEs carry no severity comparison, per the proposal (§5.2).
- `S1 exact match` = share of TP findings whose *entire* estimated vector (8 base metrics, 11 when SC/SI/SA were emitted) matches the published one field for field.
- `S3 baseline` = a null model that always guesses the modal vector among this task's target CVEs — read S1/accuracy as a margin **above** this, not in absolute terms. On tasks with a single target CVE the baseline degenerates to 100% by construction (the modal vector of one CVE is that CVE's own vector) — real property of the dataset, not a bug; the margin is only informative when a task has several target CVEs with differing vectors.
- `avg ordinal distance` (0-1, 0 = identical, 1 = opposite ends of the scale) — severity-aware: a None→High miss is penalized more than a None→Low one.

<a id="aggregate-metrics"></a>
### Aggregate metrics (across repetitions)

_Diagnostic roll-up, useful for a global read once you've checked the detail above isn't spitting nonsense — not the first thing to read._

<a id="estimates-vs-gt"></a>
#### Estimates vs ground truth

| role | estimates | matched | missed CVEs | unmatched findings | avg band vs published (0-3) | avg band vs B (0-3) | avg exploitability (0-5) | avg impact (0-3) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent | 3/3 | 3 | 0 | 0 | 0.33 | 0.33 | 4.33 | 1.67 |

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
| agent | 1.60 | 1.67 | 1.33 | 0.07 | 0.39 | 0.11 | 2.00 |

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
| retried (attempts > 1) | 1 |
| truly inconsistent tasks | 0 |
| surface-only differences (semantically equiv.) | 1 |

**Legend**

- `truly inconsistent` = LLM confirmed different conclusions across repetitions.
- `surface-only` = string-different but semantically equivalent (paraphrases, same logic).

<a id="rubric-scores"></a>
### Scores by role

| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_textual_norm |
| --- | --- | --- | --- | --- | --- |
| agent | 100.0% | 0.967 | 0.0033 | 1.33 | 0.889 |

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
| agent | 3 | 25.9 | n/a | n/a | n/a | n/a |

**Legend**

- `n` = repetitions included, across every task type (not restricted to CVSS tasks).
- `avg elapsed` = wall-clock seconds per repetition, start to save — includes every attempt when a retry (SGV or rubric) was triggered.
- Token columns = mean prompt/completion tokens the backend reported for the agent and judge calls; `n/a` when the backend didn't report them (seen on hosted Ollama Cloud runs in this project — the field is requested but not always populated, unlike local Ollama which reports it reliably).

<a id="rubric-anomalies"></a>
### Anomalies

#### Retries triggered (1)

| role | task_id | rep | attempts | final_verdict |
| --- | --- | --- | --- | --- |
| agent | task5_vuln_pcf | 3 | 2 | correct |

**Legend**

- Each row is one repetition.
- `rep` = repetition index (1-based).
- `attempts` = LLM calls within that repetition (2 means wrong on attempt 1, correct on attempt 2).
- `final_verdict` = outcome after all attempts.

