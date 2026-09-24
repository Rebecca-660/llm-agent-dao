import hashlib
import json
import platform
import random
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_ROOT = Path(__file__).resolve().parent
REVIEW_ROOT = PROJECT_ROOT / "validation" / "pilot_mechanics_v1.1_manual_review"
RUN_ID = "pilot_20260904T135552Z_be4faaf7"
SEED = 20260901
RAW_PATH = PROJECT_ROOT / "03_raw_outputs" / "pilot" / f"{RUN_ID}.jsonl"
LOG_PATH = PROJECT_ROOT / "08_logs" / "pilot" / f"{RUN_ID}_attempts.jsonl"
PREREG_PATH = PROJECT_ROOT / "00_protocol" / "preregistered_checks.md"
CHANGE_RECORD_PATH = (
    PROJECT_ROOT / "00_protocol" / "unstaking_mechanics_v1.1_change_record.md"
)
ARMS = ("S", "C0", "T3")
PERSONA_IDS = tuple(f"P{number:02d}" for number in range(1, 17))
ALLOWED_VALUES = (0, 25, 50, 75, 100)
EXPECTED_CELLS = {
    f"{persona_id}_{arm}" for persona_id in PERSONA_IDS for arm in ARMS
}
REFUSAL_PATTERN = re.compile(
    r"\b(?:i cannot|i can't|i am unable|i'm unable|i refuse|i decline|"
    r"cannot make|can't make|unable to make|as an ai)\b",
    re.IGNORECASE,
)


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def is_refusal(record: dict) -> bool:
    raw_response = record.get("raw_response") or ""
    return bool(REFUSAL_PATTERN.search(raw_response))


def valid_non_refusal(record: dict) -> bool:
    if record.get("status") != "success":
        return False
    parse_result = record.get("parse_result")
    if not parse_result or not parse_result.get("success"):
        return False
    data = parse_result.get("data") or {}
    if data.get("unstake_percentage") not in ALLOWED_VALUES:
        return False
    reason = data.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        return False
    return not is_refusal(record)


def pass_fail(value: bool) -> str:
    return "PASS" if value else "FAIL"


