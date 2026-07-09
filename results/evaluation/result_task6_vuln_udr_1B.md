# 1B — task6_vuln_udr

## Summary

| metric | value |
| --- | --- |
| total results | 2 |
| correct | 2 (100.0%) |
| wrong | 0 |
| retried (attempts > 1) | 0 |
| truly inconsistent tasks | 0 |
| surface-only differences (semantically equiv.) | 0 |

_truly inconsistent_: LLM confirmed different conclusions across repetitions. _surface-only_: string-different but semantically equivalent (paraphrases, same logic).

All tasks passed with full consistency — no anomalies detected.

## Scores by role

| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_textual_norm |
| --- | --- | --- | --- | --- | --- |
| beginner | 100.0% | 1.000 | 0.0000 | 1.00 | 1.000 |
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
| beginner | 1/1 | 1 | 2 | 1 | 1.00 | 1.00 | 4.00 | 1.00 |
| expert | 1/1 | 1 | 2 | 2 | 2.00 | 2.00 | 4.00 | 1.00 |

_`estimates` = repetitions where the agent produced a CVSS block. `matched` = findings paired to a ground-truth CVE via handler function. `band vs published` compares against the published score (BT where the vector includes Threat E); `band vs B` against the pure base score. Exploitability counts AV/AC/AT/PR/UI matches; impact counts VC/VI/VA — the impact triad is the discriminating signal on this dataset._

