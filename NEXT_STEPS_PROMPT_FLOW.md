# LLM Agent DAO 项目：逐步执行 Prompt Flow

## 使用方法

1. 每次只复制一个标有“发送给 Codex”的 Prompt。
2. 当前任务通过验收后，才发送下一条。
3. 如果 Codex 报告未通过或需要人工判断，先解决该问题，不要跳步。
4. 除非某一步明确授权，否则不得修改 `01_prompts/`、覆盖 raw outputs 或调用 API。
5. 涉及实验措辞、Pilot 判定和冻结的步骤，必须由研究者人工确认。

---

## Gate A：修复 Phase 1–8 的遗留问题

### A1 — 核实并记录最终协议名

> 本步需要研究者先决定最终名称。根据现有记录，候选名称为 `Selyth Protocol` 和 `Kelmoryn Protocol`，但仍需核实哪一个是正式选择。

发送给 Codex：

```text
Goal: 只读检查现有 protocol naming 和 leakage-check 证据，判断是否已经明确记录最终协议名；向我报告证据、缺口和建议，不修改文件。

Allowed files: 只读 00_protocol/ 下的命名与 leakage-check 文件。
Protected files: 全部文件均不得修改，尤其是 01_prompts/ 和 03_raw_outputs/。
Acceptance test: 明确列出已检查的候选名、外部搜索结论、模型诊断结论，以及是否存在可追溯的最终命名决定。
Do not: 不做新的网络搜索，不替研究者擅自选择名称，不写代码，不调用实验 API。
```

### A2 — 落盘最终命名决定

> 完成 A1 后，把下面的 `<FINAL_PROTOCOL_NAME>` 替换成研究者确认的名称。

发送给 Codex：

```text
Goal: 将研究者确认的最终协议名 <FINAL_PROTOCOL_NAME> 写入独立的命名决定记录，并说明该决定引用的现有外部搜索和模型诊断证据。

Allowed files: 新建或修改 00_protocol/protocol_name_decision.md。
Protected files: 不得修改 01_prompts/、02_code/、03_raw_outputs/、validation/ 和既有 naming/leakage 原始证据。
Acceptance test: 文件明确记录最终名称、决定日期、纳入/排除理由、引用的证据文件和“这不是商标审查”的边界说明；实际 diff 只有允许文件。
Do not: 不修改实验 prompt，不重新解释或改写原始证据，不调用 API。
```

### A3 — 诊断 `[ProtocolName]` 替换链路

发送给 Codex：

```text
Goal: 只读诊断 `[ProtocolName]` 从正式材料到 assembled prompt、validation output 和 Tiny Run 请求的完整链路，确定残留 placeholder 的直接原因和最小修复位置。

Allowed files: 只读 00_protocol/protocol_name_decision.md、01_prompts/、02_code/、validation/、03_raw_outputs/tiny_run/。
Protected files: 全部文件均不得修改。
Acceptance test: 提供文件与行号证据，说明 placeholder 应在哪一层替换、当前在哪一层缺失，以及哪些历史输出已受影响。
Do not: 不实现修复，不修改 prompt，不调用 API，不删除历史数据。
```

### A4 — 实现受控名称替换及测试

发送给 Codex：

```text
Goal: 在不改写正式实验材料的前提下，实现由最终命名记录驱动的 `[ProtocolName]` 精确替换，并加入未解析 placeholder 检查。

Allowed files: 02_code/prompt_assembler.py、02_code/tests/test_prompt_assembler.py；如现有 runner 必须传入名称，可最小修改 02_code/run_tiny_run.py。
Protected files: 00_protocol/ 中除只读最终命名记录外均受保护；不得修改 01_prompts/、03_raw_outputs/、validation/。
Acceptance test: 新测试证明所有正式组件只发生 `[ProtocolName]` 精确替换；assembled prompt 不含形如 `[Name]` 的未解析 placeholder；既有测试全部通过；报告实际 modified files。
Do not: 不把 prompt 正文或协议名硬编码进 Python，不润色实验材料，不调用 API，不覆盖历史输出。
```

