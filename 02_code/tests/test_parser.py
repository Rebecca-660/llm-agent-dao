import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "02_code"))

from parser import parse_response


def test_markdown_code_fence_wrapping_json_is_accepted() -> None:
    raw_response = (
        "```json\n"
        '{"unstake_percentage": 50, "reason": "Risk remains uncertain."}\n'
        "```"
    )

    result = parse_response(raw_response)

    assert result["success"] is True
    assert result["data"] == {
        "unstake_percentage": 50,
        "reason": "Risk remains uncertain.",
    }


def test_invalid_unstake_value_30_is_rejected_with_allowed_values() -> None:
    raw_response = json.dumps(
        {"unstake_percentage": 30, "reason": "Risk remains uncertain."}
    )

    result = parse_response(raw_response)

    assert result["success"] is False
    assert "0, 25, 50, 75, or 100" in result["error"]


def test_extra_field_is_ignored_and_required_fields_are_extracted() -> None:
    raw_response = json.dumps(
        {
            "unstake_percentage": 50,
            "reason": "Risk remains uncertain.",
            "debug": "extra value",
        }
    )

    result = parse_response(raw_response)

    assert result["success"] is True
    assert result["data"] == {
        "unstake_percentage": 50,
        "reason": "Risk remains uncertain.",
    }


def test_missing_required_reason_field_is_rejected() -> None:
    raw_response = json.dumps({"unstake_percentage": 50})

    result = parse_response(raw_response)

    assert result["success"] is False
    assert result["error"]


def test_completely_non_json_refusal_is_rejected() -> None:
    result = parse_response("I cannot make this decision.")

    assert result["success"] is False
    assert result["error"]


def test_empty_reason_string_is_rejected() -> None:
    raw_response = json.dumps({"unstake_percentage": 50, "reason": ""})

    result = parse_response(raw_response)

    assert result["success"] is False
    assert result["error"]


def test_empty_api_response_is_rejected() -> None:
    for raw_response in ("", None):
        result = parse_response(raw_response)

        assert result["success"] is False
        assert result["error"]
