# Phase 1–8 Handoff

## Current status

Phase 1–8 technical work has been completed through a corrected Tiny Technical Run. The corrected run passed the specified engineering checks. Smoke and Tiny Run data are technical artifacts only and must never enter Pilot or main-run treatment-effect analysis.

The experimental materials are **not formally frozen**. Formal freeze occurs only after the later robustness-material preparation, preregistered checks, Endpoint Pilot, researcher Pilot decision, complete prompt manifest, and Git freeze tag.

## Environment

- Python: 3.11.7
- OpenAI Python package: 2.38.0
- pytest: 7.4.0
- Corrected Tiny Run requested model: `gpt-4o-mini`
- Corrected Tiny Run returned model version: `gpt-4o-mini-2024-07-18`
- Temperature: `0`

Install the recorded dependencies with:

```powershell
python -m pip install -r requirements.txt
```

The runner requires `OPENAI_API_KEY` and `OPENAI_MODEL` in the process environment. Never commit, print, or share a real API key.

## Protocol name

- Final experimental name: `Kelmoryn Protocol`
- Decision record: `00_protocol/protocol_name_decision.md`
- The assembler reads the final name from that decision record and substitutes `[ProtocolName]` at assembly time.
- Formal source materials under `01_prompts/` retain the declared placeholder and must not be manually rewritten for rendering.

## Protected experimental materials

Everything under `01_prompts/` is formal experimental material. Code may read these files and perform only declared substitutions and fixed-order assembly. It must not summarize, improve, silently repair, or embed prompt content in Python.

At the current stage these materials are protected working materials, not frozen materials. No `prompt_manifest_v1.0.json` or formal freeze tag has yet been created.

## Phase 5 validation

- Corrected rendered artifacts are stored under `validation/`.
- `validation/P01_plus_common_shock.txt` contains P01 followed by the canonical common shock only.
- P01 × all five arms are stored under `validation/P01_all_arms/`.
- Corrected rendered artifacts use `Kelmoryn Protocol` and contain no unresolved protocol or persona placeholders.
- Machine and researcher checks are recorded in `validation/phase5_manual_review_checklist.md`.
- The researcher approved the Phase 5 rendered prompts, with no corrections required.
- The validation suite passed after the assembler correction: 16 tests passed.

Run the local validation suite with:

```powershell
python -B -m pytest -p no:cacheprovider 02_code/tests
```

## Tiny Run history

### Historical pre-fix run — retain, do not reuse

- Run ID: `tiny_20260822T130749Z_3ee55fdd`
- File: `03_raw_outputs/tiny_run/tiny_20260822T130749Z_3ee55fdd.jsonl`
- Cells: 12 unique cells; P01–P04 × S/C0/T3
- API/parse status: 12/12 API successes; 12/12 parsed; 0 recorded errors
- Known defect: all 12 assembled prompts retained the literal `[ProtocolName]` placeholder.
- Disposition: preserve unchanged as a historical pre-fix technical artifact; never use it as evidence that the corrected pipeline passed.

The JSONL does not store a separate top-level copy of the complete request prompt. The placeholder defect was established by deterministically reconstructing each prompt with the historical code path and matching all 12 reconstructed SHA-256 hashes to the stored `prompt_sha256` values.

### Corrected run — current Phase 8 technical run

- Run ID: `tiny_20260831T100803Z_85f19c73`
- File: `03_raw_outputs/tiny_run/tiny_20260831T100803Z_85f19c73.jsonl`
- Cells: 12 unique cells; P01–P04 × S/C0/T3
- Condition balance: S = 4, C0 = 4, T3 = 4
- API status: 12/12 successful
- Parse status: 12/12 successful
- Errors: 0
- `run_type`: `tiny_run` on all 12 records
- Requested model: `gpt-4o-mini`
- Returned model version: `gpt-4o-mini-2024-07-18`
- Temperature: `0`
- Required record fields: present on all 12 records
- Prompt verification: all 12 reconstructed prompts contain `Kelmoryn Protocol`, contain no unresolved placeholder, and match their stored `prompt_sha256` values.
- System verification: all 12 records use one system-prompt hash, and it matches the current canonical system prompt SHA-256: `8ca11289c6e751c39d52959bc926a488ecd800522048dd88595cd58c3b3e16d8`.

No error log was created because the corrected run recorded no API or parsing failure.

## Data isolation

- Smoke data: `03_raw_outputs/smoke/`
- Tiny technical data: `03_raw_outputs/tiny_run/`
- Both Tiny Run JSONL files must remain unchanged and separately identifiable by `run_id`.
- Neither smoke nor either Tiny Run may enter Endpoint Pilot or main-run analysis datasets.
- Historical smoke records do not contain a `run_type` field. Future analysis must exclude the entire `03_raw_outputs/smoke/` directory in addition to filtering records by `run_type`.
- The corrected Tiny Run verifies the technical pipeline only. Its outcome values and treatment differences must not be interpreted as research results.

## Historical smoke runner warning

`02_code/api_runner_smoke.py` and `02_code/test_persona_shock.py` contain a temporary embedded system instruction rather than loading the canonical system prompt. They are retained as historical smoke artifacts and must not be reused for Pilot or main runs.

The corrected Tiny Run runner, `02_code/run_tiny_run.py`, loads the canonical system prompt from `01_prompts/system/system_prompt_v1.0.txt`.

## Failure-handling discipline

For future parser or API failures:

1. Preserve the raw response or exception unchanged.
2. Record timestamp, run ID, persona ID, condition, model, run type, and error details.
3. Do not silently repair invalid model output.
4. Do not retry a completed model response merely to obtain valid JSON or a preferred decision.
5. Keep all technical, failed, smoke, Tiny Run, and Pilot attempts outside main-run datasets.

## Next step

Proceed to Gate B in `NEXT_STEPS_PROMPT_FLOW.md`: establish safe local Git and secret-protection foundations before creating the full 16-persona grid. This next step does not freeze the experimental materials.
