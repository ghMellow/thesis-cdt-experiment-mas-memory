# 1A — task8_vuln_udm

## Summary

| metric | value |
| --- | --- |
| total results | 6 |
| correct | 6 (100.0%) |
| wrong | 0 |
| retried (attempts > 1) | 2 |
| truly inconsistent tasks | 0 |
| surface-only differences (semantically equiv.) | 2 |

_truly inconsistent_: LLM confirmed different conclusions across repetitions. _surface-only_: string-different but semantically equivalent (paraphrases, same logic).

## Scores by role

| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_textual_norm |
| --- | --- | --- | --- | --- | --- |
| beginner | 100.0% | 0.917 | 0.0075 | 1.33 | 0.778 |
| expert | 100.0% | 1.000 | 0.0000 | 1.67 | 0.778 |

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

### Retries triggered (2)

| role | task_id | rep | attempts | final_verdict |
| --- | --- | --- | --- | --- |
| beginner | task8_vuln_udm | 1 | 2 | correct |
| expert | task8_vuln_udm | 1 | 3 | correct |

