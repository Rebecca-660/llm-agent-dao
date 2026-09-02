# Endpoint Pilot preregistered machine checks

- Source: `03_raw_outputs/pilot/pilot_20260901T101427Z_d4d53cb9.jsonl`
- Source SHA-256: `666e8142b5f80260bd384aca86f88614cc5257cd4addbfc5cf379e63c2a3c1e3`
- Pilot run ID: `pilot_20260901T101427Z_d4d53cb9`
- Scope: this Pilot JSONL only; no Smoke or Tiny Run data included.

## Results

| Preregistered criterion | Threshold | Observed | Machine result |
|---|---|---|---|
| Cell completeness and isolation | 48 unique P01-P16 × S/C0/T3; one Pilot run; independent context | 48 records, 48 unique; S=16, C0=16, T3=16; missing=0; duplicates=0; all `run_type=pilot`; all contexts independent | **PASS** |
| C0 mean dynamic range | 15%–75% inclusive | n=16; mean=50.00% | **PASS** |
| C0 category diversity | At least 3 categories | 1 category: [50] | **FAIL** |
| Combined category concentration | Maximum category share ≤85% | counts={50: 48}; maximum=100.00% | **FAIL** |
| Structured-output validity | At least 46/48 valid non-refusals | 48/48 (100.00%); parse failures=0; explicit-refusal screen=0; API errors=0; empty=0 | **PASS** |

## Boundary and pending human checks

The table reports each prespecified machine criterion separately. It does **not** make the researcher's final Pilot pass/fail decision. The prespecified 12-record human review for material factual hallucination and T3 executed/verifiable-action comprehension remains pending.

No treatment-effect ordering, expected direction, statistical significance, p-value, or minimum effect size was calculated or used as a criterion.

The refusal count is a reproducible narrow machine screen using the regex stored in `machine_checks.json`; sampled responses still require human judgment under the preregistered definitions.
