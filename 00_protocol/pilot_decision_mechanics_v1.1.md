# Unstaking Mechanics v1.1 GLM-4.7 Endpoint Pilot Decision

## Decision identity

- Decision date: `2026.9.4`
- Researcher name/initials: `CDY`
- Pilot run ID: `pilot_20260904T135552Z_be4faaf7`
- Provider/model: `zhipu` / `glm-4.7`
- Persona template / unstaking mechanics: `v1.1`
- Output Requirement: `v1.1`
- Answer order: canonical ascending (`0%, 25%, 50%, 75%, 100%`)
- Overall Pilot decision: **FAIL**
- Formal material freeze authorized: **NO**
- Main-run preparation authorized: **NO**
- Main-run API execution authorized: **NO**

This decision applies only to the single Pilot run identified above. All earlier Pilot runs, Tiny Runs, dry-runs, and connectivity checks remain excluded. The decision records the researcher-completed human reviews together with the five machine checks required by the existing preregistration.

## Evidence reviewed

1. Preregistered checks: `00_protocol/preregistered_checks.md`.
2. Mechanics v1.1 provenance: `00_protocol/unstaking_mechanics_v1.1_change_record.md`.
3. Machine checks: `05_processed_data/pilot_mechanics_v1.1_diagnostics/machine_checks.md` and `machine_checks.json`.
4. Fixed-seed sampling record: `05_processed_data/pilot_mechanics_v1.1_diagnostics/sampling_manifest.json`.
5. Formal 12-record review: `validation/pilot_mechanics_v1.1_manual_review/manual_review_checklist.md`.
6. Supplemental 48-record review: `validation/pilot_mechanics_v1.1_manual_review/all_48_supplemental_review.md`.

Evidence SHA-256 values at the time of this decision:

- `preregistered_checks.md`: `5a6a9dea2838079c1e0ab07d75e370a01c70c782282c8062cc6078d1c1233eb9`
- `unstaking_mechanics_v1.1_change_record.md`: `0bce4bfa8856d04406aaf6aa7da554efdf4267ce943d8c1397c5555aa9889204`
- `machine_checks.md`: `28d9dc0402743fc1091196bc4725287a668c7d3a22ca002fe4dcdfe91fbac8fd`
- `machine_checks.json`: `92afb8a06413b1252810df78d87ea5bac1c1bcc8cbe2c770e167975af7f6dbf6`
- `sampling_manifest.json`: `d89aa51edfef10d5785ebef6d7672fc322f97a37265490773745c9b7e5bb3e35`
- `manual_review_checklist.md`: `eb17927492a744bb61ddf7d02a0a01ffedeb59f8c9a59d0a4f0553fea1e2e658`
- `all_48_supplemental_review.md`: `321ca399c83866134d2d2bae9c973f4955d0ab6e1408d42a072c669be44c3269`

## Five preregistered machine criteria

| # | Criterion | Preregistered threshold | Observed result | Status |
|---:|---|---|---|---|
| 1 | Cell completeness and isolation | Exactly 48 unique P01–P16 × S/C0/T3 cells from one Pilot run; 16 per arm; no missing, duplicate, or unexpected cells | 48 records and 48 unique cells; S=16, C0=16, T3=16; missing=0, duplicate=0, unexpected=0; one `run_id`; `run_type=pilot` | **PASS** |
| 2 | C0 mean dynamic range | `15 <= C0 mean <= 75` among valid, non-refusal C0 responses | Valid C0 n=16; mean=`21.875%` | **PASS** |
| 3 | C0 response-category diversity | At least 3 distinct categories among valid, non-refusal C0 responses | 2 categories: `0%=2`, `25%=14` | **FAIL** |
| 4 | Combined category concentration | Maximum single-category share `<=0.85` among pooled valid, non-refusal responses | Category `25%` occurred in 35/48 valid responses; maximum share=`0.729167` | **PASS** |
| 5 | Structured-output validity | At least 46/48 valid and non-refusal responses | 48/48 valid and non-refusal (`1.000000`); parse failures=0; refusals=0; API errors=0; empty responses=0 | **PASS** |

Execution evidence additionally records 48 API successes, 48 attempt records, zero scheduled retries, maximum attempt number 1, and 48 successful parses. No response was repaired, replaced, or re-asked for content.

## Formal fixed-seed 12-record review

The formal sample used seed `20260901`, with four records from each of S, C0, and T3. The selected records were retained without replacement.

Researcher `CDY`, dated `2026.9.4`, recorded:

- material factual hallucination: **12/12 PASS**, exceeding the required 11/12 threshold;
- T3 executed/verifiable-action comprehension: **4/4 PASS**, meeting the required 4/4 threshold; and
- formal 12-record human-review decision: **PASS**.

Researcher notes/rationale, recorded verbatim:

> Researcher reviewed the 12 fixed-seed records and reported no problems. All 12 hallucination checks and all 4 T3 comprehension checks passed. This human PASS does not override the failed C0 category-diversity machine criterion.

The human PASS applies only to the two preregistered human criteria. It does not override or convert a failed machine criterion.

## Supplemental 48-record review

Researcher `CDY`, dated `2026.9.4`, recorded completion of **48/48** supplemental records. All record-level review boxes and the final boundary confirmation were checked, and every record-level concern field states `No concern`.

Overall supplemental notes, recorded verbatim:

> Researcher reviewed all 48 records and reported no problems.

The researcher also confirmed that this supplemental review does not replace the fixed 12-record sample or alter its formal thresholds. It is additional quality-audit evidence and cannot override a machine failure.

## Overall decision and authorization boundary

The overall Pilot decision is **FAIL** because the preregistered C0 response-category-diversity criterion requires at least three distinct valid categories, while this run contains only two (`0%` and `25%`). Passing the other four machine checks and both formal human checks does not remove that failure.

Accordingly:

- formal material freeze is **not authorized**;
- main-run preparation is **not authorized**;
- main-run API execution is **not authorized**;
- this Pilot must not be merged into any main-run dataset;
- no individual response may be selectively rerun or replaced; and
- any material or execution change requires a separately documented rationale, validation, and a complete new Pilot under a new run ID before freeze can be reconsidered.

This decision is based only on the preregistered design-quality criteria. It is **not** based on treatment ordering, the direction or magnitude of any contrast, statistical significance, a p-value, effect size, or conformity with a preferred result. No treatment-effect analysis is made in this record.
