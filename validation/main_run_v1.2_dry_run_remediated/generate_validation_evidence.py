import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "02_code"))

import run_main_run as main
from parser import parse_response


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def run_checks() -> None:
    records = load_jsonl(HERE / "main_requests.jsonl")
    summary = json.loads((HERE / "summary.json").read_text(encoding="utf-8"))
    expected = main.build_main_request_records()
    expected_by_cell = {record["cell_id"]: record for record in expected}
    actual_by_cell = {record["cell_id"]: record for record in records}
    expected_cells = set(expected_by_cell)
    counts = Counter(record["condition"] for record in records)
    comparison_fields = (
        "run_type", "persona_id", "condition", "provider", "model",
        "decoding_regime", "do_sample", "temperature", "thinking_mode",
        "persona_template_version", "output_requirement_version", "answer_order",
        "independent_context", "previous_response_id", "system_prompt", "prompt",
        "system_prompt_sha256", "prompt_sha256", "request_sha256", "source_sha256",
        "freeze_record_sha256", "main_runner_path", "main_runner_sha256",
        "verified_frozen_sha256",
    )
    differences = {}
    placeholder = re.compile(r"(?:\[[A-Za-z][A-Za-z0-9_]*\]|\{[A-Za-z][A-Za-z0-9_]*\})")
    placeholder_cells = []
    for cell, actual in actual_by_cell.items():
        reference = expected_by_cell.get(cell, {})
        changed = [field for field in comparison_fields if actual.get(field) != reference.get(field)]
        if changed:
            differences[cell] = changed
        if placeholder.search(actual.get("prompt", "") + actual.get("system_prompt", "")):
            placeholder_cells.append(cell)

    frozen = main.verify_frozen_hashes()
    runner_hash = main.shared.sha256_file(main.MAIN_RUNNER_PATH)
    parser_extra_field_result = parse_response(
        '{"unstake_percentage":25,"reason":"test","extra":"must fail"}'
    )
    checks = {
        "api_calls_zero": summary.get("api_calls_made") == 0,
        "matrix_complete": (
            len(records) == 80
            and len(actual_by_cell) == 80
            and set(actual_by_cell) == expected_cells
            and counts == Counter({arm: 16 for arm in main.CONDITIONS})
        ),
        "fresh_frozen_build_identical": not differences,
        "no_unresolved_placeholders": not placeholder_cells,
        "strict_two_field_parser": parser_extra_field_result["success"] is False,
        "main_runner_hash_recorded": all(
            record.get("main_runner_path") == "02_code/run_main_run.py"
            and record.get("main_runner_sha256") == runner_hash
            and record.get("verified_frozen_sha256", {}).get("02_code/run_main_run.py") == runner_hash
            for record in records
        ),
        "main_output_isolated": (
            main.RAW_OUTPUT_DIRECTORY == ROOT / "03_raw_outputs" / "main"
            and main.LOG_OUTPUT_DIRECTORY == ROOT / "08_logs" / "main"
        ),
    }
    passed = all(checks.values())
    evidence = {
        "result": "PASS" if passed else "FAIL",
        "api_calls_made": 0,
        "checks": checks,
        "record_count": len(records),
        "unique_cell_count": len(actual_by_cell),
        "condition_counts": dict(counts),
        "freeze_record_sha256": main.shared.sha256_file(main.FREEZE_PATH),
        "main_runner_sha256": runner_hash,
        "parser_sha256": frozen["02_code/parser.py"],
        "verified_frozen_sha256": frozen,
        "unexpected_differences": differences,
        "placeholder_cells": placeholder_cells,
        "strict_parser_probe": parser_extra_field_result,
    }
    (HERE / "validation_evidence.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Remediated main-run v1.2 dry-run validation", "",
        f"**Overall result: {evidence['result']}**", "",
        "- API calls made: 0",
        f"- Records / unique cells: {len(records)} / {len(actual_by_cell)}",
        f"- Counts: {dict(counts)}",
        f"- Exact two-field parser enforcement: {'PASS' if checks['strict_two_field_parser'] else 'FAIL'}",
        f"- Main runner hash frozen and recorded per request: {'PASS' if checks['main_runner_hash_recorded'] else 'FAIL'}",
        f"- Fresh frozen build and all request/hash metadata: {'PASS' if checks['fresh_frozen_build_identical'] else 'FAIL'}",
        f"- No unresolved placeholders: {'PASS' if checks['no_unresolved_placeholders'] else 'FAIL'}",
        f"- Main-only output isolation: {'PASS' if checks['main_output_isolated'] else 'FAIL'}", "",
        "This evidence was generated without API calls and does not authorize a real main run.",
    ]
    (HERE / "validation_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if not passed:
        raise SystemExit("FAIL: remediated dry-run validation failed")


if __name__ == "__main__":
    run_checks()
