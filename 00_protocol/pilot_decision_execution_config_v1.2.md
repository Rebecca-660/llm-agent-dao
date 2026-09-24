# Endpoint Pilot Decision — Execution Configuration v1.2

## Decision status

- Pilot run ID: `pilot_20260904T150852Z_18e62216`
- Provider/model: `zhipu` / `glm-4.7`
- Execution configuration: `stochastic_low_v1.2`
- Decision date recorded in the manual checklist: `2026-09-04`
- Researcher name/initials recorded in the manual checklist: `CDY`
- Overall decision: **PASS**
- Formal material freeze authorized: **YES**
- Main-run preparation authorized: **YES**

Researcher `CDY` explicitly confirmed the third-round Pilot as `PASS` and authorized proceeding to formal material freeze and main-run preparation. The researcher also explicitly chose not to add the preregistered per-record short rationales and accepted that record limitation. This authorization permits the later preparation steps; this record does not itself execute a freeze or a main run.

## Sources

- Prespecified criteria: `00_protocol/preregistered_checks.md`
- Fixed single-factor plan: `00_protocol/pilot_execution_config_plan_v1.2.md`
- Machine evidence: `05_processed_data/pilot_execution_config_v1.2_diagnostics/machine_checks.md`
- Machine-readable evidence: `05_processed_data/pilot_execution_config_v1.2_diagnostics/machine_checks.json`
- Fixed-seed sample record: `05_processed_data/pilot_execution_config_v1.2_diagnostics/sample_manifest.json`
- Researcher review record: `validation/pilot_execution_config_v1.2_manual_review/manual_review_checklist.md`
- Review packet: `validation/pilot_execution_config_v1.2_manual_review/review_packet.md`

Only `run_id=pilot_20260904T150852Z_18e62216` is represented in the decision evidence. Historical Pilots, Tiny Runs, dry-runs, and connectivity checks are excluded.

## Five preregistered machine criteria

### 1. Cell completeness and isolation — PASS

- Threshold: exactly 48 unique P01–P16 × S/C0/T3 cells, with 16 cells per arm, from one new Pilot run.
- Observed: 48 records; 48 unique cells; S=16, C0=16, T3=16; no missing, unexpected, or duplicate cells.
- Result: **PASS**.

### 2. C0 mean dynamic range — PASS

- Threshold: valid, non-refusal C0 mean between 15% and 75%, inclusive.
- Observed: 16 valid C0 responses; mean `25.0%`.
- Result: **PASS**.

### 3. C0 response-category diversity — PASS

- Threshold: at least 3 distinct valid, non-refusal C0 categories.
- Observed: 3 categories; 0%=1, 25%=14, 50%=1, 75%=0, 100%=0.
- Result: **PASS**.

### 4. Combined category concentration — PASS

- Threshold: no category may exceed 85% of pooled valid, non-refusal S/C0/T3 responses.
- Observed: the largest category was 25%, with 34/48 responses (`70.8333%`).
- Result: **PASS**.

### 5. Structured-output validity — PASS

- Threshold: at least 46/48 responses must be valid and non-refusal.
- Observed: 48/48 valid and non-refusal; 48 API successes; 0 API failures; 48 parse successes; 0 parse failures; 0 empty responses; 0 retries.
- Result: **PASS**.

Machine-check summary: **5/5 PASS**.

## Fixed-seed formal human review

The formal sample used `seed=20260901`, an independent `random.Random(20260901)` instance within each arm, ascending P01–P16 candidate order, and no replacement or substitution.

- S: `P15_S`, `P01_S`, `P14_S`, `P09_S`
- C0: `P15_C0`, `P01_C0`, `P14_C0`, `P09_C0`
- T3: `P15_T3`, `P01_T3`, `P14_T3`, `P09_T3`

The following is recorded exactly at the summary level present in the completed checklist:

- Material factual hallucination: all 12 judgments marked `PASS`; recorded count `12/12`; threshold result `PASS`.
- T3 executed/publicly-verifiable-action comprehension: all 4 judgments marked `PASS`; recorded count `4/4`; threshold result `PASS`.
- Researcher: `CDY`.
- Decision date: `2026-09-04`.
- Per-record short rationales: blank; the checklist records that the researcher explicitly chose not to provide them.

This decision record does not invent, summarize, or backfill rationales for the researcher.

## Supplemental 48-record review

The all-48 supplemental reading exercise was not repeated under the v1.2 acceleration plan. `00_protocol/pilot_execution_config_plan_v1.2.md` explicitly states that it was an additional teacher-workflow quality audit rather than a preregistered pass threshold. Its omission does not change the fixed 12-record sample or either formal human threshold.

## Decision boundary

The evidence supports five machine `PASS` results and the researcher's entered `12/12` and `4/4` human judgments. Researcher `CDY` explicitly confirmed an overall `PASS`, authorized formal material freeze and main-run preparation, and accepted the documented omission of per-record short rationales. Therefore:

- overall Pilot decision is **PASS**;
- formal material freeze is **authorized**;
- main-run preparation is **authorized**;
- this file does not execute a freeze or a main run.

The status above is based only on the preregistered design-quality criteria and the completion state of the decision record. It is not based on treatment ordering, statistical significance, effect size, contrast direction, or agreement with an expected result. No treatment-effect analysis is made here.
