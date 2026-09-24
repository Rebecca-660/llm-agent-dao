# Unstaking Mechanics v1.1 Draft Approval Record

## Decision identity

- Researcher name/initials: `CDY`
- Decision date: `2026.9.4`
- Decision: **APPROVE**
- Approved scope: unstaking-mechanics clarification draft only
- API execution authorized: **NO**
- Formal material freeze authorized: **NO**
- Main run authorized: **NO**

This record transcribes the researcher's completed review in `01_prompt_drafts/unstaking_mechanics_v1.1/canonical_comparison_and_manual_review.md`. It does not independently reinterpret, edit, or improve the reviewed text.

## Reviewed source identity

- Candidate text: `01_prompt_drafts/unstaking_mechanics_v1.1/persona_template_v1.1_draft.txt`
- Candidate SHA-256: `3a3ed734a4297e5ba4d99753f15e8b53753318d6e8c2403070f72b015060d7ae`
- Review checklist: `01_prompt_drafts/unstaking_mechanics_v1.1/canonical_comparison_and_manual_review.md`
- Completed checklist SHA-256: `378daf3e8fca3724e26324584a6eb4182227f197d414612e7ac8cb99e706a289`

## Reviewed candidate text

The complete text reviewed by the researcher was:

```text
You have held governance tokens in this platform for {holding_tenure}.

Your current staked governance-token position is worth $8,000. This position represents {portfolio_exposure_percentage} of your total crypto portfolio, which is worth {portfolio_exposure_usd}.

Your governance involvement is: {governance_involvement}.

Your prior experience with a major crypto incident is: {prior_incident_experience}.

80% of your governance tokens in this platform are currently staked. The staking APY is 6%. Initiating unstaking starts a 7-day waiting period and carries no additional penalty. Tokens selected for unstaking remain locked during this period and become unstaked only after the 7-day waiting period ends.

The broader crypto market has not experienced significant movement today. Your personal liquidity needs have not changed. The incident has just occurred, and the governance-token price has not yet changed materially.

You are a retail cryptocurrency investor, not a professional trader,
smart-contract developer, or blockchain security researcher.
```

## Researcher checklist results

The researcher marked all 13 review items as checked:

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

No checklist item was left unchecked.

## Researcher rationale — verbatim

> 该草案精准实现了设计目标：通过补充“锁定状态”和“完成时间点”两句话，彻底厘清了“发起解押”与“完成解押”的时序关系，且未改动任何核心实验变量（选项、人物背景、事件、回应措辞、输出格式）。重复提及“7天”是澄清时序的必要写法，未构成不当强调。批准进入下一环节的材料准备步骤。

## Recorded decision

The source checklist contains exactly one selected decision:

- `[x] APPROVE`
- `[ ] REVISE`
- `[ ] REJECT`

The approved draft is therefore authorized to proceed to the separately controlled formal-material preparation and provenance step. Approval is limited to reproducing this exact reviewed candidate without further polishing or semantic alteration.

This approval does **not** itself place the draft in `01_prompts/`, change any canonical material, authorize an API call, authorize a formal material freeze, authorize a main run, or establish that the clarification will correct the observed 0% floor. Those actions and conclusions require their own subsequent records and validation gates.
