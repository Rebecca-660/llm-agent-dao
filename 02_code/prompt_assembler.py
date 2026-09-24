from collections.abc import Mapping
from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_ROOT = PROJECT_ROOT / "01_prompts"
PROTOCOL_NAME_DECISION_PATH = (
    PROJECT_ROOT / "00_protocol" / "protocol_name_decision.md"
)

PROTOCOL_NAME_PLACEHOLDER = "[ProtocolName]"
FINAL_NAME_PATTERN = re.compile(
    r"^- Final experimental name:\s*`([^`]+)`\s*$", re.MULTILINE
)
UNRESOLVED_BRACKET_PLACEHOLDER_PATTERN = re.compile(
    r"\[[A-Za-z][A-Za-z0-9_]*\]"
)

PERSONA_TEMPLATE_PATHS = {
    version: PROMPTS_ROOT / "personas" / f"persona_template_{version}.txt"
    for version in ("v1.0", "v1.1")
}
DEFAULT_PERSONA_TEMPLATE_VERSION = "v1.0"
# Backward-compatible alias for callers reproducing pre-v1.1 requests.
PERSONA_TEMPLATE_PATH = PERSONA_TEMPLATE_PATHS[
    DEFAULT_PERSONA_TEMPLATE_VERSION
]
COMMON_SHOCK_PATH = PROMPTS_ROOT / "common_shock" / "common_shock_v1.0.txt"
TREATMENTS_ROOT = PROMPTS_ROOT / "treatments"
OUTCOME_QUESTION_PATH = PROMPTS_ROOT / "outcome" / "outcome_question_v1.0.txt"
OUTPUT_REQUIREMENT_PATHS = {
    version: PROMPTS_ROOT / "output_schema" / f"json_schema_{version}.txt"
    for version in ("v1.0", "v1.1")
}
DEFAULT_OUTPUT_REQUIREMENT_VERSION = "v1.0"
# Backward-compatible alias for callers reproducing pre-v1.1 requests.
OUTPUT_REQUIREMENT_PATH = OUTPUT_REQUIREMENT_PATHS[
    DEFAULT_OUTPUT_REQUIREMENT_VERSION
]

TREATMENT_PATHS = {
    condition_id: TREATMENTS_ROOT / f"{condition_id}_v1.0.txt"
    for condition_id in ("S", "C0", "T1", "T2", "T3")
}

PERSONA_COLUMNS = {
    "persona_id",
    "holding_tenure",
    "portfolio_exposure_percentage",
    "portfolio_exposure_usd",
    "governance_involvement",
    "prior_incident_experience",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def get_output_requirement_path(version: str) -> Path:
    try:
        return OUTPUT_REQUIREMENT_PATHS[version]
    except KeyError as error:
        allowed = ", ".join(OUTPUT_REQUIREMENT_PATHS)
        raise ValueError(
            f"Unknown output requirement version {version!r}; "
            f"expected one of: {allowed}"
        ) from error


def get_persona_template_path(version: str) -> Path:
    try:
        return PERSONA_TEMPLATE_PATHS[version]
    except KeyError as error:
        allowed = ", ".join(PERSONA_TEMPLATE_PATHS)
        raise ValueError(
            f"Unknown persona template version {version!r}; "
            f"expected one of: {allowed}"
        ) from error


def load_final_protocol_name(
    decision_path: Path = PROTOCOL_NAME_DECISION_PATH,
) -> str:
    decision_text = read_text(decision_path)
    matches = FINAL_NAME_PATTERN.findall(decision_text)
    if len(matches) != 1:
        raise ValueError(
            "Protocol name decision must contain exactly one "
            "'- Final experimental name: `<name>`' entry."
        )

    protocol_name = matches[0].strip()
    if not protocol_name:
        raise ValueError("Final protocol name must not be empty.")
    return protocol_name


def substitute_protocol_name(template: str, protocol_name: str) -> str:
    rendered = template.replace(PROTOCOL_NAME_PLACEHOLDER, protocol_name)
    unresolved = sorted(
        set(UNRESOLVED_BRACKET_PLACEHOLDER_PATTERN.findall(rendered))
    )
    if unresolved:
        raise ValueError(
            "Unresolved bracket placeholder(s): " + ", ".join(unresolved)
        )
    return rendered


def assemble_prompt(
    persona_row: Mapping[str, str],
    condition_id: str,
    *,
    persona_template_version: str = DEFAULT_PERSONA_TEMPLATE_VERSION,
    output_requirement_version: str = DEFAULT_OUTPUT_REQUIREMENT_VERSION,
) -> str:
    missing_columns = PERSONA_COLUMNS.difference(persona_row)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing persona columns: {missing}")

    try:
        treatment_path = TREATMENT_PATHS[condition_id]
    except KeyError as error:
        allowed = ", ".join(TREATMENT_PATHS)
        raise ValueError(
            f"Unknown treatment condition {condition_id!r}; expected one of: {allowed}"
        ) from error

    output_requirement_path = get_output_requirement_path(
        output_requirement_version
    )
    persona_template_path = get_persona_template_path(
        persona_template_version
    )
    components = (
        read_text(persona_template_path),
        read_text(COMMON_SHOCK_PATH),
        read_text(treatment_path),
        read_text(OUTCOME_QUESTION_PATH),
        read_text(output_requirement_path),
    )
    assembled_template = "\n\n".join(components)
    return substitute_protocol_name(
        assembled_template, load_final_protocol_name()
    )
