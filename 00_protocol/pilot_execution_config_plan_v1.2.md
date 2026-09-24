# Endpoint Pilot Execution-Configuration Plan v1.2

## Registration status and decision boundary

- Plan date: `2026-09-04`
- Status: fixed before any v1.2 dry-run or model output is generated
- Basis: `00_protocol/pilot_category_diversity_diagnosis_v1.2.md`
- Preceding failed Pilot: `pilot_20260904T135552Z_be4faaf7`
- Formal prompt change in this round: **NONE**
- Real API execution authorized by this record: **NO**
- Material freeze authorized: **NO**
- Main-run preparation authorized: **NO**

This plan prespecifies one conceptual execution factor for the next complete Endpoint Pilot. It does not lower a threshold, alter an experimental scenario, authorize a trial call, or permit selection among several configurations after observing their outputs.

## 1. The single configuration factor and its fixed value

The sole changed experimental configuration field is:

- Configuration field: `decoding_regime`
- Previous value: `greedy_v1.1`
- New fixed value: `stochastic_low_v1.2`

The new value has one fixed, indivisible API representation:

| Request subfield | `greedy_v1.1` | `stochastic_low_v1.2` |
|---|---:|---:|
| `do_sample` | `false` | `true` |
| `temperature` | `0` | `0.2` |

`do_sample=true` and `temperature=0.2` are linked implementation subfields of the one named decoding regime. They must not be varied independently, crossed factorially, tuned cell by cell, or treated as two candidate factors. The runner must expose the regime through one controlled selection and derive both request subfields from it.

The fixed low value `0.2` is selected as a conservative departure from greedy decoding: it permits sampling while limiting randomness. It is not selected because it has produced a preferred result; no request using this regime has been generated or sent at the time of this plan.

No `top_p`, seed, penalty, maximum-token, or other sampling parameter is added or changed. Any provider default not explicitly controlled in the prior run remains omitted. Thinking remains disabled.

## 2. Rationale, evidence level, and non-causal boundary

The preceding Pilot passed four of five machine checks but failed C0 category diversity, with 14 C0 selections at 25% and 2 at 0%. It used `do_sample=false` and `temperature=0`. The R21 diagnosis found numeric category compression alongside substantial lexical variation in the reasons and therefore identified decoding regime as the smallest plausible next factor.

This is a design-calibration hypothesis, not a causal conclusion. There is no controlled evidence yet that stochastic sampling will produce a third C0 category, preserve the other passing criteria, or improve meaningful persona differentiation. The purpose of the next complete Pilot is to apply the unchanged preregistered quality checks to the fixed configuration, not to seek a preferred treatment pattern.

## 3. Materials and settings held fixed

Every item below must remain identical to the preceding mechanics v1.1 Pilot:

- provider: `zhipu`;
- requested model: `glm-4.7`;
- persona grid: all 16 rows in `01_prompts/personas/personas_v1.0.csv`;
- persona template and unstaking mechanics: `01_prompts/personas/persona_template_v1.1.txt`;
- protocol name and system prompt;
- common shock v1.0;
- canonical S, C0, and T3 treatment wording used by the Endpoint Pilot;
- canonical T1 and T2 materials, although they are outside the Endpoint Pilot cells;
- treatment nesting and information content;
- outcome question v1.0;
- allowed outcome set and canonical ascending order: `0%, 25%, 50%, 75%, 100%`;
- Output Requirement v1.1 and its two-field JSON requirement;
- `thinking_mode=disabled`;
- 16 personas × S/C0/T3 = 48 planned cells;
- one independent context per cell and no previous-response chaining;
- provider endpoint and SDK request family;
- parser behavior;
- maximum attempts `3`, retry delays `1.0` and `2.0` seconds, and the existing transient-error-only retry rule;
- no retry when a successful API response contains invalid model content;
- append-only raw-output and attempt-log behavior.

Prompt text, system text, prompt/source hashes, and all formal material versions must be identical between the preceding Pilot requests and v1.2 requests. Request hashes are expected to differ because the prespecified decoding-regime payload changes.

## 4. Original acceptance thresholds retained unchanged

All five machine thresholds in `00_protocol/preregistered_checks.md` remain in force without modification:

1. **Cell completeness and isolation:** exactly 48 unique P01–P16 × S/C0/T3 cells, 16 per arm, from one new Pilot run.
2. **C0 mean dynamic range:** valid, non-refusal C0 mean between 15% and 75%, inclusive.
3. **C0 response-category diversity:** at least 3 distinct valid, non-refusal C0 categories.
4. **Combined category concentration:** no category above 85% among pooled valid, non-refusal S/C0/T3 responses.
5. **Structured-output validity:** at least 46/48 valid and non-refusal responses, with parsing failures, refusals, API errors, and empty responses separately retained and reported.

The formal human checks also remain unchanged:

- sampling seed: `20260901`;
- within each arm, sort P01–P16 and initialize an independent `random.Random(20260901)` instance;
- sample 4 from S, 4 from C0, and 4 from T3 without replacement or substitution;
- material factual hallucination: at least 11/12 PASS;
- T3 executed/publicly verifiable action comprehension: 4/4 PASS.

The previously used all-48 supplemental human read-through will **not** be repeated. It was an additional teacher-workflow quality audit, not a preregistered pass threshold. Omitting its repetition does not modify the fixed 12-record sampling rule or either formal human threshold.

## 5. Required implementation and zero-API validation

Before any real call:

1. the runner must implement `decoding_regime` as an explicit controlled parameter;
2. `greedy_v1.1` must still reproduce the previous request configuration;
3. `stochastic_low_v1.2` must map exactly to `do_sample=true` and `temperature=0.2`;
4. metadata and request hashing must record the regime and its derived fields;
5. mock tests must verify all 48 cells, independent context, append-only output, attempt/error/retry behavior, and invalid-content non-retry;
6. a zero-API 48-cell dry-run must prove that prompt, system, and source hashes are unchanged and that the sole request-configuration difference is the decoding regime;
7. any unplanned difference must stop the workflow before API authorization.

The dry-run may be machine-validated without a repeated researcher prompt-reading checklist because the formal prompt is unchanged. This efficiency rule does not waive the later fixed 12-record human review.

## 6. Run identity and data isolation

Any real v1.2 Pilot must:

- receive a new `run_id` generated only at execution time;
- use `run_type=pilot`;
- create new, exclusive JSONL raw-output and attempt-log files;
- never overwrite, append into, resume, repair, or selectively replace any old run;
- keep all earlier OpenAI and GLM-4.7 Pilots, Tiny Runs, dry-runs, connectivity checks, diagnostics, and human-review files separate;
- exclude every historical record from v1.2 threshold calculations;
- remain calibration data that can never be merged into main-run analysis data.

A real 48-call execution requires a separate, explicit researcher authorization covering API calls and token consumption. This plan supplies no such authorization.

## 7. Stopping rule

Only the single fixed `stochastic_low_v1.2` regime may be used for the next complete 48-cell Pilot. The following are prohibited:

- trialing several temperatures or sampling regimes and retaining the one that passes;
- changing the configuration after inspecting partial responses;
- rerunning an individual cell because its response is inconvenient, invalid, or unexpected;
- changing prompt wording in the same round;
- judging the Pilot by treatment ordering, contrast direction, significance, p-values, effect size, or agreement with an expected result.

After the full run, all five original machine checks and both original human checks must be applied. If any required criterion fails, the v1.2 Pilot decision is FAIL and the workflow stops. No further automatic tuning or repeated Pilot is authorized by this plan. If every criterion passes, the researcher may separately decide whether to authorize formal material freeze; passing does not itself perform the freeze.
