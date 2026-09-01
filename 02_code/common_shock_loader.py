from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
COMMON_SHOCK_PATH = (
    PROJECT_ROOT / "01_prompts" / "common_shock" / "common_shock_v1.0.txt"
)


def load_common_shock() -> str:
    return COMMON_SHOCK_PATH.read_text(encoding="utf-8")
