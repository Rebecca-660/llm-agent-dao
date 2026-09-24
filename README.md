# LLM Agent DAO

使用大语言模型扮演固定投资者角色，研究 DAO 在协议安全事件后的不同回应方式，如何影响治理代币持有者立即发起解除质押（unstaking）的决策。

本仓库包含虚构的 **Kelmoryn Protocol** 实验材料、Python 执行代码、原始响应、处理后数据、分析结果与图表。当前完成的是 **v1.2 最小范围主实验**，可直接使用已归档数据复现分析，无需重新调用模型 API。

## 实验设计

研究情境是：协议发生严重安全事件，但质押合约未直接受到影响。模型根据角色设定、共同冲击和一项回应方案，选择立即发起解除质押的比例，并给出理由。

角色由四个二水平维度组成：持有时间、资产配置比例、治理参与程度，以及是否经历过重大加密资产事件，共 `2 × 2 × 2 × 2 = 16` 个固定角色。

| 分组 | 回应内容 |
|---|---|
| S | 事件发生数小时后，协议仍未正式回应 |
| C0 | 确认事件、表示正在调查，并承诺 24 小时内更新 |
| T1 | 在 C0 基础上，表达对协议长期安全与发展的信心 |
| T2 | 在 T1 基础上，增加独立安全审查、事件复盘、升级及审计安排 |
| T3 | 在 T2 基础上，增加已转入链上专用安全储备的团队资金承诺 |

主实验包含 **16 个角色 × 5 个分组 = 80 个单元**。每个单元使用独立模型上下文，无历史对话传递。主要结果为 `unstake_percentage`，取值仅为 `0、25、50、75、100`；辅助指标 `AnyUnstake` 表示是否选择大于 0 的解除质押比例。

冻结配置：智谱 `glm-4.7`，`temperature=0.2`，`do_sample=true`，关闭 thinking；角色模板和输出要求均为 `v1.1`，答案按比例升序排列。详细规定见[主实验计划](00_protocol/main_run_plan_v1.2.md)和[材料及配置冻结记录](00_protocol/formal_material_freeze_v1.2.md)。

## 目录结构

| 路径 | 内容 |
|---|---|
| `00_protocol/` | 实验设计、预先指定的检查、Pilot 决策及材料冻结记录 |
| `01_prompts/` | 正式角色、共同冲击、处理条件、问题和输出格式 |
| `01_prompt_drafts/` | 提示词草稿、修订比较和人工审阅记录 |
| `02_code/` | 提示词组装、响应解析、API 执行器和自动化测试 |
| `03_raw_outputs/` | 按 main、pilot、smoke、tiny_run 分类保存的原始响应 |
| `05_processed_data/` | 主实验处理后数据、完整性检查及 Pilot 诊断 |
| `06_analysis/` | 统计分析脚本、结果表和分析说明 |
| `07_figures/` | 分析图表及展示用 PNG、SVG |
| `08_logs/` | API 尝试、错误及重试记录 |
| `validation/` | 零 API dry-run、请求检查和人工核验材料 |

主实验分析仅使用指定的 main 数据；Pilot、Tiny Run、smoke、连接检查和 dry-run 不进入主分析样本。

## 快速开始：复现已有结果

以下命令从项目根目录运行，使用 PowerShell。代码需要 Python 3.10 或更高版本。处理数据和基础分析脚本使用 Python 标准库；运行执行器及测试还需安装 `requirements.txt` 中的依赖。

```powershell
git -c core.autocrlf=false clone https://github.com/Rebecca-660/llm-agent-dao.git
cd llm-agent-dao
python -m pip install -r requirements.txt
```

克隆时保留仓库原始换行格式，是为了让冻结材料的逐字节 SHA-256 校验保持一致。若已有工作副本出现哈希不匹配，应检查文件内容及换行转换，不要直接更改冻结记录中的哈希。

依次生成处理后数据和分析结果：

```powershell
python -B 05_processed_data/main_v1.2/generate_processed_dataset.py
python -B 06_analysis/main_v1.2/analyze_main.py
```

这两步不调用 API、不需要密钥，会重新写入对应的派生数据、结果表和基础 SVG 图表。脚本固定读取已归档的主实验 `main_20260904T160520Z_d93b455f`，不是自动选择最近一次运行。

主要输出：

- [处理后数据](05_processed_data/main_v1.2/main_v1.2_processed.csv)及[字段说明](05_processed_data/main_v1.2/data_dictionary.md)。
- [数据完整性报告](05_processed_data/main_v1.2/integrity_report.md)。
- [各组描述统计](06_analysis/main_v1.2/arm_summary.csv)。
- [角色内配对差异](06_analysis/main_v1.2/paired_contrast_summary.csv)及[完整结果摘要](06_analysis/main_v1.2/results_summary.md)。
- [分析方法及输出说明](06_analysis/main_v1.2/README.md)。

