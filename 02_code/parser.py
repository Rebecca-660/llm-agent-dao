import json
import re
from typing import Any


ALLOWED_UNSTAKE_PERCENTAGES = {0, 25, 50, 75, 100}
REQUIRED_FIELDS = {"unstake_percentage", "reason"}


def extract_fenced_json(raw_response: str) -> str:
    match = re.fullmatch(
        r"\s*```(?:json)?\s*(.*?)\s*```\s*",
        raw_response,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if match:
        return match.group(1)
    return raw_response


def parse_response(raw_response: str) -> dict[str, Any]:
    if isinstance(raw_response, str):
        raw_response = extract_fenced_json(raw_response)

    try:
        parsed = json.loads(raw_response)
    except (json.JSONDecodeError, TypeError) as error:
        return {
            "success": False,
            "data": None,
            "error": f"Invalid JSON: {error}",
        }

    if not isinstance(parsed, dict):
        return {
            "success": False,
            "data": None,
            "error": "The JSON response must be an object.",
        }

    missing_fields = REQUIRED_FIELDS.difference(parsed)
    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        return {
            "success": False,
            "data": None,
            "error": f"Missing required field(s): {missing}.",
        }

    unexpected_fields = set(parsed).difference(REQUIRED_FIELDS)
    if unexpected_fields:
        unexpected = ", ".join(sorted(unexpected_fields))
        return {
            "success": False,
            "data": None,
            "error": f"Unexpected field(s): {unexpected}. Exactly two fields are required.",
        }

    unstake_percentage = parsed["unstake_percentage"]
    if (
        isinstance(unstake_percentage, bool)
        or not isinstance(unstake_percentage, int)
        or unstake_percentage not in ALLOWED_UNSTAKE_PERCENTAGES
    ):
        return {
            "success": False,
            "data": None,
            "error": (
                '"unstake_percentage" must be exactly one of: '
                "0, 25, 50, 75, or 100."
            ),
        }

    reason = parsed["reason"]
    if not isinstance(reason, str) or not reason.strip():
        return {
            "success": False,
            "data": None,
            "error": '"reason" must be a non-empty string.',
        }

    return {
        "success": True,
        "data": {
            "unstake_percentage": unstake_percentage,
            "reason": reason,
        },
        "error": None,
    }
