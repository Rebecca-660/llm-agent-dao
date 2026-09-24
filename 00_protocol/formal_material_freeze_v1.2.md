# Formal Material and Execution-Configuration Freeze v1.2

## Freeze status

- Freeze date: `2026-09-04`
- Researcher: `CDY`
- Status: **FROZEN FOR MINIMUM-SCOPE MAIN-RUN PREPARATION**
- Authorizing Pilot run ID: `pilot_20260904T150852Z_18e62216`
- Pilot decision: **PASS**
- Formal material freeze authorized: **YES**
- Main-run preparation authorized: **YES**
- Real main-run API calls authorized by this record: **NO**

Researcher `CDY` approved the third-round GLM-4.7 Endpoint Pilot and authorized formal material freeze and main-run preparation in `00_protocol/pilot_decision_execution_config_v1.2.md`. This record performs that material/configuration freeze. It permits implementation and zero-API validation of a separate main-run workflow, but it does not authorize real API calls, token expenditure, or creation of main-run raw output.

## Minimum-scope main-run design

The summer-project minimum scope is frozen as one canonical main experiment:

- 16 personas × 5 arms (`S`, `C0`, `T1`, `T2`, `T3`) = **80 unique cells**;
- exactly one request per cell in the minimum-scope run;
- one independent model context per cell;
- no previous-response chaining;
- canonical treatment wording only;
- canonical ascending answer order only;
- no robustness paraphrases;
- no reverse answer order;
- no additional temperatures or decoding regimes;
- no second model.

Any later robustness or extension study must have a separate plan, run identity, output files, and authorization. It is not part of this freeze.

## Frozen experimental materials

| Component | Frozen identity | Path | SHA-256 |
|---|---|---|---|
| Protocol name | `Kelmoryn Protocol` | `00_protocol/protocol_name_decision.md` | `54db1d54c481ae31478ea2243b165ff3acbc978a0d8c3e059b74587a0e083eea` |
| Persona grid | 16-persona Cartesian grid v1.0 | `01_prompts/personas/personas_v1.0.csv` | `4e1a87fd42ca8f1d038e64fb181d0b353b85940026405af35a35856218822c08` |
| Persona/mechanics template | v1.1, approved seven-day waiting-period clarification | `01_prompts/personas/persona_template_v1.1.txt` | `3a3ed734a4297e5ba4d99753f15e8b53753318d6e8c2403070f72b015060d7ae` |
| System prompt | v1.0 | `01_prompts/system/system_prompt_v1.0.txt` | `8ca11289c6e751c39d52959bc926a488ecd800522048dd88595cd58c3b3e16d8` |
| Common shock | v1.0 | `01_prompts/common_shock/common_shock_v1.0.txt` | `266cb9d1177668f3c30a442925204133ce20ba7401fbba04d6cf2afb1ee4c360` |
| S treatment | canonical v1.0 | `01_prompts/treatments/S_v1.0.txt` | `295aa52c277f90bdaee33759c4bc124b3c74df097fa53e3ff6eec62fa53a5f56` |
| C0 treatment | canonical v1.0 | `01_prompts/treatments/C0_v1.0.txt` | `e4e6cb2a7dc47d496ee329389fb3cabae5c2e001cea8b13801ac0f7701ba8669` |
| T1 treatment | canonical v1.0 | `01_prompts/treatments/T1_v1.0.txt` | `1b715d421b0f82f02b048277e6dba458f5c61c8d8c3f0532128846ec6ab4a382` |
| T2 treatment | canonical v1.0 | `01_prompts/treatments/T2_v1.0.txt` | `dd34ab4453a1d8dae8a69cbab682f787fe84e23a92d9920877e93ba17eb2440e` |
| T3 treatment | canonical v1.0 | `01_prompts/treatments/T3_v1.0.txt` | `b53b07c49c37b630cdcab82ebdb57d7794b07bc3b8452a25982f3b8a5a4bd860` |
| Outcome question | canonical v1.0 | `01_prompts/outcome/outcome_question_v1.0.txt` | `f5c2c352155aa4aadf9c08443fe81ffd19c1d503e19437b714c253fd22828fff` |
| Output Requirement | approved v1.1, exact two-field JSON | `01_prompts/output_schema/json_schema_v1.1.txt` | `7ca5b6896c2e115d99d7edc8314899d95669e0fb0e919c96472074840d509452` |

The outcome answer order is frozen as the canonical ascending order `0%, 25%, 50%, 75%, 100%`, embodied in the canonical outcome question above. `01_prompts/outcome/outcome_order_reverse_v1.0.txt` is explicitly excluded.

Only the treatment files under `01_prompts/treatments/` listed above are in scope. Wording v2/v3 robustness materials under `01_prompts/robustness_paraphrases/` are explicitly excluded.

## Frozen provider and execution configuration

| Field | Frozen value |
|---|---|
| Provider | `zhipu` |
| API request family | OpenAI-compatible chat completions at the existing Zhipu endpoint |
| Requested model | `glm-4.7` |
| Decoding regime | `stochastic_low_v1.2` |
| `do_sample` | `true` |
| `temperature` | `0.2` |
| Sampling-mode metadata | `stochastic_temperature_0.2` |
| Thinking | disabled (`thinking.type=disabled`) |
| Context | independent for every cell |
| Previous response ID | none |
| Maximum attempts | `3` |
| Retry delays | `1.0`, then `2.0` seconds |
| Retry boundary | transient network/rate-limit/server errors only |
| Invalid model content | retain and parse as observed; do not re-ask |
| Output behavior | append-only, new run ID, independent raw JSONL and attempt log |

