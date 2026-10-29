"""Source-backed path/cell teaching cases; AuthorityEffect: None."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from textbook.path_lab.run_lab import check_recorded  # noqa: E402

if __name__ == "__main__":
    print(check_recorded())
