import re
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "02_code"))

from prompt_assembler import (
    COMMON_SHOCK_PATH,
    OUTCOME_QUESTION_PATH,
    OUTPUT_REQUIREMENT_PATH,
    PERSONA_TEMPLATE_PATH,
    PROTOCOL_NAME_DECISION_PATH,
    PROTOCOL_NAME_PLACEHOLDER,
    TREATMENT_PATHS,
    assemble_prompt,
    load_final_protocol_name,
    read_text,
    substitute_protocol_name,
)


PERSONA_ROW = {
    "persona_id": "test-persona",
    "holding_tenure": "test-tenure",
    "portfolio_exposure_percentage": "test-percentage",
    "portfolio_exposure_usd": "test-value",
    "governance_involvement": "test-governance",
    "prior_incident_experience": "test-experience",
}


def raw_assembled_template(condition_id: str) -> str:
    components = (
        read_text(PERSONA_TEMPLATE_PATH),
        read_text(COMMON_SHOCK_PATH),
        read_text(TREATMENT_PATHS[condition_id]),
        read_text(OUTCOME_QUESTION_PATH),
        read_text(OUTPUT_REQUIREMENT_PATH),
    )
    return "\n\n".join(components)


def test_final_name_is_loaded_from_decision_record() -> None:
    protocol_name = load_final_protocol_name()
    decision_text = read_text(PROTOCOL_NAME_DECISION_PATH)

    assert protocol_name
    assert re.search(
        rf"^- Final experimental name:\s*`{re.escape(protocol_name)}`\s*$",
        decision_text,
        re.MULTILINE,
    )


@pytest.mark.parametrize("condition_id", tuple(TREATMENT_PATHS))
def test_assembly_only_replaces_protocol_name_placeholder(
    condition_id: str,
) -> None:
    raw_template = raw_assembled_template(condition_id)
    protocol_name = load_final_protocol_name()

    expected = raw_template.replace(PROTOCOL_NAME_PLACEHOLDER, protocol_name)
    actual = assemble_prompt(PERSONA_ROW, condition_id)

    assert PROTOCOL_NAME_PLACEHOLDER in raw_template
    assert actual == expected
    assert PROTOCOL_NAME_PLACEHOLDER not in actual


def test_unresolved_bracket_placeholder_is_rejected() -> None:
    protocol_name = load_final_protocol_name()
    template = f"{PROTOCOL_NAME_PLACEHOLDER}\n[OtherName]"

    with pytest.raises(ValueError, match=r"\[OtherName\]"):
        substitute_protocol_name(template, protocol_name)
