import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from parser import parse_response
from run_endpoint_pilot import (
    PROJECT_ROOT,
    append_jsonl,
    build_dry_run_records,
    create_api_client,
    error_record,
    send_model_request,
    utc_timestamp,
)


RAW_DIRECTORY = PROJECT_ROOT / "03_raw_outputs" / "smoke"
LOG_DIRECTORY = PROJECT_ROOT / "08_logs" / "smoke"


def create_run_id() -> str:
    return (
        f"connectivity_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}_"
        f"{uuid.uuid4().hex[:8]}"
    )


def prepare_path(directory: Path, filename: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / filename
    with path.open("x", encoding="utf-8"):
        pass
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run exactly one isolated provider connectivity check."
    )
    parser.add_argument("--provider", required=True, choices=("openai", "zhipu"))
    parser.add_argument("--model", required=True)
    parser.add_argument(
        "--output-requirement-version", required=True, choices=("v1.0", "v1.1")
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    request = build_dry_run_records(
        args.model,
        args.output_requirement_version,
        provider=args.provider,
    )[0]
    if request["cell_id"] != "P01_S":
        raise RuntimeError("Connectivity check must use the fixed P01_S cell.")

    run_id = create_run_id()
    raw_path = prepare_path(RAW_DIRECTORY, f"{run_id}.jsonl")
    log_path = prepare_path(LOG_DIRECTORY, f"{run_id}_attempts.jsonl")
    started_at = utc_timestamp()
    client = create_api_client(args.provider)

    try:
        response, raw_text = send_model_request(client, request)
        completed_at = utc_timestamp()
        parse_result = parse_response(raw_text)
        attempt = {
            "run_id": run_id,
            "run_type": "connectivity_check",
            "provider": args.provider,
            "cell_id": request["cell_id"],
            "attempt": 1,
            "started_at": started_at,
            "completed_at": completed_at,
            "status": "response_received",
            "retry_scheduled": False,
            "response_id": response.id,
            "model_version": response.model,
            "error": None,
        }
        final = {
            **request,
            "run_id": run_id,
            "run_type": "connectivity_check",
            "run_mode": "execute",
            "cell_started_at": started_at,
            "completed_at": completed_at,
            "status": "success",
            "attempt_count": 1,
            "response_id": response.id,
            "model_version": response.model,
            "raw_response": raw_text,
            "raw_api_response": response.model_dump(mode="json"),
            "parse_result": parse_result,
            "error": None,
        }
        exit_code = 0
    except Exception as error:
        completed_at = utc_timestamp()
        serialized_error = error_record(error)
        attempt = {
            "run_id": run_id,
            "run_type": "connectivity_check",
            "provider": args.provider,
            "cell_id": request["cell_id"],
            "attempt": 1,
            "started_at": started_at,
            "completed_at": completed_at,
            "status": "api_error",
            "retry_scheduled": False,
            "response_id": None,
            "model_version": None,
            "error": serialized_error,
        }
        final = {
            **request,
            "run_id": run_id,
            "run_type": "connectivity_check",
            "run_mode": "execute",
            "cell_started_at": started_at,
            "completed_at": completed_at,
            "status": "api_error",
            "attempt_count": 1,
            "response_id": None,
            "model_version": None,
            "raw_response": None,
            "raw_api_response": None,
            "parse_result": None,
            "error": serialized_error,
        }
        exit_code = 1

    append_jsonl(log_path, attempt)
    append_jsonl(raw_path, final)
    print(
        json.dumps(
            {
                "run_id": run_id,
                "run_type": "connectivity_check",
                "provider": args.provider,
                "requested_model": args.model,
                "status": final["status"],
                "model_version": final["model_version"],
                "parse_success": bool(
                    final["parse_result"] and final["parse_result"]["success"]
                ),
                "raw_path": str(raw_path),
                "log_path": str(log_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
