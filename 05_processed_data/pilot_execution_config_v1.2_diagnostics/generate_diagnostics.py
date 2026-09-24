import json
import random
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "pilot_20260904T150852Z_18e62216"
SEED = 20260901
RAW_PATH = ROOT / "03_raw_outputs/pilot" / f"{RUN_ID}.jsonl"
LOG_PATH = ROOT / "08_logs/pilot" / f"{RUN_ID}_attempts.jsonl"
OUT_DIR = Path(__file__).resolve().parent
REVIEW_DIR = ROOT / "validation/pilot_execution_config_v1.2_manual_review"
ALLOWED_VALUES = {0, 25, 50, 75, 100}
ARMS = ("S", "C0", "T3")


def load_jsonl(path):
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def valid_non_refusal(record):
    parsed = record.get("parse_result") or {}
    data = parsed.get("data") or {}
    reason = data.get("reason")
    return (
        record.get("status") == "success"
        and parsed.get("success") is True
        and data.get("unstake_percentage") in ALLOWED_VALUES
        and isinstance(reason, str)
        and bool(reason.strip())
    )


def main():
    raw = load_jsonl(RAW_PATH)
    attempts = load_jsonl(LOG_PATH)
    if len(raw) != 48:
        raise SystemExit(f"Expected 48 records, found {len(raw)}")
    if {record.get("run_id") for record in raw} != {RUN_ID}:
        raise SystemExit("Raw output contains a different run_id")
    if any(record.get("run_type") != "pilot" for record in raw):
        raise SystemExit("Non-pilot record found")

    expected = {f"P{number:02d}_{arm}" for number in range(1, 17) for arm in ARMS}
    cells = [record["cell_id"] for record in raw]
    cell_counts = Counter(cells)
    missing = sorted(expected - set(cells))
    unexpected = sorted(set(cells) - expected)
    duplicates = sorted(cell for cell, count in cell_counts.items() if count > 1)
    arm_counts = Counter(record["condition"] for record in raw)

    valid = [record for record in raw if valid_non_refusal(record)]
    invalid = [record for record in raw if not valid_non_refusal(record)]
    parse_failures = [record for record in raw if not (record.get("parse_result") or {}).get("success")]
    api_errors = [record for record in raw if record.get("status") != "success"]
    empty_responses = [record for record in raw if not str(record.get("raw_response") or "").strip()]
    # Each valid parsed response made the requested in-character numeric decision.
    # No semantic refusal classifier is introduced after registration.
    refusal_count = 0

    c0 = [record for record in valid if record["condition"] == "C0"]
    c0_values = [(record["parse_result"]["data"]["unstake_percentage"]) for record in c0]
    c0_counts = Counter(c0_values)
    c0_mean = sum(c0_values) / len(c0_values) if c0_values else None
    pooled_values = [record["parse_result"]["data"]["unstake_percentage"] for record in valid]
    pooled_counts = Counter(pooled_values)
    max_category, max_count = pooled_counts.most_common(1)[0] if pooled_counts else (None, 0)
    max_share = max_count / len(pooled_values) if pooled_values else None

    criteria = {
        "cell_completeness_and_isolation": {
            "threshold": "exactly 48 unique P01-P16 x S/C0/T3 cells, 16 per arm, one pilot run",
            "observed": {"records": len(raw), "unique_cells": len(set(cells)), "arm_counts": dict(arm_counts), "missing": missing, "unexpected": unexpected, "duplicates": duplicates},
            "pass": len(raw) == 48 and set(cells) == expected and not duplicates and all(arm_counts[arm] == 16 for arm in ARMS),
        },
        "c0_mean_dynamic_range": {
            "threshold": "15 <= valid non-refusal C0 mean <= 75",
            "observed": {"valid_c0_n": len(c0_values), "mean": c0_mean},
            "pass": c0_mean is not None and 15 <= c0_mean <= 75,
        },
        "c0_response_category_diversity": {
            "threshold": "at least 3 distinct valid non-refusal C0 categories",
            "observed": {"category_count": len(c0_counts), "counts": {str(key): c0_counts.get(key, 0) for key in sorted(ALLOWED_VALUES)}},
            "pass": len(c0_counts) >= 3,
        },
        "combined_category_concentration": {
            "threshold": "maximum pooled valid non-refusal category share <= 0.85",
            "observed": {"valid_n": len(pooled_values), "counts": {str(key): pooled_counts.get(key, 0) for key in sorted(ALLOWED_VALUES)}, "largest_category": max_category, "largest_count": max_count, "largest_share": max_share},
            "pass": max_share is not None and max_share <= 0.85,
        },
        "structured_output_validity": {
            "threshold": "at least 46 of 48 valid non-refusal responses",
            "observed": {"valid_non_refusal": len(valid), "invalid": len(invalid), "parse_failures": len(parse_failures), "api_errors": len(api_errors), "empty_responses": len(empty_responses), "refusals": refusal_count},
            "pass": len(valid) >= 46,
        },
    }

    selected = []
    candidates = {}
    for arm in ARMS:
        arm_records = sorted((record for record in raw if record["condition"] == arm), key=lambda record: record["persona_id"])
        candidates[arm] = [record["cell_id"] for record in arm_records]
        chosen = random.Random(SEED).sample(arm_records, 4)
        selected.extend(chosen)

    selected_ids = {arm: [record["cell_id"] for record in selected if record["condition"] == arm] for arm in ARMS}
    retry_attempts = max(0, len(attempts) - len(raw))
    run_status = {
        "raw_records": len(raw),
        "attempt_log_records": len(attempts),
        "api_successes": sum(record.get("status") == "success" for record in raw),
        "api_failures": len(api_errors),
        "parse_successes": len(raw) - len(parse_failures),
        "parse_failures": len(parse_failures),
        "retry_attempts": retry_attempts,
        "records_with_multiple_attempts": sum((record.get("attempt_count") or 0) > 1 for record in raw),
    }
    report = {
        "run_id": RUN_ID,
        "data_scope": {"raw_output": RAW_PATH.relative_to(ROOT).as_posix(), "attempt_log": LOG_PATH.relative_to(ROOT).as_posix(), "historical_runs_included": 0},
        "runtime": sys.version.split()[0],
        "run_status": run_status,
        "machine_criteria": criteria,
        "machine_pass_count": sum(item["pass"] for item in criteria.values()),
        "machine_overall": "PASS" if all(item["pass"] for item in criteria.values()) else "FAIL",
        "sampling": {"seed": SEED, "method": "independent random.Random(seed).sample(sorted_arm_records, 4) per arm", "candidate_cell_ids": candidates, "selected_cell_ids": selected_ids, "replacement_permitted": False},
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "machine_checks.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT_DIR / "sample_manifest.json").write_text(json.dumps({"run_id": RUN_ID, "seed": SEED, "runtime": sys.version.split()[0], "candidate_cell_ids": candidates, "selected_cell_ids": selected_ids}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    names = {
        "cell_completeness_and_isolation": "1. Cell completeness and isolation",
        "c0_mean_dynamic_range": "2. C0 mean dynamic range",
        "c0_response_category_diversity": "3. C0 response-category diversity",
        "combined_category_concentration": "4. Combined category concentration",
        "structured_output_validity": "5. Structured-output validity",
    }
    md = ["# Pilot execution-config v1.2 machine checks", "", f"- Run ID: `{RUN_ID}`", f"- Overall machine result: **{report['machine_overall']}** ({report['machine_pass_count']}/5)", "- Scope: only the raw output and attempt log named above; no historical Pilot, Tiny Run, dry-run, or connectivity-check data were included.", "- These are design-quality checks, not treatment-effect analysis.", "", "## API and parsing status", "", f"- Raw records: {run_status['raw_records']}/48", f"- Attempt records: {run_status['attempt_log_records']}", f"- API successes/failures: {run_status['api_successes']}/{run_status['api_failures']}", f"- Parse successes/failures: {run_status['parse_successes']}/{run_status['parse_failures']}", f"- Retry attempts: {run_status['retry_attempts']}", "", "## Five preregistered machine criteria", ""]
    for key, title in names.items():
        item = criteria[key]
        md.extend([f"### {title}", "", f"- Threshold: {item['threshold']}", f"- Observed: `{json.dumps(item['observed'], ensure_ascii=False, sort_keys=True)}`", f"- Result: **{'PASS' if item['pass'] else 'FAIL'}**", ""])
    md.extend(["## Formal manual sample", "", f"- Seed: `{SEED}`", f"- Python runtime: `{sys.version.split()[0]}`", "- Independent `random.Random(20260901)` instance per arm after sorting P01-P16.", "- No replacement or substitution is permitted.", f"- S: `{', '.join(selected_ids['S'])}`", f"- C0: `{', '.join(selected_ids['C0'])}`", f"- T3: `{', '.join(selected_ids['T3'])}`", "", "The researcher must complete the formal 12-record review. This report does not make the final Pilot decision."])
    (OUT_DIR / "machine_checks.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    packet = ["# Fixed-seed formal Pilot review packet", "", f"- Run ID: `{RUN_ID}`", f"- Seed: `{SEED}`", f"- Runtime: Python `{sys.version.split()[0]}`", "- Fixed allocation: S/C0/T3 each 4 records", "- The text below preserves each selected record's raw prompt and raw response.", ""]
    for index, record in enumerate(selected, 1):
        packet.extend([f"## {index}. {record['cell_id']}", "", f"- Persona: `{record['persona_id']}`", f"- Arm: `{record['condition']}`", f"- Prompt SHA-256: `{record['prompt_sha256']}`", f"- System SHA-256: `{record['system_prompt_sha256']}`", "", "### Original prompt", "", "```text", record["prompt"], "```", "", "### Original raw response", "", "```text", str(record.get("raw_response") or ""), "```", ""])
    (REVIEW_DIR / "review_packet.md").write_text("\n".join(packet) + "\n", encoding="utf-8")

    checklist = ["# Formal 12-record manual review checklist", "", f"- Run ID: `{RUN_ID}`", f"- Sampling seed: `{SEED}`", "- Researcher name/initials: ______", "- Decision date: ______", "", "Instructions: enter `PASS` or `FAIL` and a short rationale for material factual hallucination for every row. For the four T3 rows, also enter `PASS` or `FAIL` and a short rationale for executed/publicly-verifiable-action comprehension. Do not replace any sampled record.", "", "## A. Material factual hallucination — required for all 12", "", "Threshold: at least 11/12 PASS.", "", "| # | Cell | Arm | Judgment (PASS/FAIL) | Short rationale |", "|---:|---|---|---|---|"]
    for index, record in enumerate(selected, 1):
        checklist.append(f"| {index} | `{record['cell_id']}` | `{record['condition']}` |  |  |")
    checklist.extend(["", "- Hallucination PASS count: ___ / 12", "- Criterion result (PASS requires >=11/12): ______", "", "## B. T3 executed/publicly-verifiable-action comprehension — required for sampled T3 only", "", "Threshold: 4/4 PASS.", "", "| Cell | Judgment (PASS/FAIL) | Short rationale |", "|---|---|---|"])
    for record in selected:
        if record["condition"] == "T3":
            checklist.append(f"| `{record['cell_id']}` |  |  |")
    checklist.extend(["", "- T3 comprehension PASS count: ___ / 4", "- Criterion result (PASS requires 4/4): ______", "", "## Researcher completion status", "", "- [ ] All 12 hallucination judgments and rationales completed", "- [ ] All 4 T3 comprehension judgments and rationales completed", "", "This checklist does not ask for treatment ordering, significance, effect size, or expected-direction judgments. Completing it does not itself freeze materials or authorize a main run."])
    (REVIEW_DIR / "manual_review_checklist.md").write_text("\n".join(checklist) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
