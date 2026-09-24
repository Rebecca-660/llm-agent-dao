import argparse
import json
import sys
import time
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import run_endpoint_pilot as shared
from parser import parse_response
from persona_renderer import render_persona
from prompt_assembler import (
    TREATMENT_PATHS,
    assemble_prompt,
    get_output_requirement_path,
    get_persona_template_path,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
FREEZE_PATH = PROJECT_ROOT / "00_protocol" / "formal_material_freeze_v1.2.md"
MAIN_RUNNER_PATH = Path(__file__).resolve()
DEFAULT_DRY_RUN_DIRECTORY = PROJECT_ROOT / "validation" / "main_run_v1.2_dry_run"
RAW_OUTPUT_DIRECTORY = PROJECT_ROOT / "03_raw_outputs" / "main"
LOG_OUTPUT_DIRECTORY = PROJECT_ROOT / "08_logs" / "main"

PERSONA_IDS = tuple(f"P{number:02d}" for number in range(1, 17))
CONDITIONS = ("S", "C0", "T1", "T2", "T3")
RUN_TYPE = "main"
DRY_RUN_ID = "main_dry_run_v1.2"
FROZEN_PROVIDER = "zhipu"
FROZEN_MODEL = "glm-4.7"
FROZEN_DECODING_REGIME = "stochastic_low_v1.2"
FROZEN_PERSONA_TEMPLATE_VERSION = "v1.1"
FROZEN_OUTPUT_REQUIREMENT_VERSION = "v1.1"
FROZEN_ANSWER_ORDER = "canonical_ascending"

MAX_ATTEMPTS = shared.MAX_ATTEMPTS
RETRY_DELAYS_SECONDS = shared.RETRY_DELAYS_SECONDS
UNRESOLVED_PLACEHOLDER_PATTERN = shared.UNRESOLVED_PLACEHOLDER_PATTERN
CANONICAL_OPTION_ORDER = shared.CANONICAL_OPTION_ORDER

FROZEN_FILE_PATHS = (
    "00_protocol/protocol_name_decision.md",
    "01_prompts/personas/personas_v1.0.csv",
    "01_prompts/personas/persona_template_v1.1.txt",
    "01_prompts/system/system_prompt_v1.0.txt",
    "01_prompts/common_shock/common_shock_v1.0.txt",
    "01_prompts/treatments/S_v1.0.txt",
    "01_prompts/treatments/C0_v1.0.txt",
    "01_prompts/treatments/T1_v1.0.txt",
    "01_prompts/treatments/T2_v1.0.txt",
    "01_prompts/treatments/T3_v1.0.txt",
    "01_prompts/outcome/outcome_question_v1.0.txt",
    "01_prompts/output_schema/json_schema_v1.1.txt",
    "02_code/prompt_assembler.py",
    "02_code/parser.py",
    "02_code/run_endpoint_pilot.py",
    "02_code/run_main_run.py",
)


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def extract_frozen_hashes(freeze_path: Path = FREEZE_PATH) -> dict[str, str]:
    text = freeze_path.read_text(encoding="utf-8")
    hashes: dict[str, str] = {}
    for relative in FROZEN_FILE_PATHS:
        matching_lines = [line for line in text.splitlines() if f"`{relative}`" in line]
        values = []
        for line in matching_lines:
            values.extend(
                token.strip("`")
                for token in line.split()
                if len(token.strip("`|")) == 64
                and all(char in "0123456789abcdef" for char in token.strip("`|"))
            )
        normalized = [value.strip("`|") for value in values]
        if len(set(normalized)) != 1:
            raise ValueError(f"Freeze must contain exactly one SHA-256 for {relative}.")
        hashes[relative] = normalized[0]
    return hashes


def verify_frozen_hashes(freeze_path: Path = FREEZE_PATH) -> dict[str, str]:
    expected = extract_frozen_hashes(freeze_path)
    mismatches = []
    for relative, frozen_hash in expected.items():
        actual_hash = shared.sha256_file(PROJECT_ROOT / relative)
        if actual_hash != frozen_hash:
            mismatches.append(f"{relative}: expected {frozen_hash}, found {actual_hash}")
    if mismatches:
        raise RuntimeError("Frozen file hash mismatch: " + "; ".join(mismatches))
    return expected


def validate_frozen_selection(
    *, provider: str, model: str, decoding_regime: str,
    persona_template_version: str, output_requirement_version: str,
    answer_order: str,
) -> None:
    actual = {
        "provider": provider,
        "model": model,
        "decoding_regime": decoding_regime,
        "persona_template_version": persona_template_version,
        "output_requirement_version": output_requirement_version,
        "answer_order": answer_order,
    }
    frozen = {
        "provider": FROZEN_PROVIDER,
        "model": FROZEN_MODEL,
        "decoding_regime": FROZEN_DECODING_REGIME,
        "persona_template_version": FROZEN_PERSONA_TEMPLATE_VERSION,
        "output_requirement_version": FROZEN_OUTPUT_REQUIREMENT_VERSION,
        "answer_order": FROZEN_ANSWER_ORDER,
    }
    if actual != frozen:
        raise ValueError(f"Main-run selection must match freeze: {frozen!r}; found {actual!r}")


def build_main_request_records(
    *, provider: str = FROZEN_PROVIDER, model: str = FROZEN_MODEL,
    decoding_regime: str = FROZEN_DECODING_REGIME,
    persona_template_version: str = FROZEN_PERSONA_TEMPLATE_VERSION,
    output_requirement_version: str = FROZEN_OUTPUT_REQUIREMENT_VERSION,
    answer_order: str = FROZEN_ANSWER_ORDER,
) -> list[dict[str, Any]]:
    validate_frozen_selection(
        provider=provider, model=model, decoding_regime=decoding_regime,
        persona_template_version=persona_template_version,
        output_requirement_version=output_requirement_version,
        answer_order=answer_order,
    )
    frozen_hashes = verify_frozen_hashes()
    decoding = shared.decoding_configuration(decoding_regime, provider)
    personas = shared.load_pilot_personas()
    system_prompt = shared.SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    system_hash = shared.sha256_text(system_prompt)
    persona_path = get_persona_template_path(persona_template_version)
    output_path = get_output_requirement_path(output_requirement_version)
    generated_at = utc_timestamp()
    records = []
    for persona_id in PERSONA_IDS:
        persona = personas[persona_id]
        for condition in CONDITIONS:
            assembled = assemble_prompt(
                persona, condition,
                persona_template_version=persona_template_version,
                output_requirement_version=output_requirement_version,
            )
            prompt = render_persona(assembled, persona)
            unresolved = UNRESOLVED_PLACEHOLDER_PATTERN.findall(prompt)
            if unresolved:
                raise ValueError(f"Unresolved placeholders in {persona_id}_{condition}: {unresolved}")
            if CANONICAL_OPTION_ORDER not in prompt:
                raise ValueError(f"Canonical answer order missing from {persona_id}_{condition}.")
            records.append({
                "run_id": DRY_RUN_ID,
                "run_type": RUN_TYPE,
                "run_mode": "dry_run",
                "cell_id": f"{persona_id}_{condition}",
                "persona_id": persona_id,
                "condition": condition,
                "provider": provider,
                "api_base_url": shared.provider_base_url(provider),
                "sdk_name": "openai",
                "openai_sdk_version": shared.OPENAI_SDK_VERSION,
                "decoding_regime": decoding_regime,
                "sampling_mode": decoding["sampling_mode"],
                "do_sample": decoding["do_sample"],
                "thinking_mode": shared.ZHIPU_THINKING_MODE,
                "model": model,
                "temperature": decoding["temperature"],
                "generated_at": generated_at,
                "wording_version": "canonical_v1.0",
                "persona_template_version": persona_template_version,
                "persona_template_path": shared.relative_path(persona_path),
                "output_requirement_version": output_requirement_version,
                "output_requirement_path": shared.relative_path(output_path),
                "answer_order": answer_order,
                "independent_context": True,
                "previous_response_id": None,
                "system_prompt": system_prompt,
                "prompt": prompt,
                "system_prompt_sha256": system_hash,
                "prompt_sha256": shared.sha256_text(prompt),
                "request_sha256": shared.request_sha256(
                    provider=provider, model=model, system_prompt=system_prompt,
                    prompt=prompt, decoding_regime=decoding_regime,
                ),
                "source_sha256": shared.source_hashes(
                    condition, output_requirement_version, persona_template_version
                ),
                "freeze_record_path": shared.relative_path(FREEZE_PATH),
                "freeze_record_sha256": shared.sha256_file(FREEZE_PATH),
                "main_runner_path": shared.relative_path(MAIN_RUNNER_PATH),
                "main_runner_sha256": shared.sha256_file(MAIN_RUNNER_PATH),
                "verified_frozen_sha256": frozen_hashes,
            })
    validate_main_records(records)
    return records


def validate_main_records(records: list[dict[str, Any]]) -> None:
    expected = {f"{persona}_{condition}" for persona in PERSONA_IDS for condition in CONDITIONS}
    cells = [record.get("cell_id") for record in records]
    if len(cells) != 80 or set(cells) != expected or len(cells) != len(set(cells)):
        raise ValueError("Main run must contain exactly the 80 unique expected cells.")
    if Counter(record["condition"] for record in records) != Counter({arm: 16 for arm in CONDITIONS}):
        raise ValueError("Each main-run arm must contain exactly 16 cells.")
    if any(record.get("run_type") != RUN_TYPE for record in records):
        raise ValueError("Every main-run request must use run_type=main.")
    if any(not record.get("independent_context") or record.get("previous_response_id") is not None for record in records):
        raise ValueError("Every main-run cell must use an independent context.")


def write_dry_run(records: list[dict[str, Any]], output_directory: Path) -> tuple[Path, Path]:
    validate_main_records(records)
    output_directory.mkdir(parents=True, exist_ok=False)
    request_path = output_directory / "main_requests.jsonl"
    summary_path = output_directory / "summary.json"
    with request_path.open("x", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    summary = {
        "run_id": DRY_RUN_ID, "run_type": RUN_TYPE, "run_mode": "dry_run",
        "api_calls_made": 0, "record_count": len(records),
        "unique_cell_count": len({record["cell_id"] for record in records}),
        "persona_count": len({record["persona_id"] for record in records}),
        "condition_counts": dict(Counter(record["condition"] for record in records)),
        "provider": records[0]["provider"], "model": records[0]["model"],
        "decoding_regime": records[0]["decoding_regime"],
        "do_sample": records[0]["do_sample"], "temperature": records[0]["temperature"],
        "thinking_mode": records[0]["thinking_mode"],
        "persona_template_version": records[0]["persona_template_version"],
        "output_requirement_version": records[0]["output_requirement_version"],
        "answer_order": records[0]["answer_order"],
        "all_independent_context": True,
        "freeze_record_sha256": records[0]["freeze_record_sha256"],
        "main_runner_sha256": records[0]["main_runner_sha256"],
    }
    with summary_path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    return request_path, summary_path


def create_execution_run_id() -> str:
    return f"main_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}_{uuid.uuid4().hex[:8]}"


def prepare_execution_paths(
    run_id: str, raw_output_directory: Path = RAW_OUTPUT_DIRECTORY,
    log_output_directory: Path = LOG_OUTPUT_DIRECTORY,
) -> tuple[Path, Path]:
    if not run_id.startswith("main_") or "pilot" in run_id.lower():
        raise ValueError("Main execution requires a new main_ run ID.")
    raw_output_directory.mkdir(parents=True, exist_ok=True)
    log_output_directory.mkdir(parents=True, exist_ok=True)
    raw_path = raw_output_directory / f"{run_id}.jsonl"
    log_path = log_output_directory / f"{run_id}_attempts.jsonl"
    with raw_path.open("x", encoding="utf-8"):
        pass
    try:
        with log_path.open("x", encoding="utf-8"):
            pass
    except Exception:
        raw_path.unlink(missing_ok=True)
        raise
    return raw_path, log_path


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def is_transient_error(error: Exception) -> bool:
    return shared.is_transient_error(error)


def execute_main(
    request_records: list[dict[str, Any]], *, client: Any, run_id: str,
    raw_path: Path, attempt_log_path: Path, sleep_fn: Any = time.sleep,
) -> list[dict[str, Any]]:
    validate_main_records(request_records)
    if not run_id.startswith("main_") or "pilot" in run_id.lower():
        raise ValueError("Main execution requires a new main_ run ID.")
    final_records = []
    for request in request_records:
        cell_started_at = utc_timestamp()
        final = None
        for attempt in range(1, MAX_ATTEMPTS + 1):
            started_at = utc_timestamp()
            try:
                response, raw_text = shared.send_model_request(client, request)
                completed_at = utc_timestamp()
                parsed = parse_response(raw_text)
                append_jsonl(attempt_log_path, {
                    "run_id": run_id, "run_type": RUN_TYPE,
                    "provider": request["provider"], "cell_id": request["cell_id"],
                    "attempt": attempt, "started_at": started_at,
                    "completed_at": completed_at, "status": "response_received",
                    "transient_error": False, "retry_scheduled": False,
                    "retry_delay_seconds": None, "response_id": response.id,
                    "model_version": response.model, "error": None,
                })
                final = {
                    **request, "run_id": run_id, "run_type": RUN_TYPE,
                    "run_mode": "execute", "cell_started_at": cell_started_at,
                    "completed_at": completed_at, "status": "success",
                    "attempt_count": attempt, "response_id": response.id,
                    "model_version": response.model, "raw_response": raw_text,
                    "raw_api_response": response.model_dump(mode="json"),
                    "parse_result": parsed, "error": None,
                }
                break
            except Exception as error:
                completed_at = utc_timestamp()
                transient = is_transient_error(error)
                retry = transient and attempt < MAX_ATTEMPTS
                delay = RETRY_DELAYS_SECONDS[attempt - 1] if retry else None
                serialized = shared.error_record(error)
                append_jsonl(attempt_log_path, {
                    "run_id": run_id, "run_type": RUN_TYPE,
                    "provider": request["provider"], "cell_id": request["cell_id"],
                    "attempt": attempt, "started_at": started_at,
                    "completed_at": completed_at, "status": "api_error",
                    "transient_error": transient, "retry_scheduled": retry,
                    "retry_delay_seconds": delay, "response_id": None,
                    "model_version": None, "error": serialized,
                })
                if retry:
                    sleep_fn(delay)
                    continue
                final = {
                    **request, "run_id": run_id, "run_type": RUN_TYPE,
                    "run_mode": "execute", "cell_started_at": cell_started_at,
                    "completed_at": completed_at, "status": "api_error",
                    "attempt_count": attempt, "response_id": None,
                    "model_version": None, "raw_response": None,
                    "raw_api_response": None, "parse_result": None,
                    "error": serialized,
                }
                break
        if final is None:
            raise RuntimeError(f"No final record for {request['cell_id']}.")
        append_jsonl(raw_path, final)
        final_records.append(final)
    return final_records


def create_api_client() -> Any:
    return shared.create_api_client(FROZEN_PROVIDER)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Frozen 80-cell minimum-scope main-run runner.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--provider", required=True, choices=(FROZEN_PROVIDER,))
    parser.add_argument("--model", required=True, choices=(FROZEN_MODEL,))
    parser.add_argument("--decoding-regime", required=True, choices=(FROZEN_DECODING_REGIME,))
    parser.add_argument("--persona-template-version", required=True, choices=(FROZEN_PERSONA_TEMPLATE_VERSION,))
    parser.add_argument("--output-requirement-version", required=True, choices=(FROZEN_OUTPUT_REQUIREMENT_VERSION,))
    parser.add_argument("--answer-order", required=True, choices=(FROZEN_ANSWER_ORDER,))
    parser.add_argument("--output-directory", type=Path, default=DEFAULT_DRY_RUN_DIRECTORY)
    parser.add_argument("--raw-output-directory", type=Path, default=RAW_OUTPUT_DIRECTORY)
    parser.add_argument("--log-output-directory", type=Path, default=LOG_OUTPUT_DIRECTORY)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    records = build_main_request_records(
        provider=args.provider, model=args.model,
        decoding_regime=args.decoding_regime,
        persona_template_version=args.persona_template_version,
        output_requirement_version=args.output_requirement_version,
        answer_order=args.answer_order,
    )
    if args.dry_run:
        requests_path, summary_path = write_dry_run(records, args.output_directory)
        print(f"Generated {len(records)} dry-run main requests.")
        print(f"Requests: {requests_path}")
        print(f"Summary: {summary_path}")
        print("API calls made: 0")
        return 0
    client = create_api_client()
    run_id = create_execution_run_id()
    raw_path, log_path = prepare_execution_paths(
        run_id, args.raw_output_directory, args.log_output_directory
    )
    final = execute_main(
        records, client=client, run_id=run_id, raw_path=raw_path,
        attempt_log_path=log_path,
    )
    api_successes = sum(record["status"] == "success" for record in final)
    parse_successes = sum(bool(record["parse_result"] and record["parse_result"]["success"]) for record in final)
    print(f"Run ID: {run_id}")
    print(f"Recorded cells: {len(final)}/80")
    print(f"API successes: {api_successes}/80")
    print(f"Parse successes: {parse_successes}/80")
    print(f"Raw output: {raw_path}")
    print(f"Attempt log: {log_path}")
    return 0 if len(final) == 80 else 1


if __name__ == "__main__":
    sys.exit(main())
