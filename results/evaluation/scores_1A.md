# Evaluation Report: 1A

## Summary

| metric | value |
| --- | --- |
| total results | 24 |
| correct | 24 (100.0%) |
| wrong | 0 |
| retried (attempts > 1) | 1 |
| truly inconsistent tasks | 2 |
| surface-only differences (semantically equiv.) | 6 |

_truly inconsistent_: LLM confirmed different conclusions across repetitions. _surface-only_: string-different but semantically equivalent (paraphrases, same logic).

## Anomalies

### Retries triggered (1)

| role | task_id | rep | attempts | final_verdict |
| --- | --- | --- | --- | --- |
| expert | task2_math_real | 2 | 2 | correct |

### Truly inconsistent reasoning (2)

**beginner — task2_math_real**
> Rep 1 and 2 compute sqrt(3009.515) ≈ 54.8500 and round to 54.85; rep 3 reports sqrt(3009.515) = 54.8570 and rounds to 54.86 — different final numerical answers for the standard deviation.

- **rep 1:** The input data (X) is {312.4, 298.7, 415.2, 389.6, 301.1}. N = 5.  1. Calculate the Arithmetic Mean (Mean): Sum = 312.4 + 298.7 + 415.2 + 389.6 + 301.1 = 1717.0 Mean = Sum / N = 1717.0 / 5 = 343.40  2. Calculate the Sample Standard Deviation (s): First, calculate the squared differences from the mean (Mean = 343.40): (312.4 - 343.4)^2 = (-31.0)^2 = 961.00 (298.7 - 343.4)^2 = (-44.7)^2 = 1998.09 (415.2 - 343.4)^2 = (71.8)^2 = 5155.24 (389.6 - 343.4)^2 = (46.2)^2 = 2134.44 (301.1 - 343.4)^2 = (-42.3)^2 = 1789.29  Sum of squared differences = 961.00 + 1998.09 + 5155.24 + 2134.44 + 1789.29 = 12038.06  Sample Variance (s^2) = Sum of squared differences / (N - 1) = 12038.06 / (5 - 1) = 12038.06 / 4 = 3009.515  Sample Standard Deviation (s) = sqrt(3009.515)   std = 54.8500...  Rounded to 2 decimal places, std = 54.85.

- **rep 2:** The input data points (X) are: 312.4, 298.7, 415.2, 389.6, 301.1. N = 5.  1. Calculate the Arithmetic Mean (Mean): Sum of values (Σx) = 312.4 + 298.7 + 415.2 + 389.6 + 301.1 = 1717.0 Mean (x̄) = Σx / N = 1717.0 / 5 = 343.40  2. Calculate the Sample Standard Deviation (s): First, calculate the squared differences from the mean: (312.4 - 343.4)^2 = (-31.0)^2 = 961.00 (298.7 - 343.4)^2 = (-44.7)^2 = 1998.09 (415.2 - 343.4)^2 = (71.8)^2 = 5155.24 (389.6 - 343.4)^2 = (46.2)^2 = 2134.44 (301.1 - 343.4)^2 = (-42.3)^2 = 1789.29  Sum of squared differences (Σ(x-x̄)²): 961.00 + 1998.09 + 5155.24 + 2134.44 + 1789.29 = 12038.06  Calculate the Sample Variance (s²): s² = Σ(x-x̄)² / (N-1) = 12038.06 / (5 - 1) = 12038.06 / 4 = 3009.515  Calculate the Sample Standard Deviation (s): s = sqrt(3009.515)   s ≈ 54.8500  Rounding to 2 decimal places gives Mean = 343.40 and Std Dev = 54.85.

- **rep 3:** The input data (X) is: {312.4, 298.7, 415.2, 389.6, 301.1}. N = 5.  1. Calculate the Arithmetic Mean (Mean): Sum of values = 312.4 + 298.7 + 415.2 + 389.6 + 301.1 = 1717.0 Mean = Sum / N = 1717.0 / 5 = 343.40  2. Calculate the Sample Standard Deviation (s): First, calculate the squared differences from the mean (Mean = 343.40): (312.4 - 343.4)^2 = (-31.0)^2 = 961.00 (298.7 - 343.4)^2 = (-44.7)^2 = 1998.09 (415.2 - 343.4)^2 = (71.8)^2 = 5155.24 (389.6 - 343.4)^2 = (46.2)^2 = 2134.44 (301.1 - 343.4)^2 = (-42.3)^2 = 1789.29  Sum of squared differences = 961.00 + 1998.09 + 5155.24 + 2134.44 + 1789.29 = 12038.06  Sample Variance (s^2) = Sum of squared differences / (N - 1) = 12038.06 / (5 - 1) = 12038.06 / 4 = 3009.515  Sample Standard Deviation (s) = sqrt(3009.515) = 54.8570  Rounding to 2 decimal places gives: Mean = 343.40, Std Dev = 54.86.


**expert — task2_math_real**
> Rep 1 and 2 compute sqrt(3009.515) = 54.8500, rounding to 54.85; rep 3 computes sqrt(3009.515) = 54.8567, rounding to 54.86 — the final standard deviation value differs numerically.

