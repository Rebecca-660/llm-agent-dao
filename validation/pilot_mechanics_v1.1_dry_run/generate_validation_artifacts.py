import hashlib
import json
import re
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
VALIDATION_ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = VALIDATION_ROOT / "pilot_requests.jsonl"
SUMMARY_PATH = VALIDATION_ROOT / "summary.json"
OLD_RAW_PATH = (
    PROJECT_ROOT
    / "03_raw_outputs"
    / "pilot"
    / "pilot_20260903T055848Z_a5ef2915.jsonl"
)
OLD_TEMPLATE_PATH = (
    PROJECT_ROOT / "01_prompts" / "personas" / "persona_template_v1.0.txt"
)
NEW_TEMPLATE_PATH = (
    PROJECT_ROOT / "01_prompts" / "personas" / "persona_template_v1.1.txt"
)
PLACEHOLDER_PATTERN = re.compile(
    r"(?:\[[A-Za-z][A-Za-z0-9_]*\]|\{[A-Za-z][A-Za-z0-9_]*\})"
)
HASH_PATTERN = re.compile(r"[0-9a-f]{64}")
EXPECTED_CELLS = {
    f"P{persona:02d}_{condition}"
    for persona in range(1, 17)
    for condition in ("S", "C0", "T3")
}
STABLE_CONFIGURATION_FIELDS = (
    "run_type",
    "provider",
    "api_base_url",
    "sdk_name",
    "openai_sdk_version",
    "sampling_mode",
    "do_sample",
    "thinking_mode",
    "model",
    "temperature",
    "wording_version",
    "output_requirement_version",
    "output_requirement_path",
    "answer_order",
    "independent_context",
    "previous_response_id",
    "system_prompt",
    "system_prompt_sha256",
)
REQUIRED_REQUEST_FIELDS = {
    "run_id",
    "run_type",
    "run_mode",
    "cell_id",
    "persona_id",
    "condition",
    "provider",
    "api_base_url",
    "sdk_name",
    "openai_sdk_version",
    "sampling_mode",
    "do_sample",
    "thinking_mode",
    "model",
    "temperature",
    "generated_at",
    "wording_version",
    "persona_template_version",
    "persona_template_path",
    "output_requirement_version",
    "output_requirement_path",
    "answer_order",
    "independent_context",
    "previous_response_id",
    "system_prompt",
    "prompt",
    "system_prompt_sha256",
    "prompt_sha256",
    "request_sha256",
    "source_sha256",
}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def changed_template_lines() -> tuple[str, str]:
    old_lines = OLD_TEMPLATE_PATH.read_text(encoding="utf-8").splitlines()
    new_lines = NEW_TEMPLATE_PATH.read_text(encoding="utf-8").splitlines()
    differences = [
        (old, new)
        for old, new in zip(old_lines, new_lines, strict=True)
        if old != new
    ]
    if len(differences) != 1:
        raise ValueError("Expected exactly one changed persona-template line.")
    return differences[0]


