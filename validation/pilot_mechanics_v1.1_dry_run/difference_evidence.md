# Pilot Mechanics v1.1 Dry-Run Difference Evidence

- Historical comparison run: `pilot_20260903T055848Z_a5ef2915`
- Dry-run ID: `pilot_dry_run_v1`
- API calls made: **0**
- Matrix: **48 records, 48 unique cells**
- Arm counts: **S=16, C0=16, T3=16**
- Unresolved placeholders: **0**
- Persona template: `v1.0` → `v1.1`
- Provider/model: `zhipu` / `glm-4.7` — unchanged
- Output Requirement: `v1.1` — unchanged
- Answer order: `canonical_ascending` — unchanged
- Temperature/sampling/thinking: `0` / `greedy_do_sample_false` / `disabled` — unchanged
- Independent context: `true` — unchanged

## Automated result

All 48 same-cell prompts satisfy this exact identity:

`new prompt = historical prompt with the single canonical persona mechanics line replaced by the approved v1.1 mechanics line`

All non-persona source hashes are equal within each same-cell comparison. Prompt hashes, system hashes, request-hash format, source-hash format, metadata completeness, cell uniqueness, arm balance, and placeholder absence were checked for all 48 records. Detailed per-cell hashes are preserved in `difference_evidence.json`.

## Exact sole material change

Canonical v1.0:

> 80% of your governance tokens in this platform are currently staked. The staking APY is 6%. Unstaking requires a 7-day waiting period and carries no additional penalty.

Approved v1.1:

> 80% of your governance tokens in this platform are currently staked. The staking APY is 6%. Initiating unstaking starts a 7-day waiting period and carries no additional penalty. Tokens selected for unstaking remain locked during this period and become unstaked only after the 7-day waiting period ends.

The expected prompt and request hashes change because the approved persona text changed. The dry-run generation timestamp, run mode, and dry-run ID are execution-record fields rather than experimental-material changes.
