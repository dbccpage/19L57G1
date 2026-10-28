"""First-steps finite correspondence check; AuthorityEffect: None."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from textbook.first_steps.checks import check  # noqa: E402

if __name__ == "__main__":
    print(check())
