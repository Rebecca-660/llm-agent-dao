# Endpoint Pilot Decision v1.0

## Scope and evidence

- Pilot run ID: `pilot_20260901T101427Z_d4d53cb9`
- Pilot raw record: `03_raw_outputs/pilot/pilot_20260901T101427Z_d4d53cb9.jsonl`
- Machine-check evidence: `05_processed_data/pilot_diagnostics/machine_checks.md` and `05_processed_data/pilot_diagnostics/machine_checks.json`
- Human-review evidence: `validation/pilot_manual_review/review_packet.md` and `validation/pilot_manual_review/manual_review_checklist.md`
- Prespecified sampling seed: `20260901`

This record preserves the researcher's currently documented decision and distinguishes completed judgments from incomplete review documentation. It does not revise the preregistered checks or any experimental material.

## Preregistered machine checks

| # | Criterion | Prespecified threshold | Observed result | Status |
|---|---|---|---|---|
| 1 | Cell completeness and isolation | Exactly 48 unique `P01`–`P16` × `S/C0/T3` cells from one Pilot run, with independent contexts | 48 records and 48 unique cells; 16 per arm; no missing, duplicate, or unexpected cells; all `run_type=pilot`; all contexts independent | PASS |
| 2 | C0 mean dynamic range | Valid non-refusal C0 mean between 15% and 75%, inclusive | 16 valid C0 responses; mean 50.00% | PASS |
| 3 | C0 response-category diversity | At least 3 distinct categories among valid non-refusal C0 responses | 1 distinct category: `50` | **FAIL** |
| 4 | Combined category concentration | No category may exceed 85% of pooled valid non-refusal S/C0/T3 responses | `50` occurred in 48/48 responses; maximum share 100% | **FAIL** |
| 5 | Structured-output validity | At least 46/48 valid non-refusal responses | 48/48 valid non-refusals; 0 parse failures, 0 explicit-refusal-screen matches, 0 API errors, and 0 empty responses | PASS |

Two prespecified machine criteria failed: C0 response-category diversity and combined category concentration.

## Human-review status

### Judgments currently recorded

The manual checklist currently records:

- material factual hallucination: `12/12` marked PASS, meeting the preregistered threshold of at least 11/12;
- sampled T3 comprehension: `4/4` marked PASS;
- all three detailed T3 checks marked for each sampled T3 response: already executed, publicly verifiable, and not recast as compensation, increased yield, or a token-price guarantee;
- confirmation that no sampled record was replaced; and
- confirmation that effect direction, treatment ordering, significance, and preferred results were not used as pass conditions.

### Documentation still incomplete or internally inconsistent

- All 12 material-hallucination `Rationale` fields are blank.
- All 4 T3-comprehension `Rationale` fields are blank.
- The checklist records the review date as `2026.8.31`, which precedes the Pilot run dated `2026-09-01`; this date has not been corrected in the source checklist.
- The single sentence in `Notes` does not supply a separate short rationale for each sampled judgment.

Accordingly, the human checkboxes and summary counts are recorded, but the requested per-record rationale documentation and a chronologically consistent review date remain pending.

## Researcher decision, preserved verbatim

Researcher name/initials as recorded: `CDY`

> PENDING — Human review passed, but machine criteria 3 and 4 failed. Full deployment is not yet authorized.

The checklist therefore does **not** authorize formal material freeze or any main run. The current materials must not proceed to `freeze` or `main` while this decision remains pending and the two preregistered machine failures remain unresolved.

## Decision boundary

This pending decision is based on prespecified design-quality checks: response-category diversity, category concentration, structured-output quality, and documented human comprehension/hallucination review. It is **not** based on:

- an expected ordering among `S`, `C0`, and `T3`;
- the sign or magnitude of any treatment effect;
- statistical significance or a p-value; or
- agreement with a preferred substantive result.

No Pilot output is authorized for inclusion in main-run analysis. Any subsequent material change must use a new version, preserve this failed Pilot and its raw outputs unchanged, and be evaluated in a complete new Pilot run under a new `run_id` before freeze can be reconsidered.
