# Evaluation Report: 1B

## Summary

| metric | value |
| --- | --- |
| total results | 30 |
| correct | 30 (100.0%) |
| wrong | 0 |
| retried (attempts > 1) | 0 |
| truly inconsistent tasks | 1 |
| surface-only differences (semantically equiv.) | 9 |

_truly inconsistent_: LLM confirmed different conclusions across repetitions. _surface-only_: string-different but semantically equivalent (paraphrases, same logic).

## Anomalies

### Truly inconsistent reasoning (1)

**beginner — task2_math_real**
> Passage 3 contains a minor calculation error in the sum of squared deviations (12040.06) compared to the correct value used in Passages 1 and 2 (12038.06), making the intermediate key claims different.

- **rep 1:** To calculate the arithmetic mean, sum the values: 312.4 + 298.7 + 415.2 + 389.6 + 301.1 = 1717.0. Then divide by N=5: 1717.0 / 5 = 343.4, rounded to two decimals is 343.40 Mbps. For sample standard deviation, first find the mean, which is 343.4. Then compute each deviation from the mean: -31.0, -44.7, 71.8, 46.2, -42.3. Square each deviation: 961.00, 1998.09, 5155.24, 2134.44, 1789.29. Sum the squared deviations: 961.00 + 1998.09 + 5155.24 + 2134.44 + 1789.29 = 12038.06. Then, divide by N-1=4 to get variance: 12038.06 / 4 = 3009.515. Finally, take the square root of the variance: sqrt(3009.515) ≈ 54.86 Mbps, rounded to two decimals.

- **rep 2:** Calculated the arithmetic mean by summing the values: 312.4 + 298.7 + 415.2 + 389.6 + 301.1 = 1717.0, then dividing by 5 to get 343.40. For sample standard deviation, calculated each value minus the mean, squared the differences, summed them to 12038.06, divided by N-1=4 to get variance 3009.515, then took the square root to get approximately 54.86.

- **rep 3:** The arithmetic mean is calculated by summing the values: 312.4 + 298.7 + 415.2 + 389.6 + 301.1 = 1717.0. Then divide by N=5: 1717.0 / 5 = 343.40. For sample standard deviation, first find the squared differences from the mean: (312.4 - 343.4)^2 = 961, (298.7 - 343.4)^2 = 2000.09, (415.2 - 343.4)^2 = 5155.24, (389.6 - 343.4)^2 = 2134.44, (301.1 - 343.4)^2 = 1789.29. Sum these: 961 + 2000.09 + 5155.24 + 2134.44 + 1789.29 = 12040.06. Then divide by N-1=4: 12040.06 / 4 = 3010.015. Finally, take the square root: sqrt(3010.015) ≈ 54.8636, rounded to two decimals is 54.86.


## Scores by role

| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_math_delta | avg_textual_norm |
| --- | --- | --- | --- | --- | --- | --- |
| beginner | 100.0% | 0.797 | 0.0488 | 1.00 | 0.000 | 0.975 |
| expert | 100.0% | 0.990 | 0.0005 | 1.00 | 0.005 | 0.988 |

**Legend**

| metric | scope | meaning |
| --- | --- | --- |
| `accuracy` | all | share of repetitions with verdict = correct |
| `avg_confidence` | all | mean self-reported confidence (0–1) |
| `brier_score` | all | mean((confidence − is\_correct)²) — lower = better calibration; 0 = perfect, 0.25 = random |
| `avg_attempts` | all | mean LLM call attempts per repetition (>1 means retry was triggered) |
| `avg_math_delta` | math | mean \|answer − ground\_truth\| on math tasks — lower = more precise |
| `avg_textual_norm` | textual | mean normalized judge score (0–1) — higher = better rubric coverage |

