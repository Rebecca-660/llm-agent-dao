# Unstaking Mechanics v1.1 Change and Provenance Record

## Change identity

- Formal material version: `persona_template_v1.1`
- Formal material path: `01_prompts/personas/persona_template_v1.1.txt`
- Previous canonical version retained at: `01_prompts/personas/persona_template_v1.0.txt`
- Researcher approval: **APPROVE**
- Researcher name/initials: `CDY`
- Approval date: `2026.9.4`
- Source Pilot run ID: `pilot_20260903T055848Z_a5ef2915`
- Scope of change: waiting-period mechanics clarification only

## Provenance chain

1. The GLM-4.7 Pilot decision recorded an overall FAIL and did not authorize freeze or a main run: `00_protocol/pilot_decision_glm4.7_v1.1.md`.
2. The subsequent evidence report distinguished direct observations, reasonable inference, and unconfirmed causes: `00_protocol/pilot_floor_diagnosis_glm4.7_v1.1.md`.
3. The minimum candidate was drafted and compared with the canonical persona: `01_prompt_drafts/unstaking_mechanics_v1.1/persona_template_v1.1_draft.txt` and `canonical_comparison_and_manual_review.md`.
4. Researcher `CDY` checked all 13 review items, selected only APPROVE, dated the decision `2026.9.4`, and approved the exact draft for formal-material preparation: `00_protocol/unstaking_mechanics_v1.1_approval.md`.
5. The approved candidate was copied without editing to `01_prompts/personas/persona_template_v1.1.txt`.

## SHA-256 identities

| Artifact | SHA-256 |
|---|---|
| Previous canonical `01_prompts/personas/persona_template_v1.0.txt` | `20e58530d17bf29914a442597aa06b277ef3f00c8f0e5827ee6f7a897f07c290` |
| Approved draft `01_prompt_drafts/unstaking_mechanics_v1.1/persona_template_v1.1_draft.txt` | `3a3ed734a4297e5ba4d99753f15e8b53753318d6e8c2403070f72b015060d7ae` |
| Formal `01_prompts/personas/persona_template_v1.1.txt` | `3a3ed734a4297e5ba4d99753f15e8b53753318d6e8c2403070f72b015060d7ae` |
| Completed review `01_prompt_drafts/unstaking_mechanics_v1.1/canonical_comparison_and_manual_review.md` | `378daf3e8fca3724e26324584a6eb4182227f197d414612e7ac8cb99e706a289` |
| Approval record `00_protocol/unstaking_mechanics_v1.1_approval.md` | `f2ed924a27d5fd21af8ff6f2a3da740de4ecdc740ca4827d802689b7b53580ba` |

The matching draft and formal hashes establish byte-for-byte identity at the time this record was created.

## Exact old/new difference

Only the waiting-period mechanics passage in the persona template changed.

### Previous canonical v1.0 passage

```text
80% of your governance tokens in this platform are currently staked. The staking APY is 6%. Unstaking requires a 7-day waiting period and carries no additional penalty.
```

### Approved formal v1.1 passage

```text
80% of your governance tokens in this platform are currently staked. The staking APY is 6%. Initiating unstaking starts a 7-day waiting period and carries no additional penalty. Tokens selected for unstaking remain locked during this period and become unstaked only after the 7-day waiting period ends.
```

The formal v1.1 passage makes explicit that:

- initiating unstaking starts the existing seven-day waiting period;
- selected tokens remain locked during that period; and
- completion occurs only after the waiting period ends.

The 80% staked share, 6% APY, seven-day duration, and absence of an additional penalty are retained.

## Unchanged material boundary

No other experimental-material change is part of this version:

- all other persona-template lines and all five persona placeholders are unchanged;
- persona dimensions and levels are unchanged;
- common shock wording and facts are unchanged;
- S/C0/T1/T2/T3 treatment wording, information quantity, and nesting are unchanged;
- the outcome question, current decision time point, five response levels, and canonical ascending answer order are unchanged;
- Output Requirement v1.1 and its JSON schema are unchanged;
- provider, model, temperature, sampling configuration, assembler, runner, validation, processed data, and raw outputs are unchanged by this step.

The previous canonical persona template remains preserved and must remain reproducible. This new version must be selected explicitly in subsequent assembler/runner work; its existence alone does not change prior requests.

## Authorization boundary

This record documents incorporation of the approved text as a separately versioned formal material. It does not establish that the clarification resolves the observed floor effect. It does not authorize API calls, material freeze, or a main run. Those actions remain subject to separate code, validation, dry-run, researcher-approval, and new-Pilot gates.