如需重新生成展示用图表，额外安装绘图库；它们目前没有列入 `requirements.txt`：

```powershell
python -m pip install matplotlib numpy
python -B 06_analysis/main_v1.2/create_presentation_figures.py
```

展示图表输出到 `07_figures/main_v1.2/presentation/`。

## 测试与零 API 检查

运行自动化测试：

```powershell
python -B -m pytest 02_code/tests -q
```

当前版本的测试已知问题：根目录缺少历史测试数据 `test_personas.csv`，导致 `test_persona_grid.py` 中的旧角色一致性检查和 `test_persona_renderer.py` 中的 P01 渲染检查失败。本次本地验证为 73 项通过、2 项失败；主实验 80 单元的零 API 检查通过。主实验使用 `01_prompts/personas/personas_v1.0.csv`。

主实验 dry-run 会核对冻结文件哈希、组装 80 个请求并输出检查文件，不发送模型请求。输出目录必须尚不存在，因此示例使用临时目录中的唯一名称：

```powershell
$dryRunDirectory = Join-Path $env:TEMP ('llm-agent-dao-dry-run-' + [guid]::NewGuid().ToString('N'))
python -B 02_code/run_main_run.py --dry-run --provider zhipu --model glm-4.7 --decoding-regime stochastic_low_v1.2 --persona-template-version v1.1 --output-requirement-version v1.1 --answer-order canonical_ascending --output-directory $dryRunDirectory
```

不要直接使用已归档的 `validation/main_run_v1.2_dry_run/` 作为新输出目录；执行器会拒绝覆盖。

## 新的模型运行

复现仓库中的分析不需要重新采集数据。若研究计划需要新一轮模型运行，应另行确定运行范围和 API 费用；新结果不会自动替换现有主分析数据。

当前主实验执行器读取环境变量 `ZAI_API_KEY`。仓库中的 `.env.example` 对应早期 OpenAI 路径；执行器不会自动加载 `.env` 文件。需要执行时，在当前 PowerShell 会话中设置智谱密钥：

```powershell
$env:ZAI_API_KEY = '<your-zhipu-api-key>'
```

在上面的主实验命令中，将 `--dry-run` 替换为 `--execute`，并移除 `--output-directory` 参数，即会实际请求模型并产生 API 费用。执行器生成独立 run ID，将原始输出写入 `03_raw_outputs/main/`，尝试日志写入 `08_logs/main/`。

每个单元最多尝试 3 次，仅对符合规则的暂时性 API 错误重试。成功返回但格式无效的响应保留为无效数据，不因结果或格式问题重新提问。提示词和执行配置受冻结哈希约束。

## 已归档主实验结果

80 个计划单元中有 **79 个有效结果**；`P11_S` 为缺失。缺失值不填补，也不当作 0%，仅从需要该观测的统计量中排除。

| 分组 | 有效 / 计划 | 平均解除质押比例 | AnyUnstake 比例 |
|---|---:|---:|---:|
| S | 15 / 16 | 21.67% | 86.67% |
| C0 | 16 / 16 | 25.00% | 93.75% |
| T1 | 16 / 16 | 18.75% | 68.75% |
| T2 | 16 / 16 | 17.19% | 68.75% |
| T3 | 16 / 16 | 9.38% | 37.50% |

分析包含 `C0 − S`、`T1 − C0`、`T2 − T1` 和 `T3 − T2` 的角色内配对比较，以及精确符号翻转检验。完整配对结果及其分母见[结果摘要](06_analysis/main_v1.2/results_summary.md)。

这些结果描述的是单一模型及配置下的 16 个固定角色，不是 80 位独立人类受试者。检验结果仅作为固定角色集合的诊断，不能直接推广为真实投资者的行为效应。当前主实验不包含多模型、重复采样、反向答案顺序或措辞稳健性检验；仓库中存在部分相关材料，不代表已完成这些扩展。

## 文件管理

`.gitignore` 排除本地报告目录 `09_report/`、交接目录 `10_handoff/`、密钥文件 `.env`、根目录的其他 Markdown 文件，以及 Word、PowerPoint、PDF 参考材料。根目录 `README.md` 单独允许版本控制；实验子目录中的 Markdown 说明继续保留。

原始响应和尝试日志用于追溯已归档实验；新运行应保存为新文件，避免覆盖历史记录。