### A5 — 重新生成 validation 文件

发送给 Codex：

```text
Goal: 使用修复后的既有 renderer/assembler 重新生成 Phase 2/5 validation artifacts，不修改正式 prompt。

Allowed files: validation/P01_plus_common_shock.txt、validation/P01_C0_rendered.txt、validation/P01_all_arms/ 下五个文件。
Protected files: 00_protocol/、01_prompts/、03_raw_outputs/、02_code/（本步只运行，不修改）。
Acceptance test: 所有 validation 文件使用最终协议名且无 placeholder；P01 五臂的 Persona、Shock、Outcome 完全一致；C0–T3 嵌套测试通过；完整测试套件通过。
Do not: 不调用 API，不手工编辑生成文本，不修改实验措辞。
```

### A6 — 人工审读 validation（必须人工确认）

发送给 Codex：

```text
Goal: 对重新生成的 validation artifacts 做只读审计，生成一份供研究者逐项勾选的审读报告。

Allowed files: 只读 validation/ 和 01_prompts/；新建 validation/phase5_manual_review_checklist.md。
Protected files: 不得修改任何正式 prompt、代码、raw output 或既有 validation 文本。
Acceptance test: checklist 覆盖协议名、placeholder、Persona 一致性、common shock 一致性、decision time、串臂、treatment 嵌套、outcome 和 JSON 要求；清楚标出机器检查结果与必须人工判断的项目。
Do not: 不替研究者签署人工通过，不调用 API。
```

### A7 — 重跑 12-call Tiny Technical Run

> 仅当研究者确认 A6 通过后发送；本步会产生真实 API 调用和费用。

发送给 Codex：

```text
Goal: 在人工确认 Phase 5 validation 通过后，使用新 run_id 运行 4 personas × S/C0/T3 的 12-call Tiny Technical Run，并保留旧 run。

Allowed files: 新建 03_raw_outputs/tiny_run/ 下的新 JSONL；必要时新建对应错误日志。运行既有 02_code/run_tiny_run.py，但不得在本步修改它。
Protected files: 00_protocol/、01_prompts/、validation/、既有 03_raw_outputs/ 文件全部不得修改或覆盖。
Acceptance test: 12 个唯一 cell，无重复或缺失；每臂 4 条；所有请求使用最终协议名且无 placeholder；记录 run_type、run_id、model/version、temperature、timestamps、prompt/system hashes、raw response 和 parse result；报告成功、失败与解析统计。
Do not: 不因输出决策不理想而重问，不把 Tiny Run 当研究结果，不修改 prompt，不覆盖旧数据。
```

### A8 — Tiny Run 技术验收与交接更新

发送给 Codex：

```text
Goal: 只读验收最新 Tiny Run，并准确更新交接状态。

Allowed files: 只读 01_prompts/、02_code/、03_raw_outputs/tiny_run/、validation/；修改 PHASE_1_8_HANDOFF.md。
Protected files: 不得修改 01_prompts/、02_code/、03_raw_outputs/ 或 validation/。
Acceptance test: 核对 12 个 cell、placeholder、hash、解析、错误、run_type 和数据隔离；handoff 明确区分旧 Tiny Run 与修复后 Tiny Run，且不声称实验材料已正式冻结。
Do not: 不分析 treatment effect，不删除旧记录，不调用 API。
```

---

## Gate B：建立安全的版本控制基础

### B1 — Git 与密钥保护检查

发送给 Codex：

```text
Goal: 建立本项目的本地 Git 基础和密钥保护，但不提交任何内容。

Allowed files: 初始化 .git/；新建 .gitignore 和 .env.example。
Protected files: 不得读取、打印、修改或提交 .env；不得修改 00_protocol/、01_prompts/、02_code/、03_raw_outputs/、validation/。
Acceptance test: git status 可用；.gitignore 排除 .env、__pycache__/、*.pyc、.pytest_cache/；.env.example 只含无敏感值的变量名模板；确认 .env 未被跟踪。
Do not: 不显示密钥，不执行 git add/commit，不修改研究材料。
```