- **rep 1:** The input data (throughput measurements) are X = {312.4, 298.7, 415.2, 389.6, 301.1}. N = 5.  1. Calculate the Arithmetic Mean (Mean): Sum of values (ΣX) = 312.4 + 298.7 + 415.2 + 389.6 + 301.1 = 1717.0 Mean (μ) = ΣX / N = 1717.0 / 5 = 343.40  2. Calculate the Sample Standard Deviation (s): First, calculate the squared differences from the mean: (312.4 - 343.4)² = (-31.0)² = 961.00 (298.7 - 343.4)² = (-44.7)² = 1998.09 (415.2 - 343.4)² = (71.8)² = 5155.24 (389.6 - 343.4)² = (46.2)² = 2134.44 (301.1 - 343.4)² = (-42.3)² = 1789.29  Sum of squared differences (Σ(X-μ)²): 961.00 + 1998.09 + 5155.24 + 2134.44 + 1789.29 = 12038.06  Calculate the Sample Variance (s²): N - 1 = 5 - 1 = 4 Variance (s²) = 12038.06 / 4 = 3009.515  Calculate the Sample Standard Deviation (s): Standard Deviation (s) = sqrt(3009.515) = 54.8500  Rounding the results to 2 decimal places gives Mean = 343.40 and Standard Deviation = 54.85.

- **rep 2:** The input data points (X) are: 312.4, 298.7, 415.2, 389.6, 301.1. N = 5.  1. Calculate the Arithmetic Mean (Mean): Sum of values (ΣX) = 312.4 + 298.7 + 415.2 + 389.6 + 301.1 = 1717.0 Mean (μ) = ΣX / N = 1717.0 / 5 = 343.40  2. Calculate the Sample Standard Deviation (s): First, calculate the squared differences from the mean: (312.4 - 343.4)^2 = (-31.0)^2 = 961.00 (298.7 - 343.4)^2 = (-44.7)^2 = 1998.09 (415.2 - 343.4)^2 = (71.8)^2 = 5155.24 (389.6 - 343.4)^2 = (46.2)^2 = 2134.44 (301.1 - 343.4)^2 = (-42.3)^2 = 1789.29  Sum of squared differences (Σ(X-μ)²): 961.00 + 1998.09 + 5155.24 + 2134.44 + 1789.29 = 12038.06  Calculate the Sample Variance (s²): s² = Σ(X-μ)² / (N-1) = 12038.06 / (5 - 1) = 12038.06 / 4 = 3009.515  Calculate the Sample Standard Deviation (s): s = sqrt(3009.515)   s ≈ 54.8500  Rounding to 2 decimal places: Mean = 343.40, Standard Deviation = 54.85.

- **rep 3:** The input data (throughput measurements) is X = {312.4, 298.7, 415.2, 389.6, 301.1}. N = 5.  1. Calculate the Arithmetic Mean (Mean): Sum of values = 312.4 + 298.7 + 415.2 + 389.6 + 301.1 = 1717.0 Mean = Sum / N = 1717.0 / 5 = 343.40  2. Calculate the Sample Standard Deviation (s): First, calculate the squared differences from the mean (Mean = 343.40): (312.4 - 343.4)^2 = (-31.0)^2 = 961.00 (298.7 - 343.4)^2 = (-44.7)^2 = 1998.09 (415.2 - 343.4)^2 = (71.8)^2 = 5155.24 (389.6 - 343.4)^2 = (46.2)^2 = 2134.44 (301.1 - 343.4)^2 = (-42.3)^2 = 1789.29  Sum of squared differences = 961.00 + 1998.09 + 5155.24 + 2134.44 + 1789.29 = 12038.06  Sample Variance (s^2) = Sum of squared differences / (N - 1) = 12038.06 / (5 - 1) = 12038.06 / 4 = 3009.515  Sample Standard Deviation (s) = sqrt(3009.515) = 54.8567  Rounding to 2 decimal places gives: Mean = 343.40, Std Dev = 54.86.


## Scores by role

| role | accuracy | avg_confidence | brier_score | avg_attempts | avg_math_delta | avg_textual_norm |
| --- | --- | --- | --- | --- | --- | --- |
| beginner | 100.0% | 0.954 | 0.0060 | 1.00 | 0.003 | 1.000 |
| expert | 100.0% | 0.979 | 0.0017 | 1.08 | 0.003 | 1.000 |

**Legend**

| metric | scope | meaning |
| --- | --- | --- |
| `accuracy` | all | share of repetitions with verdict = correct |
| `avg_confidence` | all | mean self-reported confidence (0–1) |
| `brier_score` | all | mean((confidence − is\_correct)²) — lower = better calibration; 0 = perfect, 0.25 = random |
| `avg_attempts` | all | mean LLM call attempts per repetition (>1 means retry was triggered) |
| `avg_math_delta` | math | mean \|answer − ground\_truth\| on math tasks — lower = more precise |
| `avg_textual_norm` | textual | mean normalized judge score (0–1) — higher = better rubric coverage |
