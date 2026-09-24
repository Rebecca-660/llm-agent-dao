# Pilot execution config v1.2 dry-run difference summary

**Overall result: PASS**

## Comparison

- Previous request source: `run_id=pilot_20260904T135552Z_be4faaf7`.
- New dry-run source: `run_id=pilot_dry_run_v1`.
- 48 records and 48 unique cells in each source; new grid is P01-P16 × S/C0/T3 (16 per condition).
- API calls made: 0.

## Material identity

- Prompt/system/source hashes equal in all cells: PASS.
- Unresolved placeholder cells: 0.
- Fixed materials/configuration: `model=glm-4.7`, mechanics/persona template `v1.1`, Output Requirement `v1.1`, answer order `canonical_ascending`, thinking disabled, independent context.

## Sole planned execution change

R22 treats `decoding_regime` as the single conceptual execution factor. Its linked API fields changed together:

- `greedy_v1.1` → `stochastic_low_v1.2`
- `do_sample=false` → `do_sample=true`
- `temperature=0` → `temperature=0.2`
- `sampling_mode=greedy_do_sample_false` → `sampling_mode=stochastic_temperature_0.2`
- Request hash changed in all 48 cells, as expected; prompt/system/source hashes did not change.

Unexpected differences: **0**.

Machine-readable cell-level evidence is in `per_cell_difference_evidence.json`.
