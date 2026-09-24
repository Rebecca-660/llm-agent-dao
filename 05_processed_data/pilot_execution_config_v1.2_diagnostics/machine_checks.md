# Pilot execution-config v1.2 machine checks

- Run ID: `pilot_20260904T150852Z_18e62216`
- Overall machine result: **PASS** (5/5)
- Scope: only the raw output and attempt log named above; no historical Pilot, Tiny Run, dry-run, or connectivity-check data were included.
- These are design-quality checks, not treatment-effect analysis.

## API and parsing status

- Raw records: 48/48
- Attempt records: 48
- API successes/failures: 48/0
- Parse successes/failures: 48/0
- Retry attempts: 0

## Five preregistered machine criteria

### 1. Cell completeness and isolation

- Threshold: exactly 48 unique P01-P16 x S/C0/T3 cells, 16 per arm, one pilot run
- Observed: `{"arm_counts": {"C0": 16, "S": 16, "T3": 16}, "duplicates": [], "missing": [], "records": 48, "unexpected": [], "unique_cells": 48}`
- Result: **PASS**

### 2. C0 mean dynamic range

- Threshold: 15 <= valid non-refusal C0 mean <= 75
- Observed: `{"mean": 25.0, "valid_c0_n": 16}`
- Result: **PASS**

### 3. C0 response-category diversity

- Threshold: at least 3 distinct valid non-refusal C0 categories
- Observed: `{"category_count": 3, "counts": {"0": 1, "100": 0, "25": 14, "50": 1, "75": 0}}`
- Result: **PASS**

### 4. Combined category concentration

- Threshold: maximum pooled valid non-refusal category share <= 0.85
- Observed: `{"counts": {"0": 13, "100": 0, "25": 34, "50": 1, "75": 0}, "largest_category": 25, "largest_count": 34, "largest_share": 0.7083333333333334, "valid_n": 48}`
- Result: **PASS**

### 5. Structured-output validity

- Threshold: at least 46 of 48 valid non-refusal responses
- Observed: `{"api_errors": 0, "empty_responses": 0, "invalid": 0, "parse_failures": 0, "refusals": 0, "valid_non_refusal": 48}`
- Result: **PASS**

## Formal manual sample

- Seed: `20260901`
- Python runtime: `3.14.4`
- Independent `random.Random(20260901)` instance per arm after sorting P01-P16.
- No replacement or substitution is permitted.
- S: `P15_S, P01_S, P14_S, P09_S`
- C0: `P15_C0, P01_C0, P14_C0, P09_C0`
- T3: `P15_T3, P01_T3, P14_T3, P09_T3`

The researcher must complete the formal 12-record review. This report does not make the final Pilot decision.
