"""Finite X302 textbook examples and independent comparison; AuthorityEffect: None."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from textbook.reasoning_lab.revision import check_examples, check_population  # noqa: E402

if __name__ == '__main__':
    print(check_examples())
    print(check_population())
