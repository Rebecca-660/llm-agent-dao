# GLM-4.7 Endpoint Pilot 0% Floor Diagnosis v1.1

## Record identity and scope

- Diagnosis date: `2026-09-04`
- Pilot run ID: `pilot_20260903T055848Z_a5ef2915`
- Provider/model: `zhipu` / `glm-4.7`
- Run type: `pilot`
- Output Requirement: `v1.1`
- Raw record: `03_raw_outputs/pilot/pilot_20260903T055848Z_a5ef2915.jsonl`
- Raw SHA-256: `5ee208decea0755a278d93f87ab6835ff09fe727c313a686802172e16bae5704`
- Status of this document: diagnostic evidence record only; it does not approve a prompt revision, material freeze, or main run.

This report concerns only the identified GLM-4.7 Pilot. It does not analyze treatment effects and does not use treatment ordering, statistical significance, effect size, or agreement with an expected result as a diagnostic criterion. The applicable prohibition appears in `00_protocol/preregistered_checks.md`, lines 138–149.

## Evidence basis

The evidence reviewed was limited to the materials and records authorized for this diagnosis:

1. The preregistered Pilot design and thresholds (`00_protocol/preregistered_checks.md`, lines 7–13 and 33–79).
2. The signed Pilot decision (`00_protocol/pilot_decision_glm4.7_v1.1.md`, lines 3–15 and 34–82).
3. The canonical persona, common shock, S/C0/T3 treatment, outcome, and Output Requirement v1.1 files.
4. The request metadata, assembled prompts, raw responses, and parse results in the 48 JSONL records of the identified run.
5. The preserved machine results in `05_processed_data/pilot_v1.1_diagnostics/machine_checks.md` and `machine_checks.json`.

The raw run metadata records `temperature=0`, `sampling_mode=greedy_do_sample_false`, `do_sample=false`, `thinking_mode=disabled`, canonical ascending answer order, independent context, and Output Requirement v1.1. The runner constants and request construction corresponding to this configuration appear in `02_code/run_endpoint_pilot.py`, lines 50–57, 125–147, and 243–264.

## 1. Directly established facts

### 1.1 Preregistered machine outcomes

The following facts are reproduced from the preserved diagnostics, not recalculated using any other run:

- The run contains 48 unique cells: 16 each for S, C0, and T3 (`machine_checks.md`, line 13; `machine_checks.json`, lines 24–47).
- Structured validity was 46/48, with two preserved parsing failures and no refusal candidates, API errors, or empty responses (`machine_checks.md`, lines 17–24; `machine_checks.json`, lines 89–117).
- Among the 46 valid, non-refusal responses, **42 selected 0%** and **4 selected 25%**. Thus 0% represented **42/46 = 91.3043%** of valid responses (`machine_checks.md`, line 16; `machine_checks.json`, lines 73–87).
- The valid C0 mean was **3.125%**, below the preregistered inclusive lower bound of 15% (`machine_checks.md`, line 14; `preregistered_checks.md`, lines 45–53).
- Valid C0 responses occupied only **2 categories**, with `0%=14` and `25%=2`, rather than the required minimum of 3 categories (`machine_checks.md`, line 15; `preregistered_checks.md`, lines 55–60).
- Consequently, the C0 dynamic-range, C0 category-diversity, and pooled concentration criteria failed. Cell completeness/isolation and structured validity passed. The signed overall decision is FAIL, with freeze and main run not authorized (`pilot_decision_glm4.7_v1.1.md`, lines 34–44 and 64–82).

### 1.2 Response-text diagnostic counts

The following counts are transparent descriptive coding of the `reason` field in the 46 successfully parsed records. They are not new pass/fail thresholds and are not treatment-effect analysis.

- **45/46 reasons relied on the stated safety or intactness of the staking contract as supporting justification.** This coding includes reasons that used contract safety to justify holding all tokens or keeping a majority staked. It excludes `P09_C0`, where contract safety was acknowledged with “despite” while the stated decision rationale was risk reduction. The common shock supplies the underlying fact that there was no evidence the staking contract was compromised and that staked tokens remained intact (`01_prompts/common_shock/common_shock_v1.0.txt`, line 3).
- **18/46 reasons explicitly invoked the seven-day waiting period or characterized immediate action/unstaking as unnecessary.** For reproducibility, this narrow count includes explicit references to the `7-day waiting period`/`waiting period`, `no immediate need`, or `immediate action unnecessary`; it does not count generic statements about waiting for further information unless one of those concepts is also explicit.
- The **4 valid nonzero responses** were `P05_S`, `P05_C0`, `P07_S`, and `P09_C0`; each selected 25%. Their original records appear respectively on JSONL lines 13, 14, 19, and 26. No valid response selected 50%, 75%, or 100%.

