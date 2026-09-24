# Endpoint Design Pilot — Preregistered Checks

## Registration status

- Protocol basis: Summer Project Protocol v1.1 and Atomic-Task Workflow v1.1
- Registration date: 2026-09-01
- Pilot design: 16 personas × 3 endpoint arms (`S`, `C0`, `T3`) = 48 planned calls
- Treatment wording: canonical wording only
- Answer order: canonical order (`0%, 25%, 50%, 75%, 100%`)
- Decoding temperature: `0`
- Stratified manual-review seed: `20260901`

This document was created before the Endpoint Pilot. It must be committed before any Endpoint Pilot API call is made. Pilot outputs must not be used to revise these checks retroactively.

## Purpose and decision boundary

The Endpoint Pilot evaluates design usability, dynamic range, prompt comprehension, and output quality. It is not a test of whether the hypothesized treatment ordering appears.

Pilot data are calibration data only. They must never be merged into a main-run analysis dataset, even when a Pilot persona and arm are identical to a later main-run cell.

## Response definitions

For these checks, a response is **valid and non-refusal** only when all of the following hold:

1. The API call returned a model response rather than an API error or empty value.
2. The response can be parsed under the prespecified parser procedure.
3. `unstake_percentage` is exactly one of `0`, `25`, `50`, `75`, or `100`.
4. `reason` is present and contains a non-empty concise explanation.
5. The response is not a refusal to make the requested in-character decision.

Invalid values must not be rounded or coerced. A refusal must not be coded as 0%. Parsing failures, refusals, API errors, and empty responses must be retained and reported separately.

## Machine-checkable criteria

### 1. Cell completeness and isolation

- Exactly 48 planned persona×arm cells must be attempted: 16 personas × `S/C0/T3`.
- Each expected cell must occur exactly once within the Pilot run.
- Duplicate and missing cells must be reported.
- Every record must use a new Pilot `run_id` and `run_type: "pilot"`.
- Smoke and Tiny Run records must not be included in Pilot diagnostics.

Cell completeness is an engineering requirement. API failures remain preserved as failed attempts and are not silently replaced merely to complete the matrix.

### 2. C0 mean dynamic range

Among valid, non-refusal C0 responses, the mean `unstake_percentage` must be between **15% and 75%, inclusive**.

- Pass: `15 ≤ C0 mean ≤ 75`.
- Fail: C0 mean below 15 or above 75.
- If no valid C0 mean can be calculated, this criterion fails.

This check detects an obvious floor or ceiling. It is not an effect-direction criterion.

### 3. C0 response-category diversity

Among valid, non-refusal C0 responses, at least **3 distinct categories** from `0/25/50/75/100` must appear.

- Pass: 3–5 distinct categories.
- Fail: fewer than 3 distinct categories.

### 4. Combined category concentration

Across valid, non-refusal responses pooled over `S`, `C0`, and `T3`, no single `unstake_percentage` category may account for more than **85%** of responses.

- Pass: maximum category share `≤ 0.85`.
- Fail: maximum category share `> 0.85`.

The denominator is the number of valid, non-refusal responses pooled across the three arms.

### 5. Structured-output validity

At least **95%** of all 48 planned responses must be valid and non-refusal.

- Required minimum: **46 of 48** responses.
- Pass: valid non-refusal count `≥ 46`.
- Fail: valid non-refusal count `< 46`.

Parsing failures and refusals must also be reported as separate counts and rates. API errors and empty values must be reported separately and cannot be removed from the denominator of 48.

## Prespecified stratified manual sample

Exactly 12 Pilot records will be selected for human review: 4 from `S`, 4 from `C0`, and 4 from `T3`.

The sampling procedure is fixed as follows:

1. Use only the single completed Endpoint Pilot run identified by its Pilot `run_id`.
2. Within each arm, sort the 16 records by `persona_id` in ascending order (`P01` through `P16`).
3. In Python 3.14.4, initialize an independent `random.Random(20260901)` instance for each arm.
4. Apply `sample(sorted_arm_records, 4)` once within each arm.
5. Preserve the selected IDs and sampling script/output as part of the Pilot review archive.

No sampled record may be replaced because its content is inconvenient, invalid, surprising, or inconsistent with the hypothesis. Invalid or refused sampled records remain in the human-review package and are evaluated as observed.

### Runtime-version implementation amendment

- Amendment date: `2026-09-03`
- Timing: after completion of the GLM-4.7 Pilot but before generation or inspection of the fixed-seed manual-review sample
- Original runtime entry: Python `3.11`
- Amended runtime entry: Python `3.14.4`, the Python runtime already installed in the research environment
- Researcher instruction: use the locally installed runtime rather than downloading a separate Python runtime

This amendment changes only the declared Python runtime used to execute the already-fixed sampling procedure. It does not change the seed (`20260901`), independent-per-arm initialization, ascending persona sort, sample size, arm allocation, non-replacement rule, human thresholds, or any Pilot response. The exact candidate lists, selected IDs, runtime version, and sampling output must be preserved so the realized sample remains directly auditable. The amendment was not motivated by treatment ordering, significance, effect size, or any sampled response because the sample had not yet been generated.

## Human-review criteria

### 6. Material factual hallucination

At least **11 of the 12** stratified sampled responses must contain no materially hallucinated factual claim.

A materially hallucinated factual claim includes, at minimum:

- stating or assuming that the staking contract was compromised or damaged when the prompt does not say so;
- stating or assuming that the holder's staked assets were already lost, frozen, or directly unsafe;
- inventing a token-price movement, broader market movement, liquidity need, compensation, reimbursement, yield change, governance result, additional exploit, or other decision-relevant event absent from the prompt;
- materially changing the stated timing, loss, shutdown status, audit status, or response action.

Minor stylistic inference that does not introduce a decision-relevant fact should be documented but does not automatically count as material hallucination. The human reviewer must record a pass/fail judgment and short rationale for each sampled response.

- Pass: at least 11/12 responses have no material factual hallucination.
- Fail: fewer than 11/12 pass.

### 7. T3 executed/verifiable-action comprehension

All 4 sampled T3 responses must treat the on-chain security-reserve action as **already executed and publicly verifiable**, rather than as a future promise or verbal assurance only.

For each sampled T3 response, the human reviewer must record whether it:

- recognizes or remains consistent with already-executed status;
- remains consistent with public on-chain verifiability;
- avoids rewriting the reserve as holder compensation, a yield increase, or a token-price guarantee.

- Pass: all 4 sampled T3 responses are consistent with the executed and verifiable nature of the action.
- Fail: one or more sampled T3 responses materially recast the action as merely planned, promised, unverifiable, or mechanically compensatory.

Any systematic misunderstanding observed outside the 4 sampled T3 records may be documented as additional diagnostic evidence, but the prespecified stratified sample remains the formal manual check.

## Criteria that are explicitly prohibited

None of the following may be used to pass, fail, tune, or freeze the Pilot materials:

- `S mean > T3 mean` or any other required treatment ordering;
- `C0 mean > T3 mean`, `S mean > C0 mean`, or a required sign for any contrast;
- statistical significance or a p-value threshold;
- a minimum treatment-effect size;
- agreement with the researcher's preferred or expected result;
- modifying wording merely because observed treatment differences are small, null, reversed, or surprising.

Treatment means and distributions may be viewed only for the preregistered dynamic-range and category checks above. A null or reversed treatment pattern must be accepted when material comprehension, dynamic range, structured output, and the other preregistered quality criteria pass.

## Pilot decision procedure

The researcher, not an AI tool, makes and signs the final Pilot pass/fail decision after reviewing:

1. the machine-checkable results;
2. the reproducible 12-record stratified sample;
3. the material-hallucination judgments;
4. the T3 comprehension judgments; and
5. any documented implementation failure.

If a prespecified design-quality criterion fails, any material revision must create a new protocol/prompt version. The failed Pilot raw outputs must be preserved unchanged, the reason for revision must be recorded, and the full 48-cell Endpoint Pilot must be rerun under a new `run_id`. Selective replacement of calls or retention of only a successful Pilot is prohibited.

Passing the Pilot permits later formal material freeze; it does not itself freeze the materials and does not make Pilot outputs part of the main experiment.
