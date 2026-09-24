import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
RUN_ID = "main_20260904T160520Z_d93b455f"
RAW_PATH = ROOT / "03_raw_outputs/main/main_20260904T160520Z_d93b455f.jsonl"
LOG_PATH = ROOT / "08_logs/main/main_20260904T160520Z_d93b455f_attempts.jsonl"
FREEZE_PATH = ROOT / "00_protocol/formal_material_freeze_v1.2.md"
PLAN_PATH = ROOT / "00_protocol/main_run_plan_v1.2.md"
ARMS = ("S", "C0", "T1", "T2", "T3")
EXPECTED_CELLS = {
    f"P{persona:02d}_{arm}" for persona in range(1, 17) for arm in ARMS
}
ALLOWED_VALUES = {0, 25, 50, 75, 100}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_jsonl_with_lines(path: Path) -> list[tuple[int, dict, str]]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            rows.append((line_number, json.loads(line), line))
    return rows


def classify(record: dict) -> str:
    if record.get("status") == "api_error":
        return "api_error"
    raw = record.get("raw_response")
    if raw is None or not str(raw).strip():
        return "empty_response"
    api_choices = (record.get("raw_api_response") or {}).get("choices") or []
    explicit_refusal = any(
        ((choice.get("message") or {}).get("refusal") not in (None, ""))
        for choice in api_choices
    )
    if explicit_refusal:
        return "refusal"
    parsed = record.get("parse_result") or {}
    if not parsed.get("success"):
        error = str(parsed.get("error") or "")
        if '"unstake_percentage" must be exactly one of' in error:
            return "illegal_value"
        return "parse_failure"
    value = (parsed.get("data") or {}).get("unstake_percentage")
    if value not in ALLOWED_VALUES or isinstance(value, bool):
        return "illegal_value"
    return "valid"


