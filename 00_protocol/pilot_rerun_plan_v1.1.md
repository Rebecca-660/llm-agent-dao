# Endpoint Pilot Rerun Plan v1.1

## Registration status and authority boundary

- Plan version: `v1.1`
- Plan date: `2026-09-02`
- Status: pre-data rerun plan
- Original checks: `00_protocol/preregistered_checks.md`
- First-Pilot decision: `00_protocol/pilot_decision_v1.0.md`
- Output-requirement change record: `00_protocol/output_requirement_v1.1_change_record.md`
- v1.1 dry-run evidence: `validation/pilot_v1.1_dry_run/`

This plan was written before any v1.1 Pilot response was generated or inspected. It does not change the original preregistered thresholds and does not authorize an API call, material freeze, or main run. This file and the approved v1.1 implementation/evidence must be committed before the researcher separately authorizes execution of the rerun.

## First-Pilot failure evidence

- Run ID: `pilot_20260901T101427Z_d4d53cb9`
- Raw output: `03_raw_outputs/pilot/pilot_20260901T101427Z_d4d53cb9.jsonl`
- Raw-output SHA-256: `666e8142b5f80260bd384aca86f88614cc5257cd4addbfc5cf379e63c2a3c1e3`
- Machine evidence: `05_processed_data/pilot_diagnostics/machine_checks.md` and `machine_checks.json`

The first Pilot contained all 48 expected cells, and 48/48 responses were valid and parsed successfully. All 48 responses selected `unstake_percentage = 50`. It failed two prespecified design-quality criteria:

1. C0 response-category diversity was 1 category rather than at least 3.
2. The pooled maximum category share was 100% rather than at most 85%.

The first Pilot passed cell completeness/isolation, the inclusive 15%–75% C0 mean check, and the 46/48 structured-output-validity requirement. Its pending researcher decision does not authorize freeze or a main run.

## Repair hypothesis and causal boundary

Every first-Pilot assembled prompt contained the completed answer example `"unstake_percentage": 50`, and every raw response selected that value. The repair hypothesis is that presenting one valid outcome as a completed JSON example may have anchored the model on 50 and contributed to the observed category concentration.

This is a design hypothesis, not an established causal finding. The first Pilot cannot distinguish example anchoring from midpoint preference, coarse-category behavior, model-specific behavior, or other causes. The rerun tests whether removing the completed answer example restores acceptable response variation while holding all other experimental materials fixed. It does not guarantee that the original thresholds will pass.

## Sole experimental-material change

The rerun changes only the versioned output-requirement component:

- Old: `01_prompts/output_schema/json_schema_v1.0.txt`
  - SHA-256: `85915c44fe1e083ef06e23eb1e645a890d8ebf9a5088c33209da5024ddd95076`
- New: `01_prompts/output_schema/json_schema_v1.1.txt`
  - SHA-256: `7ca5b6896c2e115d99d7edc8314899d95669e0fb0e919c96472074840d509452`

Version v1.1 removes the completed numeric answer example. It preserves the fields `unstake_percentage` and `reason`, the five allowed integer values `0/25/50/75/100`, one concise non-empty reason, and JSON-only output. The researcher approved the explicit formatting clarifications: exactly two fields and no additional commentary, Markdown, or code fences.

No change is permitted to:

- protocol name;
- the 16-persona grid or persona template;
- common shock;
- canonical S, C0, or T3 treatment wording;
- decision time;
- outcome question;
- canonical ascending answer order;
- system prompt;
- decoding temperature;
- parser validity rules; or
- retry and append-only recording rules.

The code change that makes the material version explicit is an implementation/provenance control, not an additional experimental-material change. The v1.1 dry-run comparison reports that all 48 same-cell prompt prefixes are byte-identical after removing their final versioned output-requirement component, and that all other source hashes match.

## Fixed rerun design

- Design: 16 personas × `S/C0/T3` = 48 planned cells.
- Persona IDs: exactly `P01` through `P16`.
- Each arm: exactly 16 cells.
- Treatment wording: canonical v1.0 wording.
- Answer order: canonical ascending `0%, 25%, 50%, 75%, 100%`.
- Output requirement: explicit `v1.1` selection.
- Requested model: `gpt-4o-mini`, matching the first Pilot request.
- Decoding temperature: `0`.
- Context: independent for every persona×arm cell; `previous_response_id` must be null.
- Run type: `pilot`.
- Run ID: a new unique execution `run_id`, never the first-Pilot run ID and never a dry-run ID.
- Output: a new exclusively created append-only JSONL and a separate attempt log.
- Model version: the provider-returned exact version must be recorded. Any difference from the first Pilot's recorded `gpt-4o-mini-2024-07-18` must be reported as a comparability issue rather than concealed.

Network timeouts, rate limits, and server errors may follow the existing fixed retry rule, with every attempt logged. A successfully returned model response that is invalid, refused, or surprising must be retained as observed and must not be re-asked for content repair.

## Original machine criteria, carried forward unchanged

### 1. Cell completeness and isolation

- Exactly 48 planned persona×arm cells: 16 personas × `S/C0/T3`.
- Each expected cell occurs exactly once within the new Pilot run.
- Missing, duplicate, unexpected, failed, and retried cells are reported.
- Every final record has the new `run_id` and `run_type: "pilot"`.
- Smoke, Tiny Run, dry-run, first-Pilot, and main-run records are excluded from the rerun diagnostics.