No `top_p`, request seed, penalty, or other omitted provider parameter is added by this freeze. A main-run implementation must not tune configuration after inspecting responses.

## Frozen assembly, parsing, and execution-code identities

| Code artifact | Role | SHA-256 |
|---|---|---|
| `02_code/prompt_assembler.py` | assembles version-controlled persona, shock, treatment, outcome, output requirement, and final protocol name | `5192affbc4f7390d6921be59ecb21fd583187cb3c8fba6bf3dafb08ee6671324` |
| `02_code/parser.py` | strictly rejects missing or additional fields and validates the legal five-point integer value and non-empty reason | `2dca4a6e41f5b153d89473711ad970ae6007180c67e1040427ce64bb1bf6b6f9` |
| `02_code/run_endpoint_pilot.py` | validated provider, request hashing, independent-context, append-only, attempt, and retry reference implementation | `bfc97548438b0c6db51e407adb29db48d3a94d1358af970bb771b5850f8e9106` |
| `02_code/run_main_run.py` | frozen 80-cell main runner, including main-run identity, hash metadata, isolation, retry, and append-only behavior | `28c531ab73b659e38a298fb45aa3666d3924010c897f48d1d524f76492ea241e` |

The Endpoint Pilot runner currently defines only the three Pilot arms `S/C0/T3`; it is therefore a frozen reference implementation, not authorization to reuse a 48-cell Pilot as the main experiment. A separate main-run runner must explicitly enumerate all five frozen arms and all 80 unique cells. Its implementation must preserve the frozen assembly, parser, provider, decoding, error, retry, hashing, metadata, and append-only behavior, and must pass a separate zero-API dry-run before any real-call authorization.

## Authorization and evidence provenance

| Evidence artifact | SHA-256 |
|---|---|
| `00_protocol/pilot_decision_execution_config_v1.2.md` | `40777a2923fa97259210a79b6d5bf8fbfed3292e25d09d1aa78aa02dde914452` |
| `00_protocol/pilot_execution_config_plan_v1.2.md` | `ab5a411bc4893bf2c2b4f702384984ac779c9c8e1fa55279f26c4db50cf128e0` |
| `00_protocol/unstaking_mechanics_v1.1_change_record.md` | `0bce4bfa8856d04406aaf6aa7da554efdf4267ce943d8c1397c5555aa9889204` |
| `05_processed_data/pilot_execution_config_v1.2_diagnostics/machine_checks.json` | `1a681b992fe4ae535d02a3b741612c9274e9260a503592958784bb232f2e6c4c` |
| `05_processed_data/pilot_execution_config_v1.2_diagnostics/machine_checks.md` | `21f79f134d213afbe8205535fd577c1be02b0942419b6d14e0517ddf623b1d8e` |
| `05_processed_data/pilot_execution_config_v1.2_diagnostics/sample_manifest.json` | `bfbfd072f4d99914a97fc1ae5f5f8b2bd8fd2d9dc4470cc336e70ece8d161df0` |

The authorizing Pilot passed all five preregistered machine checks. Researcher `CDY` recorded 12/12 material-hallucination PASS judgments and 4/4 T3-comprehension PASS judgments, accepted the absence of per-record short rationales, and explicitly authorized freeze and main-run preparation. This freeze does not reinterpret Pilot responses or use treatment ordering, statistical significance, effect size, or preferred direction.

## Data isolation

All of the following remain calibration, validation, or engineering evidence and are permanently excluded from the main-run dataset:

- every Endpoint Pilot run, including `pilot_20260904T150852Z_18e62216`;
- all earlier OpenAI and GLM-4.7 Pilot runs;
- all Tiny Run and smoke outputs;
- every dry-run request manifest;
- connectivity checks;
- Pilot diagnostics and manual-review packets.

The main run must use a newly generated `run_id`, `run_type=main`, a new exclusive raw-output JSONL, and a new exclusive attempt log. It must not overwrite, append to, resume, repair, or selectively copy any earlier run.

## Post-freeze change control and next gate

After this record, any change to a frozen prompt, material version, model, provider, decoding regime, answer order, parser semantics, or main design requires a new versioned change record and appropriate revalidation. No such change is authorized here.

The next authorized work is limited to:

1. implementing the separate 80-cell main-run runner and tests; and
2. producing an independent zero-API dry-run manifest proving the complete 16 × 5 matrix, frozen hashes/configuration, independent contexts, metadata completeness, append-only destinations, and data isolation.

A later real main run requires a separate, explicit researcher authorization covering the exact call count and token cost. **No real API call is authorized by this freeze.**

## Pre-main remediation amendment — 2026-09-04

Before any main-run data were generated, the final zero-API preflight identified two auditability gaps. This amendment closes only those gaps:

1. The parser now enforces the already-approved Output Requirement v1.1 literally by rejecting any JSON object whose keys are not exactly `unstake_percentage` and `reason`. Its previous SHA-256 was `ce8e99c0d1248bed5e0237f8da046337147f827a0f1be9657ebb347d3dc2f7cb`; its frozen replacement SHA-256 is recorded in the code table above.
2. The completed main runner is now itself frozen in the code table above, and every generated request records both its path and SHA-256.

No prompt, outcome, answer order, persona, treatment, shock, provider, model, decoding configuration, retry rule, analysis rule, or experimental cell changed. No API call or main-run raw output was produced during this amendment. The earlier dry-run evidence remains preserved as historical pre-remediation evidence; a new independent dry run is required after this amendment.