def main() -> None:
    raw_rows = load_jsonl_with_lines(RAW_PATH)
    attempt_rows = load_jsonl_with_lines(LOG_PATH)
    records = [record for _, record, _ in raw_rows]
    attempts = [record for _, record, _ in attempt_rows]

    if any(record.get("run_id") != RUN_ID or record.get("run_type") != "main" for record in records):
        raise RuntimeError("Raw input contains a foreign run_id or run_type.")
    if any(record.get("run_id") != RUN_ID or record.get("run_type") != "main" for record in attempts):
        raise RuntimeError("Attempt log contains a foreign run_id or run_type.")

    cells = [record.get("cell_id") for record in records]
    cell_counts = Counter(cells)
    duplicates = sorted(cell for cell, count in cell_counts.items() if count > 1)
    missing = sorted(EXPECTED_CELLS - set(cells))
    unexpected = sorted(set(cells) - EXPECTED_CELLS)
    arm_counts = Counter(record.get("condition") for record in records)
    if (
        len(records) != 80
        or duplicates
        or missing
        or unexpected
        or arm_counts != Counter({arm: 16 for arm in ARMS})
    ):
        raise RuntimeError("The authorized main run does not contain the exact 80-cell matrix.")

    attempts_by_cell = Counter(record.get("cell_id") for record in attempts)
    retry_cells = sorted(cell for cell, count in attempts_by_cell.items() if count > 1)
    retry_scheduled_count = sum(bool(record.get("retry_scheduled")) for record in attempts)

    processed = []
    for line_number, record, raw_line in raw_rows:
        outcome_status = classify(record)
        parsed_data = (record.get("parse_result") or {}).get("data") or {}
        valid = outcome_status == "valid"
        value = parsed_data.get("unstake_percentage") if valid else None
        reason = parsed_data.get("reason") if valid else None
        processed.append({
            "run_id": RUN_ID,
            "run_type": "main",
            "cell_id": record["cell_id"],
            "persona_id": record["persona_id"],
            "condition": record["condition"],
            "raw_line_number": line_number,
            "raw_record_sha256": sha256_bytes(raw_line.encode("utf-8")),
            "request_sha256": record.get("request_sha256"),
            "prompt_sha256": record.get("prompt_sha256"),
            "system_prompt_sha256": record.get("system_prompt_sha256"),
            "response_id": record.get("response_id"),
            "api_status": record.get("status"),
            "attempt_count": record.get("attempt_count"),
            "outcome_status": outcome_status,
            "parse_success": bool((record.get("parse_result") or {}).get("success")),
            "parse_error": (record.get("parse_result") or {}).get("error"),
            "unstake_percentage": value,
            "any_unstake": (1 if value > 0 else 0) if valid else None,
            "reason": reason,
        })

    status_counts = Counter(row["outcome_status"] for row in processed)
    required_statuses = (
        "valid", "parse_failure", "illegal_value", "empty_response", "refusal", "api_error"
    )
    status_counts_complete = {status: status_counts.get(status, 0) for status in required_statuses}
    parse_failures = [row["cell_id"] for row in processed if row["outcome_status"] == "parse_failure"]
    if parse_failures != ["P11_S"]:
        raise RuntimeError(f"Expected only P11_S as parse failure; found {parse_failures!r}.")
    p11 = next(row for row in processed if row["cell_id"] == "P11_S")
    if any(p11[field] is not None for field in ("unstake_percentage", "any_unstake", "reason")):
        raise RuntimeError("P11_S must remain missing without repair or imputation.")

    fields = list(processed[0])
    with (OUT / "main_v1.2_processed.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(processed)
    with (OUT / "main_v1.2_processed.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
        for row in processed:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    report = {
        "result": "PASS",
        "run_id": RUN_ID,
        "run_type": "main",
        "source_files": {
            RAW_PATH.relative_to(ROOT).as_posix(): sha256_file(RAW_PATH),
            LOG_PATH.relative_to(ROOT).as_posix(): sha256_file(LOG_PATH),
            FREEZE_PATH.relative_to(ROOT).as_posix(): sha256_file(FREEZE_PATH),
            PLAN_PATH.relative_to(ROOT).as_posix(): sha256_file(PLAN_PATH),
        },
        "record_count": len(records),
        "unique_cell_count": len(set(cells)),
        "arm_counts": {arm: arm_counts[arm] for arm in ARMS},
        "missing_cells": missing,
        "unexpected_cells": unexpected,
        "duplicate_cells": duplicates,
        "attempt_record_count": len(attempts),
        "retry_scheduled_count": retry_scheduled_count,
        "cells_with_multiple_attempts": retry_cells,
        "api_success_count": sum(record.get("status") == "success" for record in records),
        "outcome_status_counts": status_counts_complete,
        "validity_rate": status_counts_complete["valid"] / 80,
        "parse_failure_cells": parse_failures,
        "missing_data_rule": "Invalid records remain missing; no re-ask, repair, rounding, coercion, inference, or imputation.",
        "excluded_data_classes": ["Pilot", "Tiny Run", "dry-run", "smoke", "connectivity-check"],
        "treatment_effect_analysis_performed": False,
    }
    (OUT / "integrity_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    report_lines = [
        "# Main v1.2 engineering acceptance report", "",
        "**Result: PASS**", "",
        f"- Authorized run: `{RUN_ID}` only",
        f"- Raw records / unique cells: {len(records)} / {len(set(cells))}",
        f"- Arm counts: " + ", ".join(f"{arm}={arm_counts[arm]}" for arm in ARMS),
        f"- Attempt records: {len(attempts)}; scheduled retries: {retry_scheduled_count}",
        f"- API successes: {report['api_success_count']}/80",
        f"- Valid parsed outcomes: {status_counts_complete['valid']}/80 ({report['validity_rate']:.2%})",
        f"- Parse failures: {status_counts_complete['parse_failure']} (`P11_S`)",
        f"- Illegal values: {status_counts_complete['illegal_value']}",
        f"- Empty responses: {status_counts_complete['empty_response']}",
        f"- Explicit refusals: {status_counts_complete['refusal']}",
        f"- API errors: {status_counts_complete['api_error']}",
        "- Missing, unexpected, or duplicate cells: 0 / 0 / 0", "",
        "`P11_S` remains missing for `unstake_percentage`, `any_unstake`, and `reason`. Its raw response and parser error remain accessible through the raw line locator and hashes; it was not repaired, re-asked, coerced, or imputed.", "",
        "Pilot, Tiny Run, dry-run, smoke, and connectivity-check records were not read into or included in this dataset. No treatment-effect comparison was computed.",
    ]
    (OUT / "integrity_report.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