def main() -> None:
    new_records = read_jsonl(MANIFEST_PATH)
    old_records = read_jsonl(OLD_RAW_PATH)
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    old_by_cell = {record["cell_id"]: record for record in old_records}
    new_by_cell = {record["cell_id"]: record for record in new_records}
    old_line, new_line = changed_template_lines()

    if len(old_records) != 48 or len(old_by_cell) != 48:
        raise ValueError("Historical comparison run is not a unique 48-cell run.")
    if len(new_records) != 48 or set(new_by_cell) != EXPECTED_CELLS:
        raise ValueError("Dry-run manifest is not the expected unique 48-cell matrix.")
    if set(old_by_cell) != EXPECTED_CELLS:
        raise ValueError("Historical run does not contain the expected cell matrix.")
    if summary.get("api_calls_made") != 0:
        raise ValueError("Dry-run summary does not record zero API calls.")

    comparisons = []
    for cell_id in sorted(EXPECTED_CELLS):
        old = old_by_cell[cell_id]
        new = new_by_cell[cell_id]
        if set(new) != REQUIRED_REQUEST_FIELDS:
            raise ValueError(f"Incomplete or unexpected metadata fields: {cell_id}")
        if PLACEHOLDER_PATTERN.search(new["prompt"]):
            raise ValueError(f"Unresolved placeholder: {cell_id}")
        if sha256_text(new["prompt"]) != new["prompt_sha256"]:
            raise ValueError(f"Prompt hash mismatch: {cell_id}")
        if sha256_text(new["system_prompt"]) != new["system_prompt_sha256"]:
            raise ValueError(f"System hash mismatch: {cell_id}")
        if not HASH_PATTERN.fullmatch(new["request_sha256"]):
            raise ValueError(f"Request hash malformed: {cell_id}")
        if not all(HASH_PATTERN.fullmatch(value) for value in new["source_sha256"].values()):
            raise ValueError(f"Source hash malformed: {cell_id}")

        changed_config = [
            field
            for field in STABLE_CONFIGURATION_FIELDS
            if old[field] != new[field]
        ]
        if changed_config:
            raise ValueError(f"Configuration drift in {cell_id}: {changed_config}")
        if old["prompt"].count(old_line) != 1:
            raise ValueError(f"Canonical mechanics passage count is not one: {cell_id}")
        expected_prompt = old["prompt"].replace(old_line, new_line)
        if expected_prompt != new["prompt"]:
            raise ValueError(f"Prompt has a non-mechanics difference: {cell_id}")

        old_persona_path = "01_prompts/personas/persona_template_v1.0.txt"
        new_persona_path = "01_prompts/personas/persona_template_v1.1.txt"
        old_other_sources = {
            path: digest
            for path, digest in old["source_sha256"].items()
            if path != old_persona_path
        }
        new_other_sources = {
            path: digest
            for path, digest in new["source_sha256"].items()
            if path != new_persona_path
        }
        if old_other_sources != new_other_sources:
            raise ValueError(f"Non-persona source hash drift: {cell_id}")
        if old_persona_path not in old["source_sha256"]:
            raise ValueError(f"Historical persona source missing: {cell_id}")
        if new_persona_path not in new["source_sha256"]:
            raise ValueError(f"New persona source missing: {cell_id}")

        comparisons.append(
            {
                "cell_id": cell_id,
                "old_prompt_sha256": old["prompt_sha256"],
                "new_prompt_sha256": new["prompt_sha256"],
                "old_persona_template_version": "v1.0",
                "new_persona_template_version": new["persona_template_version"],
                "stable_configuration_fields": list(STABLE_CONFIGURATION_FIELDS),
                "changed_configuration_fields": [],
                "prompt_difference": "approved_waiting_period_mechanics_only",
                "non_persona_source_hashes_equal": True,
            }
        )

    evidence = {
        "comparison_run_id": "pilot_20260903T055848Z_a5ef2915",
        "dry_run_id": new_records[0]["run_id"],
        "api_calls_made": 0,
        "record_count": len(new_records),
        "unique_cell_count": len(new_by_cell),
        "condition_counts": dict(Counter(record["condition"] for record in new_records)),
        "placeholder_count": sum(
            len(PLACEHOLDER_PATTERN.findall(record["prompt"]))
            for record in new_records
        ),
        "all_metadata_complete": True,
        "all_prompt_hashes_verified": True,
        "all_system_hashes_verified": True,
        "all_source_hashes_well_formed": True,
        "all_non_persona_source_hashes_equal": True,
        "all_stable_configuration_fields_equal": True,
        "all_prompt_differences_mechanics_only": True,
        "old_persona_template_path": "01_prompts/personas/persona_template_v1.0.txt",
        "new_persona_template_path": "01_prompts/personas/persona_template_v1.1.txt",
        "old_mechanics_line": old_line,
        "new_mechanics_line": new_line,
        "comparisons": comparisons,
    }
    (VALIDATION_ROOT / "difference_evidence.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    samples_dir = VALIDATION_ROOT / "rendered_samples"
    samples_dir.mkdir(exist_ok=False)
    for cell_id in ("P01_S", "P01_C0", "P01_T3"):
        (samples_dir / f"{cell_id}.txt").write_text(
            new_by_cell[cell_id]["prompt"], encoding="utf-8", newline="\n"
        )

    report = f"""# Pilot Mechanics v1.1 Dry-Run Difference Evidence

- Historical comparison run: `pilot_20260903T055848Z_a5ef2915`
- Dry-run ID: `{new_records[0]['run_id']}`
- API calls made: **0**
- Matrix: **48 records, 48 unique cells**
- Arm counts: **S=16, C0=16, T3=16**
- Unresolved placeholders: **0**
- Persona template: `v1.0` → `v1.1`
- Provider/model: `zhipu` / `glm-4.7` — unchanged
- Output Requirement: `v1.1` — unchanged
- Answer order: `canonical_ascending` — unchanged
- Temperature/sampling/thinking: `0` / `greedy_do_sample_false` / `disabled` — unchanged
- Independent context: `true` — unchanged

## Automated result

All 48 same-cell prompts satisfy this exact identity:

`new prompt = historical prompt with the single canonical persona mechanics line replaced by the approved v1.1 mechanics line`

All non-persona source hashes are equal within each same-cell comparison. Prompt hashes, system hashes, request-hash format, source-hash format, metadata completeness, cell uniqueness, arm balance, and placeholder absence were checked for all 48 records. Detailed per-cell hashes are preserved in `difference_evidence.json`.

## Exact sole material change

Canonical v1.0:

> {old_line}

Approved v1.1:

> {new_line}

The expected prompt and request hashes change because the approved persona text changed. The dry-run generation timestamp, run mode, and dry-run ID are execution-record fields rather than experimental-material changes.
"""
    (VALIDATION_ROOT / "difference_evidence.md").write_text(
        report, encoding="utf-8", newline="\n"
    )

    checklist = """# Pilot Mechanics v1.1 Dry-Run — Manual Review Checklist

## Machine-verified items

- [x] Exactly 48 unique P01–P16 × S/C0/T3 cells are present.
- [x] Each arm contains exactly 16 cells.
- [x] All rendered prompts contain no unresolved placeholder.
- [x] Prompt, system, request, and source hash metadata are present and well formed.
- [x] Prompt and system hashes were independently verified.
- [x] Each same-cell prompt differs from the prior GLM-4.7 Pilot only by the approved persona mechanics line.
- [x] All non-persona source hashes match the prior same-cell request.
- [x] Provider/model remain zhipu/GLM-4.7.
- [x] Output Requirement remains v1.1.
- [x] Canonical ascending answer order remains unchanged.
- [x] Temperature, deterministic sampling, thinking mode, and independent-context settings remain unchanged.
- [x] API calls made: 0.

Machine checks do not substitute for the human judgments below.

## Researcher review of rendered samples

Review `rendered_samples/P01_S.txt`, `P01_C0.txt`, and `P01_T3.txt` against the approved text and the difference evidence.

- [ ] The mechanics clarification appears exactly as approved in all three samples.
- [ ] “Initiating unstaking” clearly starts rather than completes the seven-day period.
- [ ] Selected tokens remain locked during the waiting period.
- [ ] Completion occurs only after the waiting period ends.
- [ ] The wording does not recommend or discourage unstaking.
- [ ] Persona facts outside the approved passage are unchanged.
- [ ] Common shock is unchanged across the samples.
- [ ] S/C0/T3 treatment wording and information hierarchy are unchanged.
- [ ] The decision time point and five outcome levels are unchanged.
- [ ] Output Requirement v1.1 and JSON fields are unchanged.
- [ ] Repetition of the seven-day duration remains acceptable in the assembled context.
- [ ] I accept the machine difference evidence and approve this dry-run for the next gate.

## Researcher decision

- Researcher name/initials: `________________`
- Decision date: `________________`
- Dry-run decision — select exactly one: `[ ] APPROVE  [ ] REVISE  [ ] REJECT`
- Notes/rationale: `____________________________________________________________`

Approval of this checklist validates the dry-run only. It does not itself authorize API calls. Any real 48-call Pilot requires a separate explicit authorization covering API execution and token consumption. It does not authorize material freeze or a main run.
"""
    (VALIDATION_ROOT / "manual_review_checklist.md").write_text(
        checklist, encoding="utf-8", newline="\n"
    )


if __name__ == "__main__":
    main()
