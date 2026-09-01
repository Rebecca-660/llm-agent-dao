import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = (
    PROJECT_ROOT / "01_prompts" / "personas" / "persona_template_v1.0.txt"
)
PERSONAS_PATH = PROJECT_ROOT / "test_personas.csv"

PLACEHOLDER_COLUMNS = (
    "holding_tenure",
    "portfolio_exposure_percentage",
    "portfolio_exposure_usd",
    "governance_involvement",
    "prior_incident_experience",
)


def render_persona(template: str, persona: dict[str, str]) -> str:
    rendered = template
    for column in PLACEHOLDER_COLUMNS:
        rendered = rendered.replace("{" + column + "}", persona[column])
    return rendered


def render_all_personas() -> dict[str, str]:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    with PERSONAS_PATH.open(newline="", encoding="utf-8-sig") as csv_file:
        personas = csv.DictReader(csv_file)
        return {
            persona["persona_id"]: render_persona(template, persona)
            for persona in personas
        }


def format_persona_output(persona_id: str, rendered: str) -> str:
    if rendered.endswith("\n"):
        rendered = rendered[:-1]
    return f"===== {persona_id} =====\n{rendered}"


def main() -> None:
    rendered_personas = render_all_personas()
    output = "\n".join(
        format_persona_output(persona_id, rendered)
        for persona_id, rendered in rendered_personas.items()
    )
    print(output, end="")


if __name__ == "__main__":
    main()
