from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTCOME_DIR = PROJECT_ROOT / "01_prompts" / "outcome"
CANONICAL_PATH = OUTCOME_DIR / "outcome_question_v1.0.txt"
REVERSE_PATH = OUTCOME_DIR / "outcome_order_reverse_v1.0.txt"

CANONICAL_OPTIONS = "0%, 25%, 50%, 75%, or 100%"
REVERSE_OPTIONS = "100%, 75%, 50%, 25%, or 0%"


def test_reverse_order_changes_only_the_option_sequence() -> None:
    canonical = CANONICAL_PATH.read_text(encoding="utf-8")
    reverse = REVERSE_PATH.read_text(encoding="utf-8")

    assert canonical.count(CANONICAL_OPTIONS) == 1
    assert REVERSE_OPTIONS not in canonical
    assert reverse == canonical.replace(CANONICAL_OPTIONS, REVERSE_OPTIONS)


def test_reverse_order_contains_each_allowed_option_once() -> None:
    reverse = REVERSE_PATH.read_text(encoding="utf-8")

    options = re.findall(r"(?<!\d)(?:100|75|50|25|0)%", reverse)
    assert options == ["100%", "75%", "50%", "25%", "0%"]
