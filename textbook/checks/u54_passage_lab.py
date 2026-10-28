"""Reproduce the passage teaching lab; AuthorityEffect: None."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from textbook.change_lab.run_lab import check_recorded  # noqa: E402

if __name__ == "__main__":
    print(check_recorded())
