from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TREATMENTS_DIR = PROJECT_ROOT / "01_prompts" / "treatments"


def read_treatment(condition_id: str) -> str:
    path = TREATMENTS_DIR / f"{condition_id}_v1.0.txt"
    return path.read_text(encoding="utf-8")


def test_treatments_are_strictly_nested() -> None:
    c0 = read_treatment("C0")
    t1 = read_treatment("T1")
    t2 = read_treatment("T2")
    t3 = read_treatment("T3")

    assert t1.startswith(c0)
    assert t2.startswith(t1)
    assert t3.startswith(t2)

    assert len(t1) > len(c0)
    assert len(t2) > len(t1)
    assert len(t3) > len(t2)