### B2 — 首次版本快照建议

发送给 Codex：

```text
Goal: 只读审计当前仓库，提出首个 commit 的文件清单、应排除项目和建议 commit message，等待我确认。

Allowed files: 只读整个项目和 git status。
Protected files: 全部文件不得修改；不得 stage 或 commit。
Acceptance test: 明确列出将跟踪、忽略和需要人工确认的文件，特别说明 .env、raw outputs、截图和 Word/PDF 的处理建议。
Do not: 不执行 git add、git commit、git tag 或远程操作。
```

---

## Gate C：Phase 9 — 完整 Persona Grid

### C1 — 生成 16 个 Persona

发送给 Codex：

```text
Goal: 仅根据已冻结的四个 persona dimensions 做 Cartesian product，生成完整 16-persona CSV。

Allowed files: 新建 01_prompts/personas/personas_v1.0.csv、02_code/tests/test_persona_grid.py。
Protected files: 不得修改其他 01_prompts/ 文件、test_personas.csv、03_raw_outputs/ 或 validation/。
Acceptance test: 正好 16 行、persona_id 唯一、无重复/缺失组合、每个二元维度各 level 出现 8 次、字段与 canonical template placeholders 匹配；全部测试通过。
Do not: 不自由丰富 Persona，不加入人口统计信息，不调用 API。
```

### C2 — 渲染抽样与人工审读

发送给 Codex：

```text
Goal: 从完整 16-persona grid 中选择覆盖各 level 的样例进行渲染，供人工逐字审读。

Allowed files: 新建 validation/full_grid_persona_samples/ 下的样例和 checklist。
Protected files: 不得修改 01_prompts/、02_code/、03_raw_outputs/ 或既有 validation 文件。
Acceptance test: 样例覆盖每个维度的两个 level；除 placeholder substitution 外与 canonical template 字符一致；无未解析 placeholder；研究者可逐项勾选。
Do not: 不调用 API，不替研究者宣布人工审读通过。
```

---

## Gate D：Phase 10–11 — Robustness 与预注册

### D1 — 起草第二版 treatment paraphrases

发送给 Codex：

```text
Goal: 为 S/C0/T1/T2/T3 分别起草 wording version 2，仅作为 draft，保持事实、信息量、语气、时间点和 treatment 层级等价。

Allowed files: 仅新建 01_prompt_drafts/robustness_paraphrases/v2/ 下的草稿与逐条对照表。
Protected files: 01_prompts/ 全部不得修改；不得修改代码、validation 或 raw outputs。
Acceptance test: 每个 draft 与 canonical 逐句对照；明确标注可能的语义偏移供人工判断；C0–T3 的增量层级不变。
Do not: 不把 draft 移入正式 prompts，不声称语义等价已经人工通过，不调用 API。
```

### D2 — 人工核对并采纳 version 2

> 研究者先逐句确认或提出修改，再发送本步。

发送给 Codex：

```text
Goal: 根据研究者逐条确认的版本，将 treatment wording version 2 从 draft 复制为正式 robustness materials，并记录 provenance。

Allowed files: 新建 01_prompts/robustness_paraphrases/v2/ 和对应 change/provenance 记录。
Protected files: 不得修改 canonical treatments、其他正式 prompts、raw outputs。
Acceptance test: 正式文件与研究者批准文本完全一致；记录来源、批准日期和人工语义等价确认；测试验证文件完整且不存在意外 placeholder。
Do not: 不再润色已批准文本，不生成 version 3，不调用 API。
```

### D3 — 重复 D1/D2 制作 version 3

发送给 Codex：

```text
Goal: 在 version 2 已人工通过后，为五个 treatments 起草 wording version 3，仅写入 draft，并生成与 canonical 的逐句语义对照。

Allowed files: 仅新建 01_prompt_drafts/robustness_paraphrases/v3/。
Protected files: 01_prompts/、代码和 raw outputs 全部不得修改。
Acceptance test: 五臂齐全；事实、时间点、信息量、语气和层级均有对照；所有风险点明确标出供人工审核。
Do not: 不自动采纳为正式材料，不调用 API。
```

