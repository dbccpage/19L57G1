"""Bounded X303 textbook controls; AuthorityEffect: None."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from textbook.reasoning_lab.agency import check_examples  # noqa: E402

if __name__ == '__main__':
    print(check_examples())
