# Output Requirement v1.1 Pilot dry-run review

## Scope

- Run mode: `dry_run`
- API calls: `0`
- Model label used for request construction: `gpt-4o-mini`
- Output requirement: `v1.1`
- Request manifest: `pilot_requests.jsonl`
- Machine comparison: `comparison_audit.json`
- Rendered samples: `P01_S_rendered.txt`, `P01_C0_rendered.txt`, `P01_T3_rendered.txt`
- Historical comparison source: `validation/pilot_dry_run/pilot_requests.jsonl` using output requirement v1.0

This checklist reviews request construction only. It does not approve an API call, a Pilot result, material freeze, or a main run.

## Machine checks

- [x] Exactly 48 request records were generated.
- [x] All 48 cell IDs are unique.
- [x] The matrix contains P01–P16 × S/C0/T3, with 16 cells per arm.
- [x] No unresolved bracket or brace placeholder was detected.
- [x] All records identify `output_requirement_version: v1.1`.
- [x] All records identify `01_prompts/output_schema/json_schema_v1.1.txt` as the output-requirement path.
- [x] All 48 prompt SHA-256 values match their prompt text.
- [x] All 48 system-prompt SHA-256 values match their system-prompt text.
- [x] Every recorded source SHA-256 matches the current source file.
- [x] No request contains a completed numeric assignment such as `"unstake_percentage": 50` or another allowed value.
- [x] For all 48 matched cells, removing the final versioned output-requirement component leaves byte-identical prompt prefixes between the historical v1.0 dry-run and the new v1.1 dry-run.
- [x] For all 48 matched cells, all recorded source hashes other than the versioned output-requirement file are unchanged.
- [x] No API call occurred.

## Researcher rendered-sample review

Read all three rendered sample files from beginning to end before completing this section.

### P01 × S

- [x] Persona, common shock, Silence treatment, outcome question, and protocol name are correct.
- [x] Output requirement contains no completed or recommended unstaking answer.
- [x] Output requirement still clearly requires strict JSON with exactly `unstake_percentage` and `reason`.

### P01 × C0

- [x] Persona, common shock, C0 treatment, outcome question, and protocol name are correct.
- [x] Output requirement contains no completed or recommended unstaking answer.
- [x] Output requirement still clearly requires strict JSON with exactly `unstake_percentage` and `reason`.

### P01 × T3

- [x] Persona, common shock, complete T3 treatment, outcome question, and protocol name are correct.
- [x] T3 still describes an already-executed and publicly verifiable action.
- [x] Output requirement contains no completed or recommended unstaking answer.
- [x] Output requirement still clearly requires strict JSON with exactly `unstake_percentage` and `reason`.

## Cross-version judgment

- [x] I confirm that the behavioral outcome remains the immediate unstaking percentage with levels 0/25/50/75/100.
- [x] I confirm that the only experimental-material text change in each matched prompt is output requirement v1.0 → v1.1.
- [x] I confirm that persona, common shock, arm wording, decision time, outcome question, answer order, and system prompt are unchanged.
- [x] I understand that this dry-run verifies construction but does not prove that removing the example will resolve category concentration.
- [x] I approve these v1.1 rendered requests for the next preregistered rerun-planning step; this is not authorization to call the API yet.

Researcher name/initials:  CDY
Review date:  2026.9.1
Decision (`APPROVE`, `REVISE`, or `REJECT`): APPROVE
Notes:试运行请求构建验证通过。v1.1 版本严格实现了“移除具体数值示例”的目标，且未对人物背景、事件冲击、干预措辞、决策时间、问题或系统提示产生任何意外改动。所有机器哈希与结构检查均已确认。该版本符合预注册重跑计划的材料构建要求，可据此准备下一阶段，但尚未批准实际 API 调用执行。
