# Minimum-Scope Main Run Plan v1.2

## 1. Registration status and authority

- Plan date: `2026-09-04`
- Researcher: `CDY`
- Status: **fixed before any main-run data are generated**
- Material/configuration authority: `00_protocol/formal_material_freeze_v1.2.md`
- Authorizing Pilot decision: `00_protocol/pilot_decision_execution_config_v1.2.md`
- Authorizing Pilot run ID: `pilot_20260904T150852Z_18e62216`
- Main-run API calls authorized by this plan: **NO**

This plan defines the summer-project minimum-scope main experiment, its engineering checks, and its analysis before any main response exists. It authorizes runner implementation, tests, and a zero-API dry-run only. The real 80-call run requires a separate explicit authorization for API calls and token consumption.

No Pilot treatment ordering, contrast, significance result, or preferred direction is used to define this plan. Pilot, Tiny Run, smoke, dry-run, and connectivity-check data are calibration or engineering evidence only and can never enter the main analysis dataset.

## 2. Research question and minimum scope

The research question is whether increasingly substantive crisis responses change the immediate decision of long-term governance-token holders to initiate unstaking after a serious protocol incident that has not directly compromised the staking contract.

The minimum main design is the complete Cartesian product:

- personas: `P01`–`P16` from the frozen 16-persona grid;
- arms: `S`, `C0`, `T1`, `T2`, `T3`;
- cells: 16 personas × 5 arms = **80 unique persona × arm cells**;
- calls: exactly one new request for each planned cell;
- statistical design unit: the 16 prespecified fixed persona profiles;
- model calls are measurements of those fixed profiles, not 80 independent human subjects.

Each cell must use a new independent context and must not receive any prior treatment response, previous-response ID, or conversation history.

The minimum scope excludes:

- treatment wording robustness v2/v3;
- reversed answer order;
- additional temperature or decoding settings;
- stochastic repetitions of the same cell;
- a second model;
- human-sample calibration;
- claims about real DAO investors or a population-representative causal effect.

These exclusions must be reported as limitations or future extensions rather than silently described as completed robustness.

## 3. Frozen materials and execution configuration

Every main request must match the identities and SHA-256 values in `00_protocol/formal_material_freeze_v1.2.md`. The runner must fail before an API call if a frozen hash differs.

### 3.1 Materials

- protocol name: `Kelmoryn Protocol`;
- persona grid: `01_prompts/personas/personas_v1.0.csv`;
- persona/mechanics template: `01_prompts/personas/persona_template_v1.1.txt`;
- system prompt: `01_prompts/system/system_prompt_v1.0.txt`;
- common shock: `01_prompts/common_shock/common_shock_v1.0.txt`;
- treatments: canonical `S_v1.0.txt`, `C0_v1.0.txt`, `T1_v1.0.txt`, `T2_v1.0.txt`, and `T3_v1.0.txt`;
- outcome: `01_prompts/outcome/outcome_question_v1.0.txt`;
- answer order: canonical ascending `0%, 25%, 50%, 75%, 100%`;
- output requirement: `01_prompts/output_schema/json_schema_v1.1.txt` with exactly two fields and no concrete answer example;
- parser semantics: frozen `02_code/parser.py` behavior.

### 3.2 Provider and request configuration

- `run_type=main`;
- provider: `zhipu`;
- requested model: `glm-4.7`;
- decoding regime: `stochastic_low_v1.2`;
- `do_sample=true`;
- `temperature=0.2`;
- sampling-mode metadata: `stochastic_temperature_0.2`;
- thinking: disabled;
- no added `top_p`, request seed, penalty, or other sampling parameter;
- maximum attempts: 3;
- retry delays: 1.0 and 2.0 seconds;
- retry eligibility: transient network, rate-limit, and server errors only;
- successful API response with invalid content: retain and parse as invalid; never re-ask;
- output: new run ID and new exclusive append-only raw JSONL plus attempt log.

The exact returned model/version string and SDK version must be recorded as metadata; they must not be silently substituted for the requested model identity.

## 4. Run construction and stopping rules

### 4.1 Before execution

The runner and zero-API dry-run must establish all of the following:

1. exactly 80 expected cell IDs, with 16 in each of the five arms;
2. no duplicate, missing, or unexpected cell;
3. `run_type=main` for every record;
4. frozen material, source, prompt, and system hashes;
5. the frozen provider/model/decoding configuration;
6. independent context and no previous-response chaining;
7. complete request metadata and deterministic request hashing;
8. refusal to overwrite an existing raw-output or log path;
9. no use of a Pilot/Tiny/dry-run/connectivity run ID or file;
10. full automated test-suite success.

Any failure stops the workflow before real-call authorization.

### 4.2 During execution

- Send each of the 80 planned cells once under one newly generated main run ID.
- Do not inspect partial outcomes to change prompts, order, configuration, or remaining calls.
- Do not rerun a successful API response because its decision, reason, direction, or format is inconvenient.
- Apply only the frozen transient-error retry rule.
- Record every attempt, error, retry decision, timestamp, raw API response, raw response, and parse result.
- Never overwrite, resume, repair, or selectively append to a historical run.

