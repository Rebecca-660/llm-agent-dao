# Main v1.2 minimum-scope analysis

This directory implements only the quantitative analyses prespecified in `00_protocol/main_run_plan_v1.2.md`. It uses the accepted processed dataset for `main_20260904T160520Z_d93b455f`; no Pilot, Tiny Run, dry-run, smoke, or connectivity-check observations are included.

Reproduce from the project root with:

```powershell
python -B 05_processed_data/main_v1.2/generate_processed_dataset.py
python -B 06_analysis/main_v1.2/analyze_main.py
```

Outputs:

- `arm_summary.csv`: valid/missing denominators, means, medians, and AnyUnstake summaries;
- `outcome_distribution.csv`: complete five-category distribution by arm;
- `persona_arm_outcomes.csv`: the 16 × 5 outcome table;
- `paired_differences.csv`: every persona-level adjacent-arm difference, including explicit omissions;
- `paired_contrast_summary.csv`: four primary estimands and sign counts/proportions;
- `exact_sign_flip_results.json`: exact enumeration metadata and p-values;
- `results.json`: combined machine-readable results.

Figures are written to `07_figures/main_v1.2/`. P-values are finite-profile diagnostics and are not population inference about human investors. No optional regression, reason coding, or exploratory analysis is included here.
