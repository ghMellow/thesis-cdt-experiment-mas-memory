# framing_B1_e2b — task8_vuln_udm

## Summary

| metric | value |
| --- | --- |
| total results | 3 |
| correct | 0 (0.0%) |
| wrong | 3 |
| retried (attempts > 1) | 3 |
| truly inconsistent tasks | 0 |
| surface-only differences (semantically equiv.) | 4 |

_truly inconsistent_: LLM confirmed different conclusions across repetitions. _surface-only_: string-different but semantically equivalent (paraphrases, same logic).

## Scores by role

| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_textual_norm |
| --- | --- | --- | --- | --- | --- |
| expert | 0.0% | 1.000 | 1.0000 | 3.00 | 0.593 |

**Legend**

| metric | scope | meaning |
| --- | --- | --- |
| `accuracy` | all | share of repetitions with verdict = correct |
| `avg_confidence` | all | mean self-reported confidence (0–1) |
| `brier_score` | all | mean((confidence − is\_correct)²) — calibration error; 0 = perfect, 0.5 = poor; note: depends on both accuracy AND confidence (e.g., 100% accuracy + 50% confidence = 0.25) |
| `avg_attempts` | all | mean LLM call attempts per repetition (>1 means retry was triggered) |
| `avg_math_delta` | math | mean \|answer − ground\_truth\| on math tasks — lower = more precise |
| `avg_textual_norm` | textual | mean normalized judge score (0–1) — higher = better rubric coverage |

## Anomalies

### Wrong verdicts (3)

| role | task_id | rep | attempts | confidence | score/delta |
| --- | --- | --- | --- | --- | --- |
| expert | task8_vuln_udm | 1 | 3 | 1.000 | 5.0 |
| expert | task8_vuln_udm | 2 | 3 | 1.000 | 5.0 |
| expert | task8_vuln_udm | 3 | 3 | 1.000 | 6.0 |

_`rep` = repetition index. `attempts` = total LLM calls (all failed). `confidence` = agent self-reported confidence on the final answer. `score/delta` = normalized rubric score (textual) or |answer − ground_truth| (math)._

### Retries triggered (3)

| role | task_id | rep | attempts | final_verdict |
| --- | --- | --- | --- | --- |
| expert | task8_vuln_udm | 1 | 3 | wrong |
| expert | task8_vuln_udm | 2 | 3 | wrong |
| expert | task8_vuln_udm | 3 | 3 | wrong |

_Each row is one repetition. `rep` = repetition index (1-based). `attempts` = LLM calls within that repetition (2 means wrong on attempt 1, correct on attempt 2). `final_verdict` = outcome after all attempts._

