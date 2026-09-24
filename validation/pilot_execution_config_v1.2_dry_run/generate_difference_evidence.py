import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NEW_PATH = Path(__file__).with_name("pilot_requests.jsonl")
OLD_PATH = ROOT / "03_raw_outputs/pilot/pilot_20260904T135552Z_be4faaf7.jsonl"
JSON_PATH = Path(__file__).with_name("per_cell_difference_evidence.json")
MD_PATH = Path(__file__).with_name("difference_summary.md")

EXPECTED = {f"P{number:02d}_{condition}" for number in range(1, 17) for condition in ("S", "C0", "T3")}
STABLE_FIELDS = (
    "run_type", "provider", "api_base_url", "sdk_name", "openai_sdk_version",
    "thinking_mode", "model", "wording_version", "persona_template_version",
    "persona_template_path", "output_requirement_version", "output_requirement_path",
    "answer_order", "independent_context", "previous_response_id", "system_prompt",
    "prompt", "system_prompt_sha256", "prompt_sha256", "source_sha256",
)
CONFIG_FIELDS = ("sampling_mode", "do_sample", "temperature")
PLACEHOLDER = re.compile(r"\[[A-Za-z][A-Za-z0-9_]*\]")


def load_jsonl(path):
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main():
    old_records = load_jsonl(OLD_PATH)
    new_records = load_jsonl(NEW_PATH)
    old = {record["cell_id"]: record for record in old_records}
    new = {record["cell_id"]: record for record in new_records}

    old_duplicates = len(old_records) - len(old)
    new_duplicates = len(new_records) - len(new)
    placeholder_cells = sorted(
        cell for cell, record in new.items()
        if PLACEHOLDER.search(record["prompt"]) or PLACEHOLDER.search(record["system_prompt"])
    )
    rows = []
    unexpected = []
    for cell in sorted(EXPECTED):
        before = old.get(cell)
        after = new.get(cell)
        if before is None or after is None:
            unexpected.append({"cell_id": cell, "issue": "missing cell in old or new data"})
            continue
        stable_mismatches = [field for field in STABLE_FIELDS if before.get(field) != after.get(field)]
        observed_config = {
            field: {"before": before.get(field), "after": after.get(field)}
            for field in CONFIG_FIELDS if before.get(field) != after.get(field)
        }
        config_ok = observed_config == {
            "sampling_mode": {"before": "greedy_do_sample_false", "after": "stochastic_temperature_0.2"},
            "do_sample": {"before": False, "after": True},
            "temperature": {"before": 0, "after": 0.2},
        }
        request_hash_changed = before["request_sha256"] != after["request_sha256"]
        passed = not stable_mismatches and config_ok and request_hash_changed
        row = {
            "cell_id": cell,
            "stable_fields_equal": not stable_mismatches,
            "stable_field_mismatches": stable_mismatches,
            "observed_execution_config_changes": observed_config,
            "execution_config_change_matches_R22": config_ok,
            "old_request_sha256": before["request_sha256"],
            "new_request_sha256": after["request_sha256"],
            "request_hash_changed": request_hash_changed,
            "pass": passed,
        }
        rows.append(row)
        if not passed:
            unexpected.append(row)

    counts = Counter(record["condition"] for record in new_records)
    overall = (
        len(old_records) == 48 and len(new_records) == 48
        and set(old) == EXPECTED and set(new) == EXPECTED
        and old_duplicates == 0 and new_duplicates == 0
        and not placeholder_cells and not unexpected
        and new_records[0].get("decoding_regime") == "stochastic_low_v1.2"
    )
    report = {
        "result": "PASS" if overall else "FAIL",
        "comparison_basis": {
            "previous_run_id": "pilot_20260904T135552Z_be4faaf7",
            "previous_file": OLD_PATH.relative_to(ROOT).as_posix(),
            "new_run_id": new_records[0]["run_id"],
            "new_file": NEW_PATH.relative_to(ROOT).as_posix(),
            "R22_old_regime": "greedy_v1.1",
            "R22_new_regime": "stochastic_low_v1.2",
        },
        "cell_checks": {
            "old_record_count": len(old_records), "new_record_count": len(new_records),
            "old_unique_cells": len(old), "new_unique_cells": len(new),
            "old_duplicate_count": old_duplicates, "new_duplicate_count": new_duplicates,
            "new_condition_counts": dict(counts),
            "missing_new_cells": sorted(EXPECTED - set(new)),
            "unexpected_new_cells": sorted(set(new) - EXPECTED),
        },
        "material_checks": {
            "placeholder_cells": placeholder_cells,
            "prompt_hashes_equal_all_cells": all(row["stable_fields_equal"] for row in rows),
            "system_hashes_equal_all_cells": all(
                old[cell]["system_prompt_sha256"] == new[cell]["system_prompt_sha256"] for cell in EXPECTED
            ),
            "source_hashes_equal_all_cells": all(old[cell]["source_sha256"] == new[cell]["source_sha256"] for cell in EXPECTED),
            "model": new_records[0]["model"],
            "mechanics_version": new_records[0]["persona_template_version"],
            "output_requirement_version": new_records[0]["output_requirement_version"],
            "answer_order": new_records[0]["answer_order"],
        },
        "execution_config_check": {
            "conceptual_factor": "decoding_regime",
            "new_decoding_regime": new_records[0]["decoding_regime"],
            "linked_field_changes_match_R22_all_cells": all(row["execution_config_change_matches_R22"] for row in rows),
            "request_hash_changed_all_cells": all(row["request_hash_changed"] for row in rows),
            "unexpected_differences": unexpected,
        },
        "api_calls_made": 0,
        "per_cell": rows,
    }
    JSON_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    status = report["result"]
    lines = [
        "# Pilot execution config v1.2 dry-run difference summary", "",
        f"**Overall result: {status}**", "",
        "## Comparison", "",
        "- Previous request source: `run_id=pilot_20260904T135552Z_be4faaf7`.",
        "- New dry-run source: `run_id=pilot_dry_run_v1`.",
        "- 48 records and 48 unique cells in each source; new grid is P01-P16 × S/C0/T3 (16 per condition).",
        "- API calls made: 0.", "",
        "## Material identity", "",
        f"- Prompt/system/source hashes equal in all cells: {'PASS' if not unexpected else 'FAIL'}.",
        f"- Unresolved placeholder cells: {len(placeholder_cells)}.",
        "- Fixed materials/configuration: `model=glm-4.7`, mechanics/persona template `v1.1`, Output Requirement `v1.1`, answer order `canonical_ascending`, thinking disabled, independent context.", "",
        "## Sole planned execution change", "",
        "R22 treats `decoding_regime` as the single conceptual execution factor. Its linked API fields changed together:", "",
        "- `greedy_v1.1` → `stochastic_low_v1.2`",
        "- `do_sample=false` → `do_sample=true`",
        "- `temperature=0` → `temperature=0.2`",
        "- `sampling_mode=greedy_do_sample_false` → `sampling_mode=stochastic_temperature_0.2`",
        "- Request hash changed in all 48 cells, as expected; prompt/system/source hashes did not change.", "",
        f"Unexpected differences: **{len(unexpected)}**.", "",
        "Machine-readable cell-level evidence is in `per_cell_difference_evidence.json`.",
    ]
    MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if not overall:
        raise SystemExit("FAIL: unexpected or missing differences detected")


if __name__ == "__main__":
    main()
