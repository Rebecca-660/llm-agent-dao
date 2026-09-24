# Unstaking Mechanics v1.1 Draft — Canonical Comparison and Manual Review

## Status and scope

- Status: **DRAFT — NOT FORMAL EXPERIMENTAL MATERIAL**
- Diagnostic basis: `00_protocol/pilot_floor_diagnosis_glm4.7_v1.1.md`
- Canonical comparison source: `01_prompts/personas/persona_template_v1.0.txt`
- Unchanged outcome source: `01_prompts/outcome/outcome_question_v1.0.txt`
- Candidate file: `01_prompt_drafts/unstaking_mechanics_v1.1/persona_template_v1.1_draft.txt`
- Researcher decision: **PENDING**
- Freeze/main-run authorization: **NO**

This candidate addresses only the potential confusion between initiating unstaking now and completing unstaking after the seven-day waiting period. It is not evidence that this ambiguity caused the observed 0% concentration, and it does not recommend any unstaking percentage.

## Exact changed passage

### Canonical v1.0

> 80% of your governance tokens in this platform are currently staked. The staking APY is 6%. Unstaking requires a 7-day waiting period and carries no additional penalty.

### Candidate v1.1 draft

> 80% of your governance tokens in this platform are currently staked. The staking APY is 6%. Initiating unstaking starts a 7-day waiting period and carries no additional penalty. Tokens selected for unstaking remain locked during this period and become unstaked only after the 7-day waiting period ends.

### Atomic comparison

| Element | Canonical v1.0 | Candidate v1.1 draft | Intended status | Potential semantic risk requiring human judgment |
|---|---|---|---|---|
| Currently staked share | `80%` | `80%` | Unchanged | None identified. |
| Staking return | `The staking APY is 6%.` | Identical | Unchanged | None identified. |
| Trigger for waiting period | `Unstaking requires a 7-day waiting period` | `Initiating unstaking starts a 7-day waiting period` | Clarified | “Starts” makes the temporal trigger explicit. Confirm that this is the intended protocol mechanic and not a new substantive feature. |
| Waiting-period duration | `7-day` | `7-day` | Unchanged | None identified. |
| Status during waiting period | Implicit/not stated | `Tokens selected for unstaking remain locked during this period` | Newly explicit clarification | This adds an explicit interim-state fact. Confirm that “remain locked” accurately expresses the intended mechanic and does not imply an additional restriction. |
| Completion timing | Implicit/not stated | `become unstaked only after the 7-day waiting period ends` | Newly explicit clarification | “Only after” rules out immediate completion. Confirm that it does not alter the intended decision construct. |
| Additional penalty | `carries no additional penalty` | Identical phrase, now attached to initiating unstaking | Intended unchanged | Confirm that moving the grammatical attachment does not change whether the absence of penalty applies to the whole unstaking process. |
| Behavioral direction | No recommendation | No recommendation | Unchanged | Although neutral in wording, making the process clearer could change decisions; that is the intended measurement repair to assess in a new Pilot, not proof of equivalence. |

## Full persona template line-by-line comparison

Blank-line structure is preserved. Only canonical line 9 is replaced; the remaining nonblank lines are character-identical.

| Canonical line(s) | Content | Draft status |
|---:|---|---|
| 1 | Holding-tenure sentence and `{holding_tenure}` | Character-identical |
| 3 | Position value, portfolio exposure, and both exposure placeholders | Character-identical |
| 5 | Governance involvement and `{governance_involvement}` | Character-identical |
| 7 | Prior incident experience and `{prior_incident_experience}` | Character-identical |
| 9 | Staked share, APY, waiting-period mechanic, and no-penalty fact | Only changed passage; exact comparison above |
| 11 | Market movement, liquidity needs, incident timing, and token price | Character-identical |
| 13–14 | Retail-investor role and excluded professional roles | Character-identical |

The candidate retains exactly these five persona placeholders:

- `{holding_tenure}`
- `{portfolio_exposure_percentage}`
- `{portfolio_exposure_usd}`
- `{governance_involvement}`
- `{prior_incident_experience}`

Note: the canonical template contains five placeholder fields as listed above; no placeholder was added, removed, renamed, or resolved in the draft.

## Explicitly unchanged materials and constructs

The candidate does not edit or paraphrase any of the following:

- the canonical outcome question, including “initiate unstaking for right now”;
- the five allowed outcome levels `0%, 25%, 50%, 75%, 100%` or their order;
- the decision time point;
- common shock facts;
- S, C0, T1, T2, or T3 wording and information hierarchy;
- persona dimensions or their levels;
- the 80% currently staked share, $8,000 position value, 6% APY, market conditions, liquidity facts, or role restrictions;
- the absence of an additional unstaking penalty;
- Output Requirement v1.1, its JSON fields, legal values, or concise-reason requirement;
- provider, model, temperature, sampling configuration, or runner behavior.

No option is described as preferred, safer, rational, expected, or recommended. No example answer is included.

## Semantic risks for researcher review

1. **Mechanic accuracy:** confirm that initiating unstaking truly begins the seven-day clock.
2. **Locked-state accuracy:** confirm that selected tokens remain locked throughout the waiting period.
3. **Completion accuracy:** confirm that selected tokens become unstaked only after the waiting period ends.
4. **Penalty scope:** confirm that “no additional penalty” still applies to the same process as in v1.0.
5. **Construct preservation:** confirm that the draft clarifies how the existing action works without changing which action the outcome measures.
6. **Decision-time preservation:** confirm that “right now” still asks whether to initiate the process at the present decision point, not whether to complete an immediate exit.
7. **Neutrality:** confirm that the new wording neither encourages nor discourages unstaking.
8. **Information balance:** confirm that the clarification applies identically to every persona and treatment arm and adds no arm-specific information.
9. **Salience risk:** repeating `7-day waiting period` twice may increase the salience of the delay even while clarifying it. Decide whether this risk is acceptable or whether a revised neutral formulation is required.

## Researcher manual review checklist

Do not mark approval unless the exact candidate passage above has been reviewed.

- [x] The draft clarifies a process mechanic and does not recommend a behavior.
- [x] Initiating unstaking is correctly described as starting the seven-day waiting period.
- [x] Tokens selected for unstaking are correctly described as remaining locked during that period.
- [x] Completion only after the waiting period is accurate.
- [x] The seven-day duration is unchanged.
- [x] The no-additional-penalty fact is unchanged in meaning.
- [x] The present decision time point is unchanged.
- [x] The five outcome levels and their order are unchanged.
- [x] Persona dimensions, common shock, and treatment content are unchanged.
- [x] Output fields and JSON requirements are unchanged.
- [x] The text does not imply a preferred unstaking percentage.
- [x] The repeated mention of the seven-day period does not create unacceptable emphasis.
- [x] All listed semantic risks have been considered.

## Researcher decision

- Researcher name/initials: `_CDY______________`
- Decision date: `__2026.9.4______________`
- Decision — select exactly one: `[x] APPROVE  [ ] REVISE  [ ] REJECT`
- Notes/rationale: `该草案精准实现了设计目标：通过补充“锁定状态”和“完成时间点”两句话，彻底厘清了“发起解押”与“完成解押”的时序关系，且未改动任何核心实验变量（选项、人物背景、事件、回应措辞、输出格式）。重复提及“7天”是澄清时序的必要写法，未构成不当强调。批准进入下一环节的材料准备步骤。`

Approval here would authorize only the next provenance/formal-material preparation step. It would not authorize API calls, material freeze, or a main run.