### 4.3 Execution interruption

If the process terminates before all 80 planned cell records are written, preserve the incomplete run unchanged and mark it `aborted/incomplete`. Do not treat it as the main analysis run and do not resume it. A complete restart under a new run ID requires a separate researcher decision and API-cost authorization; the abandoned run remains archived and excluded.

### 4.4 End of run

One completed authorized 80-cell run is the main dataset source regardless of whether its treatment pattern is null, reversed, small, or statistically insignificant. No further main run, temperature, model, or wording specification may be selected after observing results under this minimum plan.

## 5. Engineering quality and validity checks

Before statistical analysis, report these checks without computing treatment effects:

### 5.1 Cell and run integrity

- record count and unique cell count;
- expected/missing/unexpected/duplicate cells;
- counts by arm;
- unique main run ID and `run_type=main`;
- independent-context status;
- prompt/system/source/request hash presence and frozen-hash agreement;
- absence of all Pilot, Tiny Run, dry-run, smoke, and connectivity-check records.

An incomplete, duplicate, contaminated, or hash-mismatched run fails engineering acceptance and stops analysis pending a documented researcher decision. It must not be silently repaired.

### 5.2 API and attempt status

- total attempts;
- API successes and failures by error class;
- retry count and cells with more than one attempt;
- completion timestamps and returned model/version values;
- empty responses.

### 5.3 Structured-response validity

A response is valid only if the frozen parser returns success and:

- the response is a JSON object;
- `unstake_percentage` is the integer 0, 25, 50, 75, or 100;
- `reason` is a non-empty string;
- required fields are present under the frozen parser procedure.

Report valid, parse-failure, illegal-value, empty-response, refusal, and API-error counts separately, with all denominators. Do not round, coerce, infer, or repair an invalid response. A refusal is missing, not 0%.

The design does not add a post hoc minimum-validity threshold for selecting a favorable run. If all 80 cells were properly attempted but some responses are invalid, preserve them as missing and apply the prespecified missing-data rules below. The validity rate remains a prominently reported quality limitation.

## 6. Outcomes and analysis population

### 6.1 Primary outcome

`unstake_percentage`, taking only `0`, `25`, `50`, `75`, or `100`, measured as the percentage of currently staked tokens for which the persona would initiate unstaking immediately.

### 6.2 Secondary outcome

`AnyUnstake = 1` if a valid `unstake_percentage > 0`; otherwise `AnyUnstake = 0` when the valid value is 0. Invalid, refused, empty, or failed responses remain missing and are never assigned 0.

### 6.3 Analysis population

- Arm-level summaries use all valid responses in that arm and report their exact denominator.
- A paired contrast uses a persona only when both relevant arm outcomes are valid.
- No imputation, weighting, rounding, winsorization, outcome transformation, or selective exclusion is permitted.
- Reasons are analyzed only for records with a non-empty reason from an otherwise valid parsed response.

## 7. Prespecified quantitative analysis

### 7.1 Primary descriptive summaries

For each of `S`, `C0`, `T1`, `T2`, and `T3`, report:

- valid and missing counts;
- mean and median `unstake_percentage`;
- count and percentage in each category `0/25/50/75/100`;
- `AnyUnstake` count and rate;
- the complete persona × arm outcome table.

Do not treat the monotonic ordering of arm means as a pass criterion.

### 7.2 Primary estimands

The four primary estimands are the mean persona-level adjacent-arm paired differences, in percentage points:

1. `C0 − S`: minimal acknowledgment relative to organizational silence;
2. `T1 − C0`: generic reassurance relative to minimal acknowledgment;
3. `T2 − T1`: specific corrective plan relative to generic reassurance;
4. `T3 − T2`: executed, publicly verifiable action relative to plan only.

For each contrast and each complete persona pair, define

`d[p,a,b] = unstake_percentage[p,a] − unstake_percentage[p,b]`,

where the first named arm is `a` and the second is `b`. Report:

- number of complete pairs;
- all 16 persona-level differences when complete;
- mean difference;
- median difference;
- minimum and maximum difference;
- counts of negative, zero, and positive differences;
- proportion negative, zero, and positive among complete pairs.

Direction is reported as observed. No required sign, minimum effect size, or expected ordering is imposed.

### 7.3 Exact paired sign-flip/permutation calculation

For each primary contrast, use the complete persona-level numeric differences and the absolute mean difference as the statistic. Enumerate all `2^n` sign assignments for the `n` complete pairs, including zero differences as observed. The two-sided exact p-value is the fraction of assignments for which the permuted absolute mean is at least the observed absolute mean; include equality in the numerator. Record `n`, the observed statistic, number of assignments, numerator, and exact p-value.

