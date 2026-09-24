# Primary Model Replacement Decision v1.0

## Decision record

- Decision version: `v1.0`
- Decision date: `2026-09-03`
- Researcher decision: replace the previously planned OpenAI primary model with Zhipu AI `glm-4.7`
- New provider: `zhipu`
- New requested model: `glm-4.7`
- Role: replacement primary model, not a secondary-model robustness check
- Status: approved for zero-API implementation and dry-run validation only

This record documents the researcher's model-selection decision before any Zhipu Pilot or main-run response is generated or inspected. It does not authorize a paid API call, approve a Pilot, freeze the materials, or authorize a main run.

## Reason for replacement

The OpenAI rerun attempt could not execute successfully because the API account had no available credit. Zhipu AI provides the researcher with an active resource package explicitly associated with `glm-4.7`. The replacement is therefore based on API accessibility, available research resources, and the need to complete the minimum summer-project scope. It is not based on observed treatment ordering, statistical significance, effect size, or a preference for particular model decisions.

No claim is made that `glm-4.7` is behaviorally equivalent to `gpt-4o-mini` or any newer Zhipu model. Model identity is part of the scope of inference. Findings from the new main experiment, if eventually authorized and completed, will be reported as behavior observed from the recorded `glm-4.7` configuration rather than generalized to all language models.

## Relationship to earlier Pilot records

The following records remain preserved but are excluded from the new Zhipu Pilot and all later main-run data:

1. First completed OpenAI Pilot: `pilot_20260901T101427Z_d4d53cb9`. It used Output Requirement v1.0 and failed the preregistered category-diversity and category-concentration criteria.
2. Failed OpenAI v1.1 execution attempt: `pilot_20260903T014531Z_1ab7dbe1`. It produced API errors because the account credit balance was exhausted and is not a valid completed Pilot.
3. All Smoke, Tiny Run, dry-run, validation, and Pilot records produced before this decision.

These records must never be pooled with, substituted into, or selectively used to complete the new Zhipu Pilot. The new Pilot must use a new run ID, new exclusively created raw JSONL, and new attempt log.

## Fixed experimental materials

The model replacement does not authorize changes to:

- the final protocol name;
- the 16-persona grid or canonical persona template;
- the common shock;
- canonical `S`, `C0`, and `T3` wording;
- the decision time;
- the canonical ascending answer order;
- the outcome question;
- the system prompt;
- Output Requirement `v1.1`;
- parser validity rules;
- the original Pilot machine or human-review thresholds; or
- the fixed manual-review seed `20260901`.

The prompt presented to each matched cell must remain byte-identical to the approved Output Requirement v1.1 dry-run prompt. Provider-specific request envelopes and response structures must be recorded separately and must not be inserted into the experimental prompt text.

## Provider execution configuration

The Zhipu Pilot configuration is fixed as follows before any call:

- provider: `zhipu`;
- requested model: `glm-4.7`;
- API endpoint: `https://open.bigmodel.cn/api/paas/v4/`;
- SDK: OpenAI-compatible Python SDK, with its installed version recorded;
- endpoint family: Chat Completions;
- stream: disabled/default non-streaming execution;
- registered temperature field: `0`;
- sampling: `do_sample=false` for deterministic greedy decoding;
- thinking mode: disabled;
- context: a new independent system/user message pair for every cell;
- retries: only the existing logged transient-error rule;
- invalid model content: preserve without re-asking or silent repair;
- output requirement: explicit `v1.1` selection.

Because `do_sample=false` causes the provider to ignore sampling parameters, the recorded temperature remains a provenance link to the preregistered deterministic setting rather than an active random-sampling control. Both fields must remain visible in request metadata and hashes.

## Required validation sequence

Before a real Zhipu Pilot may be authorized:

1. Implement the provider-specific request path with mock tests and zero API calls.
2. Generate a separate 48-cell `P01`–`P16` × `S/C0/T3` Zhipu dry-run manifest.
3. Verify that all experimental prompt hashes match the previously approved Output Requirement v1.1 prompts for the same cells.
4. Verify provider, model, endpoint, sampling, thinking, SDK, output-requirement, and source metadata.
5. Complete and sign a human dry-run checklist.
6. Commit the decision, implementation, tests, and approved dry-run evidence.
7. Obtain separate researcher authorization for one paid connectivity call.
8. After a successful connectivity check, obtain separate authorization for the complete 48-call Pilot.

No Pilot may be passed or failed using expected treatment ordering or significance. The original preregistered machine thresholds, fixed-seed manual review, data-isolation rules, and researcher-only final decision remain applicable.