These coding counts describe repeated language in observed responses. They do not establish why the model selected those answers.

### 1.3 Wording relationship in the formal materials

The canonical persona states: “Unstaking requires a 7-day waiting period and carries no additional penalty” (`01_prompts/personas/persona_template_v1.0.txt`, line 9).

The canonical outcome asks what percentage the participant would “initiate unstaking for right now” (`01_prompts/outcome/outcome_question_v1.0.txt`, line 1). Output Requirement v1.1 requires one allowed integer and one concise reason but does not explain the mechanics of initiating an unstaking request (`01_prompts/output_schema/json_schema_v1.1.txt`, lines 1–8).

Across the authorized canonical files, the text does **not explicitly state** that initiating unstaking now starts the seven-day waiting period, that selected tokens remain locked during that waiting period, and that completion occurs only after the waiting period ends. This absence is a property of the inspected wording; it is not evidence by itself that the model misunderstood it.

## 2. Reasonable inferences

### 2.1 Potential initiation/completion confusion

It is a **reasonable, evidence-supported inference** that at least some responses may have treated “initiate unstaking right now” as if the relevant action were an immediate completed exit. The support for this inference is the combination of:

1. the formal wording relationship described above;
2. the 18 reasons explicitly invoking the waiting period or lack of need for immediate action; and
3. repeated language such as “the 7-day waiting period prevents immediate exit, so I will wait ... before acting.”

Under the natural mechanics contemplated by the project, initiating now is the action that begins the waiting period; the inability to complete exit immediately does not logically prevent initiation. The observed reasons therefore expose a plausible distinction that the current wording leaves implicit.

This is **not a demonstrated causal explanation** for the 0% selections. The model was not queried about its interpretation, and no controlled comparison has yet varied only this clarification.

### 2.2 Deterministic decoding as a possible amplifier

The run used deterministic/greedy configuration (`temperature=0`, `do_sample=false`, thinking disabled). Given the highly repeated response patterns, deterministic decoding may have amplified convergence on a single preferred completion. This is a **plausible but unverified contributor**, not an established cause. No within-model controlled comparison at a different fixed decoding configuration is available here.

## 3. Unknown or unconfirmed causes

The present evidence does not establish the relative contribution, if any, of:

- ambiguity between initiating unstaking and completing unstaking;
- deterministic decoding;
- GLM-4.7-specific response tendencies;
- the strong common-shock reassurance that the staking contract was not compromised and tokens remained intact;
- the absence of changed price or personal liquidity need in the persona/common scenario;
- the discrete five-category response scale or ascending option order; or
- interactions among any of these features.

In particular, the fact that 45/46 reasons used staking-contract safety is direct textual evidence of a repeated rationale, but it does not show that the safety statement is defective or causally responsible for the floor. That statement is part of the controlled scenario and is not approved for alteration by this diagnosis.

## 4. Why the earlier OpenAI Pilot is not a single-factor causal comparison

The earlier OpenAI Pilot and this GLM-4.7 Pilot cannot identify a causal effect of removing the completed 50% answer example. Between them, more than one factor changed, including provider/model, Output Requirement version, API execution path, and provider-specific decoding configuration. The earlier concentration at 50% and the present concentration at 0% are therefore historical observations from different configurations, not a randomized or single-factor comparison.

Accordingly, neither “the example caused 50%” nor “removing the example caused 0%” is established by comparing the two Pilots. Likewise, the comparison cannot isolate a GLM-4.7 model effect.

## 5. Minimal candidate direction for a subsequent draft

The first and smallest candidate direction is to **clarify the existing seven-day waiting-period mechanics only**. A later draft may make explicit the following already-intended temporal relationship:

- initiating unstaking now starts the seven-day waiting period;
- tokens selected for unstaking remain locked during that period; and
- unstaking completes only after the waiting period ends.

This section specifies a drafting direction, not approved prompt wording. Any candidate text must be created separately, compared line by line with the canonical material, and reviewed by the researcher before it can become a new formal version.

To preserve interpretability, the first remediation round should not simultaneously change temperature, model/provider, treatment wording, persona dimensions, common shock, outcome levels, answer order, or Output Requirement v1.1. A full 48-cell Pilot under a new run ID would still be required after any approved material change (`00_protocol/preregistered_checks.md`, lines 151–163).

## 6. Decision boundary

This diagnosis does not approve the candidate clarification, does not revise any experimental material, and does not authorize freeze or a main run. The controlling Pilot decision remains **FAIL**, formal material freeze remains **NO**, and main run authorization remains **NO** until a separately approved revision passes the required validation and a new complete Pilot is evaluated under the preregistered rules.
