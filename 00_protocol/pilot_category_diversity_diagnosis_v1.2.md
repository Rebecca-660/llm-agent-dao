# GLM-4.7 Pilot Category-Diversity Diagnosis v1.2

## Record identity and scope

- Diagnosis date: `2026-09-04`
- Selected Pilot run ID: `pilot_20260904T135552Z_be4faaf7`
- Provider/model: `zhipu` / `glm-4.7`
- Persona mechanics: `v1.1`
- Output Requirement: `v1.1`
- Raw SHA-256: `2c6b01611e2f44a59d8039f7fa654cdb60df91d6c908ecc92005db3a34efc6f0`
- Attempt-log SHA-256: `bc1e2d1c5af16402b3189a83e7019dee3230867c44e574c4b0a88f07154676dd`
- Status: read-only diagnostic evidence record; no prompt, configuration, freeze, main-run, or API authorization is created by this document.

This diagnosis addresses the remaining failure of the preregistered C0 category-diversity criterion. It does not calculate or interpret treatment ordering, contrasts, statistical significance, p-values, or effect sizes.

## Evidence boundary

The diagnosis uses the current preregistration, the mechanics v1.1 change/approval chain, the signed decision for this Pilot, the current formal prompt materials and runner, the 48 raw records and 48 attempt records for the selected run, and the isolated diagnostics generated from that run. No earlier Pilot raw response, Tiny Run, dry-run, or connectivity-check record was included in the calculations below.

The applicable preregistered thresholds are recorded in `00_protocol/preregistered_checks.md`, lines 33–79. The signed result and authorization boundary are recorded in `00_protocol/pilot_decision_mechanics_v1.1.md`, especially its five-criterion table and overall-decision section.

## 1. Directly established facts

### 1.1 C0 validity and category distribution

For the selected run:

- valid, non-refusal C0 responses: **16/16**;
- C0 mean `unstake_percentage`: **21.875%**;
- distinct C0 categories: **2**;
- C0 category counts: **0%=2**, **25%=14**, **50%=0**, **75%=0**, **100%=0**;
- C0 diversity threshold: at least **3** distinct categories;
- C0 diversity result: **FAIL**.

These values are preserved in `05_processed_data/pilot_mechanics_v1.1_diagnostics/machine_checks.md` and `machine_checks.json`. The two 0% C0 records are `P04_C0` and `P11_C0`, on raw JSONL lines 11 and 32. The other 14 C0 records selected 25%.

The remaining machine checks were: cell completeness/isolation PASS, C0 mean dynamic range PASS, combined category concentration PASS, and structured-output validity PASS. This document does not average those results with the failed diversity criterion.

### 1.2 Request configuration

All 48 records used one identical execution configuration:

- requested and returned model: `glm-4.7`;
- provider: `zhipu`;
- `temperature=0`;
- `do_sample=false`;
- `thinking_mode=disabled`;
- sampling metadata: `greedy_do_sample_false`;
- answer order: `canonical_ascending` (`0%, 25%, 50%, 75%, 100%`);
- `independent_context=true` and `previous_response_id=null`;
- persona mechanics/template: `v1.1`;
- Output Requirement: `v1.1`.

The fixed runner values and payload construction appear in `02_code/run_endpoint_pilot.py`, lines 52–59 and 126–147; per-record metadata are assembled at lines 264–283. The attempt log contains 48 response-received records, maximum attempt 1, and zero scheduled retries. Thus API retry variation did not produce the observed category pattern.

### 1.3 Answer and reason repetition

Across all 48 valid records, without separating or comparing treatment means:

- 35 responses selected 25% and 13 selected 0%;
- no response selected 50%, 75%, or 100%;
- all 35 responses selecting 25% used language matching either “partially unstaking” or “partial unstake”;
- all 35 responses selecting 25% also used risk-reduction, exposure-reduction, risk-mitigation, or risk-management language;
- all 13 responses selecting 0% explicitly invoked the staking contract as secure or safe;
- there were **40 distinct exact reason strings among 48 responses**.

Within C0 alone:

- there were **13 distinct exact reason strings among 16 responses**;
- one exact reason occurred three times, one exact reason occurred twice, and the remaining eleven reason strings occurred once each;
- the three-repeat reason was used by `P10_C0`, `P14_C0`, and `P15_C0`;
- the two-repeat reason was used by `P03_C0` and `P16_C0`.

Accordingly, the observed concentration is primarily concentration in the numeric response categories, not wholesale verbatim duplication of the complete reasons. Semantic motifs nevertheless repeat strongly: partial risk reduction maps to 25%, while contract-safety justification maps to 0%.

### 1.4 Persona pattern within C0

The 16-persona grid varies four binary dimensions. The two C0 records selecting 0% share three levels:

- holding tenure: `2 years`;
- governance involvement: `Passive holder`;
- prior incident experience: `No prior experience`.

They differ on portfolio exposure: `P04` has 50% exposure and `P11` has 10% exposure. The other 14 persona combinations selected 25% in C0.

This establishes that the outputs were not literally invariant across every persona. It also establishes that the realized persona variation crossed only one boundary in the five-category response scale. It does not establish that any persona dimension caused either category.

### 1.5 Formal wording relevant to the remaining pattern

The mechanics clarification is present in the formal persona at `01_prompts/personas/persona_template_v1.1.txt`, line 9: initiating unstaking starts the seven-day waiting period, selected tokens remain locked during it, and completion follows the waiting period.

Other scenario facts remain intentionally fixed, including:

- no evidence that the staking contract was compromised and staked tokens remain intact (`01_prompts/common_shock/common_shock_v1.0.txt`, line 3);
- no material token-price movement, a stable broader market, and unchanged personal liquidity need (`persona_template_v1.1.txt`, line 11; `common_shock_v1.0.txt`, line 5);
- a significant module exploit and uncertain longer-term platform consequences (`common_shock_v1.0.txt`, lines 1–5);
- exactly five ordered outcome categories (`01_prompts/outcome/outcome_question_v1.0.txt`, line 1; `01_prompts/output_schema/json_schema_v1.1.txt`, lines 3–6).

These facts can rationally support competing considerations—risk reduction versus retaining a position—but the present evidence does not identify how GLM-4.7 internally weighted them.

## 2. What improved after the mechanics clarification—and what cannot be concluded

The preceding documented GLM-4.7 Pilot had C0 mean 3.125%, pooled maximum-category share 91.3043%, and structured validity 46/48. The current mechanics v1.1 Pilot has C0 mean 21.875%, pooled maximum-category share 72.9167%, and structured validity 48/48. Thus the current run passes dynamic range, pooled concentration, and structured validity, whereas those first two design-quality criteria had previously failed. Cell completeness passed in both. C0 diversity remains at two categories, although the C0 counts shifted from 14 zero/2 twenty-five to 2 zero/14 twenty-five.

Those are observed differences between two complete runs. They do **not** prove that the mechanics clarification caused the changes. The calls are model generations rather than paired deterministic counterfactuals, and run-level conditions may include unobserved service behavior. The comparison may motivate the current diagnosis but is not a treatment-effect analysis or causal estimate.

## 3. Assessment of candidate mechanisms

### 3.1 Deterministic decoding

**Evidence:** every request used `do_sample=false`, `temperature=0`, and disabled thinking; 35/48 numeric answers converged on 25%. The runner explicitly labels this regime `greedy_do_sample_false`.

**Reasonable inference:** greedy decoding may map a range of close latent judgments to the same highest-probability discrete option. Because the formal prompt now passes the mean and pooled-concentration checks and the reasons show lexical variation, decoding mode is a plausible remaining contributor to category compression.

**Unknown:** no controlled GLM-4.7 run has held every prompt and request field constant while varying only the decoding regime. It is therefore unproven that stochastic decoding would create a third C0 category, and it could add noise without improving meaningful persona sensitivity.

### 3.2 Discrete five-category scale

**Evidence:** only the fixed set `0/25/50/75/100` is legal, and all current answers occupy the two lowest categories. The 35 partial-risk reasons all map to 25% even though their wording is not identical.

**Reasonable inference:** a coarse five-point scale can quantize multiple moderately different judgments into one category, particularly near 25%.

**Unknown:** the scale is a teacher/project requirement and was not experimentally varied. There is no evidence here that adding categories would be valid, desirable, or responsible for the failure. It must remain unchanged in the next minimal round.

### 3.3 Persona differentiation

**Evidence:** P04_C0 and P11_C0 differ from the other 14 C0 outputs and share three persona levels; 13 distinct C0 reason strings also show some response differentiation.

**Reasonable inference:** persona information is being used to some extent, but most combinations do not move the selected value across another 25-point boundary under the current execution regime.

**Unknown:** this single Cartesian grid does not identify which dimension, combination, or interaction matters. Changing persona facts after observing these outputs would introduce a new material change and would not be the smallest next test.

### 3.4 Scenario facts

**Evidence:** every prompt combines a substantial exploit and long-run uncertainty with an intact staking contract, stable price/market conditions, and unchanged liquidity need. The response reasons repeatedly use both the risk and safety sides of this information.

**Reasonable inference:** these fixed facts may create two dominant response modes—no unstaking because the staked position is intact, or 25% partial unstaking to manage uncertainty.

**Unknown:** the scenario facts are central controlled materials. The current data do not prove that any fact is incorrectly worded or should be removed, strengthened, or weakened. Editing them now would confound the mechanics revision with a further material intervention.

## 4. Minimum recommendation for the next round

The evidence is sufficient to recommend the following **single conceptual factor** for a controlled next Pilot:

> Keep every formal prompt, persona, treatment, outcome, answer order, model/provider, and Output Requirement unchanged; change only the GLM-4.7 decoding regime from the current greedy/non-sampling regime to one fixed, prespecified stochastic-sampling regime.

This recommendation is based on minimality, not on proof that decoding caused the failure. It avoids another prompt revision when the current prompt already passes four of five machine checks and both human checks. It also directly tests a plausible compression mechanism while preserving the experimental construct.

The decoding regime may require coordinated API fields (for example, enabling sampling and specifying its fixed sampling intensity). Those linked fields must be treated as **one prespecified execution regime**, documented before any new data, rather than as separately tuned factors. The exact supported field values must be fixed in the next protocol record and verified by zero-API mock/dry-run tests. Multiple regimes must not be run and compared post hoc to select whichever passes.

The following must remain fixed:

- `glm-4.7` and provider `zhipu`;
- persona template/unstaking mechanics v1.1;
- all 16 persona rows and dimensions;
- common shock and S/C0/T3 treatments;
- canonical outcome and ascending answer order;
- Output Requirement v1.1;
- independent context and retry/error rules;
- all five machine thresholds, seed `20260901`, 11/12 hallucination threshold, and 4/4 T3 comprehension threshold.

## 5. Decision and stopping boundary

This report recommends only that a single fixed decoding regime be preregistered as the next minimal test. It does not choose unsupported API values, change the runner, authorize an API call, approve freeze, or authorize a main run. If a supported fixed regime cannot be specified before observing new output, the workflow must stop for a researcher decision rather than trying several settings and retaining a preferred result.

The controlling Pilot decision remains **FAIL**. No preregistered threshold is reduced or waived. If a new full Pilot is later authorized, it must use a new run ID, preserve all prior data, and be evaluated without reference to treatment ordering, significance, effect size, or expected direction.
