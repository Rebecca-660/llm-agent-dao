# Unstaking Mechanics v1.1 Endpoint Pilot — Preregistered Machine Checks

- Selected run ID: `pilot_20260904T135552Z_be4faaf7`
- Raw SHA-256: `2c6b01611e2f44a59d8039f7fa654cdb60df91d6c908ecc92005db3a34efc6f0`
- Attempt-log SHA-256: `bc1e2d1c5af16402b3189a83e7019dee3230867c44e574c4b0a88f07154676dd`
- Generator runtime: Python `3.14.4`
- Input isolation: only the selected raw output and its attempt log were loaded
- Old Pilot, Tiny Run, dry-run, and connectivity-check data: excluded
- Treatment ordering, significance, and effect size: not calculated

## Execution status

- API successes: **48/48**
- API errors: **0**
- Attempt records: **48**
- Retries scheduled: **0**
- Maximum attempt number: **1**
- Parse successes: **48/48**
- Parse failures: **0**

## Five preregistered machine criteria

| # | Criterion | Prespecified threshold | Observed | Result |
|---:|---|---|---|---|
| 1 | Cell completeness and isolation | Exactly 48 unique P01–P16 × S/C0/T3 cells; 16 per arm; one Pilot run | 48 records; 48 unique; S=16, C0=16, T3=16; missing=0, duplicate=0, unexpected=0 | **PASS** |
| 2 | C0 mean dynamic range | 15%–75%, inclusive | Valid C0 n=16; mean=21.875% | **PASS** |
| 3 | C0 response-category diversity | At least 3 categories | 2 categories; counts={0: 2, 25: 14} | **FAIL** |
| 4 | Combined category concentration | Maximum category share ≤0.85 | Valid pooled n=48; category 25 has 35/48 = 0.729167 | **PASS** |
| 5 | Structured-output validity | At least 46/48 valid and non-refusal | 48/48 = 1.000000; parse failures=0; refusals=0; API errors=0; empty=0 | **PASS** |

## Decision boundary

These results apply only to `pilot_20260904T135552Z_be4faaf7`. They are inputs to the researcher decision and do not alone authorize material freeze or a main run. The fixed-seed human review remains required. No treatment ordering, significance test, or effect-size criterion was used.