### 2. C0 mean dynamic range

- Denominator: valid, non-refusal C0 responses only.
- PASS: `15 ≤ C0 mean ≤ 75`.
- FAIL: mean below 15, above 75, or not calculable.

### 3. C0 response-category diversity

- Denominator: valid, non-refusal C0 responses only.
- PASS: at least 3 distinct categories among `0/25/50/75/100`.
- FAIL: fewer than 3 distinct categories.

### 4. Combined category concentration

- Denominator: valid, non-refusal responses pooled across S, C0, and T3.
- PASS: maximum single-category share `≤ 0.85`.
- FAIL: maximum single-category share `> 0.85`, or no valid pooled denominator.

### 5. Structured-output validity

- Denominator: all 48 planned responses; API errors and empty responses remain in the denominator.
- Valid and non-refusal retains the exact definition in `preregistered_checks.md`.
- PASS: at least 46/48 valid non-refusal responses (`≥95%` under the original integer-count rule).
- FAIL: fewer than 46/48.
- Parsing failures, schema-invalid responses, refusals, API errors, and empty responses are reported separately and are never coerced into a valid outcome.

## Original manual criteria, carried forward unchanged

### Sampling procedure

- Formal sample size: exactly 12 records, stratified as 4 S, 4 C0, and 4 T3.
- Seed: `20260901`.
- Use only the single completed v1.1 Pilot run identified by its new `run_id`.
- Within each arm, sort records by `persona_id` ascending from P01 to P16.
- In Python 3.11, initialize an independent `random.Random(20260901)` instance for each arm and call `sample(sorted_arm_records, 4)` once.
- Preserve selected IDs and reproducibility evidence.
- Never replace a sampled record because it is invalid, refused, inconvenient, surprising, or inconsistent with a hypothesis.

### 6. Material factual hallucination

- The researcher records a PASS/FAIL judgment and short rationale for every sampled response.
- PASS: at least 11/12 sampled responses contain no materially hallucinated factual claim under the original definition.
- FAIL: fewer than 11/12 pass.

### 7. T3 executed/verifiable-action comprehension

- All 4 sampled T3 responses must remain consistent with the action being already executed and publicly verifiable.
- They must not recast the reserve as a future verbal promise, holder compensation, increased yield, or a token-price guarantee.
- PASS: all 4 pass.
- FAIL: one or more materially misunderstand the action.

A supplemental read-through of all 48 responses may be recorded for the teacher's workflow requirement, but it must not replace the fixed 12-record formal sample or change either formal human threshold.

## Prohibited decision criteria

None of the following may be used to pass, fail, tune, or freeze the rerun:

- `S > T3`, `C0 > T3`, `S > C0`, or any other expected treatment ordering;
- a required positive or negative contrast;
- statistical significance, p-values, or confidence-interval exclusion;
- a minimum treatment-effect size;
- agreement with the researcher's preferred result; or
- further wording changes merely because effects are null, small, reversed, or surprising.

Treatment means and distributions may be viewed only as required for the carried-forward dynamic-range and category checks. No treatment-effect analysis from either Pilot may enter the main-run dataset.

## Data isolation and preservation

1. The first-Pilot JSONL and logs remain immutable and are never overwritten, deleted, truncated, repaired, or selectively discarded.
2. The v1.1 Pilot uses a new `run_id`, new JSONL, and new attempt log created exclusively before writing.
3. First-Pilot and v1.1-Pilot records are never pooled for any threshold calculation.
4. Diagnostics must accept an explicitly selected v1.1 run and reject accidental inclusion of Smoke, Tiny Run, dry-run, first-Pilot, or main-run data.
5. Pilot records are design-calibration data only and never enter a main-run analysis dataset, even when persona and arm identifiers match later main cells.
6. Any later main run must occur only after a separate researcher PASS decision and formal material freeze, and must use still newer run IDs.
7. All failures, retries, invalid responses, refusals, and raw model text remain preserved exactly as observed.

## Preconditions before any API execution

- [x] Output Requirement v1.1 exists as a separate approved formal file; v1.0 remains preserved.
- [x] The assembler/runner explicitly selects and records the output-requirement version/path/hash.
- [x] The v1.1 zero-API dry-run contains exactly 48 unique cells and reports no concrete completed outcome example.
- [x] The researcher marked the v1.1 rendered requests `APPROVE` for rerun planning and explicitly stated that this was not API authorization.
- [ ] Correct the v1.1 dry-run checklist's entered review date if it precedes the generated dry-run evidence; preserve the correction transparently.
- [ ] Commit the approved v1.1 material, provenance record, implementation/tests, dry-run evidence, researcher review, and this plan before API execution.
- [ ] Verify a clean, reviewable Git status for all files entering the rerun snapshot.
- [ ] Obtain a separate, explicit researcher instruction authorizing the 48 real API calls and their cost.

Until every unchecked precondition is satisfied, the v1.1 Pilot rerun is **not authorized**.

## Post-rerun decision boundary

After the new run is complete, the original machine checks and fixed-seed human checks must be calculated and reported without threshold changes. The researcher alone records `PASS`, `FAIL`, or `PENDING` and whether freeze is authorized. A passing Pilot permits a later freeze step but does not itself freeze materials or convert Pilot data into main-run data.
