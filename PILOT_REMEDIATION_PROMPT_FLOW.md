# Endpoint Pilot 50% 集中问题：修复 Prompt Flow

## 目的与边界

首轮 Endpoint Pilot 的 48 条有效回答全部选择 50%。这导致以下预注册机器标准未通过：

- C0 至少出现 3 个不同 response categories；实际为 1 个。
- S/C0/T3 合并后任一类别占比不得超过 85%；实际 50% 占 100%。

当前最明确的待检验原因，是正式输出要求向每个模型请求展示了一个完整且合法的示范值：`"unstake_percentage": 50`。本分支只处理这种可能的测量锚定，不根据 treatment effect 的大小、方向或显著性优化材料。

本分支遵循：

1. Summer Project Protocol v1.1 与 Atomic-Task Workflow v1.1 的冻结前修订纪律；
2. Kazinnik 论文“固定调查工具、避免把目标答案暗示给模型、先验证测量再扩展”的原则；
3. 老师规定的五档 outcome `0/25/50/75/100`。论文使用的二元 Yes/No 不直接移植到本项目；
4. 失败 Pilot、旧 prompt 和所有 raw outputs 永久保留；
5. 每次只执行一个原子任务。

---

## R1 — 记录首轮 Pilot 的研究者决定

> 研究者先完成当前人工清单。若逐条 Rationale 暂未填写，必须把清单和决定标为 pending，不得声称人工验收已完整结束。

发送给 Codex：

```text
Goal: 原样记录研究者对首轮 Endpoint Pilot 的决定，说明人工检查状态、两项机器标准失败以及当前不得进入 freeze/main run。

Allowed files: 新建 00_protocol/pilot_decision_v1.0.md。
Protected files: 不得修改 preregistered_checks、prompts、代码、validation、processed data 或 raw outputs。
Acceptance test: 引用具体 run_id、machine_checks 和 manual checklist；逐项列出五项机器标准；区分人工检查已完成与仍待填写部分；明确是否授权 freeze；说明失败不基于 treatment ordering 或显著性。
Do not: 不替研究者改变决定，不修改材料，不调用 API。
```

---

## R2 — 只读审计 50% 的完整生成链路

发送给 Codex：

```text
Goal: 只读审计首轮 Pilot 中 50% 从正式输出要求、assembled prompt、runner 请求、raw response 到 parser 的完整链路，区分证据、推断和未证实原因。

Allowed files: 只读两个项目 docx、参考 PDF、01_prompts/output_schema/、01_prompts/outcome/、02_code/prompt_assembler.py、02_code/run_endpoint_pilot.py、02_code/parser.py、validation/pilot_dry_run/、03_raw_outputs/pilot/ 和 05_processed_data/pilot_diagnostics/。
Protected files: 全部文件不得修改。
Acceptance test: 提供文件与行号/记录证据；确认每个请求是否包含具体示范值 50；确认 parser 是否改写数值；报告 option-order、temperature 和模型配置；明确“示范值锚定”是已证实事实、强推断还是因果定论。
Do not: 不修改 prompt，不调用 API，不分析 treatment effect，不把相关性写成已证明的因果关系。
```

---

## R3 — 起草无具体答案示例的 Output Requirement v1.1

> 只有 R2 支持输出示例是最小修复位置时才执行。

发送给 Codex：

```text
Goal: 起草 Output Requirement v1.1，只移除具体答案示范造成的潜在锚定，同时保持字段、合法值、简短 reason 和严格 JSON 要求不变。

Allowed files: 仅新建 01_prompt_drafts/output_schema_v1.1/ 下的候选文本和 canonical-v1.0 对照表。
Protected files: 不得修改 01_prompts/、代码、validation、protocol checks 或 raw outputs。
Acceptance test: draft 不包含任何被呈现为答案的 0/25/50/75/100 示例值；仍明确要求恰好两个字段、合法整数集合和非空简短 reason；对照表逐项证明除输出表达方式外没有改变 outcome construct；标出所有需研究者人工判断的语义风险。
Do not: 不改成 Yes/No，不改变五档 outcome，不改变 treatment/persona/shock，不调用 API，不自动采纳草稿。
```

### R3 人工确认

研究者需要确认：

- [ ] 五档 outcome 未改变；
- [ ] 没有暗示任何具体选择；
- [ ] JSON 字段与 parser 预期一致；
- [ ] reason 要求未改变；
- [ ] 这是测量格式修复，不是根据 treatment effect 优化 wording。

---

## R4 — 将批准文本纳入正式材料并记录 provenance

发送给 Codex：

```text
Goal: 将研究者批准的 Output Requirement v1.1 原样复制为新的正式材料，并记录首轮 Pilot 失败、修改范围和 provenance；保留 v1.0。

Allowed files: 新建 01_prompts/output_schema/json_schema_v1.1.txt 和 00_protocol/output_requirement_v1.1_change_record.md。
Protected files: 不得修改或覆盖 json_schema_v1.0.txt、其他 prompts、raw outputs、processed data 或 validation。
Acceptance test: 正式 v1.1 与批准 draft 逐字节一致；记录来源、批准信息、SHA-256、旧/新差异和首轮 Pilot run_id；明确旧 Pilot 永不纳入新 Pilot 或 main 数据。
Do not: 不再润色批准文本，不修改其他实验材料，不调用 API。
```

---

## R5 — 让 assembler/runner 显式选择材料版本

发送给 Codex：

