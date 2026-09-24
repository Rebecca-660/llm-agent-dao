# Zhipu Pilot Execution Authorization v1.0

## Researcher decisions

- Decision date: `2026-09-03`
- Provider: `zhipu`
- Primary model: `glm-4.7`
- Output Requirement: `v1.1`
- Planned design: 16 personas × `S/C0/T3` = 48 calls
- Status: authorized for one complete Endpoint Pilot execution

The researcher reviewed the machine-verified dry-run status and stated that they trusted the fixed configuration and did not require an additional signed human dry-run checklist before continuing. The checklist at `validation/pilot_zhipu_glm4.7_dry_run/manual_review_checklist.md` remains visibly unsigned; no AI agent has completed or signed it on the researcher's behalf.

The researcher then explicitly authorized:

> 授权使用 GLM-4.7 执行48次真实 Endpoint Pilot API 调用及相关 token 消耗。

This authorization applies only to one complete 48-cell Endpoint Pilot using the configuration recorded in `00_protocol/primary_model_replacement_decision_v1.0.md`:

- canonical 16-persona grid;
- canonical `S`, `C0`, and `T3` treatment wording;
- canonical ascending answer order;
- Output Requirement `v1.1`;
- `temperature=0` retained as registered metadata;
- `do_sample=false`;
- thinking mode disabled;
- independent context for every cell;
- a new unique run ID;
- new exclusively created append-only raw JSONL and attempt log.

The successful one-call record `connectivity_20260903T055423Z_fa718aa2` is a connectivity check only. It must not be counted among, substituted for, pooled with, or analyzed as part of the 48-cell Pilot.

All earlier OpenAI Pilot, failed API, Tiny Run, Smoke, connectivity, validation, and dry-run records remain excluded from the new Pilot dataset. Successfully returned but invalid or surprising model content must be retained without re-asking. The execution step does not determine whether the Pilot passes, authorize material freeze, or authorize a main run.
