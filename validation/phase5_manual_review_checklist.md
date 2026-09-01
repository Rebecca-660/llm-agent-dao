# Phase 5 Manual Review Checklist

Review date: 2026-08-26  
Scope: `validation/P01_plus_common_shock.txt`, `validation/P01_C0_rendered.txt`, and `validation/P01_all_arms/P01_{S,C0,T1,T2,T3}.txt`

## Status legend

- `[x] Machine` — verified by exact-text or structural comparison during this audit.
- `[ ] Human` — requires the researcher to read the rendered prompts and make the stated judgment.
- Completion of machine checks does **not** constitute researcher approval of Phase 5.

## A. Protocol name and placeholders

- [x] Machine — Every full-arm prompt contains `Kelmoryn Protocol` exactly three times: common shock, condition, and outcome question.
- [x] Machine — `P01_plus_common_shock.txt` contains `Kelmoryn Protocol` exactly once.
- [x] Machine — No reviewed artifact contains `[ProtocolName]`.
- [x] Machine — No reviewed artifact contains an unresolved square-bracket placeholder shaped like `[Name]`.
- [x] Machine — No reviewed artifact contains an unresolved persona placeholder shaped like `{field_name}`.
- [x] Human — Confirm that `Kelmoryn Protocol` is spelled and capitalized correctly everywhere it appears.

## B. Persona consistency

- [x] Machine — The complete Persona section is character-for-character identical across S, C0, T1, T2, and T3.
- [x] Machine — The Persona section in `P01_C0_rendered.txt` matches the Persona section in `P01_all_arms/P01_C0.txt`.
- [x] Human — Read P01 and confirm that tenure, staked position, portfolio exposure, governance involvement, prior incident experience, APY, and unstaking delay describe one coherent investor.
- [x] Human — Confirm that the Persona contains no accidental condition-specific or incident-response information.

## C. Common shock consistency

- [x] Machine — The canonical common shock appears exactly once in each of the five full-arm prompts.
- [x] Machine — The common shock is character-for-character identical across all five arms.
- [x] Machine — `P01_plus_common_shock.txt` ends with the exact canonical common shock and contains no treatment, outcome, or JSON requirement afterward.
- [x] Human — Confirm that the incident is severe enough to create forward-looking platform risk.
- [x] Human — Confirm that the shock does not state or imply that the staking contract or the holder's staked assets have already been compromised.
- [x] Human — Confirm that all incident-status facts are confined to the common shock rather than introduced by a treatment.

## D. Decision time

- [x] Machine — Every condition locates the decision several hours after the incident became public.
- [x] Machine — S uses “Several hours have passed since the incident became public”; C0–T3 use “Several hours after the incident became public”.
- [x] Human — Confirm that these two constructions communicate the same decision time and do not create a timing difference between Silence and response arms.
- [x] Human — Confirm that no later sentence introduces a different elapsed time in any arm.

## E. Treatment assignment and cross-arm contamination

- [x] Machine — Each full-arm file contains exactly one complete copy of its designated formal treatment text.
- [x] Machine — S contains the formal Silence text and no response statement.
- [x] Machine — C0 contains no reassurance, corrective plan, or executed-action additions beyond the formal C0 text.
- [x] Machine — T1 contains C0 plus the formal reassurance addition and no T2/T3 addition.
- [x] Machine — T2 contains complete T1 plus the formal corrective-plan addition and no T3 addition.
- [x] Machine — T3 contains complete T2 plus the formal executed/verifiable-action addition.
- [x] Human — Read the five prompts side by side and confirm that no wording or fact has leaked into the wrong arm.
- [x] Human — Confirm that differences between arms are limited to the intended crisis-response increments.

## F. Treatment nesting and interpretation

- [x] Machine — Formal T1 starts with complete C0, character for character.
- [x] Machine — Formal T2 starts with complete T1, character for character.
- [x] Machine — Formal T3 starts with complete T2, character for character.
- [x] Human — Confirm that T1 is generic reassurance rather than a specific corrective commitment.
- [x] Human — Confirm that T2 is a specific future corrective plan, not an already completed action.
- [x] Human — Confirm that T3 clearly describes an already executed, publicly verifiable, materially costly action.
- [x] Human — Confirm that T3 does not introduce compensation, increased staking yield, a token-price guarantee, or another mechanical payoff change.

## G. Outcome question

- [x] Machine — The canonical outcome question appears exactly once in every full-arm prompt.
- [x] Machine — Outcome wording is character-for-character identical across S, C0, T1, T2, and T3.
- [x] Machine — Every prompt presents the same ordered choices: 0%, 25%, 50%, 75%, or 100%.
- [x] Machine — Every prompt retains “right now”.
- [x] Human — Confirm that the question asks for the percentage for which unstaking would be initiated now, rather than a forecast of possible future behavior.
- [x] Human — Confirm that the five options are clear, mutually exclusive, and exhaustive for the intended response scale.

## H. JSON output requirement

- [x] Machine — The canonical JSON requirement appears exactly once in every full-arm prompt.
- [x] Machine — The JSON requirement is character-for-character identical across all five arms.
- [x] Machine — The required fields are `unstake_percentage` and `reason`.
- [x] Machine — The displayed schema uses an allowed example value and requests one concise reason sentence.
- [x] Human — Confirm that the requirement is understandable and does not add treatment-specific information.
- [x] Human — Confirm that the required output is consistent with the system prompt and the planned strict parser.

## I. File-level consistency

- [x] Machine — `P01_C0_rendered.txt` is character-for-character identical to `P01_all_arms/P01_C0.txt`.
- [x] Machine — All five full prompts follow the intended order: Persona → Common Shock → Condition → Outcome Question → Output Requirement.
- [x] Human — Read each full prompt from beginning to end and confirm that transitions are clear and no duplicated, truncated, or awkwardly joined passage is present.

## Researcher decision

Complete this section only after personally reviewing every unchecked item.

- [x] APPROVE — Phase 5 rendered prompts are approved for the next technical stage.
- [ ] DO NOT APPROVE — One or more issues require correction before proceeding.

Researcher name/initials: __CDY__________________  
Decision date: __2026.8.27__________________  
Notes or required corrections:

____No corrections required.________________________________________________________________

____________________________________________________________________