### D4 — 创建反向答案顺序版本

发送给 Codex：

```text
Goal: 创建 outcome 的反向选项顺序版本，只把 0/25/50/75/100 改为 100/75/50/25/0。

Allowed files: 新建 01_prompts/outcome/outcome_order_reverse_v1.0.txt 和精确差异测试。
Protected files: 不得修改 canonical outcome 或其他正式 prompt。
Acceptance test: 除选项排列顺序外，字符内容与 canonical outcome 完全一致；测试自动证明这一点。
Do not: 不润色问题，不改变 JSON schema，不调用 API。
```

### D5 — 写死 Pilot 预注册检查

发送给 Codex：

```text
Goal: 根据 Protocol v1.1 和 Atomic Workflow v1.1，整理并写入 Endpoint Pilot 的预注册检查，不查看或分析任何未来 Pilot 数据。

Allowed files: 新建 00_protocol/preregistered_checks.md。
Protected files: 不得修改 01_prompts/、代码、validation 或 raw outputs。
Acceptance test: 完整包含 C0 15%–75%、至少 3 类、单类不超过 85%、有效率至少 95%、固定 seed 分层抽 12 条、11/12 hallucination 要求、T3 action 理解检查，以及 treatment effect 不作为通过标准。
Do not: 不查看 Pilot 结果，不增加“必须符合预期方向/显著性”的标准，不调用 API。
```

---

## Gate E：Phase 12 — Endpoint Design Pilot

### E1 — Pilot runner 只读设计审查

发送给 Codex：

```text
Goal: 只读审查现有代码距离 16 personas × S/C0/T3 Endpoint Pilot runner 的要求还有哪些缺口，并给出最小实现方案。

Allowed files: 只读 00_protocol/preregistered_checks.md、01_prompts/、02_code/ 和 validation/。
Protected files: 全部文件不得修改。
Acceptance test: 覆盖 cell 枚举、独立 context、run metadata、append-only raw output、错误/retry、parser、run_type、hash 和数据隔离；指出可复用与不可复用代码。
Do not: 不实现、不调用 API、不查看 Tiny Run 的 treatment effect。
```

### E2 — 实现并 dry-run Pilot runner

发送给 Codex：

```text
Goal: 实现 Endpoint Pilot runner 并只做零 API 的 dry-run 验证。

Allowed files: 新建/修改明确需要的 02_code/ runner 和 tests；新建 validation/pilot_dry_run/ 请求清单。
Protected files: 不得修改 01_prompts/、03_raw_outputs/ 或既有 validation artifacts。
Acceptance test: dry-run 正好生成 48 个唯一 cells；16 personas × S/C0/T3 完整；无 placeholder；每个请求 hash 和 metadata 齐全；tests 全部通过；未发生 API 调用。
Do not: 不调用 API，不修改实验材料。
```

### E3 — 运行 48-call Endpoint Pilot

> 仅在研究者批准 dry-run 后发送；本步会产生真实 API 调用和费用。

发送给 Codex：

```text
Goal: 使用 canonical wording 和固定 answer order 运行 16 personas × S/C0/T3 的 48-call Endpoint Pilot。

Allowed files: 新建 03_raw_outputs/pilot/ 下的独立 run JSONL 和 08_logs/ 下对应日志。
Protected files: 不得修改 00_protocol/preregistered_checks.md、01_prompts/、validation/ 或任何既有 raw output。
Acceptance test: 48 个预期 cell 均有记录；成功、失败、retry、解析与 metadata 完整；所有 raw output append-only；明确标记 run_type=pilot。
Do not: 不因结果不理想重问，不静默修复非法输出，不修改 prompt，不判定 Pilot 是否通过。
```

### E4 — Pilot 机器检查与人工抽样包

发送给 Codex：

