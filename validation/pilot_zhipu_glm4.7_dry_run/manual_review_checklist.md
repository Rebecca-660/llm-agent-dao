# Zhipu GLM-4.7 Primary-Model Pilot Dry-Run Review

## Scope

- Decision record: `00_protocol/primary_model_replacement_decision_v1.0.md`
- Run mode: `dry_run`
- API calls: `0`
- Provider: `zhipu`
- Requested primary model: `glm-4.7`
- Endpoint: `https://open.bigmodel.cn/api/paas/v4/`
- Output requirement: `v1.1`
- Sampling: `do_sample=false`
- Thinking mode: `disabled`
- Request manifest: `pilot_requests.jsonl`
- Machine comparison: `comparison_audit.json`
- Rendered samples: `P01_S_rendered.txt`, `P01_C0_rendered.txt`, `P01_T3_rendered.txt`
- Approved same-cell comparison source: `validation/pilot_v1.1_dry_run/pilot_requests.jsonl`

This checklist reviews request construction only. It does not authorize a paid connectivity call, the 48-call Pilot, material freeze, or a main run.

## Machine checks already completed

- [x] Exactly 48 request records were generated.
- [x] All 48 cell IDs are unique.
- [x] The matrix contains P01–P16 × S/C0/T3, with 16 cells per arm.
- [x] All 48 records identify `provider: zhipu` and `model: glm-4.7`.
- [x] All 48 records identify the fixed Zhipu API endpoint.
- [x] All 48 records identify `sampling_mode: greedy_do_sample_false` and `do_sample: false`.
- [x] All 48 records identify `thinking_mode: disabled`.
- [x] All 48 records identify Output Requirement v1.1.
- [x] No unresolved bracket or brace placeholder was detected.
- [x] No request contains a completed numeric unstaking-answer example.
- [x] All 48 experimental prompts are byte-identical to the same-cell prompts in the previously approved v1.1 dry-run.
- [x] All 48 prompt SHA-256 values match the previously approved same-cell prompt hashes.
- [x] Provider-specific request hashes differ from the OpenAI-envelope hashes and record the Zhipu request structure.
- [x] No API call occurred.

## Researcher rendered-sample review

Read all three rendered sample files from beginning to end before completing this section. The files are copied byte-for-byte from the previously approved same-cell v1.1 rendered samples because the comparison audit verified that the experimental prompts did not change.

### P01 × S

- [ ] Persona, common shock, Silence treatment, outcome question, decision time, protocol name, and answer order are unchanged and correct.
- [ ] Output Requirement v1.1 contains no completed or recommended unstaking answer.
- [ ] The request still requires strict JSON with exactly `unstake_percentage` and `reason`.

### P01 × C0

- [ ] Persona, common shock, C0 treatment, outcome question, decision time, protocol name, and answer order are unchanged and correct.
- [ ] Output Requirement v1.1 contains no completed or recommended unstaking answer.
- [ ] The request still requires strict JSON with exactly `unstake_percentage` and `reason`.

### P01 × T3

- [ ] Persona, common shock, complete T3 treatment, outcome question, decision time, protocol name, and answer order are unchanged and correct.
- [ ] T3 still describes an already-executed and publicly verifiable action.
- [ ] Output Requirement v1.1 contains no completed or recommended unstaking answer.
- [ ] The request still requires strict JSON with exactly `unstake_percentage` and `reason`.

## Provider-replacement judgment

- [ ] I confirm that Zhipu AI `glm-4.7` is the replacement primary model, not merely a robustness model.
- [ ] I confirm that the behavioral outcome remains the immediate unstaking percentage with levels 0/25/50/75/100.
- [ ] I confirm that persona, common shock, treatment wording, outcome question, answer order, system prompt, and Output Requirement v1.1 are unchanged.
- [ ] I understand that `do_sample=false` disables random sampling and causes the provider to ignore temperature as an active sampling control, while the registered temperature value remains recorded as `0`.
- [ ] I confirm that thinking mode is disabled for every request.
- [ ] I understand that prior OpenAI records are preserved but excluded from the new Zhipu Pilot and main dataset.
- [ ] I understand that changing the primary model changes the scope of inference and that results must be reported as GLM-4.7 behavior rather than behavior of all LLMs.
- [ ] I approve this dry-run for the next connectivity-test planning step; this is not authorization to call the API.

Researcher name/initials:

Review date:

Decision (`APPROVE`, `REVISE`, or `REJECT`):

Notes:
