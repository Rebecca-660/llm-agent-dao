import argparse
import csv
import hashlib
import json
import re
import sys
import time
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from openai import (
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
    OpenAI,
    RateLimitError,
    __version__ as OPENAI_SDK_VERSION,
)

from parser import parse_response
from persona_renderer import render_persona
from prompt_assembler import (
    COMMON_SHOCK_PATH,
    OUTPUT_REQUIREMENT_PATHS,
    OUTCOME_QUESTION_PATH,
    PERSONA_COLUMNS,
    PERSONA_TEMPLATE_PATH,
    PROTOCOL_NAME_DECISION_PATH,
    TREATMENT_PATHS,
    assemble_prompt,
    get_output_requirement_path,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PERSONAS_PATH = PROJECT_ROOT / "01_prompts" / "personas" / "personas_v1.0.csv"
SYSTEM_PROMPT_PATH = (
    PROJECT_ROOT / "01_prompts" / "system" / "system_prompt_v1.0.txt"
)
DEFAULT_OUTPUT_DIRECTORY = PROJECT_ROOT / "validation" / "pilot_dry_run"
RAW_OUTPUT_DIRECTORY = PROJECT_ROOT / "03_raw_outputs" / "pilot"
LOG_OUTPUT_DIRECTORY = PROJECT_ROOT / "08_logs" / "pilot"

PERSONA_IDS = tuple(f"P{number:02d}" for number in range(1, 17))
CONDITIONS = ("S", "C0", "T3")
TEMPERATURE = 0
PROVIDER = "openai"
RUN_TYPE = "pilot"
RUN_MODE = "dry_run"
DRY_RUN_ID = "pilot_dry_run_v1"
MAX_ATTEMPTS = 3
RETRY_DELAYS_SECONDS = (1.0, 2.0)
TRANSIENT_ERROR_TYPES = (
    APIConnectionError,
    APITimeoutError,
    RateLimitError,
    InternalServerError,
)
CANONICAL_OPTION_ORDER = "0%, 25%, 50%, 75%, or 100%"
UNRESOLVED_PLACEHOLDER_PATTERN = re.compile(
    r"(?:\[[A-Za-z][A-Za-z0-9_]*\]|\{[A-Za-z][A-Za-z0-9_]*\})"
)


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def relative_path(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def load_pilot_personas(
    path: Path = PERSONAS_PATH,
) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = set(reader.fieldnames or ())
        rows = list(reader)

    if fieldnames != PERSONA_COLUMNS:
        raise ValueError(
            "Pilot persona columns do not match the canonical assembler columns."
        )

    personas = {row["persona_id"]: row for row in rows}
    if len(rows) != len(personas):
        raise ValueError("Pilot persona IDs must be unique.")
    if set(personas) != set(PERSONA_IDS):
        raise ValueError("Pilot personas must contain exactly P01 through P16.")
    return personas


def request_sha256(
    *, model: str, system_prompt: str, prompt: str
) -> str:
    request_payload = {
        "provider": PROVIDER,
        "model": model,
        "temperature": TEMPERATURE,
        "instructions": system_prompt,
        "input": prompt,
        "previous_response_id": None,
    }
    serialized = json.dumps(
        request_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return sha256_text(serialized)


def source_hashes(
    condition: str, output_requirement_version: str
) -> dict[str, str]:
    output_requirement_path = get_output_requirement_path(
        output_requirement_version
    )
    source_paths = (
        PROTOCOL_NAME_DECISION_PATH,
        PERSONAS_PATH,
        PERSONA_TEMPLATE_PATH,
        COMMON_SHOCK_PATH,
        TREATMENT_PATHS[condition],
        OUTCOME_QUESTION_PATH,
        output_requirement_path,
        SYSTEM_PROMPT_PATH,
    )
    return {relative_path(path): sha256_file(path) for path in source_paths}


def build_dry_run_records(
    model: str, output_requirement_version: str
) -> list[dict[str, Any]]:
    if not model.strip():
        raise ValueError("Model name must not be empty.")

    output_requirement_path = get_output_requirement_path(
        output_requirement_version
    )

    personas = load_pilot_personas()
    system_prompt = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    system_prompt_hash = sha256_text(system_prompt)
    generated_at = utc_timestamp()
    records: list[dict[str, Any]] = []

    for persona_id in PERSONA_IDS:
        persona = personas[persona_id]
        for condition in CONDITIONS:
            assembled_template = assemble_prompt(
                persona,
                condition,
                output_requirement_version=output_requirement_version,
            )
            prompt = render_persona(assembled_template, persona)
            unresolved = UNRESOLVED_PLACEHOLDER_PATTERN.findall(prompt)
            if unresolved:
                raise ValueError(
                    f"Unresolved placeholders in {persona_id}_{condition}: "
                    + ", ".join(sorted(set(unresolved)))
                )
            if CANONICAL_OPTION_ORDER not in prompt:
                raise ValueError(
                    f"Canonical answer order missing from {persona_id}_{condition}."
                )

            records.append(
                {
                    "run_id": DRY_RUN_ID,
                    "run_type": RUN_TYPE,
                    "run_mode": RUN_MODE,
                    "cell_id": f"{persona_id}_{condition}",
                    "persona_id": persona_id,
                    "condition": condition,
                    "provider": PROVIDER,
                    "openai_sdk_version": OPENAI_SDK_VERSION,
                    "model": model,
                    "temperature": TEMPERATURE,
                    "generated_at": generated_at,
                    "wording_version": "canonical_v1.0",
                    "output_requirement_version": output_requirement_version,
                    "output_requirement_path": relative_path(
                        output_requirement_path
                    ),
                    "answer_order": "canonical_ascending",
                    "independent_context": True,
                    "previous_response_id": None,
                    "system_prompt": system_prompt,
                    "prompt": prompt,
                    "system_prompt_sha256": system_prompt_hash,
                    "prompt_sha256": sha256_text(prompt),
                    "request_sha256": request_sha256(
                        model=model,
                        system_prompt=system_prompt,
                        prompt=prompt,
                    ),
                    "source_sha256": source_hashes(
                        condition, output_requirement_version
                    ),
                }
            )

    validate_records(records)
    return records


def validate_records(records: list[dict[str, Any]]) -> None:
    expected_cells = {
        f"{persona_id}_{condition}"
        for persona_id in PERSONA_IDS
        for condition in CONDITIONS
    }
    actual_cells = [record["cell_id"] for record in records]
    if len(actual_cells) != 48 or set(actual_cells) != expected_cells:
        raise ValueError("Dry run must contain exactly the expected 48 cells.")
    if len(actual_cells) != len(set(actual_cells)):
        raise ValueError("Dry run contains duplicate cells.")

    condition_counts = Counter(record["condition"] for record in records)
    if condition_counts != Counter({condition: 16 for condition in CONDITIONS}):
        raise ValueError("Each Pilot condition must contain exactly 16 cells.")


def write_dry_run(
    records: list[dict[str, Any]], output_directory: Path
) -> tuple[Path, Path]:
    output_directory.mkdir(parents=True, exist_ok=False)
    requests_path = output_directory / "pilot_requests.jsonl"
    summary_path = output_directory / "summary.json"

    with requests_path.open("x", encoding="utf-8", newline="\n") as output_file:
        for record in records:
            output_file.write(json.dumps(record, ensure_ascii=False) + "\n")

    summary = {
        "run_id": DRY_RUN_ID,
        "run_type": RUN_TYPE,
        "run_mode": RUN_MODE,
        "output_requirement_version": records[0][
            "output_requirement_version"
        ],
        "output_requirement_path": records[0]["output_requirement_path"],
        "api_calls_made": 0,
        "record_count": len(records),
        "unique_cell_count": len({record["cell_id"] for record in records}),
        "persona_count": len({record["persona_id"] for record in records}),
        "condition_counts": dict(
            Counter(record["condition"] for record in records)
        ),
        "all_independent_context": all(
            record["independent_context"]
            and record["previous_response_id"] is None
            for record in records
        ),
    }
    with summary_path.open("x", encoding="utf-8", newline="\n") as summary_file:
        summary_file.write(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
        )
    return requests_path, summary_path


def create_execution_run_id() -> str:
    return (
        f"pilot_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}_"
        f"{uuid.uuid4().hex[:8]}"
    )


def prepare_execution_paths(
    run_id: str,
    raw_output_directory: Path = RAW_OUTPUT_DIRECTORY,
    log_output_directory: Path = LOG_OUTPUT_DIRECTORY,
) -> tuple[Path, Path]:
    raw_output_directory.mkdir(parents=True, exist_ok=True)
    log_output_directory.mkdir(parents=True, exist_ok=True)
    raw_path = raw_output_directory / f"{run_id}.jsonl"
    attempt_log_path = log_output_directory / f"{run_id}_attempts.jsonl"

    # Exclusive creation prevents overwriting or silently resuming an old run.
    with raw_path.open("x", encoding="utf-8"):
        pass
    with attempt_log_path.open("x", encoding="utf-8"):
        pass
    return raw_path, attempt_log_path


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as output_file:
        output_file.write(json.dumps(record, ensure_ascii=False) + "\n")


def error_record(error: Exception) -> dict[str, str]:
    return {"type": type(error).__name__, "message": str(error)}


def is_transient_error(error: Exception) -> bool:
    return isinstance(error, TRANSIENT_ERROR_TYPES)


def execute_pilot(
    request_records: list[dict[str, Any]],
    *,
    client: Any,
    run_id: str,
    raw_path: Path,
    attempt_log_path: Path,
    sleep_fn: Any = time.sleep,
) -> list[dict[str, Any]]:
    validate_records(request_records)
    final_records: list[dict[str, Any]] = []

    for request_record in request_records:
        cell_started_at = utc_timestamp()
        final_record: dict[str, Any] | None = None

        for attempt in range(1, MAX_ATTEMPTS + 1):
            attempt_started_at = utc_timestamp()
            try:
                response = client.responses.create(
                    model=request_record["model"],
                    instructions=request_record["system_prompt"],
                    input=request_record["prompt"],
                    temperature=request_record["temperature"],
                    previous_response_id=None,
                )
                completed_at = utc_timestamp()
                raw_response_text = response.output_text
                parse_result = parse_response(raw_response_text)

                append_jsonl(
                    attempt_log_path,
                    {
                        "run_id": run_id,
                        "run_type": RUN_TYPE,
                        "cell_id": request_record["cell_id"],
                        "attempt": attempt,
                        "started_at": attempt_started_at,
                        "completed_at": completed_at,
                        "status": "response_received",
                        "transient_error": False,
                        "retry_scheduled": False,
                        "retry_delay_seconds": None,
                        "response_id": response.id,
                        "model_version": response.model,
                        "error": None,
                    },
                )
                final_record = {
                    **request_record,
                    "run_id": run_id,
                    "run_mode": "execute",
                    "cell_started_at": cell_started_at,
                    "completed_at": completed_at,
                    "status": "success",
                    "attempt_count": attempt,
                    "response_id": response.id,
                    "model_version": response.model,
                    "raw_response": raw_response_text,
                    "raw_api_response": response.model_dump(mode="json"),
                    "parse_result": parse_result,
                    "error": None,
                }
                # A received response is a completed model decision. Invalid
                # content is preserved and never retried for format repair.
                break
            except Exception as error:
                completed_at = utc_timestamp()
                transient = is_transient_error(error)
                retry_scheduled = transient and attempt < MAX_ATTEMPTS
                retry_delay = (
                    RETRY_DELAYS_SECONDS[attempt - 1]
                    if retry_scheduled
                    else None
                )
                serialized_error = error_record(error)
                append_jsonl(
                    attempt_log_path,
                    {
                        "run_id": run_id,
                        "run_type": RUN_TYPE,
                        "cell_id": request_record["cell_id"],
                        "attempt": attempt,
                        "started_at": attempt_started_at,
                        "completed_at": completed_at,
                        "status": "api_error",
                        "transient_error": transient,
                        "retry_scheduled": retry_scheduled,
                        "retry_delay_seconds": retry_delay,
                        "response_id": None,
                        "model_version": None,
                        "error": serialized_error,
                    },
                )

                if retry_scheduled:
                    sleep_fn(retry_delay)
                    continue

                final_record = {
                    **request_record,
                    "run_id": run_id,
                    "run_mode": "execute",
                    "cell_started_at": cell_started_at,
                    "completed_at": completed_at,
                    "status": "api_error",
                    "attempt_count": attempt,
                    "response_id": None,
                    "model_version": None,
                    "raw_response": None,
                    "raw_api_response": None,
                    "parse_result": None,
                    "error": serialized_error,
                }
                break

        if final_record is None:
            raise RuntimeError(
                f"No final record produced for {request_record['cell_id']}."
            )
        append_jsonl(raw_path, final_record)
        final_records.append(final_record)

    return final_records


def create_openai_client() -> OpenAI:
    # Disable SDK-level retries so every retry is controlled and logged here.
    return OpenAI(max_retries=0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the Endpoint Pilot request matrix without API calls."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--model", required=True)
    parser.add_argument(
        "--output-requirement-version",
        required=True,
        choices=tuple(OUTPUT_REQUIREMENT_PATHS),
        help=(
            "Explicit formal output-requirement version. "
            "Use v1.0 only to reproduce the first Pilot; use v1.1 for the rerun."
        ),
    )
    parser.add_argument(
        "--output-directory",
        type=Path,
        default=DEFAULT_OUTPUT_DIRECTORY,
    )
    parser.add_argument(
        "--raw-output-directory",
        type=Path,
        default=RAW_OUTPUT_DIRECTORY,
    )
    parser.add_argument(
        "--log-output-directory",
        type=Path,
        default=LOG_OUTPUT_DIRECTORY,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    records = build_dry_run_records(
        args.model, args.output_requirement_version
    )
    if args.dry_run:
        requests_path, summary_path = write_dry_run(
            records, args.output_directory
        )
        print(f"Generated {len(records)} dry-run Pilot requests.")
        print(f"Requests: {requests_path}")
        print(f"Summary: {summary_path}")
        print("API calls made: 0")
        return 0

    run_id = create_execution_run_id()
    raw_path, attempt_log_path = prepare_execution_paths(
        run_id,
        args.raw_output_directory,
        args.log_output_directory,
    )
    client = create_openai_client()
    final_records = execute_pilot(
        records,
        client=client,
        run_id=run_id,
        raw_path=raw_path,
        attempt_log_path=attempt_log_path,
    )
    api_successes = sum(
        record["status"] == "success" for record in final_records
    )
    parse_successes = sum(
        bool(record["parse_result"] and record["parse_result"]["success"])
        for record in final_records
    )
    print(f"Run ID: {run_id}")
    print(f"Recorded cells: {len(final_records)}/48")
    print(f"API successes: {api_successes}/48")
    print(f"Parse successes: {parse_successes}/48")
    print(f"Raw output: {raw_path}")
    print(f"Attempt log: {attempt_log_path}")
    return 0 if len(final_records) == 48 else 1


if __name__ == "__main__":
    sys.exit(main())
