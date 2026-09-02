# Output Requirement v1.1 draft: canonical comparison and review

## Status and scope

- Status: **DRAFT — not approved for experimental use**
- Canonical source: `01_prompts/output_schema/json_schema_v1.0.txt`
- Candidate: `01_prompt_drafts/output_schema_v1.1/output_requirement_v1.1_draft.txt`
- Intended change: remove the concrete, valid example assignment `"unstake_percentage": 50` so that no allowed outcome is presented as a model answer.
- Out of scope: persona, common shock, treatments, outcome question, five outcome levels, answer order, system prompt, model, temperature, parser, and runner.

This draft must not be copied into `01_prompts/` or used for an API call until the researcher completes the manual review below.

## Text comparison

### Canonical v1.0

```text
{
  "unstake_percentage": 50,
  "reason": "One concise sentence explaining the main reason for the decision."
}

The value of "unstake_percentage" must be exactly one of: 0, 25, 50, 75, or 100.
The value of "reason" must be one concise sentence explaining the main reason for the decision.
```

### Candidate v1.1

```text
Return only one valid JSON object and no other text.

The JSON object must contain exactly these two fields:

- "unstake_percentage": choose exactly one integer from the allowed set 0, 25, 50, 75, or 100.
- "reason": provide one non-empty concise sentence explaining the main reason for the decision.

Do not include any additional fields, commentary, Markdown, or code fences.
```

## Constraint-by-constraint comparison

| Element | Canonical v1.0 | Candidate v1.1 | Outcome-construct effect |
|---|---|---|---|
| Response format | Shows a concrete JSON object, then states field rules | States the JSON-object rules without showing a completed object | Formatting expression changes; the measured unstaking decision does not change |
| Concrete outcome example | Assigns the valid value `50` to `unstake_percentage` | No allowed value is assigned to `unstake_percentage` as an answer | Removes the suspected measurement anchor; does not remove or add an outcome category |
| Output object count | Implied by the single displayed object | Explicitly requires one object | Formatting clarification only |
| Field set | Displays `unstake_percentage` and `reason` | Requires exactly the same two named fields | Same substantive fields; extra fields are now explicitly prohibited |
| `unstake_percentage` type | The displayed example is an integer; allowed values are enumerated | Explicitly requires an integer | Makes the existing parser expectation explicit; no outcome level changes |
| Allowed outcomes | `0, 25, 50, 75, 100` | `0, 25, 50, 75, 100` | Unchanged five-level outcome |
| Binary conversion | None | None | The outcome is not changed to Yes/No |
| `reason` | One concise sentence explaining the main reason | One non-empty concise sentence explaining the main reason | Same descriptive reason construct; non-empty requirement is made explicit |
| Additional prose/fences | Not stated in this component, although the system prompt asks for JSON only | Explicitly prohibited | Output-format clarification; no decision content changes |
| Persona/shock/treatment/outcome wording | Not contained in this component | Not contained in this component | Unchanged and outside this draft |

## Exact preservation claims

The candidate preserves all of the following:

1. The primary outcome remains the percentage of currently staked tokens for which the agent would initiate unstaking right now.
2. The response remains a five-level choice: `0`, `25`, `50`, `75`, or `100`.
3. The machine-readable field remains named `unstake_percentage`.
4. The explanatory field remains named `reason` and still requests one concise sentence stating the main reason.
5. The response remains strict JSON rather than free text or a Yes/No decision.
6. No fact, treatment content, decision time, persona attribute, or incident detail is added, removed, or reworded.

The only intended measurement change is that no valid outcome value is instantiated inside a completed answer example.

## Risks requiring researcher judgment

The researcher must judge each item rather than treating this comparison as automatic approval:

1. **Removal of visual JSON example.** Although the required object and fields are stated explicitly, removing a completed example could change format-compliance rates. This is intentional only to eliminate the suspected answer anchor.
2. **Exactly two fields.** Canonical v1.0 displayed two fields but did not literally say “exactly.” Candidate v1.1 makes that boundary explicit. Confirm that this is a formatting clarification rather than an unwanted tightening.
3. **Explicit integer type.** Canonical v1.0 demonstrated an integer and enumerated integer values; candidate v1.1 states the type directly. Confirm equivalence with the intended parser contract.
4. **Explicit non-empty reason.** Canonical v1.0 requested one concise explanatory sentence; candidate v1.1 additionally states “non-empty.” Confirm that this only makes the intended validity requirement explicit.
5. **No Markdown or code fences.** The existing parser can accept fenced JSON, but the candidate tells the model not to produce fences. Confirm that stricter presentation does not alter the behavioral construct.
6. **Allowed-value ordering.** The values remain written in canonical ascending order. This preserves the current canonical specification but could still carry order or midpoint salience; this draft does not attempt to solve or test answer-order effects.
7. **Causal uncertainty.** The first Pilot establishes that all requests contained the example value and all responses selected it, but it does not prove that the example caused the concentration. A complete new Pilot with all other materials held fixed is required to test the repair.
8. **No guarantee of category diversity.** Removing the example may or may not produce three categories. The original preregistered thresholds must not be relaxed after seeing the rerun.

## Researcher manual review

- [x] The five outcome levels are unchanged.
- [x] No allowed outcome value is presented as a completed or recommended answer.
- [x] The fields remain exactly `unstake_percentage` and `reason`.
- [x] The reason requirement remains substantively equivalent.
- [x] The JSON-only requirement is acceptable.
- [x] The “exactly two fields,” integer, non-empty, and no-fence clarifications are acceptable.
- [x] No persona, shock, treatment, outcome-question, or decision-time content has changed.
- [x] I understand that this draft does not prove that anchoring caused the first Pilot result.
- [x] I approve this exact candidate for the next versioning step.

Researcher name/initials: CDY
Review date: 2026.9.1 
Decision (`APPROVE`, `REVISE`, or `REJECT`): APPROVE
Notes: V1.1 完美达成了预设目标：移除了具体的数值示例，消除了输出格式中的隐式锚点。同时，新增的“纯 JSON”和“禁止代码块”要求强化了格式约束，有利于工程解析。所有五个核心决策等级及变量字段均未受任何影响。可以直接推进至下一轮 Pilot。


