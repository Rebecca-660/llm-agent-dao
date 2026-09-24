# Independent arithmetic check

This is the prespecified manual arithmetic check, separate from the analysis script.

## One arm mean: S

The 15 valid S values in `persona_arm_outcomes.csv` contain thirteen `25` values and two `0` values; P11 is missing.

`(13 × 25 + 2 × 0) / 15 = 325 / 15 = 21.6666667`

Scripted result in `arm_summary.csv`: `21.666666666666668`.

Result: **MATCH** (21.67% when displayed to two decimals).

## One persona-level paired difference: P01, C0 − S

P01 has `C0 = 25` and `S = 25`.

`25 − 25 = 0` percentage points.

Scripted result in `paired_differences.csv`: `0` percentage points.

Result: **MATCH**.

This verifies arithmetic transcription only. It does not review response content or alter any result.
