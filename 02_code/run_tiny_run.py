import csv
import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from openai import OpenAI

from parser import parse_response
from persona_renderer import render_persona
from prompt_assembler import assemble_prompt


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PERSONAS_PATH = PROJECT_ROOT / "test_personas.csv"
SYSTEM_PROMPT_PATH = (
    PROJECT_ROOT / "01_prompts" / "system" / "system_prompt_v1.0.txt"
)
OUTPUT_DIRECTORY = PROJECT_ROOT / "03_raw_outputs" / "tiny_run"

PERSONA_IDS = ("P01", "P02", "P03", "P04")
CONDITIONS = ("S", "C0", "T3")
TEMPERATURE = 0


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as output_file:
        output_file.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_test_personas() -> dict[str, dict[str, str]]:
    with PERSONAS_PATH.open(newline="", encoding="utf-8-sig") as csv_file:
        rows = list(csv.DictReader(csv_file))

    personas = {row["persona_id"]: row for row in rows}
    missing = set(PERSONA_IDS).difference(personas)
    extra = set(personas).difference(PERSONA_IDS)
    if missing or extra or len(rows) != len(PERSONA_IDS):
        raise ValueError(
            "test_personas.csv must contain exactly P01, P02, P03, and P04 "
            f"once each; missing={sorted(missing)}, extra={sorted(extra)}."
        )
    return personas


def require_environment_variable(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Required environment variable {name} is not set.")
    return value


def main() -> int:
    require_environment_variable("OPENAI_API_KEY")
    model = require_environment_variable("OPENAI_MODEL")

    personas = load_test_personas()
    system_prompt = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    system_prompt_hash = sha256_text(system_prompt)

    run_id = f"tiny_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}_{uuid.uuid4().hex[:8]}"
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIRECTORY / f"{run_id}.jsonl"

    client = OpenAI()
    expected_cells = [
        (persona_id, condition)
        for persona_id in PERSONA_IDS
        for condition in CONDITIONS
    ]
    seen_cells: set[tuple[str, str]] = set()
    successful_calls = 0
    parsed_calls = 0

    print(f"Run ID: {run_id}")
    print(f"Model: {model}")
    print(f"Output: {output_path}")
    print(f"Planned calls: {len(expected_cells)}")

    for index, (persona_id, condition) in enumerate(expected_cells, start=1):
        cell = (persona_id, condition)
        if cell in seen_cells:
            raise RuntimeError(f"Duplicate cell encountered before API call: {cell}")
        seen_cells.add(cell)

        persona = personas[persona_id]
        assembled_template = assemble_prompt(persona, condition)
        prompt = render_persona(assembled_template, persona)
        prompt_hash = sha256_text(prompt)
        started_at = utc_timestamp()

        print(
            f"[{index:02d}/{len(expected_cells)}] "
            f"Calling {persona_id} × {condition}...",
            flush=True,
        )

        base_record: dict[str, Any] = {
            "run_id": run_id,
            "run_type": "tiny_run",
            "cell_id": f"{persona_id}_{condition}",
            "persona_id": persona_id,
            "condition": condition,
            "model": model,
            "temperature": TEMPERATURE,
            "timestamp": started_at,
            "prompt_sha256": prompt_hash,
            "system_prompt_sha256": system_prompt_hash,
        }

        try:
            response = client.responses.create(
                model=model,
                instructions=system_prompt,
                input=prompt,
                temperature=TEMPERATURE,
            )
            completed_at = utc_timestamp()
            raw_response_text = response.output_text
            parse_result = parse_response(raw_response_text)

            record = {
                **base_record,
                "completed_at": completed_at,
                "status": "success",
                "response_id": response.id,
                "model_version": response.model,
                "raw_response": raw_response_text,
                "raw_api_response": response.model_dump(mode="json"),
                "parse_result": parse_result,
                "error": None,
            }
            successful_calls += 1
            if parse_result["success"]:
                parsed_calls += 1
                print("  saved; JSON parsed successfully", flush=True)
            else:
                print(
                    f"  saved; parse failed: {parse_result['error']}",
                    flush=True,
                )
        except Exception as error:
            record = {
                **base_record,
                "completed_at": utc_timestamp(),
                "status": "api_error",
                "response_id": None,
                "model_version": None,
                "raw_response": None,
                "raw_api_response": None,
                "parse_result": None,
                "error": {
                    "type": type(error).__name__,
                    "message": str(error),
                },
            }
            print(f"  saved API error: {type(error).__name__}: {error}", flush=True)

        append_jsonl(output_path, record)

    missing_cells = set(expected_cells).difference(seen_cells)
    duplicate_or_missing = len(seen_cells) != len(expected_cells) or bool(missing_cells)

    print("\nTiny-run summary")
    print(f"Attempted cells: {len(seen_cells)}/{len(expected_cells)}")
    print(f"Successful API calls: {successful_calls}/{len(expected_cells)}")
    print(f"Successfully parsed responses: {parsed_calls}/{len(expected_cells)}")
    print(f"Duplicate or missing cells: {duplicate_or_missing}")
    print(f"Results saved to: {output_path}")

    all_checks_passed = (
        successful_calls == len(expected_cells)
        and parsed_calls == len(expected_cells)
        and not duplicate_or_missing
    )
    if all_checks_passed:
        print("Tiny technical run completed successfully.")
        return 0

    print("Tiny technical run completed with errors; inspect the JSONL records.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
