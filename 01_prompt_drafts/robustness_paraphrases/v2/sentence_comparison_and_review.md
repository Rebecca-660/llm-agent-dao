# Treatment Wording Version 2 — Sentence Comparison and Human Review

## Status and scope

These files are draft robustness materials only. They have not been approved as semantically equivalent and must not be used by an API runner or moved into `01_prompts/` until the researcher completes a sentence-level review.

The paraphrase changes treatment wording only. It does not change the Persona, common shock, system prompt, outcome question, JSON schema, or protocol-name placeholder.

## Structural checks

- [x] Draft S contains silence only.
- [x] Draft T1 contains the complete draft C0 followed by one reassurance increment.
- [x] Draft T2 contains the complete draft T1 followed by one corrective-plan increment.
- [x] Draft T3 contains the complete draft T2 followed by one already-executed and verifiable-action increment.
- [x] All arms preserve the decision time as several hours after the incident became public.
- [x] All response arms preserve the 24-hour update commitment.
- [x] T2 and T3 preserve the 48-hour post-mortem, seven-day DAO-review submission, and pre-reactivation independent audit.
- [x] T3 preserves prior execution, the team's own treasury allocation, restricted reserve use, and public on-chain verifiability.

These structural checks do not constitute human semantic-equivalence approval.

## S — Silence

| Canonical sentence | Draft v2 sentence | Intended invariant | Potential semantic-shift risk for human review |
|---|---|---|---|
| Several hours have passed since the incident became public. `[ProtocolName]` has not issued an official response. | Several hours have elapsed since the incident became public, and `[ProtocolName]` has issued no official response. | Same elapsed time; no official response. | “Elapsed” may sound slightly more formal than “passed”; confirm that joining the two sentences does not alter emphasis. |

Human review:

- [x] Equivalent in facts and timing.
- [x] Equivalent in tone and emphasis.
- [x] Still represents organizational silence rather than delayed acknowledgment.

## C0 — Minimal acknowledgment

| Canonical sentence | Draft v2 sentence | Intended invariant | Potential semantic-shift risk for human review |
|---|---|---|---|
| Several hours after the incident became public, `[ProtocolName]` issued the following statement: | Several hours after the incident was made public, `[ProtocolName]` released the following statement: | Same decision time and existence of an official statement. | “Was made public” is passive; confirm it does not imply who disclosed the incident. “Released” should be equivalent to “issued.” |
| We are aware of today's incident and are actively investigating what happened. | We are aware of the incident that occurred today and are actively investigating the circumstances. | Awareness, same-day incident, active investigation. | “Circumstances” could be read as slightly broader than “what happened”; confirm information content remains equivalent. |
| We will provide a further update within the next 24 hours. | We will provide another update within the next 24 hours. | Same future update and deadline. | “Another” may imply the current statement is the first update, as does “further”; confirm equivalence. |

Human review:

- [x] Equivalent in facts, timing, information amount, and tone.
- [x] Contains acknowledgment and investigation only, without reassurance or a corrective plan.

## T1 — Generic reassurance increment

Draft T1 includes the complete draft C0 above, plus:

| Canonical sentence | Draft v2 sentence | Intended invariant | Potential semantic-shift risk for human review |
|---|---|---|---|
| We remain confident in the protocol's long-term security, development, and ability to continue serving its users. | We continue to have confidence in the protocol's long-term security, future development, and capacity to keep serving its users. | Generic confidence in long-term security, development, and continued service. | “Future development” may sound slightly more forward-looking than “development”; “capacity” should not be read as a new operational fact. |

Human review:

- [x] Equivalent generic reassurance.
- [x] Does not add a specific action, deadline, guarantee, or new incident fact.

## T2 — Corrective-plan increment

Draft T2 includes the complete draft T1 above, plus:

| Canonical sentence | Draft v2 sentence | Intended invariant | Potential semantic-shift risk for human review |
|---|---|---|---|
| In addition, we have initiated an independent security review. | Additionally, we have begun an independent security review. | Independent security review has been initiated. | “Begun” and “initiated” should indicate the same implementation status; confirm neither sounds more complete. |
| A detailed post-mortem will be released within 48 hours. | We will publish a detailed post-mortem within 48 hours. | Same document, detail level, and deadline. | Active voice names the team as publisher; confirm this is already implicit in the canonical statement. |
| A proposed security upgrade will be submitted for DAO review within seven days, and the affected module will undergo an additional independent audit before it is reactivated. | Within seven days, we will submit a proposed security upgrade for DAO review, and the affected module will receive another independent audit before it is reactivated. | Same proposed upgrade, DAO review, deadline, additional audit, and sequencing before reactivation. | Active voice makes the team the submitter; “receive” may sound slightly less technical than “undergo.” Confirm no change in commitment strength. |

Human review:

- [x] Equivalent corrective actions, deadlines, sequencing, and commitment strength.
- [x] Remains a plan/review response and does not introduce T3's costly on-chain reserve action.

## T3 — Executed and verifiable-action increment

Draft T3 includes the complete draft T2 above, plus:

| Canonical sentence | Draft v2 sentence | Intended invariant | Potential semantic-shift risk for human review |
|---|---|---|---|
| In addition, the core team has already transferred a dedicated portion of its own treasury allocation into a publicly verifiable on-chain security reserve that can only be used for approved security audits and protocol remediation. | Additionally, the core team has already moved a designated portion of its own treasury allocation into a publicly verifiable on-chain security reserve. This reserve may be used only for approved security audits and protocol remediation. | Already executed transfer; dedicated portion; own treasury allocation; on-chain reserve; restricted approved uses. | “Moved” may sound less formal than “transferred”; “designated” must retain the meaning of “dedicated.” Splitting the use restriction into a second sentence may change emphasis or perceived length. |
| The transaction and reserve balance are publicly visible on-chain. | Both the transaction and the reserve balance are publicly visible on-chain. | Same two publicly observable objects and verification channel. | “Both” adds emphasis but no intended fact; confirm emphasis remains acceptable. |

Human review:

- [x] Equivalent executed status, material commitment, source of funds, use restriction, and verifiability.
- [x] Does not introduce holder compensation, yield changes, token-price protection, or a guarantee.
- [x] Does not sound more or less costly, credible, or forceful merely because of the paraphrase.

## Cross-arm human decision

- [x] C0–T3 remain strictly nested in information content as well as exact draft text.
- [x] Differences between adjacent arms remain limited to the intended increment.
- [x] The five drafts are acceptable candidates for formal wording version 2.

Researcher decision:

- [x] APPROVE AS SEMANTICALLY EQUIVALENT
- [ ] REVISE BEFORE APPROVAL

Researcher name/initials: __CDY__________________  
Decision date: __2026.8.30__________________  
Required revisions or notes:

____No corrections required.________________________________________________________________

____________________________________________________________________
