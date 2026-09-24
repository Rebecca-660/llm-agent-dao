import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "02_code"))

import run_main_run as main


HERE = Path(__file__).resolve().parent
MANIFEST_PATH = HERE / "main_requests.jsonl"
SUMMARY_PATH = HERE / "summary.json"
EVIDENCE_PATH = HERE / "validation_evidence.json"
REPORT_PATH = HERE / "validation_summary.md"
EXPECTED_CELLS = {
    f"P{number:02d}_{arm}"
    for number in range(1, 17)
    for arm in ("S", "C0", "T1", "T2", "T3")
}
PLACEHOLDER = re.compile(r"(?:\[[A-Za-z][A-Za-z0-9_]*\]|\{[A-Za-z][A-Za-z0-9_]*\})")


def load_jsonl(path):
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main_check():
    records = load_jsonl(MANIFEST_PATH)
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    expected_records = main.build_main_request_records()
    expected_by_cell = {record["cell_id"]: record for record in expected_records}
    actual_by_cell = {record["cell_id"]: record for record in records}
    cells = [record.get("cell_id") for record in records]
    counts = Counter(record.get("condition") for record in records)

    per_cell = []
    unexpected = []
    comparison_fields = (
        "persona_id", "condition", "run_type", "provider", "api_base_url",
        "model", "decoding_regime", "sampling_mode", "do_sample",
        "thinking_mode", "temperature", "wording_version",
        "persona_template_version", "persona_template_path",
        "output_requirement_version", "output_requirement_path",
        "answer_order", "independent_context", "previous_response_id",
        "system_prompt", "prompt", "system_prompt_sha256", "prompt_sha256",
        "request_sha256", "source_sha256", "freeze_record_sha256",
        "verified_frozen_sha256",
    )
    for cell in sorted(EXPECTED_CELLS):
        actual = actual_by_cell.get(cell)
        expected = expected_by_cell.get(cell)
        if actual is None or expected is None:
            issue = {"cell_id": cell, "pass": False, "issue": "missing actual or expected cell"}
            per_cell.append(issue)
            unexpected.append(issue)
            continue
        mismatches = [field for field in comparison_fields if actual.get(field) != expected.get(field)]
        recomputed_prompt_hash = main.shared.sha256_text(actual["prompt"])
        recomputed_system_hash = main.shared.sha256_text(actual["system_prompt"])
        placeholder_matches = sorted(set(PLACEHOLDER.findall(actual["prompt"] + actual["system_prompt"])))
        passed = (
            not mismatches
            and recomputed_prompt_hash == actual["prompt_sha256"]
            and recomputed_system_hash == actual["system_prompt_sha256"]
            and not placeholder_matches
        )
        item = {
            "cell_id": cell,
            "pass": passed,
            "field_mismatches_against_fresh_frozen_build": mismatches,
            "prompt_sha256_recomputed_match": recomputed_prompt_hash == actual["prompt_sha256"],
            "system_prompt_sha256_recomputed_match": recomputed_system_hash == actual["system_prompt_sha256"],
            "unresolved_placeholders": placeholder_matches,
            "prompt_sha256": actual["prompt_sha256"],
            "system_prompt_sha256": actual["system_prompt_sha256"],
            "request_sha256": actual["request_sha256"],
            "source_sha256": actual["source_sha256"],
        }
        per_cell.append(item)
        if not passed:
            unexpected.append(item)

    frozen_hashes = main.verify_frozen_hashes()
    record_config_ok = all(
        record.get("run_type") == "main"
        and record.get("provider") == "zhipu"
        and record.get("model") == "glm-4.7"
        and record.get("decoding_regime") == "stochastic_low_v1.2"
        and record.get("do_sample") is True
        and record.get("temperature") == 0.2
        and record.get("thinking_mode") == "disabled"
        and record.get("persona_template_version") == "v1.1"
        and record.get("output_requirement_version") == "v1.1"
        and record.get("answer_order") == "canonical_ascending"
        and record.get("independent_context") is True
        and record.get("previous_response_id") is None
        for record in records
    )
    matrix_ok = (
        len(records) == 80
        and len(actual_by_cell) == 80
        and set(actual_by_cell) == EXPECTED_CELLS
        and counts == Counter({arm: 16 for arm in main.CONDITIONS})
    )
    output_boundary_ok = (
        main.RAW_OUTPUT_DIRECTORY == ROOT / "03_raw_outputs/main"
        and main.LOG_OUTPUT_DIRECTORY == ROOT / "08_logs/main"
        and main.RUN_TYPE == "main"
        and main.create_execution_run_id().startswith("main_")
    )
    summary_ok = (
        summary.get("api_calls_made") == 0
        and summary.get("record_count") == 80
        and summary.get("unique_cell_count") == 80
        and summary.get("condition_counts") == {arm: 16 for arm in main.CONDITIONS}
        and summary.get("run_type") == "main"
        and summary.get("run_mode") == "dry_run"
    )
    overall = matrix_ok and record_config_ok and output_boundary_ok and summary_ok and not unexpected
    evidence = {
        "result": "PASS" if overall else "FAIL",
        "api_calls_made": 0,
        "manifest": MANIFEST_PATH.relative_to(ROOT).as_posix(),
        "freeze_record": main.FREEZE_PATH.relative_to(ROOT).as_posix(),
        "freeze_record_sha256": main.shared.sha256_file(main.FREEZE_PATH),
        "verified_frozen_sha256": frozen_hashes,
        "matrix": {
            "record_count": len(records),
            "unique_cell_count": len(actual_by_cell),
            "condition_counts": dict(counts),
            "missing_cells": sorted(EXPECTED_CELLS - set(actual_by_cell)),
            "unexpected_cells": sorted(set(actual_by_cell) - EXPECTED_CELLS),
            "pass": matrix_ok,
        },
        "configuration": {
            "provider": "zhipu", "model": "glm-4.7",
            "decoding_regime": "stochastic_low_v1.2",
            "do_sample": True, "temperature": 0.2,
            "thinking_mode": "disabled",
            "persona_template_version": "v1.1",
            "output_requirement_version": "v1.1",
            "answer_order": "canonical_ascending",
            "independent_context": True,
            "all_records_match": record_config_ok,
        },
        "hash_and_content": {
            "all_cells_match_fresh_frozen_build": not unexpected,
            "unexpected_differences": unexpected,
            "unresolved_placeholder_cell_count": sum(bool(item.get("unresolved_placeholders")) for item in per_cell),
        },
        "output_boundary": {
            "raw_output_directory": main.RAW_OUTPUT_DIRECTORY.relative_to(ROOT).as_posix(),
            "attempt_log_directory": main.LOG_OUTPUT_DIRECTORY.relative_to(ROOT).as_posix(),
            "exclusive_creation_mode": "Path.open('x')",
            "main_run_id_prefix": "main_",
            "pass": output_boundary_ok,
        },
        "summary_consistency_pass": summary_ok,
        "per_cell": per_cell,
    }
    EVIDENCE_PATH.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = [
        "# Main Run v1.2 dry-run validation summary", "",
        f"**Overall result: {evidence['result']}**", "",
        "- API calls made: 0",
        f"- Records / unique cells: {len(records)} / {len(actual_by_cell)}",
        f"- Counts by arm: S={counts['S']}, C0={counts['C0']}, T1={counts['T1']}, T2={counts['T2']}, T3={counts['T3']}",
        f"- Matrix completeness: {'PASS' if matrix_ok else 'FAIL'}",
        f"- Frozen configuration on all records: {'PASS' if record_config_ok else 'FAIL'}",
        f"- Fresh frozen-build prompt/system/request/source hash comparison: {'PASS' if not unexpected else 'FAIL'}",
        f"- Unresolved placeholder cells: {evidence['hash_and_content']['unresolved_placeholder_cell_count']}",
        f"- Main-only output paths and exclusive creation boundary: {'PASS' if output_boundary_ok else 'FAIL'}",
        f"- Dry-run summary consistency: {'PASS' if summary_ok else 'FAIL'}", "",
        "The manifest is suitable for the later read-only preflight only if the overall result is PASS. This dry-run does not authorize or perform real API calls.",
    ]
    REPORT_PATH.write_text("\n".join(report) + "\n", encoding="utf-8")
    if not overall:
        raise SystemExit("FAIL: main dry-run contains an unexpected difference")


if __name__ == "__main__":
    main_check()