```text
Goal: 最小修改 assembler 和 Endpoint Pilot runner，使新 Pilot 显式选择 Output Requirement v1.1，同时保留对首轮 v1.0 请求的可复现能力。

Allowed files: 修改 02_code/prompt_assembler.py、02_code/run_endpoint_pilot.py 及对应 tests；必要时新增测试辅助文件。
Protected files: 不得修改 01_prompts/、protocol、既有 validation 或 raw outputs。
Acceptance test: output requirement 路径/版本来自显式受控参数而非 prompt 正文硬编码；默认或 CLI 行为无歧义；metadata 和 source hashes 记录所用版本；测试证明 v1.0/v1.1 均可重现且新请求不含作为示范答案的具体 unstake 值；全部测试通过。
Do not: 不调用 API，不改变 persona/shock/treatment/outcome，不覆盖旧数据。
```

---

## R6 — 新版本零 API validation 与 dry-run

发送给 Codex：

```text
Goal: 使用 Output Requirement v1.1 生成独立的 validation 和48-cell Pilot dry-run证据，确认唯一变化来自批准的输出要求版本。

Allowed files: 新建 validation/pilot_v1.1_dry_run/ 下的 rendered samples、48-cell request manifest 和人工检查清单。
Protected files: 不得修改 prompts、代码、既有 validation 或 raw outputs。
Acceptance test: 48个唯一 P01-P16 × S/C0/T3 cells；无 placeholder；每条 metadata/hash 完整；不含具体示范答案值；与首轮同 cell prompt 的差异只来自 output requirement v1.0→v1.1；完整测试通过；API调用为0。
Do not: 不调用 API，不手工编辑生成文本，不修改实验材料。
```

---

## R7 — 在新数据产生前冻结修复与重跑规则

发送给 Codex：

```text
Goal: 在重跑 Pilot 前记录修复假设、唯一材料变化、沿用的原预注册阈值和新 run 的数据隔离规则。

Allowed files: 新建 00_protocol/pilot_rerun_plan_v1.1.md。
Protected files: 不得修改 preregistered_checks.md、prompts、代码、validation 或 raw outputs。
Acceptance test: 明确首轮失败证据；声明只更换 output requirement v1.0→v1.1；原五项机器阈值和人工阈值原样沿用；固定 seed 仍为20260901；禁止按效果方向/显著性判定；要求新 run_id、旧数据保留且不混合。
Do not: 不查看未来重跑结果，不降低阈值，不调用 API。
```

> `pilot_rerun_plan_v1.1.md` 与相关代码/材料必须在重跑 API 前形成可追溯 Git commit。

---

## R8 — 重跑完整48-call Endpoint Pilot

> 只有研究者批准 R3、验收 R6，并确认 R7 已提交后才能执行。本步产生真实 API 费用。

发送给 Codex：

```text
Goal: 使用 canonical treatment、canonical answer order 和批准的 Output Requirement v1.1，按新 run_id 重跑16 personas × S/C0/T3的48-call Endpoint Pilot。

Allowed files: 新建 03_raw_outputs/pilot/ 下的独立 JSONL 和 08_logs/ 下对应日志。
Protected files: 不得修改 protocol、prompts、代码、validation 或任何既有 raw output/log。
Acceptance test: 48个预期cell均有记录；run_type=pilot；output requirement version/hash明确；成功、失败、attempt、retry、解析和metadata完整；append-only；与旧Pilot完全隔离。
Do not: 不因结果不理想重问，不静默修复非法输出，不修改prompt，不判断Pilot是否通过。
```

---

## R9 — 按原阈值验收新 Pilot

发送给 Codex：

```text
Goal: 严格沿用原预注册规则验收最新 Pilot，并生成固定seed的12条正式人工审读包；另外生成48条逐条阅读清单作为老师工作流要求的补充质量审计。

Allowed files: 只读最新和历史 03_raw_outputs/pilot/、00_protocol/preregistered_checks.md、00_protocol/pilot_rerun_plan_v1.1.md；新建独立的 05_processed_data/pilot_v1.1_diagnostics/ 和 validation/pilot_v1.1_manual_review/。
Protected files: 不得修改 prompts、代码、protocol、历史 diagnostics、validation 或 raw outputs。
Acceptance test: 单独报告五项原机器阈值；seed=20260901的正式12条样本可复现且不替换；保留原始prompt/response；48条补充清单不改变12条正式判定阈值；新旧run不混合；不使用显著性或预期ordering。
Do not: 不替研究者作最终Pilot决定，不修改材料，不调用API。
```

---

## R10 — 研究者决定与返回主流程

研究者完成审读后发送：

```text
Goal: 原样记录研究者对修复后 Endpoint Pilot 的最终决定和逐项依据，并判断是否授权进入材料冻结。

Allowed files: 新建 00_protocol/pilot_decision_v1.1.md。
Protected files: 不得修改 preregistered checks、prompts、代码、diagnostics、validation 或 raw outputs。
Acceptance test: 引用新run_id、五项机器结果、12条正式人工检查和48条补充阅读状态；明确PASS/FAIL/PENDING及是否允许freeze；不以treatment ordering、显著性或偏好结果为依据。
Do not: 不替研究者改变判断，不修改材料，不调用API。
```

只有 `pilot_decision_v1.1.md` 明确批准 freeze 后，才返回 `NEXT_STEPS_PROMPT_FLOW.md` 的 Gate F。若新 Pilot 仍未通过，必须停止并重新诊断，不能继续修改到得到理想结果。

---

## 暑期项目最低范围说明

本修复分支不要求立即复制 Kazinnik 论文的人类样本校准、八模型比较或完整约1,968-call robustness。最低范围仍是：修复后 Pilot通过 → 冻结材料 → canonical 80-call main run → 基础完整性与配对分析 → reason descriptive coding → 图表、README、归档和简版报告。人类校准和完整跨模型 robustness 应明确列为限制与未来扩展。
