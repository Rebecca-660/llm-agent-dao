# AI Project Orientation - Task 0A.1

**Date：** 2026-08-19

---

## 1.User Prompt

Read the attached Protocol and Atomic-Task Workflow as project context only.
Do not write code, do not modify files, and do not execute any step yet.
Summarize: (1) project goal, (2) protected experimental materials, (3) freeze rules,
(4) pilot vs. main-run data boundary, and (5) the next single task.
Future work must be performed one atomic task at a time.

---

## 2. AI Response

1. **Project goal:** Run a controlled, reproducible LLM-agent experiment testing whether increasingly substantive DAO crisis responses change long-term governance-token holders’ immediate unstaking decisions after a serious protocol incident.

2. **Protected experimental materials:** The system prompt, persona dimensions/template, common shock, five treatment arms (S, C0, T1, T2, T3), outcome question, JSON schema, treatment paraphrases, answer-order variants, and later the reason-coding prompt/codebook. Code may only read, substitute defined placeholders, assemble, call, and parse—not rewrite or embed these materials.

3. **Freeze rules:** Before the main run, preregister pilot checks; pass the endpoint design checks; then freeze all canonical and robustness materials using a SHA-256 manifest and Git tag. Treatments must remain strictly nested and share the same decision time. Pilot results cannot be used to optimize treatment effects. After freezing, no prompt changes based on main results; substantive changes require a new protocol version and new runs.

4. **Pilot vs. main-run boundary:** Smoke tests, the 12-call tiny run, and the 48-call endpoint pilot are technical/design-calibration data only. They must be identified by separate run types and excluded from formal treatment-effect analysis. Main-run data must come exclusively from new run IDs generated after freezing; pilot observations cannot be pooled with them.

5. **Next single task:** **Task 0B.1 — Generate 3–5 candidate fictional protocol names only.** Do not write the common shock or conduct leakage searches yet.

Future work will proceed one atomic task at a time, with each task explicitly defining its goal, allowed files, protected files, acceptance test, and prohibited actions.

No code was written, no files were modified, and no project step was executed. Sources: :codex-file-citation{path="C:/Users/轩/xwechat_files/wxid_ss5gif56wted22_5895/msg/attach/9e20f478899dc29eb19741386f9343c8/2026-08/Rec/d0de5cc54196f8c1/F/0/LLM_Agent_DAO_Summer_Project_Experimental_Protocol.docx" purpose="source"} :codex-file-citation{path="C:/Users/轩/xwechat_files/wxid_ss5gif56wted22_5895/msg/attach/9e20f478899dc29eb19741386f9343c8/2026-08/Rec/d0de5cc54196f8c1/F/2/LLM_Agent_DAO_Atomic_Task_Execution_Workflow_v1.1.docx" purpose="source"}

---

## 3. Human Check

According to Workflow requirements, does AI accurately restate the following five points?
- [Yes] (1) project goal
- [Yes] (2) protected experimental materials
- [Yes] (3) freeze rules
- [Yes] (4) pilot vs. main-run data boundary
- [Yes] (5) the next single task

**Conclude：** Pass
