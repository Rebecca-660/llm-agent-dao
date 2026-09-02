"""Reproduce preregistered Endpoint Pilot diagnostics and manual-review sample.

Reads only the frozen Pilot JSONL and writes derived diagnostic/review artifacts.
Run from the repository root with Python 3.11.
"""

from __future__ import annotations

import hashlib
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path


SEED = 20260901
ARMS = ("S", "C0", "T3")
EXPECTED_PERSONAS = tuple(f"P{i:02d}" for i in range(1, 17))
ALLOWED_VALUES = {0, 25, 50, 75, 100}
RAW_DIR = Path("03_raw_outputs/pilot")
DIAGNOSTIC_DIR = Path("05_processed_data/pilot_diagnostics")
REVIEW_DIR = Path("validation/pilot_manual_review")

# A deliberately narrow screen for an explicit refusal to make the requested
# decision. It is reported separately from human factual/comprehension review.
REFUSAL_RE = re.compile(
    r"\b(?:i\s+(?:cannot|can't|am unable to|refuse to|won't|will not)\s+"
    r"(?:make|provide|choose|decide|comply)|as an ai)\b",
    re.IGNORECASE,
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def classify(record: dict) -> dict:
    raw_response = record.get("raw_response")
    parsed = record.get("parse_result") or {}
    data = parsed.get("data") or {}
    reason = data.get("reason")
    api_error = record.get("status") != "success" or record.get("error") is not None
    empty = not isinstance(raw_response, str) or not raw_response.strip()
    parse_failure = not bool(parsed.get("success"))
    schema_invalid = (
        data.get("unstake_percentage") not in ALLOWED_VALUES
        or not isinstance(reason, str)
        or not reason.strip()
    )
    refusal = bool(REFUSAL_RE.search(raw_response or ""))
    valid_non_refusal = not any(
        (api_error, empty, parse_failure, schema_invalid, refusal)
    )
    return {
        "api_error": api_error,
        "empty_response": empty,
        "parse_failure": parse_failure,
        "schema_invalid": schema_invalid,
        "explicit_refusal_screen": refusal,
        "valid_non_refusal": valid_non_refusal,
    }


def sample_cpython311(population: list[dict], k: int, seed: int) -> list[dict]:
    """Exact CPython 3.11 ``random.sample`` pool branch used for n=16, k=4."""
    rng = random.Random(seed)
    pool = list(population)
    n = len(pool)
    result = [None] * k
    for i in range(k):
        j = rng._randbelow(n - i)
        result[i] = pool[j]
        pool[j] = pool[n - i - 1]
    return result


def main() -> None:
    raw_files = sorted(RAW_DIR.glob("*.jsonl"))
    if len(raw_files) != 1:
        raise RuntimeError(f"Expected one Pilot JSONL, found {len(raw_files)}")
    raw_path = raw_files[0]
    records = [json.loads(line) for line in raw_path.read_text(encoding="utf-8").splitlines()]
    for line_number, record in enumerate(records, 1):
        record["_raw_line_number"] = line_number
        record["_classification"] = classify(record)

    run_ids = sorted({r.get("run_id") for r in records})
    expected_cells = {f"{p}_{arm}" for p in EXPECTED_PERSONAS for arm in ARMS}
    cell_counts = Counter(r.get("cell_id") for r in records)
    actual_cells = set(cell_counts)
    duplicates = sorted(cell for cell, count in cell_counts.items() if count > 1)
    missing = sorted(expected_cells - actual_cells)
    unexpected = sorted(actual_cells - expected_cells)
    arm_counts = Counter(r.get("condition") for r in records)

    valid = [r for r in records if r["_classification"]["valid_non_refusal"]]
    valid_c0 = [r for r in valid if r.get("condition") == "C0"]
    c0_values = [r["parse_result"]["data"]["unstake_percentage"] for r in valid_c0]
    pooled_values = [r["parse_result"]["data"]["unstake_percentage"] for r in valid]
    c0_mean = sum(c0_values) / len(c0_values) if c0_values else None
    pooled_counts = Counter(pooled_values)
    maximum_share = max(pooled_counts.values()) / len(pooled_values) if pooled_values else None

    classification_counts = {
        key: sum(r["_classification"][key] for r in records)
        for key in (
            "api_error",
            "empty_response",
            "parse_failure",
            "schema_invalid",
            "explicit_refusal_screen",
            "valid_non_refusal",
        )
    }
    completeness_pass = (
        len(records) == 48
        and actual_cells == expected_cells
        and not duplicates
        and len(run_ids) == 1
        and all(r.get("run_type") == "pilot" for r in records)
        and all(r.get("independent_context") is True for r in records)
        and all(r.get("previous_response_id") is None for r in records)
    )

    results = {
        "scope": {
            "source_file": raw_path.as_posix(),
            "source_file_sha256": sha256_file(raw_path),
            "run_ids": run_ids,
            "record_count": len(records),
            "run_type_values": sorted({str(r.get("run_type")) for r in records}),
            "excluded_non_pilot_files": True,
        },
        "classification_rule": {
            "valid_non_refusal": (
                "successful non-empty response; parser success; allowed percentage; "
                "non-empty reason; no match to the explicit-refusal regex"
            ),
            "explicit_refusal_regex": REFUSAL_RE.pattern,
            "note": "Human judgments are required only for the prespecified sampled records.",
        },
        "checks": {
            "cell_completeness_and_isolation": {
                "threshold": "Exactly 48 unique P01-P16 x S/C0/T3 cells; one Pilot run_id; pilot records only; independent contexts",
                "observed": {
                    "records": len(records),
                    "unique_cells": len(actual_cells),
                    "arm_counts": dict(sorted(arm_counts.items())),
                    "missing_cells": missing,
                    "duplicate_cells": duplicates,
                    "unexpected_cells": unexpected,
                    "run_ids": run_ids,
                    "all_run_type_pilot": all(r.get("run_type") == "pilot" for r in records),
                    "all_independent_context": all(r.get("independent_context") is True for r in records),
                    "all_previous_response_id_null": all(r.get("previous_response_id") is None for r in records),
                },
                "pass": completeness_pass,
            },
            "c0_mean_dynamic_range": {
                "threshold": "15 <= C0 mean <= 75 among valid non-refusals",
                "observed": {"valid_c0_n": len(c0_values), "mean": c0_mean},
                "pass": c0_mean is not None and 15 <= c0_mean <= 75,
            },
            "c0_response_category_diversity": {
                "threshold": "At least 3 distinct categories among valid non-refusal C0 responses",
                "observed": {"distinct_count": len(set(c0_values)), "categories": sorted(set(c0_values))},
                "pass": len(set(c0_values)) >= 3,
            },
            "combined_category_concentration": {
                "threshold": "No category share > 0.85 among pooled valid non-refusals",
                "observed": {
                    "pooled_valid_n": len(pooled_values),
                    "category_counts": {str(k): pooled_counts[k] for k in sorted(pooled_counts)},
                    "maximum_category_share": maximum_share,
                },
                "pass": maximum_share is not None and maximum_share <= 0.85,
            },
            "structured_output_validity": {
                "threshold": "At least 46 of 48 valid non-refusal responses",
                "observed": {**classification_counts, "denominator": 48},
                "pass": classification_counts["valid_non_refusal"] >= 46,
            },
        },
        "not_assessed": [
            "treatment-effect direction or ordering",
            "statistical significance",
            "minimum treatment-effect size",
            "final researcher Pilot decision",
            "human hallucination and T3-comprehension criteria (pending review)",
        ],
    }

    selected = []
    for arm in ARMS:
        arm_records = sorted(
            (r for r in records if r.get("condition") == arm),
            key=lambda r: r["persona_id"],
        )
        if [r["persona_id"] for r in arm_records] != list(EXPECTED_PERSONAS):
            raise RuntimeError(f"Arm {arm} does not contain sorted P01-P16")
        selected.extend(sample_cpython311(arm_records, 4, SEED))

    manifest = {
        "seed": SEED,
        "python_sampling_semantics": "CPython 3.11 random.sample pool branch (n=16, k=4)",
        "python_used": ".".join(map(str, sys.version_info[:3])),
        "algorithm": (
            "For each arm S, C0, T3 independently: sort records by persona_id ascending, "
            "initialize random.Random(20260901), then apply the exact CPython 3.11 "
            "random.sample pool branch for n=16, k=4 once."
        ),
        "source_file": raw_path.as_posix(),
        "source_file_sha256": sha256_file(raw_path),
        "run_id": run_ids[0] if len(run_ids) == 1 else run_ids,
        "selected": [
            {
                "arm": r["condition"],
                "persona_id": r["persona_id"],
                "cell_id": r["cell_id"],
                "raw_line_number": r["_raw_line_number"],
                "prompt_sha256_recorded": r["prompt_sha256"],
                "prompt_sha256_recomputed": sha256_text(r["prompt"]),
                "raw_response_sha256": sha256_text(r["raw_response"]),
                "status": r["status"],
                "parse_success": r["parse_result"]["success"],
            }
            for r in selected
        ],
    }

    DIAGNOSTIC_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    (DIAGNOSTIC_DIR / "machine_checks.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (DIAGNOSTIC_DIR / "sampling_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    checks = results["checks"]
    report_lines = [
        "# Endpoint Pilot preregistered machine checks",
        "",
        f"- Source: `{raw_path.as_posix()}`",
        f"- Source SHA-256: `{sha256_file(raw_path)}`",
        f"- Pilot run ID: `{run_ids[0]}`",
        "- Scope: this Pilot JSONL only; no Smoke or Tiny Run data included.",
        "",
        "## Results",
        "",
        "| Preregistered criterion | Threshold | Observed | Machine result |",
        "|---|---|---|---|",
        f"| Cell completeness and isolation | 48 unique P01-P16 × S/C0/T3; one Pilot run; independent context | 48 records, 48 unique; S=16, C0=16, T3=16; missing=0; duplicates=0; all `run_type=pilot`; all contexts independent | **{'PASS' if checks['cell_completeness_and_isolation']['pass'] else 'FAIL'}** |",
        f"| C0 mean dynamic range | 15%–75% inclusive | n={len(c0_values)}; mean={c0_mean:.2f}% | **{'PASS' if checks['c0_mean_dynamic_range']['pass'] else 'FAIL'}** |",
        f"| C0 category diversity | At least 3 categories | {len(set(c0_values))} category: {sorted(set(c0_values))} | **{'PASS' if checks['c0_response_category_diversity']['pass'] else 'FAIL'}** |",
        f"| Combined category concentration | Maximum category share ≤85% | counts={dict(sorted(pooled_counts.items()))}; maximum={maximum_share:.2%} | **{'PASS' if checks['combined_category_concentration']['pass'] else 'FAIL'}** |",
        f"| Structured-output validity | At least 46/48 valid non-refusals | {classification_counts['valid_non_refusal']}/48 ({classification_counts['valid_non_refusal']/48:.2%}); parse failures={classification_counts['parse_failure']}; explicit-refusal screen={classification_counts['explicit_refusal_screen']}; API errors={classification_counts['api_error']}; empty={classification_counts['empty_response']} | **{'PASS' if checks['structured_output_validity']['pass'] else 'FAIL'}** |",
        "",
        "## Boundary and pending human checks",
        "",
        "The table reports each prespecified machine criterion separately. It does **not** make the researcher's final Pilot pass/fail decision. The prespecified 12-record human review for material factual hallucination and T3 executed/verifiable-action comprehension remains pending.",
        "",
        "No treatment-effect ordering, expected direction, statistical significance, p-value, or minimum effect size was calculated or used as a criterion.",
        "",
        "The refusal count is a reproducible narrow machine screen using the regex stored in `machine_checks.json`; sampled responses still require human judgment under the preregistered definitions.",
    ]
    (DIAGNOSTIC_DIR / "machine_checks.md").write_text(
        "\n".join(report_lines) + "\n", encoding="utf-8"
    )

    packet = [
        "# Endpoint Pilot stratified manual-review packet",
        "",
        f"- Seed: `{SEED}`",
        "- Sampler: exact CPython 3.11 `random.sample` pool semantics for n=16, k=4; a fresh `random.Random(seed)` instance within each arm",
        f"- Source run: `{run_ids[0]}`",
        f"- Source SHA-256: `{sha256_file(raw_path)}`",
        "- Sampling order: within each arm sort P01-P16, then sample 4 once; sampled records were not replaced.",
        "",
        "The prompt and response below are copied verbatim from the Pilot JSONL. Review content without using expected treatment ordering or significance.",
    ]
    for index, r in enumerate(selected, 1):
        packet.extend(
            [
                "",
                f"## {index}. {r['cell_id']}",
                "",
                f"- Arm: `{r['condition']}`; persona: `{r['persona_id']}`; raw JSONL line: `{r['_raw_line_number']}`",
                f"- Status: `{r['status']}`; parse success: `{str(r['parse_result']['success']).lower()}`; response ID: `{r['response_id']}`",
                f"- Recorded prompt SHA-256: `{r['prompt_sha256']}`",
                f"- Recomputed prompt SHA-256: `{sha256_text(r['prompt'])}`",
                f"- Raw-response SHA-256: `{sha256_text(r['raw_response'])}`",
                "",
                "### Original prompt",
                "",
                "```text",
                r["prompt"],
                "```",
                "",
                "### Original response",
                "",
                "```json",
                r["raw_response"],
                "```",
            ]
        )
    (REVIEW_DIR / "review_packet.md").write_text(
        "\n".join(packet) + "\n", encoding="utf-8"
    )

    checklist = [
        "# Endpoint Pilot manual-review checklist",
        "",
        f"Sample seed: `{SEED}`  ",
        f"Source run: `{run_ids[0]}`  ",
        "Evidence packet: `review_packet.md`",
        "",
        "For every sampled record, inspect the original prompt and response and select exactly one hallucination judgment. Add a short rationale. Do not infer a required treatment ordering.",
        "",
        "## A. Material factual hallucination (all 12)",
        "",
    ]
    for r in selected:
        checklist.extend(
            [
                f"### {r['cell_id']}",
                "",
                "- [ ] PASS — no materially hallucinated factual claim",
                "- [ ] FAIL — one or more materially hallucinated factual claims",
                "- Rationale:",
                "",
            ]
        )
    checklist.extend(
        [
            "## B. T3 executed/verifiable-action comprehension (sampled T3 only)",
            "",
            "For each sampled T3 response, check all three components and then select exactly one overall judgment.",
            "",
        ]
    )
    for r in (r for r in selected if r["condition"] == "T3"):
        checklist.extend(
            [
                f"### {r['cell_id']}",
                "",
                "- [ ] Consistent with the action being already executed",
                "- [ ] Consistent with public on-chain verifiability",
                "- [ ] Does not recast the reserve as compensation, increased yield, or a token-price guarantee",
                "- [ ] PASS — overall T3 comprehension",
                "- [ ] FAIL — overall T3 comprehension",
                "- Rationale:",
                "",
            ]
        )
    checklist.extend(
        [
            "## C. Researcher summary (complete after all judgments)",
            "",
            "- Hallucination passes: ____ / 12 (preregistered threshold: at least 11/12)",
            "- T3 comprehension passes: ____ / 4 (preregistered threshold: 4/4)",
            "- [ ] I confirmed that no sampled record was replaced.",
            "- [ ] I did not use effect direction, treatment ordering, significance, or preferred results as a pass condition.",
            "- Researcher name/initials:",
            "- Review date:",
            "- Final Pilot decision (researcher only; consider machine and human checks together):",
            "- Notes:",
            "",
            "This checklist intentionally does not pre-fill or sign any human judgment or final Pilot decision.",
        ]
    )
    (REVIEW_DIR / "manual_review_checklist.md").write_text(
        "\n".join(checklist) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
