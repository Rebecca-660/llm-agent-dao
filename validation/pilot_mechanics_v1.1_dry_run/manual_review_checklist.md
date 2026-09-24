# Pilot Mechanics v1.1 Dry-Run — Manual Review Checklist

## Machine-verified items

- [x] Exactly 48 unique P01–P16 × S/C0/T3 cells are present.
- [x] Each arm contains exactly 16 cells.
- [x] All rendered prompts contain no unresolved placeholder.
- [x] Prompt, system, request, and source hash metadata are present and well formed.
- [x] Prompt and system hashes were independently verified.
- [x] Each same-cell prompt differs from the prior GLM-4.7 Pilot only by the approved persona mechanics line.
- [x] All non-persona source hashes match the prior same-cell request.
- [x] Provider/model remain zhipu/GLM-4.7.
- [x] Output Requirement remains v1.1.
- [x] Canonical ascending answer order remains unchanged.
- [x] Temperature, deterministic sampling, thinking mode, and independent-context settings remain unchanged.
- [x] API calls made: 0.

Machine checks do not substitute for the human judgments below.

## Researcher review of rendered samples

Review `rendered_samples/P01_S.txt`, `P01_C0.txt`, and `P01_T3.txt` against the approved text and the difference evidence.

- [x] The mechanics clarification appears exactly as approved in all three samples.
- [x] “Initiating unstaking” clearly starts rather than completes the seven-day period.
- [x] Selected tokens remain locked during the waiting period.
- [x] Completion occurs only after the waiting period ends.
- [x] The wording does not recommend or discourage unstaking.
- [x] Persona facts outside the approved passage are unchanged.
- [x] Common shock is unchanged across the samples.
- [x] S/C0/T3 treatment wording and information hierarchy are unchanged.
- [x] The decision time point and five outcome levels are unchanged.
- [x] Output Requirement v1.1 and JSON fields are unchanged.
- [x] Repetition of the seven-day duration remains acceptable in the assembled context.
- [x] I accept the machine difference evidence and approve this dry-run for the next gate.

## Researcher decision

- Researcher name/initials: `__CDY______________`
- Decision date: `__2026.9.4______________`
- Dry-run decision — select exactly one: `[x] APPROVE  [ ] REVISE  [ ] REJECT`
- Notes/rationale: `干运行请求构建验证通过。V1.1 机械机制澄清已按批准内容正确应用于所有 48 个单元格，人物背景、共同冲击、各分支措辞、输出要求及决策变量均未受非预期影响。所有哈希与结构检查均匹配。该干运行验证了构建正确性，可据此准备下一环节，但尚未授权执行实际 API 调用或材料冻结。`

Approval of this checklist validates the dry-run only. It does not itself authorize API calls. Any real 48-call Pilot requires a separate explicit authorization covering API execution and token consumption. It does not authorize material freeze or a main run.
