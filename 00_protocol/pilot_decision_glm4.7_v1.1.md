# GLM-4.7 Endpoint Pilot Decision v1.1

## Decision identity

- Decision date: `2026-09-03`
- Researcher name/initials: `CDY`
- Pilot run ID: `pilot_20260903T055848Z_a5ef2915`
- Provider: `zhipu`
- Requested and returned model: `glm-4.7`
- Output Requirement: `v1.1`
- Overall Pilot decision: **FAIL**
- Formal material freeze authorized: **NO**
- Main run authorized: **NO**

This decision applies only to the single GLM-4.7 Pilot run identified above. Earlier OpenAI Pilot data, the failed OpenAI v1.1 execution attempt, Tiny Run data, dry-run manifests, and the GLM-4.7 connectivity check are preserved but excluded from this decision and from all calculations reported below.

## Evidence reviewed

1. Original preregistered criteria: `00_protocol/preregistered_checks.md`.
2. Primary-model replacement record: `00_protocol/primary_model_replacement_decision_v1.0.md`.
3. Machine results: `05_processed_data/pilot_v1.1_diagnostics/machine_checks.md` and `machine_checks.json`.
4. Fixed-seed sampling record: `05_processed_data/pilot_v1.1_diagnostics/sampling_manifest.json`.
5. Formal 12-record review: `validation/pilot_v1.1_manual_review/manual_review_checklist.md`.
6. Supplemental 48-record review: `validation/pilot_v1.1_manual_review/all_48_supplemental_review_completed.md`.

Evidence SHA-256 values at the time of decision:

- `machine_checks.json`: `f93745cd93cc8c6fa03548871aa35c9521d2667ecaa0529d41c5b4c4e0122665`
- `machine_checks.md`: `19057f2d16d79a2f97288c0d13113c39e3ddeecc19e62ece66054fff80d900bd`
- `sampling_manifest.json`: `66b9036ea4f1fa5564a98f015d1d580b2cfa39b3cf17f9d400fc9f2e37a94ef4`
- `manual_review_checklist.md`: `dd30f48afbf86708d52dc58d708612333ce9018fb9dd61875438c2226e3855c7`
- `all_48_supplemental_review_completed.md`: `1f886c7a21e2487d892a1fbd73d4d70f61b49f72472349a7cac4d8a5ef4ef9b3`

## Five preregistered machine criteria

| # | Criterion | Preregistered threshold | Observed result | Status |
|---:|---|---|---|---|
| 1 | Cell completeness and isolation | Exactly 48 unique P01–P16 × S/C0/T3 cells from one Pilot run; 16 per arm; no missing, duplicate, or unexpected cells | 48 records and 48 unique cells; S=16, C0=16, T3=16; one run ID; `run_type=pilot` | **PASS** |
| 2 | C0 mean dynamic range | `15 <= C0 mean <= 75` among valid, non-refusal C0 responses | Valid C0 n=16; mean=`3.125%` | **FAIL** |
| 3 | C0 response-category diversity | At least 3 distinct categories among valid, non-refusal C0 responses | 2 categories: `0%=14`, `25%=2` | **FAIL** |
| 4 | Combined category concentration | Maximum single-category share `<=0.85` among pooled valid, non-refusal responses | Category `0%` occurred in 42/46 valid responses; maximum share=`0.913043` | **FAIL** |
| 5 | Structured-output validity | At least 46/48 valid and non-refusal responses | 46/48 valid and non-refusal (`0.958333`); 2 parsing failures; 0 refusal candidates; 0 API errors; 0 empty responses | **PASS** |

The two parsing failures were `P02_S` and `P11_T3`. Both original responses remain preserved exactly as observed. Neither was repaired, coerced, replaced, or re-asked.

## Formal fixed-seed human review

The formal sample was generated using seed `20260901`, stratified as four records from each of S, C0, and T3. The sample was not replaced or adjusted after selection.

The researcher recorded:

- Material factual hallucination: **12/12 PASS**, exceeding the required 11/12 threshold.
- T3 executed/verifiable-action comprehension: **4/4 PASS**, meeting the required 4/4 threshold.
- Formal 12-record human-review result: **PASS**.

The human-review PASS applies only to the two preregistered human criteria. It does not override, average with, or convert any failed machine criterion into a pass.

## Supplemental 48-record read-through

The researcher recorded completion of all **48/48** supplemental records, with 192 checklist items marked complete. The completion entry identifies researcher `CDY`, review date `2026.9.3`, and states that the supplemental review does not alter the formal fixed-seed 12-record thresholds.

The supplemental read-through is additional quality-audit evidence only. It does not replace the fixed sample, change a preregistered threshold, or override a machine failure.

## Final decision and boundary

The GLM-4.7 Endpoint Pilot is **FAIL** because three preregistered design-quality criteria were not met:

1. the C0 mean (`3.125%`) was below the inclusive lower bound of `15%`;
2. C0 contained only 2 response categories rather than at least 3; and
3. the pooled maximum category share (`91.3043%`) exceeded the maximum allowed `85%`.

This failure is based solely on the preregistered dynamic-range, response-category-diversity, and category-concentration criteria. It is **not** based on treatment ordering, the sign or magnitude of a contrast, statistical significance, a p-value, or whether results match a preferred hypothesis.

Accordingly:

- the current materials are **not authorized for formal freeze**;
- a canonical main run is **not authorized**;
- this Pilot must never be merged into a main-run analysis dataset;
- no individual response may be selectively rerun or replaced; and
- no new prompt wording or experimental-material revision is approved by this decision record.

Any subsequent diagnosis must preserve this failed Pilot and separate evidence from inference. Any later material or execution change requires a separately documented rationale and a complete new Pilot under a new run ID before freeze can be reconsidered.
