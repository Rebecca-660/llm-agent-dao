# Treatment Wording Version 3 — Sentence Comparison and Human Review

## Status and scope

These files are draft robustness materials only. They have not been approved as semantically equivalent and must not be moved into `01_prompts/` or used by an API runner until sentence-level human review is complete.

Version 3 paraphrases treatment wording only. Persona, common shock, system prompt, outcome question, JSON schema, and the `[ProtocolName]` placeholder remain outside the paraphrase operation.

## Machine-checked structure

- [x] S contains silence only.
- [x] T1 contains the complete v3 C0 plus one reassurance increment.
- [x] T2 contains the complete v3 T1 plus one corrective-plan increment.
- [x] T3 contains the complete v3 T2 plus one executed/verifiable-action increment.
- [x] All arms retain a decision time several hours after the incident became public.
- [x] The 24-hour, 48-hour, and seven-day commitments remain in their intended arms.
- [x] T3 retains already-executed status, the core team's own treasury allocation, restricted uses, and public on-chain visibility.

Machine checks do not establish human semantic equivalence.

## S — Silence

| Canonical sentence | Draft v3 sentence | Intended invariant | Potential semantic-shift risk |
|---|---|---|---|
| Several hours have passed since the incident became public. | Several hours have gone by since the incident became public. | Same elapsed time. | “Gone by” is slightly less formal; confirm it does not make the delay feel longer or more conversational. |
| `[ProtocolName]` has not issued an official response. | `[ProtocolName]` has provided no official response. | No official response exists. | “Provided” versus “issued” may differ slightly in formality; confirm silence strength is unchanged. |

Human review:

- [x] Equivalent facts, timing, tone, and emphasis.
- [x] Still represents silence, not an acknowledgment or delayed-response promise.

## C0 — Minimal acknowledgment

| Canonical sentence | Draft v3 sentence | Intended invariant | Potential semantic-shift risk |
|---|---|---|---|
| Several hours after the incident became public, `[ProtocolName]` issued the following statement: | Several hours after the incident became public, `[ProtocolName]` provided this statement: | Same decision time and existence of a statement. | “Provided this statement” may sound less formal than “issued the following statement.” |
| We are aware of today's incident and are actively investigating what happened. | We are aware of the incident today and are actively examining what occurred. | Awareness, same-day incident, and active fact-finding. | “Examining” might sound less formal or intensive than “investigating”; confirm commitment strength is unchanged. |
| We will provide a further update within the next 24 hours. | We will share an additional update within 24 hours. | Same promised update and deadline. | “Share” may sound less formal than “provide”; omitting “next” must not change the 24-hour deadline. |

Human review:

- [x] Equivalent facts, timing, information amount, tone, and investigation strength.
- [x] Contains no reassurance, corrective plan, or new incident fact.

## T1 — Generic reassurance increment

Draft T1 contains the complete draft C0 above, plus:

| Canonical sentence | Draft v3 sentence | Intended invariant | Potential semantic-shift risk |
|---|---|---|---|
| We remain confident in the protocol's long-term security, development, and ability to continue serving its users. | We continue to be confident in the protocol's long-term security, its development, and its capacity to continue serving users. | Same generic confidence in security, development, and continued service. | “Capacity” may sound more operational than “ability”; omission of “its” before users should not broaden the referenced user group. |

Human review:

- [x] Equivalent generic reassurance and confidence strength.
- [x] Adds no action, deadline, guarantee, or incident fact.

## T2 — Corrective-plan increment

Draft T2 contains the complete draft T1 above, plus:

| Canonical sentence | Draft v3 sentence | Intended invariant | Potential semantic-shift risk |
|---|---|---|---|
| In addition, we have initiated an independent security review. | We have also started an independent security review. | Review has begun and is independent. | “Started” may sound less formal than “initiated”; confirm implementation status is identical. |
| A detailed post-mortem will be released within 48 hours. | We will make a detailed post-mortem public within 48 hours. | Same document, detail level, publication, and deadline. | Active voice names the team as responsible; “make public” may sound broader than “released.” |
| A proposed security upgrade will be submitted for DAO review within seven days, and the affected module will undergo an additional independent audit before it is reactivated. | Within seven days, a proposed security upgrade will be put forward for DAO review, and the affected module will be independently audited again before reactivation. | Same proposal, DAO review, deadline, additional independent audit, and pre-reactivation sequence. | “Put forward” may sound less procedurally binding than “submitted”; confirm commitment strength. “Before reactivation” omits the explicit pronoun but should retain the sequence. |

Human review:

- [x] Equivalent corrective actions, deadlines, sequencing, independence, and commitment strength.
- [x] Does not introduce an already-completed costly action or the T3 reserve.

## T3 — Executed and verifiable-action increment

Draft T3 contains the complete draft T2 above, plus:

| Canonical sentence | Draft v3 sentence | Intended invariant | Potential semantic-shift risk |
|---|---|---|---|
| In addition, the core team has already transferred a dedicated portion of its own treasury allocation into a publicly verifiable on-chain security reserve that can only be used for approved security audits and protocol remediation. | The core team has also already placed a dedicated portion of its own treasury allocation in a publicly verifiable on-chain security reserve. Funds in this reserve are restricted to approved security audits and protocol remediation. | Same actor, completed transfer, dedicated portion, own treasury source, on-chain reserve, and exclusive approved uses. | “Placed ... in” may sound less transaction-specific than “transferred ... into.” Splitting the restriction into a second sentence may change emphasis. Confirm “restricted to” is as exclusive as “can only be used for.” |
| The transaction and reserve balance are publicly visible on-chain. | The transaction and reserve balance can both be viewed publicly on-chain. | Same transaction and balance, public visibility, and on-chain verification. | “Can be viewed” may sound slightly less immediate than “are visible”; “both” adds emphasis. |

Human review:

- [x] Equivalent executed status, material cost, funding source, use restriction, and verifiability.
- [x] Does not add compensation, staking-yield changes, token-price protection, or a guarantee.
- [x] Does not become more or less credible, forceful, or reassuring because of the paraphrase.

## Cross-arm human decision

- [x] C0–T3 remain nested in both exact draft text and information content.
- [x] Each adjacent contrast contains only its intended increment.
- [x] Version 3 is meaningfully reworded without changing facts, timing, information amount, tone, or response strength.
- [x] The five drafts are acceptable candidates for formal wording version 3.

Researcher decision:

- [x] APPROVE AS SEMANTICALLY EQUIVALENT
- [ ] REVISE BEFORE APPROVAL

Researcher name/initials: __CDY__________________  
Decision date: __2026.8.30__________________  
Required revisions or notes:

____No corrections required________________________________________________________________

____________________________________________________________________
