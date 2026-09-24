"""Generate preregistered GLM-4.7 Pilot diagnostics and review packets.

This script is preserved as executable provenance.  It reads exactly one locked
Pilot JSONL for calculations.  Other Pilot JSONLs are inventoried and hashed but
never loaded into the calculation dataset.
"""

from __future__ import annotations

import hashlib
import json
import platform
import random
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "pilot_20260903T055848Z_a5ef2915"
SEED = 20260901
CONDITIONS = ("S", "C0", "T3")
ALLOWED_VALUES = {0, 25, 50, 75, 100}
RAW_PATH = PROJECT_ROOT / "03_raw_outputs" / "pilot" / f"{RUN_ID}.jsonl"
DIAGNOSTIC_DIR = PROJECT_ROOT / "05_processed_data" / "pilot_v1.1_diagnostics"
REVIEW_DIR = PROJECT_ROOT / "validation" / "pilot_v1.1_manual_review"
EXPECTED_CELLS = {
    f"P{persona:02d}_{condition}"
    for persona in range(1, 17)
    for condition in CONDITIONS
}
REFUSAL_PHRASES = (
    "i cannot make",
    "i can't make",
    "i am unable to make",
    "i cannot decide",
    "i can't decide",
    "i refuse",
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_text_exclusive(path: Path, text: str) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as output_file:
        output_file.write(text.rstrip() + "\n")


def write_json_exclusive(path: Path, value: Any) -> None:
    write_text_exclusive(
        path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False)
    )


