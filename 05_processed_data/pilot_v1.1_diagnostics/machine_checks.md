# GLM-4.7 Endpoint Pilot — Preregistered Machine Checks

- Selected run ID: `pilot_20260903T055848Z_a5ef2915`
- Raw SHA-256: `5ee208decea0755a278d93f87ab6835ff09fe727c313a686802172e16bae5704`
- Generator runtime: Python `3.14.4`
- Historical Pilot files: inventoried and excluded from calculations
- Treatment ordering, contrasts, significance, and effect size: not calculated

## Five machine criteria

| # | Criterion | Threshold | Observed | Result |
|---:|---|---|---|---|
| 1 | Cell completeness and isolation | Exactly 48 unique P01-P16 x S/C0/T3 cells from one run; run_type=pilot | 48 records; 48 unique cells; S=16, C0=16, T3=16; no missing/duplicate/unexpected cells | **PASS** |
| 2 | C0 mean dynamic range | 15 <= mean <= 75 among valid non-refusal C0 responses | valid C0 n=16; mean=3.125% | **FAIL** |
| 3 | C0 response-category diversity | At least 3 distinct categories among valid non-refusal C0 responses | 2 categories; counts=0:14, 25:2 | **FAIL** |
| 4 | Combined category concentration | Maximum single-category share <= 0.85 among pooled valid non-refusal responses | valid pooled n=46; category 0 has 42/46 = 0.913043 | **FAIL** |
| 5 | Structured-output validity | At least 46 of all 48 planned responses valid and non-refusal | 46/48 = 0.958333; parse failures=2; refusal candidates=0; API errors=0; empty=0 | **PASS** |

## Preserved parse failures

- `P02_S`: Invalid JSON: Invalid control character at: line 3 column 233 (char 262)
- `P11_T3`: Invalid JSON: Expecting property name enclosed in double quotes: line 2 column 1 (char 2)

The two malformed responses remain unchanged and were not re-asked, repaired, or coerced.

## Decision boundary

These machine results are inputs to the researcher decision. They do not by themselves authorize material freeze or a main run. The formal 12-record human review remains required even when one or more machine criteria fail.