```text
Goal: 严格按预注册规则计算 Pilot 机器检查，并按预设 seed 生成 S/C0/T3 各 4 条的 12 条人工审读包。

Allowed files: 只读 03_raw_outputs/pilot/ 和 00_protocol/preregistered_checks.md；新建 05_processed_data/pilot_diagnostics/ 和 validation/pilot_manual_review/。
Protected files: 不得修改 prompts、代码、预注册文件或 raw outputs。
Acceptance test: 逐项报告预注册阈值；抽样可由 seed 重现；展示原始 prompt/response 供人工判断；不使用显著性或预期 ordering 作为通过条件。
Do not: 不替研究者作最终 Pilot 判定，不修改材料。
```

### E5 — 研究者记录 Pilot 决定

> 研究者完成 12 条人工审读后，把结论和理由提供给 Codex。

发送给 Codex：

```text
Goal: 原样记录研究者对 Endpoint Pilot 的通过/不通过决定、逐项依据和下一步，不改变实验材料。

Allowed files: 新建 00_protocol/pilot_decision_v1.0.md。
Protected files: 不得修改 preregistered checks、prompts、代码、processed data 或 raw outputs。
Acceptance test: 决定引用具体机器检查和人工审读记录；明确是否允许进入 freeze；若不通过，仅记录需要建立新版本的原因，不直接修改材料。
Do not: 不替研究者改变判定，不根据 treatment effect 优化设计。
```

---

## Gate F：Phase 13 — 正式冻结

### F1 — Freeze 前完整审计

发送给 Codex：

```text
Goal: 在 Pilot 被研究者判定通过后，对所有 main/robustness 会使用的正式实验材料做只读完整性审计。

Allowed files: 只读 00_protocol/、01_prompts/、相关 tests 和 pilot decision。
Protected files: 全部文件不得修改。
Acceptance test: 列出 manifest 应覆盖的精确文件；确认 canonical、v2、v3、两种 answer order、system、persona、shock、schema 均齐全；报告任何缺口并停止 freeze。
Do not: 不生成 manifest、不打 tag、不修改材料。
```

### F2 — 生成 manifest 并冻结

发送给 Codex：

```text
Goal: 为审计通过的全部正式实验材料生成 SHA-256 manifest，运行验证测试，并准备冻结 commit/tag。

Allowed files: 新建 00_protocol/prompt_manifest_v1.0.json；必要时新增只读 hash-verification 代码和测试；执行经我确认的本地 git commit/tag。
Protected files: 不得修改任何已批准的 01_prompts/ 内容或 raw outputs。
Acceptance test: manifest 覆盖所有 main/robustness 材料；重新计算 hash 全部一致；测试通过；git 工作树和 tag 状态清楚报告。
Do not: 不在存在缺口或未提交改动时强行冻结，不做远程 push，不修改 prompt。
```

---

## Gate G：冻结后的 Main Run 与分析

冻结之后仍坚持一次一个原子任务，推荐顺序如下：

1. Batch-of-5 runner。
2. 网络错误 retry 规则。
3. 完整 run metadata 和日志。
4. 启动时 manifest assertion。
5. Canonical main dry-run（80 cells，零 API）。
6. Canonical main 16 × 5 = 80 calls。
7. Dataset completeness 检查。
8. 已冻结 paraphrase v2。
9. 已冻结 paraphrase v3。
10. Answer-order reversal。
11. Temperature sensitivity。
12. Second-model robustness。
13. Run-type 过滤与数据集构建。
14. 五臂 means 和 outcome distribution。
15. AnyUnstake。
16. Persona-level paired differences。
17. 六个 specifications 的 effect range。
18. Exact paired sign-flip/permutation test。
19. Reason codebook 人工冻结。
20. Reason coding 与人工复核。
21. Figures、tables、README 和 final report。

进入 Gate G 时，让 Codex根据 frozen manifest 和当时仓库状态，为上述每一项继续生成同格式的原子 Prompt；不要提前一次性授权全部 API 调用。

---

## 当前应发送的第一条

从 **A1 — 核实并记录最终协议名** 开始。A1 是只读任务，不会修改任何文件。