def main() -> None:
    if REVIEW_ROOT.exists():
        raise FileExistsError(REVIEW_ROOT)
    REVIEW_ROOT.mkdir(parents=True)

    rows = read_jsonl(RAW_PATH)
    attempts = read_jsonl(LOG_PATH)
    cells = [row.get("cell_id") for row in rows]
    run_ids = {row.get("run_id") for row in rows}
    run_types = {row.get("run_type") for row in rows}
    condition_counts = Counter(row.get("condition") for row in rows)
    missing_cells = sorted(EXPECTED_CELLS.difference(cells))
    unexpected_cells = sorted(set(cells).difference(EXPECTED_CELLS))
    duplicate_cells = sorted(
        cell for cell, count in Counter(cells).items() if count > 1
    )

    valid_rows = [row for row in rows if valid_non_refusal(row)]
    valid_c0 = [row for row in valid_rows if row["condition"] == "C0"]
    c0_values = [row["parse_result"]["data"]["unstake_percentage"] for row in valid_c0]
    pooled_values = [
        row["parse_result"]["data"]["unstake_percentage"] for row in valid_rows
    ]
    c0_mean = sum(c0_values) / len(c0_values) if c0_values else None
    c0_counts = Counter(c0_values)
    pooled_counts = Counter(pooled_values)
    maximum_category, maximum_count = (
        pooled_counts.most_common(1)[0] if pooled_counts else (None, 0)
    )
    maximum_share = maximum_count / len(valid_rows) if valid_rows else None

    parse_failures = [
        {
            "cell_id": row["cell_id"],
            "error": (row.get("parse_result") or {}).get("error"),
        }
        for row in rows
        if row.get("status") == "success"
        and not (row.get("parse_result") or {}).get("success")
    ]
    refusals = [row["cell_id"] for row in rows if is_refusal(row)]
    api_errors = [row["cell_id"] for row in rows if row.get("status") == "api_error"]
    empty_responses = [
        row["cell_id"]
        for row in rows
        if row.get("status") == "success" and not row.get("raw_response")
    ]

    checks = [
        {
            "criterion": 1,
            "name": "Cell completeness and isolation",
            "threshold": "Exactly 48 unique P01-P16 x S/C0/T3 cells from one run; run_type=pilot",
            "observed": {
                "records": len(rows),
                "unique_cells": len(set(cells)),
                "condition_counts": dict(condition_counts),
                "missing_cells": missing_cells,
                "duplicate_cells": duplicate_cells,
                "unexpected_cells": unexpected_cells,
                "run_ids": sorted(run_ids),
                "run_types": sorted(run_types),
            },
            "result": pass_fail(
                len(rows) == 48
                and set(cells) == EXPECTED_CELLS
                and not duplicate_cells
                and condition_counts == Counter({arm: 16 for arm in ARMS})
                and run_ids == {RUN_ID}
                and run_types == {"pilot"}
            ),
        },
        {
            "criterion": 2,
            "name": "C0 mean dynamic range",
            "threshold": "15 <= mean <= 75 among valid non-refusal C0 responses",
            "observed": {"valid_n": len(valid_c0), "mean": c0_mean},
            "result": pass_fail(c0_mean is not None and 15 <= c0_mean <= 75),
        },
        {
            "criterion": 3,
            "name": "C0 response-category diversity",
            "threshold": "At least 3 distinct categories among valid non-refusal C0 responses",
            "observed": {
                "valid_n": len(valid_c0),
                "distinct_categories": len(c0_counts),
                "category_counts": dict(sorted(c0_counts.items())),
            },
            "result": pass_fail(len(c0_counts) >= 3),
        },
        {
            "criterion": 4,
            "name": "Combined category concentration",
            "threshold": "Maximum single-category share <= 0.85 among pooled valid non-refusal responses",
            "observed": {
                "valid_n": len(valid_rows),
                "category_counts": dict(sorted(pooled_counts.items())),
                "maximum_category": maximum_category,
                "maximum_count": maximum_count,
                "maximum_share": maximum_share,
            },
            "result": pass_fail(maximum_share is not None and maximum_share <= 0.85),
        },
        {
            "criterion": 5,
            "name": "Structured-output validity",
            "threshold": "At least 46 of all 48 planned responses valid and non-refusal",
            "observed": {
                "valid_non_refusal": len(valid_rows),
                "denominator": 48,
                "rate": len(valid_rows) / 48,
                "parse_failure_count": len(parse_failures),
                "refusal_candidate_count": len(refusals),
                "api_error_count": len(api_errors),
                "empty_response_count": len(empty_responses),
            },
            "result": pass_fail(len(valid_rows) >= 46),
        },
    ]

    diagnostics = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator_python": platform.python_version(),
        "selected_run_id": RUN_ID,
        "selected_raw_path": RAW_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "selected_raw_sha256": sha256_file(RAW_PATH),
        "selected_attempt_log_path": LOG_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "selected_attempt_log_sha256": sha256_file(LOG_PATH),
        "input_isolation": {
            "selected_run_only": True,
            "historical_pilot_data_loaded": False,
            "tiny_run_data_loaded": False,
            "dry_run_data_loaded": False,
            "connectivity_check_data_loaded": False,
        },
        "execution_status": {
            "api_successes": sum(row.get("status") == "success" for row in rows),
            "api_errors": len(api_errors),
            "attempt_records": len(attempts),
            "retry_scheduled_count": sum(bool(a.get("retry_scheduled")) for a in attempts),
            "maximum_attempt": max((a.get("attempt", 0) for a in attempts), default=0),
            "parse_successes": sum(bool((row.get("parse_result") or {}).get("success")) for row in rows),
            "parse_failures": len(parse_failures),
        },
        "checks": checks,
        "parse_failures": parse_failures,
        "refusal_candidates": refusals,
        "api_error_cells": api_errors,
        "empty_response_cells": empty_responses,
        "prohibited_analyses": {
            "treatment_ordering_calculated": False,
            "statistical_significance_calculated": False,
            "effect_size_calculated": False,
        },
        "decision_boundary": "Machine checks do not constitute the researcher's final Pilot decision and do not authorize freeze or a main run.",
    }
    write_text(
        OUTPUT_ROOT / "machine_checks.json",
        json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n",
    )

    checks_by_number = {check["criterion"]: check for check in checks}
    c0_display = "not calculable" if c0_mean is None else f"{c0_mean:.6g}%"
    share_display = "not calculable" if maximum_share is None else f"{maximum_share:.6f}"
    machine_md = f"""# Unstaking Mechanics v1.1 Endpoint Pilot — Preregistered Machine Checks

- Selected run ID: `{RUN_ID}`
- Raw SHA-256: `{sha256_file(RAW_PATH)}`
- Attempt-log SHA-256: `{sha256_file(LOG_PATH)}`
- Generator runtime: Python `{platform.python_version()}`
- Input isolation: only the selected raw output and its attempt log were loaded
- Old Pilot, Tiny Run, dry-run, and connectivity-check data: excluded
- Treatment ordering, significance, and effect size: not calculated

## Execution status

- API successes: **{diagnostics['execution_status']['api_successes']}/48**
- API errors: **{diagnostics['execution_status']['api_errors']}**
- Attempt records: **{diagnostics['execution_status']['attempt_records']}**
- Retries scheduled: **{diagnostics['execution_status']['retry_scheduled_count']}**
- Maximum attempt number: **{diagnostics['execution_status']['maximum_attempt']}**
- Parse successes: **{diagnostics['execution_status']['parse_successes']}/48**
- Parse failures: **{diagnostics['execution_status']['parse_failures']}**

## Five preregistered machine criteria

| # | Criterion | Prespecified threshold | Observed | Result |
|---:|---|---|---|---|
| 1 | Cell completeness and isolation | Exactly 48 unique P01–P16 × S/C0/T3 cells; 16 per arm; one Pilot run | {len(rows)} records; {len(set(cells))} unique; S={condition_counts['S']}, C0={condition_counts['C0']}, T3={condition_counts['T3']}; missing={len(missing_cells)}, duplicate={len(duplicate_cells)}, unexpected={len(unexpected_cells)} | **{checks_by_number[1]['result']}** |
| 2 | C0 mean dynamic range | 15%–75%, inclusive | Valid C0 n={len(valid_c0)}; mean={c0_display} | **{checks_by_number[2]['result']}** |
| 3 | C0 response-category diversity | At least 3 categories | {len(c0_counts)} categories; counts={dict(sorted(c0_counts.items()))} | **{checks_by_number[3]['result']}** |
| 4 | Combined category concentration | Maximum category share ≤0.85 | Valid pooled n={len(valid_rows)}; category {maximum_category} has {maximum_count}/{len(valid_rows)} = {share_display} | **{checks_by_number[4]['result']}** |
| 5 | Structured-output validity | At least 46/48 valid and non-refusal | {len(valid_rows)}/48 = {len(valid_rows)/48:.6f}; parse failures={len(parse_failures)}; refusals={len(refusals)}; API errors={len(api_errors)}; empty={len(empty_responses)} | **{checks_by_number[5]['result']}** |

## Decision boundary

These results apply only to `{RUN_ID}`. They are inputs to the researcher decision and do not alone authorize material freeze or a main run. The fixed-seed human review remains required. No treatment ordering, significance test, or effect-size criterion was used.
"""
    write_text(OUTPUT_ROOT / "machine_checks.md", machine_md)

    selected = []
    sampling_arms = {}
    for arm in ARMS:
        candidates = sorted(
            (row for row in rows if row["condition"] == arm),
            key=lambda row: row["persona_id"],
        )
        rng = random.Random(SEED)
        sampled = rng.sample(candidates, 4)
        selected.extend(sampled)
        sampling_arms[arm] = {
            "sorted_candidate_cell_ids": [row["cell_id"] for row in candidates],
            "selected_cell_ids": [row["cell_id"] for row in sampled],
        }

    sampling_manifest = {
        "run_id": RUN_ID,
        "seed": SEED,
        "python_version": platform.python_version(),
        "method": "Within each arm, sort by persona_id ascending; initialize an independent random.Random(seed); call sample(candidates, 4) once.",
        "sample_replacement_permitted": False,
        "arms": sampling_arms,
    }
    write_text(
        OUTPUT_ROOT / "sampling_manifest.json",
        json.dumps(sampling_manifest, ensure_ascii=False, indent=2) + "\n",
    )
    write_text(
        OUTPUT_ROOT / "selected_12_records.jsonl",
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in selected),
    )

    packet_parts = [
        "# Fixed-Seed 12-Record Formal Human Review Packet\n",
        f"- Run ID: `{RUN_ID}`\n",
        f"- Seed: `{SEED}`\n",
        f"- Python: `{platform.python_version()}`\n",
        "- Sampling: 4 records per arm, independent seed initialization, no replacement\n",
        "- Records may not be replaced because of their content or validity.\n",
    ]
    for index, row in enumerate(selected, 1):
        packet_parts.extend(
            [
                f"\n---\n\n## {index}. {row['cell_id']}\n",
                f"- Persona: `{row['persona_id']}`\n",
                f"- Arm: `{row['condition']}`\n",
                f"- API status: `{row['status']}`\n",
                f"- Parse success: `{bool((row.get('parse_result') or {}).get('success'))}`\n",
                f"- Prompt SHA-256: `{row['prompt_sha256']}`\n",
                "\n### Original assembled prompt\n\n```text\n",
                row["prompt"],
                "\n```\n\n### Original raw response\n\n```text\n",
                row.get("raw_response") or "<NO RESPONSE>",
                "\n```\n",
            ]
        )
    write_text(REVIEW_ROOT / "review_packet.md", "".join(packet_parts))

    selected_ids = [row["cell_id"] for row in selected]
    t3_ids = [row["cell_id"] for row in selected if row["condition"] == "T3"]
    checklist_parts = [
        "# Formal 12-Record Manual Review Checklist\n\n",
        f"- Run ID: `{RUN_ID}`\n",
        f"- Fixed seed: `{SEED}`\n",
        "- This checklist must be completed by the researcher.\n",
        "- Do not remove or replace sampled records.\n\n",
        "## A. Material factual hallucination\n\n",
        "Mark PASS only when the response contains no materially hallucinated decision-relevant fact; provide a short rationale.\n\n",
        "| # | Cell | Judgment (PASS/FAIL) | Rationale |\n|---:|---|---|---|\n",
    ]
    for index, cell_id in enumerate(selected_ids, 1):
        checklist_parts.append(f"| {index} | `{cell_id}` |  |  |\n")
    checklist_parts.extend(
        [
            "\n- Hallucination pass count: `____ / 12`\n",
            "- Threshold: at least 11/12\n",
            "- Criterion result — select one: `[ ] PASS  [ ] FAIL`\n\n",
            "## B. T3 executed/verifiable-action comprehension\n\n",
            "For each sampled T3 record, judge whether it remains consistent with an already executed, publicly verifiable on-chain reserve and does not recast it as compensation, yield, or a price guarantee.\n\n",
            "| # | Cell | Executed status (PASS/FAIL) | Public verifiability (PASS/FAIL) | No compensatory recast (PASS/FAIL) | Overall (PASS/FAIL) | Rationale |\n|---:|---|---|---|---|---|---|\n",
        ]
    )
    for index, cell_id in enumerate(t3_ids, 1):
        checklist_parts.append(f"| {index} | `{cell_id}` |  |  |  |  |  |\n")
    checklist_parts.extend(
        [
            "\n- T3 overall pass count: `____ / 4`\n",
            "- Threshold: 4/4\n",
            "- Criterion result — select one: `[ ] PASS  [ ] FAIL`\n\n",
            "## C. Formal human-review decision\n\n",
            "- Researcher name/initials: `________________`\n",
            "- Decision date: `________________`\n",
            "- Formal 12-record review — select one: `[ ] PASS  [ ] FAIL  [ ] PENDING`\n",
            "- Notes/rationale: `____________________________________________________________`\n\n",
            "This human decision covers only the two preregistered human criteria. It cannot override a failed machine criterion and does not authorize freeze or a main run.\n",
        ]
    )
    write_text(REVIEW_ROOT / "manual_review_checklist.md", "".join(checklist_parts))

    supplemental_parts = [
        "# All-48 Supplemental Quality Review Checklist\n\n",
        f"- Run ID: `{RUN_ID}`\n",
        "- Scope: additional teacher-workflow quality audit of all 48 records\n",
        "- This does not replace the fixed 12-record sample or alter any preregistered threshold.\n",
        "- Complete every item; do not repair or replace any response.\n",
    ]
    for index, row in enumerate(rows, 1):
        supplemental_parts.extend(
            [
                f"\n---\n\n## {index}. {row['cell_id']}\n\n",
                f"- Persona: `{row['persona_id']}`\n",
                f"- Arm: `{row['condition']}`\n",
                f"- API status: `{row['status']}`\n",
                f"- Parse success: `{bool((row.get('parse_result') or {}).get('success'))}`\n",
                "\n### Original assembled prompt\n\n```text\n",
                row["prompt"],
                "\n```\n\n### Original raw response\n\n```text\n",
                row.get("raw_response") or "<NO RESPONSE>",
                "\n```\n\n",
                "- [ ] Read the complete prompt and raw response.\n",
                "- [ ] Checked for material factual hallucination.\n",
                "- [ ] Checked that the response addresses the requested in-character decision.\n",
                "- [ ] Recorded any concern below, or wrote `No concern`.\n",
                "- Concern/notes: `________________________________________________________`\n",
            ]
        )
    supplemental_parts.extend(
        [
            "\n---\n\n## Completion record\n\n",
            "- Researcher name/initials: `________________`\n",
            "- Completion date: `________________`\n",
            "- Records completed: `____ / 48`\n",
            "- Overall supplemental notes: `________________________________________________`\n",
            "- [ ] I confirm that this supplemental review does not replace the fixed 12-record sample or alter its formal thresholds.\n",
        ]
    )
    write_text(
        REVIEW_ROOT / "all_48_supplemental_review.md",
        "".join(supplemental_parts),
    )


if __name__ == "__main__":
    main()
