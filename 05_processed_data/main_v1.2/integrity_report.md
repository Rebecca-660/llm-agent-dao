# Main v1.2 engineering acceptance report

**Result: PASS**

- Authorized run: `main_20260904T160520Z_d93b455f` only
- Raw records / unique cells: 80 / 80
- Arm counts: S=16, C0=16, T1=16, T2=16, T3=16
- Attempt records: 80; scheduled retries: 0
- API successes: 80/80
- Valid parsed outcomes: 79/80 (98.75%)
- Parse failures: 1 (`P11_S`)
- Illegal values: 0
- Empty responses: 0
- Explicit refusals: 0
- API errors: 0
- Missing, unexpected, or duplicate cells: 0 / 0 / 0

`P11_S` remains missing for `unstake_percentage`, `any_unstake`, and `reason`. Its raw response and parser error remain accessible through the raw line locator and hashes; it was not repaired, re-asked, coerced, or imputed.

Pilot, Tiny Run, dry-run, smoke, and connectivity-check records were not read into or included in this dataset. No treatment-effect comparison was computed.
