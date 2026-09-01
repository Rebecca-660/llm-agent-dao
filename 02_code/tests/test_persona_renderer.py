import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "02_code"))

from persona_renderer import format_persona_output, render_all_personas


def test_p01_matches_golden_file_exactly() -> None:
    golden_path = PROJECT_ROOT / "validation" / "golden_persona_P01.txt"
    expected = golden_path.read_text(encoding="utf-8")

    rendered_personas = render_all_personas()
    actual = format_persona_output("P01", rendered_personas["P01"])

    assert actual == expected