This calculation is a finite-profile diagnostic for whether paired differences are systematically displaced from zero. Because the 16 personas are prespecified fixed design profiles rather than a random sample of humans, it must not be presented as population inference about real investors. P-values do not determine whether results are reported, accepted, or described as substantively important.

### 7.4 Optional auxiliary output within the minimum analysis

A persona fixed-effects regression may be reported only as descriptive/auxiliary:

`Unstake_pc = alpha_p + beta1*C0_c + beta2*T1_c + beta3*T2_c + beta4*T3_c + error_pc`,

with S as the reference arm. Ordinary cluster-robust standard errors with only 16 fixed personas must not be treated as reliable population inference. The paired estimands above remain primary; regression output cannot replace them.

Prompt-specification ranges, temperature sensitivity, cross-model comparisons, and wording/order robustness are outside the minimum scope and therefore are not computed.

## 8. Missing, failed, and anomalous records

- Preserve every raw and attempt record unchanged.
- Never replace or re-ask a successful but invalid model response.
- Never code refusal, API error, empty response, illegal value, or parse failure as 0%.
- Arm summaries use available valid observations with denominators shown.
- Primary paired estimates use pairwise complete observations separately for each contrast; report exactly which persona IDs are omitted and why.
- Do not use complete-case selection across all five arms when only a two-arm contrast is required.
- Do not infer missing values from the persona's other arms.
- Report sensitivity only as a transparent table of denominators; no unregistered imputation analysis is permitted.
- A surprising but valid value is data, not an anomaly to remove.

## 9. Post-decision reason coding

Reason analysis occurs only after the quantitative outcome dataset and calculations are fixed. Reasons do not determine exclusions, recoding, treatment success, or quantitative specifications.

The frozen descriptive multi-label codebook is:

1. Future platform/security risk;
2. Confidence/trust in the team;
3. Adequacy of corrective response;
4. Value of verifiable action;
5. Wait-and-see reasoning;
6. Portfolio exposure/risk management;
7. Staking yield/opportunity cost;
8. Governance attachment.

Rules:

- zero, one, or multiple categories may be assigned when explicitly supported by the sentence;
- do not infer an unstated psychological mechanism;
- retain the original reason alongside all codes;
- add an `other/unclear` flag for relevant text that cannot be assigned without invention;
- report counts and shares by arm with valid-reason denominators;
- shares may sum above 100% because coding is multi-label;
- present reason results as descriptive attention/rationale patterns only, not mediators or causal mechanisms;
- preserve a versioned codebook, coding instructions, coding output, and any adjudication record.

The reference paper's general practice of using a fixed shared taxonomy and treating explanation frequencies as descriptive is adopted; its human-calibration, demographic weighting, and causal correction machinery is not imported into this minimum project.

No additional model/API coding call is authorized by this plan. If an LLM is later used to code reasons, its prompt, model, sampling, validation sample, costs, and researcher approval require a separate preregistered plan and authorization. Otherwise the 80 concise reasons may be coded from the frozen codebook with a fully auditable record; any AI-assisted suggestions must remain distinguishable from researcher adjudication.

## 10. Required outputs and reproducibility

The minimum project must preserve:

- exclusive append-only main raw JSONL and attempt log;
- a machine-readable processed dataset with raw-record keys and hashes;
- a data dictionary and engineering/validity report;
- reproducible analysis code;
- arm summary table and complete outcome distribution table;
- persona-level paired-difference table for all four primary contrasts;
- exact sign-flip/permutation results with calculation metadata;
- `AnyUnstake` summaries;
- descriptive reason-code table and codebook, if completed;
- figures showing arm outcomes/distributions and paired effects without hiding null or reversed results;
- README commands connecting frozen materials to raw data, processed data, tables, and figures;
- a report that clearly distinguishes LLM-agent outputs from real human behavior.

At least one arm mean and one persona-level paired difference must be independently hand-calculated and compared with the scripted result before final reporting. This is a calculation check, not a prompt or response-content review.

## 11. Decision and reporting prohibitions

After main data exist, none of the following may be changed or used to select a preferred dataset/specification:

- prompt wording or material version;
- model/provider or decoding configuration;
- answer order;
- included persona/arm cells, except prespecified missingness handling;
- primary outcome, `AnyUnstake`, contrasts, contrast direction, or paired calculation;
- treatment ordering requirements;
- a significance, p-value, or minimum effect-size threshold;
- the decision to report a result;
- reason code definitions based on which labels produce a preferred narrative.

Null, small, reversed, heterogeneous, or statistically insignificant findings remain reportable findings. Any exploratory calculation requested after inspecting outcomes must be labeled exploratory and must not replace the analysis above.

## 12. Workflow gate after this plan

The next permitted step is to implement and mock-test an independent 80-cell main-run runner against `formal_material_freeze_v1.2.md`. After that, a separate zero-API dry-run must verify all 80 requests and hashes. Only a successful read-only preflight followed by explicit researcher authorization for exactly 80 real GLM-4.7 calls and related token consumption can permit main execution.
