import csv
import itertools
import re
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PERSONA_GRID_PATH = (
    PROJECT_ROOT / "01_prompts" / "personas" / "personas_v1.0.csv"
)
PERSONA_TEMPLATE_PATH = (
    PROJECT_ROOT / "01_prompts" / "personas" / "persona_template_v1.0.txt"
)
TEST_PERSONAS_PATH = PROJECT_ROOT / "test_personas.csv"

DIMENSION_COLUMNS = (
    "holding_tenure",
    "portfolio_exposure_percentage",
    "governance_involvement",
    "prior_incident_experience",
)
LEVELS = {
    "holding_tenure": {"6 months", "2 years"},
    "portfolio_exposure_percentage": {"10%", "50%"},
    "governance_involvement": {"Passive holder", "Active voter"},
    "prior_incident_experience": {
        "No prior experience",
        "Previously experienced one",
    },
}
EXPOSURE_USD = {"10%": "$80,000", "50%": "$16,000"}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader.fieldnames or ()), list(reader)


def dimension_tuple(row: dict[str, str]) -> tuple[str, ...]:
    return tuple(row[column] for column in DIMENSION_COLUMNS)


def test_grid_schema_matches_canonical_template_placeholders() -> None:
    fieldnames, _ = read_csv(PERSONA_GRID_PATH)
    template = PERSONA_TEMPLATE_PATH.read_text(encoding="utf-8")
    placeholders = set(re.findall(r"\{([A-Za-z][A-Za-z0-9_]*)\}", template))

    assert set(fieldnames) == {"persona_id", *placeholders}
    assert len(fieldnames) == len(set(fieldnames))


def test_grid_is_complete_balanced_cartesian_product() -> None:
    _, rows = read_csv(PERSONA_GRID_PATH)

    assert len(rows) == 16
    assert len({row["persona_id"] for row in rows}) == 16
    assert {row["persona_id"] for row in rows} == {
        f"P{number:02d}" for number in range(1, 17)
    }

    actual_combinations = {dimension_tuple(row) for row in rows}
    expected_combinations = set(
        itertools.product(*(LEVELS[column] for column in DIMENSION_COLUMNS))
    )
    assert len(actual_combinations) == 16
    assert actual_combinations == expected_combinations

    for column, levels in LEVELS.items():
        assert Counter(row[column] for row in rows) == Counter(
            {level: 8 for level in levels}
        )


def test_portfolio_percentage_has_fixed_usd_mapping() -> None:
    _, rows = read_csv(PERSONA_GRID_PATH)

    for row in rows:
        assert row["portfolio_exposure_usd"] == EXPOSURE_USD[
            row["portfolio_exposure_percentage"]
        ]


def test_existing_test_persona_ids_keep_their_original_profiles() -> None:
    _, grid_rows = read_csv(PERSONA_GRID_PATH)
    _, test_rows = read_csv(TEST_PERSONAS_PATH)
    grid_by_id = {row["persona_id"]: row for row in grid_rows}

    for test_row in test_rows:
        assert grid_by_id[test_row["persona_id"]] == test_row
