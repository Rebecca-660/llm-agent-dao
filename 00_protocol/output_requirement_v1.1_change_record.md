# Output Requirement v1.1 Change and Provenance Record

## Version status

- New formal material: `01_prompts/output_schema/json_schema_v1.1.txt`
- Superseded for the planned Pilot rerun only: `01_prompts/output_schema/json_schema_v1.0.txt`
- Adoption record date: `2026-09-02`
- Status: approved formal material for validation and the planned Pilot rerun; not yet frozen for the main run
- Scope: output-format requirement only

Version v1.0 remains preserved unchanged. This record does not authorize an API call, material freeze, or main run.

## Provenance

| Role | File | SHA-256 |
|---|---|---|
| Approved draft source | `01_prompt_drafts/output_schema_v1.1/output_requirement_v1.1_draft.txt` | `7ca5b6896c2e115d99d7edc8314899d95669e0fb0e919c96472074840d509452` |
| Researcher comparison and approval record | `01_prompt_drafts/output_schema_v1.1/canonical_v1.0_comparison_and_review.md` | `e3a5fce5ab69b8ac77969b6cbb821023e097b66d5470e21a4f790f33e11d5fbe` |
| New formal v1.1 material | `01_prompts/output_schema/json_schema_v1.1.txt` | `7ca5b6896c2e115d99d7edc8314899d95669e0fb0e919c96472074840d509452` |
| Preserved formal v1.0 material | `01_prompts/output_schema/json_schema_v1.0.txt` | `85915c44fe1e083ef06e23eb1e645a890d8ebf9a5088c33209da5024ddd95076` |

The approved draft and formal v1.1 file have identical SHA-256 hashes and are byte-for-byte identical. No further editing was performed during adoption.

## Researcher approval

The approval record states:

- Researcher name/initials: `CDY`
- Review date as entered by the researcher: `2026.9.1`
- Decision: `APPROVE`
- All nine manual-review confirmations are checked, including preservation of the five outcome levels and acknowledgment that the first Pilot does not prove anchoring causally produced its result.

The approval applies to the exact draft identified by the SHA-256 above. It authorizes the next controlled versioning, code-selection, validation, and dry-run steps. It does not by itself authorize skipping those steps or proceeding directly to an API Pilot rerun.

## Triggering Pilot evidence

- First Pilot run ID: `pilot_20260901T101427Z_d4d53cb9`
- Preserved raw output: `03_raw_outputs/pilot/pilot_20260901T101427Z_d4d53cb9.jsonl`
- Raw-output SHA-256: `666e8142b5f80260bd384aca86f88614cc5257cd4addbfc5cf379e63c2a3c1e3`
- Machine evidence: `05_processed_data/pilot_diagnostics/machine_checks.md` and `machine_checks.json`
- Researcher decision: `00_protocol/pilot_decision_v1.0.md`

The first Pilot produced 48/48 valid parsed responses, all with `unstake_percentage = 50`. It passed cell completeness, C0 mean dynamic range, and structured-output validity, but failed two preregistered design checks:

1. C0 response-category diversity: one observed category rather than at least three.
2. Combined category concentration: the 50 category accounted for 100% rather than at most 85%.

Every first-Pilot request contained the completed example assignment `"unstake_percentage": 50`. The exact relationship between that example and the concentrated responses remains a strong design concern, not a proven causal conclusion. Version v1.1 provides the minimal prespecified test: remove the completed answer example while holding the outcome construct and other experimental materials fixed.

## Exact change from v1.0 to v1.1

### Removed

- The completed JSON example containing `"unstake_percentage": 50`.
- The completed example reason string.

### Preserved

- Output remains one valid JSON object.
- Field names remain exactly `unstake_percentage` and `reason`.
- Allowed outcome values remain exactly `0`, `25`, `50`, `75`, and `100`.
- `reason` remains one concise sentence explaining the main reason for the decision.
- The outcome remains a five-level immediate unstaking-percentage decision; it is not converted to Yes/No.
- Persona, common shock, all treatment wording, decision time, outcome question, answer-order materials, system prompt, model settings, and temperature are outside this change and remain unchanged.

### Formatting constraints made explicit

- Exactly two fields.
- `unstake_percentage` must be an integer from the allowed set.
- `reason` must be non-empty.
- No additional fields, commentary, Markdown, or code fences.

These clarifications were explicitly reviewed and approved by the researcher as output-format constraints rather than changes to the behavioral outcome construct.

## Data and version isolation

- The first Pilot and all of its raw records remain immutable and must never be overwritten.
- The first Pilot is a failed design-calibration run and must never be included in a new Pilot dataset or any main-run analysis dataset.
- Any Pilot using v1.1 must use a new `run_id`, a new append-only JSONL file, and metadata/hash records identifying `json_schema_v1.1.txt`.
- New-Pilot diagnostics must read only the explicitly selected new run and must not pool it with the first Pilot.
- Main-run data, if later authorized after a successful Pilot and formal freeze, must use still newer run IDs and remain isolated from both Pilot runs.
- The original preregistered machine and human thresholds must not be relaxed based on the v1.1 Pilot result.

## Next required gate

Before any new Pilot API call, the assembler/runner must explicitly select v1.1 while retaining v1.0 reproducibility, and a zero-API validation/dry-run must demonstrate that the only experimental-material change is the approved output requirement. A separate Pilot-rerun plan must then be recorded and committed before data generation.