def write_jsonl_exclusive(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as output_file:
        for row in rows:
            output_file.write(json.dumps(row, ensure_ascii=False) + "\n")


def is_refusal_candidate(record: dict[str, Any]) -> bool:
    parse_result = record.get("parse_result") or {}
    data = parse_result.get("data") or {}
    reason = str(data.get("reason", "")).lower()
    return any(phrase in reason for phrase in REFUSAL_PHRASES)


def is_valid_non_refusal(record: dict[str, Any]) -> bool:
    parse_result = record.get("parse_result") or {}
    data = parse_result.get("data") or {}
    return bool(
        record.get("status") == "success"
        and record.get("raw_response")
        and parse_result.get("success") is True
        and data.get("unstake_percentage") in ALLOWED_VALUES
        and isinstance(data.get("reason"), str)
        and data["reason"].strip()
        and not is_refusal_candidate(record)
    )


def condition_counts(records: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(record["condition"] for record in records)
    return {condition: counts[condition] for condition in CONDITIONS}


def markdown_code_block(value: str) -> str:
    return f"````text\n{value}\n````"


def main() -> None:
    if platform.python_version() != "3.14.4":
        raise RuntimeError(
            "The amended sampling runtime is fixed at Python 3.14.4; "
            f"observed {platform.python_version()}."
        )
    if not RAW_PATH.is_file():
        raise FileNotFoundError("Locked Pilot raw output is missing.")

    records = read_jsonl(RAW_PATH)
    actual_cells = [record["cell_id"] for record in records]
    duplicate_cells = sorted(
        cell for cell, count in Counter(actual_cells).items() if count > 1
    )
    missing_cells = sorted(EXPECTED_CELLS - set(actual_cells))
    unexpected_cells = sorted(set(actual_cells) - EXPECTED_CELLS)

    if any(record.get("run_id") != RUN_ID for record in records):
        raise ValueError("Raw input mixes run IDs.")
    if any(record.get("run_type") != "pilot" for record in records):
        raise ValueError("Raw input contains a non-Pilot record.")
    if any(record.get("provider") != "zhipu" for record in records):
        raise ValueError("Raw input contains a non-Zhipu record.")
    if any(record.get("model") != "glm-4.7" for record in records):
        raise ValueError("Raw input contains an unexpected requested model.")

    valid_records = [record for record in records if is_valid_non_refusal(record)]
    refusal_candidates = [record for record in records if is_refusal_candidate(record)]
    c0_valid = [record for record in valid_records if record["condition"] == "C0"]
    c0_values = [record["parse_result"]["data"]["unstake_percentage"] for record in c0_valid]
    pooled_values = [
        record["parse_result"]["data"]["unstake_percentage"]
        for record in valid_records
    ]
    c0_mean = sum(c0_values) / len(c0_values) if c0_values else None
    c0_distribution = Counter(c0_values)
    pooled_distribution = Counter(pooled_values)
    max_category, max_count = (
        pooled_distribution.most_common(1)[0]
        if pooled_distribution
        else (None, 0)
    )
    max_share = max_count / len(pooled_values) if pooled_values else None
    parse_failures = [
        {
            "cell_id": record["cell_id"],
            "error": (record.get("parse_result") or {}).get("error"),
        }
        for record in records
        if not (record.get("parse_result") or {}).get("success", False)
    ]
    api_errors = [record["cell_id"] for record in records if record.get("status") != "success"]
    empty_responses = [record["cell_id"] for record in records if not record.get("raw_response")]

    checks = [
        {
            "criterion": 1,
            "name": "Cell completeness and isolation",
            "threshold": "Exactly 48 unique P01-P16 x S/C0/T3 cells from one run; run_type=pilot",
            "observed": {
                "records": len(records),
                "unique_cells": len(set(actual_cells)),
                "condition_counts": condition_counts(records),
                "missing_cells": missing_cells,
                "duplicate_cells": duplicate_cells,
                "unexpected_cells": unexpected_cells,
                "run_ids": sorted({record["run_id"] for record in records}),
                "run_types": sorted({record["run_type"] for record in records}),
            },
            "result": "PASS"
            if len(records) == 48
            and set(actual_cells) == EXPECTED_CELLS
            and not duplicate_cells
            else "FAIL",
        },
        {
            "criterion": 2,
            "name": "C0 mean dynamic range",
            "threshold": "15 <= mean <= 75 among valid non-refusal C0 responses",
            "observed": {"valid_n": len(c0_values), "mean": c0_mean},
            "result": "PASS"
            if c0_mean is not None and 15 <= c0_mean <= 75
            else "FAIL",
        },
        {
            "criterion": 3,
            "name": "C0 response-category diversity",
            "threshold": "At least 3 distinct categories among valid non-refusal C0 responses",
            "observed": {
                "valid_n": len(c0_values),
                "distinct_categories": len(c0_distribution),
                "category_counts": {
                    str(value): c0_distribution[value]
                    for value in sorted(c0_distribution)
                },
            },
            "result": "PASS" if len(c0_distribution) >= 3 else "FAIL",
        },
        {
            "criterion": 4,
            "name": "Combined category concentration",
            "threshold": "Maximum single-category share <= 0.85 among pooled valid non-refusal responses",
            "observed": {
                "valid_n": len(pooled_values),
                "category_counts": {
                    str(value): pooled_distribution[value]
                    for value in sorted(pooled_distribution)
                },
                "maximum_category": max_category,
                "maximum_count": max_count,
                "maximum_share": max_share,
            },
            "result": "PASS"
            if max_share is not None and max_share <= 0.85
            else "FAIL",
        },
        {
            "criterion": 5,
            "name": "Structured-output validity",
            "threshold": "At least 46 of all 48 planned responses valid and non-refusal",
            "observed": {
                "valid_non_refusal": len(valid_records),
                "denominator": 48,
                "rate": len(valid_records) / 48,
                "parse_failure_count": len(parse_failures),
                "refusal_candidate_count": len(refusal_candidates),
                "api_error_count": len(api_errors),
                "empty_response_count": len(empty_responses),
            },
            "result": "PASS" if len(valid_records) >= 46 else "FAIL",
        },
    ]

    pilot_inventory = []
    for path in sorted((PROJECT_ROOT / "03_raw_outputs" / "pilot").glob("*.jsonl")):
        pilot_inventory.append(
            {
                "path": path.relative_to(PROJECT_ROOT).as_posix(),
                "sha256": sha256_file(path),
                "selected_for_calculation": path.resolve() == RAW_PATH.resolve(),
            }
        )

    generated_at = datetime.now(timezone.utc).isoformat()
    machine_output = {
        "generated_at": generated_at,
        "generator_python": platform.python_version(),
        "selected_run_id": RUN_ID,
        "selected_raw_path": RAW_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "selected_raw_sha256": sha256_file(RAW_PATH),
        "historical_input_isolation": pilot_inventory,
        "checks": checks,
        "parse_failures": parse_failures,
        "refusal_candidates": [record["cell_id"] for record in refusal_candidates],
        "api_errors": api_errors,
        "empty_responses": empty_responses,
        "decision_boundary": (
            "Machine results do not constitute the researcher's final Pilot "
            "decision and do not authorize freeze or a main run."
        ),
    }
    write_json_exclusive(DIAGNOSTIC_DIR / "machine_checks.json", machine_output)

    machine_lines = [
        "# GLM-4.7 Endpoint Pilot — Preregistered Machine Checks",
        "",
        f"- Selected run ID: `{RUN_ID}`",
        f"- Raw SHA-256: `{sha256_file(RAW_PATH)}`",
        f"- Generator runtime: Python `{platform.python_version()}`",
        "- Historical Pilot files: inventoried and excluded from calculations",
        "- Treatment ordering, contrasts, significance, and effect size: not calculated",
        "",
        "## Five machine criteria",
        "",
        "| # | Criterion | Threshold | Observed | Result |",
        "|---:|---|---|---|---|",
    ]
    observed_text = {
        1: "48 records; 48 unique cells; S=16, C0=16, T3=16; no missing/duplicate/unexpected cells",
        2: f"valid C0 n={len(c0_values)}; mean={c0_mean:.3f}%",
        3: f"{len(c0_distribution)} categories; counts=" + ", ".join(
            f"{value}:{c0_distribution[value]}" for value in sorted(c0_distribution)
        ),
        4: f"valid pooled n={len(pooled_values)}; category {max_category} has {max_count}/{len(pooled_values)} = {max_share:.6f}",
        5: f"{len(valid_records)}/48 = {len(valid_records)/48:.6f}; parse failures={len(parse_failures)}; refusal candidates={len(refusal_candidates)}; API errors={len(api_errors)}; empty={len(empty_responses)}",
    }
    for check in checks:
        machine_lines.append(
            f"| {check['criterion']} | {check['name']} | {check['threshold']} | "
            f"{observed_text[check['criterion']]} | **{check['result']}** |"
        )
    machine_lines.extend(
        [
            "",
            "## Preserved parse failures",
            "",
        ]
    )
    for failure in parse_failures:
        machine_lines.append(f"- `{failure['cell_id']}`: {failure['error']}")
    machine_lines.extend(
        [
            "",
            "The two malformed responses remain unchanged and were not re-asked, repaired, or coerced.",
            "",
            "## Decision boundary",
            "",
            "These machine results are inputs to the researcher decision. They do not by themselves authorize material freeze or a main run. The formal 12-record human review remains required even when one or more machine criteria fail.",
        ]
    )
    write_text_exclusive(DIAGNOSTIC_DIR / "machine_checks.md", "\n".join(machine_lines))

    selected_records: list[dict[str, Any]] = []
    arm_sampling: dict[str, Any] = {}
    for condition in CONDITIONS:
        pool = sorted(
            (record for record in records if record["condition"] == condition),
            key=lambda record: record["persona_id"],
        )
        rng = random.Random(SEED)
        selected = rng.sample(pool, 4)
        selected_records.extend(selected)
        arm_sampling[condition] = {
            "candidate_cell_ids_in_sort_order": [record["cell_id"] for record in pool],
            "selected_cell_ids_in_draw_order": [record["cell_id"] for record in selected],
        }

    sampling_manifest = {
        "generated_at": generated_at,
        "selected_run_id": RUN_ID,
        "raw_sha256": sha256_file(RAW_PATH),
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "seed": SEED,
        "procedure": (
            "For each arm independently: sort by persona_id ascending, initialize "
            "random.Random(20260901), then call sample(pool, 4) once."
        ),
        "replacement_permitted": False,
        "arms": arm_sampling,
        "selected_count": len(selected_records),
    }
    write_json_exclusive(DIAGNOSTIC_DIR / "sampling_manifest.json", sampling_manifest)
    write_jsonl_exclusive(DIAGNOSTIC_DIR / "selected_12_records.jsonl", selected_records)

    packet_lines = [
        "# GLM-4.7 Pilot — Fixed-Seed 12-Record Human Review Packet",
        "",
        f"- Run ID: `{RUN_ID}`",
        f"- Seed: `{SEED}`",
        f"- Runtime: CPython `{platform.python_version()}`",
        "- Allocation: 4 S, 4 C0, 4 T3",
        "- Replacement: prohibited",
        "- Selection order below is the original draw order within each arm",
        "",
        "This packet preserves the original prompt and raw response. A parsing failure remains reviewable as observed and must not be replaced.",
    ]
    for index, record in enumerate(selected_records, start=1):
        packet_lines.extend(
            [
                "",
                f"## {index}. {record['cell_id']}",
                "",
                f"- Persona: `{record['persona_id']}`",
                f"- Arm: `{record['condition']}`",
                f"- API status: `{record['status']}`",
                f"- Parse success: `{bool((record.get('parse_result') or {}).get('success'))}`",
                f"- Prompt SHA-256: `{record['prompt_sha256']}`",
                f"- Response ID: `{record.get('response_id')}`",
                "",
                "### Original prompt",
                "",
                markdown_code_block(record["prompt"]),
                "",
                "### Original raw response",
                "",
                markdown_code_block(record.get("raw_response") or "<EMPTY RESPONSE>"),
                "",
                "### Recorded parse result",
                "",
                "````json",
                json.dumps(record.get("parse_result"), ensure_ascii=False, indent=2),
                "````",
            ]
        )
    write_text_exclusive(REVIEW_DIR / "review_packet.md", "\n".join(packet_lines))

    checklist_lines = [
        "# GLM-4.7 Pilot — Formal 12-Record Manual Review Checklist",
        "",
        f"- Locked run ID: `{RUN_ID}`",
        f"- Sampling seed: `{SEED}`",
        f"- Runtime: CPython `{platform.python_version()}`",
        "- Formal threshold A: at least 11/12 responses contain no material factual hallucination",
        "- Formal threshold B: all 4 sampled T3 responses remain consistent with an already-executed, publicly verifiable action",
        "",
        "Read `review_packet.md` and enter a judgment and short rationale for every sampled response. Do not replace an inconvenient, malformed, surprising, or hypothesis-inconsistent record.",
    ]
    for index, record in enumerate(selected_records, start=1):
        checklist_lines.extend(
            [
                "",
                f"## {index}. {record['cell_id']}",
                "",
                "Material factual hallucination:",
                "",
                "- [ ] PASS — no materially hallucinated decision-relevant fact",
                "- [ ] FAIL — one or more materially hallucinated decision-relevant facts",
                "",
                "Required short rationale:",
                "",
                "",
            ]
        )
        if record["condition"] == "T3":
            checklist_lines.extend(
                [
                    "T3 executed/verifiable-action comprehension:",
                    "",
                    "- [ ] PASS — consistent with already executed and publicly verifiable status; no compensation/yield/price-guarantee rewrite",
                    "- [ ] FAIL — materially recasts or misunderstands the action",
                    "",
                    "Required short rationale:",
                    "",
                    "",
                ]
            )
    checklist_lines.extend(
        [
            "",
            "## Researcher aggregate decision",
            "",
            "Material hallucination count passing (must be at least 11/12):",
            "",
            "T3 comprehension count passing (must be 4/4):",
            "",
            "Formal 12-record manual result (`PASS`, `FAIL`, or `PENDING`):",
            "",
            "Researcher name/initials:",
            "",
            "Review date:",
            "",
            "Notes:",
        ]
    )
    write_text_exclusive(
        REVIEW_DIR / "manual_review_checklist.md", "\n".join(checklist_lines)
    )

    supplemental_lines = [
        "# GLM-4.7 Pilot — Supplemental 48-Record Read-Through",
        "",
        f"- Locked run ID: `{RUN_ID}`",
        "- Scope: all 48 records, ordered by persona P01-P16 and then S/C0/T3",
        "- Status: supplemental teacher-workflow quality audit",
        "",
        "This read-through does not replace, expand, resample, or alter the formal fixed-seed 12-record human thresholds. Findings may be documented as supplemental observations only.",
    ]
    condition_order = {condition: index for index, condition in enumerate(CONDITIONS)}
    ordered_records = sorted(
        records,
        key=lambda record: (record["persona_id"], condition_order[record["condition"]]),
    )
    for index, record in enumerate(ordered_records, start=1):
        supplemental_lines.extend(
            [
                "",
                f"## {index}. {record['cell_id']}",
                "",
                f"- Parse success: `{bool((record.get('parse_result') or {}).get('success'))}`",
                f"- Prompt SHA-256: `{record['prompt_sha256']}`",
                "- [ ] I read the original prompt and response below.",
                "- [ ] No material factual hallucination observed.",
                "- [ ] Arm information is understood without a material rewrite.",
                "- [ ] Any concern is documented in Notes.",
                "",
                "Notes:",
                "",
                "<details><summary>Original prompt</summary>",
                "",
                markdown_code_block(record["prompt"]),
                "",
                "</details>",
                "",
                "<details><summary>Original raw response</summary>",
                "",
                markdown_code_block(record.get("raw_response") or "<EMPTY RESPONSE>"),
                "",
                "</details>",
            ]
        )
    supplemental_lines.extend(
        [
            "",
            "## Supplemental completion record",
            "",
            "Records read (out of 48):",
            "",
            "Researcher name/initials:",
            "",
            "Review date:",
            "",
            "Supplemental notes:",
        ]
    )
    write_text_exclusive(
        REVIEW_DIR / "all_48_supplemental_review.md",
        "\n".join(supplemental_lines),
    )

    print(f"Locked run: {RUN_ID}")
    print("Machine checks: " + ", ".join(check["result"] for check in checks))
    print(
        "Selected cells: "
        + ", ".join(record["cell_id"] for record in selected_records)
    )
    print("API calls made: 0")


if __name__ == "__main__":
    main()
