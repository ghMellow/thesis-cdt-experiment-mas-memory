# 1B — task7_vuln_amf

## Summary

| metric | value |
| --- | --- |
| total results | 2 |
| correct | 1 (50.0%) |
| wrong | 1 |
| retried (attempts > 1) | 1 |
| truly inconsistent tasks | 0 |
| surface-only differences (semantically equiv.) | 0 |

_truly inconsistent_: LLM confirmed different conclusions across repetitions. _surface-only_: string-different but semantically equivalent (paraphrases, same logic).

## Scores by role

| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_textual_norm |
| --- | --- | --- | --- | --- | --- |
| beginner | 0.0% | 1.000 | 1.0000 | 3.00 | 0.444 |
| expert | 100.0% | 1.000 | 0.0000 | 1.00 | 1.000 |

**Legend**

| metric | scope | meaning |
| --- | --- | --- |
| `accuracy` | all | share of repetitions with verdict = correct |
| `avg_confidence` | all | mean self-reported confidence (0–1) |
| `brier_score` | all | mean((confidence − is\_correct)²) — calibration error; 0 = perfect, 0.5 = poor; note: depends on both accuracy AND confidence (e.g., 100% accuracy + 50% confidence = 0.25) |
| `avg_attempts` | all | mean LLM call attempts per repetition (>1 means retry was triggered) |
| `avg_math_delta` | math | mean \|answer − ground\_truth\| on math tasks — lower = more precise |
| `avg_textual_norm` | textual | mean normalized judge score (0–1) — higher = better rubric coverage |

## CVSS estimate (Blocco B, deterministic)

| role | estimates | matched | missed CVEs | unmatched findings | avg band vs published (0-3) | avg band vs B (0-3) | avg exploitability (0-5) | avg impact (0-3) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| beginner | 1/1 | 1 | 0 | 2 | 3.00 | 1.00 | 5.00 | 1.00 |
| expert | 1/1 | 1 | 0 | 1 | 0.00 | 1.00 | 5.00 | 1.00 |

_`estimates` = repetitions where the agent produced a CVSS block. `matched` = findings paired to a ground-truth CVE via handler function. `band vs published` compares against the published score (BT where the vector includes Threat E); `band vs B` against the pure base score. Exploitability counts AV/AC/AT/PR/UI matches; impact counts VC/VI/VA — the impact triad is the discriminating signal on this dataset._

## Anomalies

### Wrong verdicts (1)

| role | task_id | rep | attempts | confidence | score/delta |
| --- | --- | --- | --- | --- | --- |
| beginner | task7_vuln_amf | 1 | 3 | 1.000 | 4.0 |

_`rep` = repetition index. `attempts` = total LLM calls (all failed). `confidence` = agent self-reported confidence on the final answer. `score/delta` = normalized rubric score (textual) or |answer − ground_truth| (math)._

### Retries triggered (1)

| role | task_id | rep | attempts | final_verdict |
| --- | --- | --- | --- | --- |
| beginner | task7_vuln_amf | 1 | 3 | wrong |

_Each row is one repetition. `rep` = repetition index (1-based). `attempts` = LLM calls within that repetition (2 means wrong on attempt 1, correct on attempt 2). `final_verdict` = outcome after all attempts._

