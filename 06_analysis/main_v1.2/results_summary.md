# Main v1.2 prespecified minimum-scope results

## Scope and analysis population

This analysis uses only `main_20260904T160520Z_d93b455f`. It excludes all Pilot, Tiny Run, dry-run, smoke, and connectivity-check data. Of 80 planned cells, 79 produced valid parsed outcomes. `P11_S` remains missing and is excluded only from summaries requiring its outcome and from the `C0-S` pair for P11; it is not imputed or coded as 0%.

## Arm-level descriptive results

| Arm | Valid / planned | Missing | Mean unstake % | Median | AnyUnstake n / valid | AnyUnstake rate |
|---|---:|---:|---:|---:|---:|---:|
| S | 15 / 16 | 1 | 21.67 | 25 | 13 / 15 | 86.67% |
| C0 | 16 / 16 | 0 | 25.00 | 25 | 15 / 16 | 93.75% |
| T1 | 16 / 16 | 0 | 18.75 | 25 | 11 / 16 | 68.75% |
| T2 | 16 / 16 | 0 | 17.19 | 25 | 11 / 16 | 68.75% |
| T3 | 16 / 16 | 0 | 9.38 | 0 | 6 / 16 | 37.50% |

The complete category counts and valid denominators are in `outcome_distribution.csv`; the full 16 × 5 table is in `persona_arm_outcomes.csv`. No ordering is treated as a quality gate or success criterion.

## Prespecified adjacent-arm paired differences

Differences are in percentage points and use first-named arm minus second-named arm.

| Contrast | Complete pairs | Omitted | Mean | Median | Min to max | Negative / zero / positive | Exact two-sided p |
|---|---:|---|---:|---:|---:|---:|---:|
| C0 − S | 15 | P11 | 3.33 | 0 | −25 to 25 | 1 / 11 / 3 | 0.6250 |
| T1 − C0 | 16 | none | −6.25 | 0 | −25 to 25 | 5 / 10 / 1 | 0.2188 |
| T2 − T1 | 16 | none | −1.56 | 0 | −25 to 25 | 2 / 13 / 1 | 1.0000 |
| T3 − T2 | 16 | none | −7.81 | 0 | −25 to 0 | 5 / 11 / 0 | 0.0625 |

The exact tests enumerate every `2^n` sign assignment, retain zero differences, use the absolute mean difference, and include equality in the tail count. These p-values are finite-profile diagnostics for the 16 fixed personas; they are not population inference about real investors and do not determine which findings are reported or considered important.

## Analysis classification and limits

Everything reported above is prespecified in `main_run_plan_v1.2.md`. No exploratory analysis, optional fixed-effects regression, reason coding, robustness wording, reverse answer order, additional temperature, or second model is included. The results describe this fixed set of LLM-agent profiles under one model and configuration; they do not establish human behavioral effects or broad robustness.
